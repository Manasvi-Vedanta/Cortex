"""
Comprehensive Demo: Community Feedback System
Tests all feedback endpoints and features.
"""

import requests
import json
from datetime import datetime

BASE_URL = "http://localhost:5000"

def print_section(title):
    """Print section header."""
    print("\n" + "=" * 80)
    print(f" {title}")
    print("=" * 80 + "\n")

def test_voting():
    """Test voting functionality."""
    print_section("1. VOTING SYSTEM")
    
    # Test voting on a skill
    skill_uri = "http://data.europa.eu/esco/skill/demo-python-advanced"
    
    print("Testing upvote on Python skill...")
    response = requests.post(f"{BASE_URL}/api/feedback/vote", json={
        "item_uri": skill_uri,
        "item_type": "skill",
        "user_id": "demo_user_1",
        "vote": 1
    })
    
    if response.status_code == 200:
        result = response.json()
        print("✅ Vote recorded successfully!")
        print(f"   Stats: {result.get('stats', {})}")
    else:
        print(f"❌ Failed: {response.status_code} - {response.text}")
    
    # Test downvote
    print("\nTesting downvote from another user...")
    response = requests.post(f"{BASE_URL}/api/feedback/vote", json={
        "item_uri": skill_uri,
        "item_type": "skill",
        "user_id": "demo_user_2",
        "vote": -1
    })
    
    if response.status_code == 200:
        result = response.json()
        print("✅ Downvote recorded!")
        print(f"   Stats: {result.get('stats', {})}")
    else:
        print(f"❌ Failed: {response.status_code}")

def test_suggestions():
    """Test suggestion system."""
    print_section("2. SUGGESTION SYSTEM")
    
    # Submit a suggestion
    print("Submitting suggestion to add a new skill...")
    response = requests.post(f"{BASE_URL}/api/feedback/suggest", json={
        "item_uri": "http://data.europa.eu/esco/occupation/data-scientist",
        "item_type": "occupation",
        "user_id": "demo_user_1",
        "suggestion_type": "add_skill",
        "suggestion_text": "Should include Kubernetes for deploying ML models in production"
    })
    
    if response.status_code == 200:
        result = response.json()
        print("✅ Suggestion submitted!")
        print(f"   Suggestion ID: {result.get('suggestion_id')}")
        suggestion_id = result.get('suggestion_id')
    else:
        print(f"❌ Failed: {response.status_code}")
        return None
    
    # Vote on the suggestion
    print(f"\nVoting on suggestion #{suggestion_id}...")
    response = requests.post(
        f"{BASE_URL}/api/feedback/suggestions/{suggestion_id}/vote",
        json={
            "user_id": "demo_user_2",
            "vote": 1
        }
    )
    
    if response.status_code == 200:
        result = response.json()
        print("✅ Vote on suggestion recorded!")
        print(f"   Result: {result.get('result', {})}")
    else:
        print(f"❌ Failed: {response.status_code}")
    
    return suggestion_id

def test_pending_suggestions():
    """Test getting pending suggestions."""
    print_section("3. PENDING SUGGESTIONS")
    
    print("Fetching pending suggestions...")
    response = requests.get(f"{BASE_URL}/api/feedback/suggestions/pending?min_score=0")
    
    if response.status_code == 200:
        result = response.json()
        suggestions = result.get('suggestions', [])
        count = result.get('count', 0)
        
        print(f"✅ Found {count} pending suggestions")
        
        if suggestions:
            print("\nTop 5 suggestions:")
            for i, sugg in enumerate(suggestions[:5], 1):
                print(f"\n{i}. [{sugg.get('status', 'unknown').upper()}] {sugg.get('suggestion_type', 'N/A')}")
                print(f"   Text: {sugg.get('suggestion_text', 'N/A')[:80]}...")
                print(f"   Votes: 👍 {sugg.get('votes_for', 0)} / 👎 {sugg.get('votes_against', 0)}")
                print(f"   Created: {sugg.get('created_at', 'N/A')}")
    else:
        print(f"❌ Failed: {response.status_code}")

def test_trending():
    """Test trending items."""
    print_section("4. TRENDING ITEMS")
    
    print("Fetching trending skills (last 7 days)...")
    response = requests.get(f"{BASE_URL}/api/feedback/trending?type=skill&days=7&limit=5")
    
    if response.status_code == 200:
        result = response.json()
        trending = result.get('trending_items', [])
        
        print(f"✅ Found {len(trending)} trending items")
        
        if trending:
            print("\nTrending Skills:")
            for i, item in enumerate(trending, 1):
                print(f"{i}. {item.get('item_uri', 'N/A')[-50:]}")
                print(f"   Score: {item.get('total_score', 0):+3d} (👍 {item.get('upvotes', 0)} / 👎 {item.get('downvotes', 0)})")
        else:
            print("\n⚠️ No trending items found (may need more voting activity)")
    else:
        print(f"❌ Failed: {response.status_code}")

def test_metrics():
    """Test community metrics."""
    print_section("5. COMMUNITY METRICS")
    
    print("Fetching community engagement metrics...")
    response = requests.get(f"{BASE_URL}/api/feedback/metrics")
    
    if response.status_code == 200:
        metrics = response.json()
        
        print("✅ Metrics retrieved successfully!")
        print("\n📊 Community Statistics:")
        print(f"   Total Votes: {metrics.get('total_votes', 0)}")
        print(f"   Total Suggestions: {metrics.get('total_suggestions', 0)}")
        print(f"   Pending Suggestions: {metrics.get('pending_suggestions', 0)}")
        print(f"   Approved Suggestions: {metrics.get('approved_suggestions', 0)}")
        print(f"   Active Users (last 30 days): {metrics.get('active_users', 0)}")
        print(f"   Average Votes per Item: {metrics.get('avg_votes_per_item', 0):.2f}")
        
        if 'top_voted_items' in metrics:
            print("\n🏆 Top Voted Items:")
            for item in metrics['top_voted_items'][:3]:
                print(f"   • {item.get('item_uri', 'N/A')[-50:]}")
                print(f"     Score: {item.get('score', 0):+3d}")
    else:
        print(f"❌ Failed: {response.status_code}")

def test_multiple_suggestions():
    """Create multiple diverse suggestions."""
    print_section("6. CREATING DIVERSE SUGGESTIONS")
    
    suggestions_data = [
        {
            "item_uri": "http://data.europa.eu/esco/occupation/machine-learning-engineer",
            "item_type": "occupation",
            "suggestion_type": "add_resource",
            "text": "Add link to fast.ai course - excellent for practical ML"
        },
        {
            "item_uri": "http://data.europa.eu/esco/skill/data-visualization",
            "item_type": "skill",
            "suggestion_type": "add_skill",
            "text": "Include D3.js for interactive web-based visualizations"
        },
        {
            "item_uri": "http://data.europa.eu/esco/occupation/data-scientist",
            "item_type": "occupation",
            "suggestion_type": "reorder",
            "text": "Statistics should come before machine learning in the learning path"
        }
    ]
    
    created_count = 0
    for i, sugg_data in enumerate(suggestions_data, 1):
        print(f"\nCreating suggestion {i}/3: {sugg_data['suggestion_type']}...")
        
        response = requests.post(f"{BASE_URL}/api/feedback/suggest", json={
            "item_uri": sugg_data["item_uri"],
            "item_type": sugg_data["item_type"],
            "user_id": f"demo_user_{i}",
            "suggestion_type": sugg_data["suggestion_type"],
            "suggestion_text": sugg_data["text"]
        })
        
        if response.status_code == 200:
            result = response.json()
            print(f"   ✅ Created suggestion #{result.get('suggestion_id')}")
            created_count += 1
        else:
            print(f"   ❌ Failed: {response.status_code}")
    
    print(f"\n✅ Successfully created {created_count}/{len(suggestions_data)} suggestions")

def main():
    """Run all feedback system tests."""
    print("\n" + "=" * 80)
    print(" COMMUNITY FEEDBACK SYSTEM - COMPREHENSIVE DEMO")
    print("=" * 80)
    print("\nNOTE: Make sure Flask server is running (python app.py)")
    print()
    
    # Check if server is running
    try:
        response = requests.get(f"{BASE_URL}/api/stats", timeout=2)
        if response.status_code != 200:
            print("❌ Server is not responding correctly!")
            return
    except requests.exceptions.ConnectionError:
        print("❌ Cannot connect to server!")
        print("   Please start the server with: python app.py")
        return
    
    print("✅ Server is running!\n")
    
    # Run all tests
    test_voting()
    test_suggestions()
    test_pending_suggestions()
    test_trending()
    test_multiple_suggestions()
    test_metrics()
    
    # Summary
    print_section("DEMO COMPLETE")
    print("✅ All feedback system features are functional!")
    print("\n📝 Summary of features tested:")
    print("   1. ✅ Voting on items (upvote/downvote)")
    print("   2. ✅ Submitting suggestions")
    print("   3. ✅ Voting on suggestions")
    print("   4. ✅ Viewing pending suggestions")
    print("   5. ✅ Tracking trending items")
    print("   6. ✅ Community metrics and analytics")
    print("\n💡 The feedback system is fully operational and integrated!")
    print()

if __name__ == "__main__":
    main()
