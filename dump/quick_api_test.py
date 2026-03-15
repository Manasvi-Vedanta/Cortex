"""
Quick API Test Script
Tests if the GenMentor API is working properly.
"""

import requests
import json

BASE_URL = "http://localhost:5000"

def test_health():
    """Test health endpoint."""
    print("\n" + "="*60)
    print("Testing Health Endpoint")
    print("="*60)
    
    try:
        response = requests.get(f"{BASE_URL}/api/health", timeout=5)
        print(f"Status Code: {response.status_code}")
        
        if response.status_code == 200:
            data = response.json()
            print("✅ Health check passed!")
            print(f"   Model: {data.get('model')}")
            print(f"   Embedding Dim: {data.get('embedding_dimension')}")
            print(f"   LLM Available: {data.get('llm_available')}")
            return True
        else:
            print(f"❌ Health check failed with status {response.status_code}")
            return False
    except Exception as e:
        print(f"❌ Error: {e}")
        return False

def test_simple_path():
    """Test a simple learning path generation."""
    print("\n" + "="*60)
    print("Testing Learning Path Generation (Simple)")
    print("="*60)
    
    payload = {
        "goal": "I want to learn Python programming",
        "current_skills": ["basic computer skills"],
        "user_id": "test_user"
    }
    
    print(f"Sending request...")
    print(f"Goal: {payload['goal']}")
    print(f"Current Skills: {payload['current_skills']}")
    
    try:
        response = requests.post(
            f"{BASE_URL}/api/path",
            json=payload,
            timeout=60
        )
        
        print(f"\nStatus Code: {response.status_code}")
        
        if response.status_code == 200:
            data = response.json()
            print("✅ Request successful!")
            print(f"\n📊 Results:")
            print(f"   Matched Career: {data.get('matched_occupation', {}).get('label', 'N/A')}")
            print(f"   Similarity Score: {data.get('matched_occupation', {}).get('similarity_score', 0)*100:.1f}%")
            print(f"   Learning Sessions: {len(data.get('learning_path', []))}")
            print(f"   Skills to Learn: {data.get('skill_gap_summary', {}).get('skills_to_learn', 0)}")
            
            # Show first learning session
            if data.get('learning_path'):
                first_session = data['learning_path'][0]
                print(f"\n📚 First Learning Session:")
                print(f"   Title: {first_session.get('title', 'N/A')}")
                print(f"   Skills ({len(first_session.get('skills', []))}): {', '.join(first_session.get('skills', [])[:3])}...")
                
            return True
        else:
            print(f"❌ Request failed with status {response.status_code}")
            print(f"Response: {response.text}")
            return False
            
    except requests.exceptions.Timeout:
        print("❌ Request timed out (>60 seconds)")
        print("   This might indicate performance issues with the AI engine")
        return False
    except Exception as e:
        print(f"❌ Error: {e}")
        return False

def test_stats():
    """Test stats endpoint."""
    print("\n" + "="*60)
    print("Testing Stats Endpoint")
    print("="*60)
    
    try:
        response = requests.get(f"{BASE_URL}/api/stats", timeout=5)
        print(f"Status Code: {response.status_code}")
        
        if response.status_code == 200:
            data = response.json()
            print("✅ Stats retrieved!")
            print(f"   Total Occupations: {data.get('total_occupations', 0)}")
            print(f"   Total Skills: {data.get('total_skills', 0)}")
            print(f"   Total Votes: {data.get('total_votes', 0)}")
            return True
        else:
            print(f"❌ Failed with status {response.status_code}")
            return False
    except Exception as e:
        print(f"❌ Error: {e}")
        return False

def main():
    """Run all quick tests."""
    print("\n" + "="*60)
    print("  GENMENTOR API QUICK TEST")
    print("="*60)
    print("This script will test if the API is working properly.")
    print("Make sure the Flask server is running (python app.py)")
    
    results = {
        'health': False,
        'path': False,
        'stats': False
    }
    
    # Test 1: Health check
    results['health'] = test_health()
    
    if not results['health']:
        print("\n❌ Health check failed. Is the server running?")
        print("   Start with: python app.py")
        return
    
    # Test 2: Simple path generation
    results['path'] = test_simple_path()
    
    # Test 3: Stats
    results['stats'] = test_stats()
    
    # Summary
    print("\n" + "="*60)
    print("  TEST SUMMARY")
    print("="*60)
    passed = sum(results.values())
    total = len(results)
    print(f"✅ Passed: {passed}/{total}")
    
    for test_name, result in results.items():
        status = "✅ PASS" if result else "❌ FAIL"
        print(f"   {test_name.title()}: {status}")
    
    if passed == total:
        print("\n🎉 All tests passed! API is working correctly.")
    else:
        print("\n⚠️  Some tests failed. Check the errors above.")

if __name__ == "__main__":
    main()
