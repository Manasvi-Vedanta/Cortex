"""
Quick test for the two fixed endpoints
"""

import requests
import json
import sys
import io

# Fix encoding for Windows console
if sys.platform == 'win32':
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')

BASE_URL = "http://localhost:5000"

print("Testing Fixed Endpoints...")
print("=" * 60)

# Test 1: Rate Resource (needs resource_url from database)
print("\n1. Testing Resource Rating...")
print("   First, let's get an existing resource URL...")

# Get resources for a skill
response = requests.get(f"{BASE_URL}/api/resources/skill/http%3A%2F%2Fdata.europa.eu%2Fesco%2Fskill%2Ftest-python")
if response.status_code == 200:
    data = response.json()
    if data['count'] > 0:
        resource_url = data['resources'][0]['url']  # It's 'url' not 'resource_url'
        print(f"   Found resource: {resource_url[:50]}...")
        
        # Now rate it
        rate_response = requests.post(
            f"{BASE_URL}/api/resources/rate",
            json={
                "resource_url": resource_url,
                "skill_uri": "http://data.europa.eu/esco/skill/test-python",
                "user_id": "test_user",
                "rating": 5,
                "quality_score": 9,
                "review_text": "Excellent!"
            }
        )
        
        if rate_response.status_code == 200:
            print("   [PASS] Resource rating works!")
            print(f"   Response: {rate_response.json()}")
        else:
            print(f"   [FAIL] Status: {rate_response.status_code}")
            print(f"   Error: {rate_response.text}")
    else:
        print("   [SKIP] No resources found to rate")
else:
    print(f"   [FAIL] Couldn't get resources: {response.status_code}")

# Test 2: Generate Path with Resources
print("\n2. Testing Integrated Path Generation...")
print("   Generating learning path with resources...")

path_response = requests.post(
    f"{BASE_URL}/api/path/with-resources",
    json={
        "goal": "I want to learn Python basics",
        "current_skills": [],
        "user_id": "test_user"
    },
    timeout=60  # Give it more time as this is a complex operation
)

if path_response.status_code == 200:
    result = path_response.json()
    print("   [PASS] Integrated endpoint works!")
    print(f"   Matched occupation: {result.get('matched_occupation', {}).get('name', 'N/A')}")
    print(f"   Total sessions: {result.get('total_sessions', 0)}")
    print(f"   Total duration: {result.get('gantt_timeline', {}).get('total_duration_hours', 0)} hours")
    
    # Show first session with resources
    if result.get('learning_path') and len(result['learning_path']) > 0:
        first_session = result['learning_path'][0]
        print(f"\n   First session: {first_session.get('title', 'N/A')}")
        print(f"   Skills: {', '.join(first_session.get('skills', [])[:3])}")
        if 'resources' in first_session:
            print(f"   Resources attached: {len(first_session['resources'])}")
else:
    print(f"   [FAIL] Status: {path_response.status_code}")
    print(f"   Error: {path_response.text[:200]}")

print("\n" + "=" * 60)
print("Test Complete!")
