"""
API Endpoint Testing for Enhanced Features
Tests all 16 new API endpoints
"""

import requests
import json
import sys
import io
from datetime import datetime

# Fix encoding for Windows console
if sys.platform == 'win32':
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')

BASE_URL = "http://localhost:5000"

print("=" * 80)
print("ENHANCED FEATURES API ENDPOINT TESTING")
print("=" * 80)
print(f"Test Started: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
print(f"Base URL: {BASE_URL}\n")

# Test counter
tests_passed = 0
tests_failed = 0

def test_endpoint(name, method, endpoint, data=None, params=None, expected_status=200):
    """Helper function to test an endpoint"""
    global tests_passed, tests_failed
    
    try:
        # Use longer timeout for complex operations
        timeout = 60 if "/path/with-resources" in endpoint else 10
        
        url = f"{BASE_URL}{endpoint}"
        if method == "GET":
            response = requests.get(url, params=params, timeout=timeout)
        elif method == "POST":
            response = requests.post(url, json=data, timeout=timeout)
        
        if response.status_code == expected_status:
            print(f"[PASS] {name}")
            print(f"       Status: {response.status_code}")
            try:
                result = response.json()
                if isinstance(result, dict):
                    keys = list(result.keys())[:5]  # First 5 keys
                    print(f"       Response keys: {', '.join(keys)}")
                elif isinstance(result, list):
                    print(f"       Response: List with {len(result)} items")
                tests_passed += 1
                return result
            except:
                print(f"       Response: {response.text[:100]}")
                tests_passed += 1
                return response.text
        else:
            print(f"[FAIL] {name}")
            print(f"       Expected: {expected_status}, Got: {response.status_code}")
            print(f"       Error: {response.text[:200]}")
            tests_failed += 1
            return None
    except Exception as e:
        print(f"[ERROR] {name}")
        print(f"        Exception: {str(e)}")
        tests_failed += 1
        return None

print("\n" + "=" * 80)
print("SECTION 1: COMMUNITY FEEDBACK ENDPOINTS (7 endpoints)")
print("=" * 80)

# 1. Vote on Item
print("\n1. POST /api/feedback/vote - Vote on a skill")
vote_result = test_endpoint(
    "Vote on skill",
    "POST",
    "/api/feedback/vote",
    data={
        "item_uri": "http://data.europa.eu/esco/skill/test-python",
        "item_type": "skill",
        "user_id": "api_test_user",
        "vote": 1
    }
)

# 2. Add Suggestion
print("\n2. POST /api/feedback/suggest - Add a suggestion")
suggestion_result = test_endpoint(
    "Add suggestion",
    "POST",
    "/api/feedback/suggest",
    data={
        "item_uri": "http://data.europa.eu/esco/skill/test-python",
        "item_type": "skill",
        "user_id": "api_test_user",
        "suggestion_type": "improve_description",
        "suggestion_text": "Add more examples for API testing"
    }
)

suggestion_id = None
if suggestion_result and 'suggestion_id' in suggestion_result:
    suggestion_id = suggestion_result['suggestion_id']

# 3. Get Pending Suggestions
print("\n3. GET /api/feedback/suggestions/pending - Get pending suggestions")
test_endpoint(
    "Get pending suggestions",
    "GET",
    "/api/feedback/suggestions/pending",
    params={"min_score": 0}
)

# 4. Vote on Suggestion
if suggestion_id:
    print(f"\n4. POST /api/feedback/suggestions/{suggestion_id}/vote - Vote on suggestion")
    test_endpoint(
        "Vote on suggestion",
        "POST",
        f"/api/feedback/suggestions/{suggestion_id}/vote",
        data={
            "user_id": "api_test_user_2",
            "vote": 1
        }
    )
else:
    print("\n4. POST /api/feedback/suggestions/{id}/vote - SKIPPED (no suggestion ID)")
    tests_failed += 1

# 5. Get Trending Items
print("\n5. GET /api/feedback/trending - Get trending items")
test_endpoint(
    "Get trending items",
    "GET",
    "/api/feedback/trending",
    params={"type": "skill", "days": 30, "limit": 10}
)

# 6. Get Community Metrics
print("\n6. GET /api/feedback/metrics - Get community metrics")
test_endpoint(
    "Get community metrics",
    "GET",
    "/api/feedback/metrics"
)

print("\n" + "=" * 80)
print("SECTION 2: VISUALIZATION ENDPOINTS (3 endpoints)")
print("=" * 80)

# Sample learning path for visualization
sample_path = [
    {
        "session_number": 1,
        "title": "API Testing Fundamentals",
        "skills": ["REST API", "HTTP methods", "JSON"],
        "estimated_duration_hours": 15,
        "difficulty_level": "beginner",
        "prerequisites": []
    },
    {
        "session_number": 2,
        "title": "Advanced API Testing",
        "skills": ["Authentication", "Rate limiting", "Error handling"],
        "estimated_duration_hours": 20,
        "difficulty_level": "intermediate",
        "prerequisites": ["API Testing Fundamentals"]
    }
]

# 7. Visualize Learning Path
print("\n7. POST /api/path/visualize - Get full visualization data")
viz_result = test_endpoint(
    "Visualize learning path",
    "POST",
    "/api/path/visualize",
    data={"learning_path": sample_path}
)

# 8. Get Gantt Chart HTML
print("\n8. GET /api/path/visualize/gantt - Get Gantt chart HTML")
gantt_html = test_endpoint(
    "Get Gantt chart HTML",
    "GET",
    "/api/path/visualize/gantt",
    params={"path_data": json.dumps(sample_path)}
)
if gantt_html and len(gantt_html) > 1000:
    print(f"       HTML length: {len(gantt_html)} characters")

# 9. Get Dependency Graph HTML
print("\n9. GET /api/path/visualize/graph - Get dependency graph HTML")
graph_html = test_endpoint(
    "Get dependency graph HTML",
    "GET",
    "/api/path/visualize/graph",
    params={"path_data": json.dumps(sample_path)}
)
if graph_html and len(graph_html) > 1000:
    print(f"       HTML length: {len(graph_html)} characters")

print("\n" + "=" * 80)
print("SECTION 3: RESOURCE CURATION ENDPOINTS (6 endpoints)")
print("=" * 80)

# 10. Search Resources
print("\n10. GET /api/resources/search - Search for resources")
search_result = test_endpoint(
    "Search resources",
    "GET",
    "/api/resources/search",
    params={"skill": "python programming", "limit": 5}
)

# 11. Add Resource
print("\n11. POST /api/resources/add - Add a new resource")
add_resource_result = test_endpoint(
    "Add resource",
    "POST",
    "/api/resources/add",
    data={
        "skill_uri": "http://data.europa.eu/esco/skill/test-python",
        "resource_url": "https://docs.python.org/3/tutorial/",
        "resource_title": "Official Python Tutorial",
        "resource_type": "documentation",
        "provider": "Python.org",
        "description": "Comprehensive Python tutorial",
        "difficulty_level": "beginner",
        "is_free": True,
        "estimated_duration": "10 hours"
    }
)

resource_id = None
if add_resource_result and 'resource_id' in add_resource_result:
    resource_id = add_resource_result['resource_id']

# 12. Get Resources for Skill
print("\n12. GET /api/resources/skill/<uri> - Get resources for a skill")
test_endpoint(
    "Get resources for skill",
    "GET",
    "/api/resources/skill/http%3A%2F%2Fdata.europa.eu%2Fesco%2Fskill%2Ftest-python",
    params={"difficulty": "beginner", "min_quality": 0, "validated_only": False}
)

# 13. Rate Resource
if add_resource_result and 'resource_id' in add_resource_result:
    print(f"\n13. POST /api/resources/rate - Rate a resource")
    test_endpoint(
        "Rate resource",
        "POST",
        "/api/resources/rate",
        data={
            "resource_url": "https://docs.python.org/3/tutorial/",
            "skill_uri": "http://data.europa.eu/esco/skill/test-python",
            "user_id": "api_test_user",
            "rating": 5,
            "quality_score": 9,
            "review_text": "Excellent resource!"
        }
    )
else:
    print("\n13. POST /api/resources/rate - SKIPPED (no resource added)")
    tests_failed += 1

# 14. Get Popular Resources
print("\n14. GET /api/resources/popular - Get popular resources")
test_endpoint(
    "Get popular resources",
    "GET",
    "/api/resources/popular",
    params={"days": 30, "limit": 10}
)

print("\n" + "=" * 80)
print("SECTION 4: INTEGRATED ENDPOINT (1 endpoint)")
print("=" * 80)

# 15. Generate Path with Resources
print("\n15. POST /api/path/with-resources - Generate complete path with resources")
integrated_result = test_endpoint(
    "Generate path with resources",
    "POST",
    "/api/path/with-resources",
    data={
        "goal": "Learn API testing",
        "current_skills": [],
        "user_id": "api_test_user"
    },
    expected_status=200
)
if integrated_result:
    print(f"       Matched occupation: {integrated_result.get('matched_occupation', {}).get('label', 'N/A')}")
    print(f"       Total sessions: {integrated_result.get('total_sessions', 0)}")

print("\n" + "=" * 80)
print("TEST SUMMARY")
print("=" * 80)
print(f"\nTotal Tests: {tests_passed + tests_failed}")
print(f"Passed: {tests_passed}")
print(f"Failed: {tests_failed}")
print(f"Success Rate: {(tests_passed / (tests_passed + tests_failed) * 100):.1f}%")

if tests_failed == 0:
    print("\n[SUCCESS] All API endpoints are working correctly!")
else:
    print(f"\n[WARNING] {tests_failed} endpoint(s) failed. Check the errors above.")

print("\n" + "=" * 80)
print(f"Test Completed: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
print("=" * 80)
