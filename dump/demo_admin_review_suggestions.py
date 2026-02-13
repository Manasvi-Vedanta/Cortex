"""
Admin Demo: Reviewing and Implementing Community Suggestions
Shows the complete workflow for managing community feedback.
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

def view_pending_suggestions():
    """View all pending suggestions."""
    print_section("1. VIEWING PENDING SUGGESTIONS")
    
    response = requests.get(f"{BASE_URL}/api/feedback/suggestions/pending?min_score=0")
    
    if response.status_code == 200:
        result = response.json()
        suggestions = result.get('suggestions', [])
        count = result.get('count', 0)
        
        print(f"📋 Found {count} pending suggestions\n")
        
        if suggestions:
            for i, sugg in enumerate(suggestions[:10], 1):
                print(f"{i}. ID: {sugg['id']} | Type: {sugg['suggestion_type']}")
                print(f"   Text: {sugg['suggestion_text'][:80]}...")
                print(f"   Community Support: 👍 {sugg['votes_for']} / 👎 {sugg['votes_against']} (Net: {sugg['net_votes']:+d})")
                print(f"   Created: {sugg['created_at']}\n")
            
            return suggestions
        else:
            print("⚠️ No pending suggestions found")
            return []
    else:
        print(f"❌ Failed to fetch suggestions: {response.status_code}")
        return []

def approve_suggestion(suggestion_id, reviewer_id="admin"):
    """Approve a suggestion."""
    print(f"\n🔍 Reviewing suggestion #{suggestion_id}...")
    
    response = requests.post(
        f"{BASE_URL}/api/feedback/suggestions/{suggestion_id}/review",
        json={
            "reviewer_id": reviewer_id,
            "status": "approved",
            "reason": "Good suggestion with strong community support"
        }
    )
    
    if response.status_code == 200:
        result = response.json()
        print(f"✅ Suggestion #{suggestion_id} APPROVED by {reviewer_id}")
        return True
    else:
        print(f"❌ Failed to approve: {response.status_code}")
        return False

def reject_suggestion(suggestion_id, reviewer_id="admin", reason=""):
    """Reject a suggestion."""
    print(f"\n❌ Rejecting suggestion #{suggestion_id}...")
    
    response = requests.post(
        f"{BASE_URL}/api/feedback/suggestions/{suggestion_id}/review",
        json={
            "reviewer_id": reviewer_id,
            "status": "rejected",
            "reason": reason or "Does not align with current curriculum"
        }
    )
    
    if response.status_code == 200:
        result = response.json()
        print(f"✅ Suggestion #{suggestion_id} REJECTED by {reviewer_id}")
        print(f"   Reason: {reason}")
        return True
    else:
        print(f"❌ Failed to reject: {response.status_code}")
        return False

def view_approved_suggestions():
    """View all approved suggestions."""
    print_section("3. VIEWING APPROVED SUGGESTIONS")
    
    response = requests.get(f"{BASE_URL}/api/feedback/suggestions/approved")
    
    if response.status_code == 200:
        result = response.json()
        suggestions = result.get('approved_suggestions', [])
        count = result.get('count', 0)
        
        print(f"✅ Found {count} approved suggestions awaiting implementation\n")
        
        if suggestions:
            for i, sugg in enumerate(suggestions[:10], 1):
                print(f"{i}. ID: {sugg['id']} | Type: {sugg['suggestion_type']}")
                print(f"   Text: {sugg['suggestion_text'][:80]}...")
                print(f"   Reviewed by: {sugg['reviewed_by']} on {sugg['reviewed_at']}")
                print(f"   Community: 👍 {sugg['votes_for']} / 👎 {sugg['votes_against']}\n")
            
            return suggestions
        else:
            print("⚠️ No approved suggestions pending implementation")
            return []
    else:
        print(f"❌ Failed to fetch approved suggestions: {response.status_code}")
        return []

def implement_suggestion(suggestion_id):
    """Implement an approved suggestion."""
    print(f"\n⚙️ Implementing suggestion #{suggestion_id}...")
    
    response = requests.post(
        f"{BASE_URL}/api/feedback/suggestions/{suggestion_id}/implement"
    )
    
    if response.status_code == 200:
        result = response.json()
        print(f"✅ Suggestion #{suggestion_id} IMPLEMENTED!")
        print(f"   Action: {result.get('action')}")
        print(f"   Message: {result.get('message')}")
        print(f"   Details: {result.get('details', 'N/A')[:80]}...")
        return True
    else:
        error_msg = response.json().get('error', 'Unknown error')
        print(f"❌ Failed to implement: {error_msg}")
        return False

def check_metrics():
    """Check updated metrics."""
    print_section("5. UPDATED COMMUNITY METRICS")
    
    response = requests.get(f"{BASE_URL}/api/feedback/metrics")
    
    if response.status_code == 200:
        metrics = response.json()
        
        print("📊 Community Statistics:")
        print(f"   Total Suggestions: {metrics.get('total_suggestions', 0)}")
        print(f"   Pending: {metrics.get('pending_suggestions', 0)}")
        print(f"   Approved: {metrics.get('approved_suggestions', 0)}")
        print(f"   Total Votes: {metrics.get('total_votes', 0)}")
        print(f"   Active Users (30d): {metrics.get('active_users_30d', 0)}")
    else:
        print(f"❌ Failed to fetch metrics")

def demo_workflow():
    """Demonstrate the complete admin workflow."""
    print("\n" + "=" * 80)
    print(" ADMIN WORKFLOW: REVIEWING & IMPLEMENTING COMMUNITY SUGGESTIONS")
    print("=" * 80)
    print("\nThis demo shows how an admin reviews, approves, and implements suggestions.")
    print()
    
    # Check server
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
    
    # Step 1: View pending suggestions
    pending = view_pending_suggestions()
    
    if not pending:
        print("\n💡 No pending suggestions to review. Run demo_feedback_system.py first to create some!")
        return
    
    # Step 2: Review suggestions
    print_section("2. REVIEWING SUGGESTIONS")
    
    # Approve the top suggestions with good community support
    approved_count = 0
    rejected_count = 0
    
    for sugg in pending[:5]:  # Review top 5
        suggestion_id = sugg['id']
        net_votes = sugg['net_votes']
        
        if net_votes >= 1:  # Approve if net positive votes
            if approve_suggestion(suggestion_id):
                approved_count += 1
        elif net_votes < 0:  # Reject if net negative votes
            if reject_suggestion(suggestion_id, reason="Insufficient community support"):
                rejected_count += 1
        # Skip if net is 0 (leave pending for more votes)
    
    print(f"\n📊 Review Summary: {approved_count} approved, {rejected_count} rejected")
    
    # Step 3: View approved suggestions
    approved = view_approved_suggestions()
    
    if not approved:
        print("\n💡 No approved suggestions to implement")
        return
    
    # Step 4: Implement approved suggestions
    print_section("4. IMPLEMENTING APPROVED SUGGESTIONS")
    
    implemented_count = 0
    for sugg in approved[:3]:  # Implement top 3
        if implement_suggestion(sugg['id']):
            implemented_count += 1
    
    print(f"\n✅ Successfully implemented {implemented_count} suggestions")
    
    # Step 5: Check updated metrics
    check_metrics()
    
    # Summary
    print_section("WORKFLOW COMPLETE")
    print("✅ Admin workflow demonstrated successfully!")
    print("\n📝 Summary:")
    print(f"   1. Reviewed {approved_count + rejected_count} suggestions")
    print(f"   2. Approved {approved_count} suggestions")
    print(f"   3. Rejected {rejected_count} suggestions")  
    print(f"   4. Implemented {implemented_count} suggestions")
    print("\n💡 Suggestion Lifecycle:")
    print("   pending → reviewed (approved/rejected) → implemented")
    print("\n🎯 Next Steps:")
    print("   - Approved suggestions are tracked in 'suggestions_implemented' table")
    print("   - Use these to manually update curriculum or auto-apply in future")
    print("   - High-voted suggestions indicate what the community wants!")
    print()

if __name__ == "__main__":
    demo_workflow()
