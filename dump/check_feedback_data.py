"""Quick script to check feedback data in database."""
import sqlite3

conn = sqlite3.connect('genmentor.db')
cursor = conn.cursor()

# Check votes
cursor.execute('SELECT COUNT(*) FROM votes')
votes_count = cursor.fetchone()[0]

cursor.execute('SELECT item_uri, vote_value, user_id, created_at FROM votes LIMIT 5')
votes = cursor.fetchall()

# Check suggestions
cursor.execute('SELECT COUNT(*) FROM suggestions')
suggestions_count = cursor.fetchone()[0]

cursor.execute('SELECT suggestion_type, status, votes_for, votes_against, suggestion_text FROM suggestions LIMIT 5')
suggestions = cursor.fetchall()

print("=" * 80)
print("FEEDBACK SYSTEM DATABASE STATUS")
print("=" * 80)
print(f"\nTotal Votes: {votes_count}")
print(f"Total Suggestions: {suggestions_count}")

print("\n" + "-" * 80)
print("RECENT VOTES:")
print("-" * 80)
for vote in votes:
    vote_symbol = "👍" if vote[1] == 1 else "👎" if vote[1] == -1 else "◯"
    print(f"{vote_symbol} Vote: {vote[1]:+2d} | User: {vote[2][:20]:20s} | {vote[3]}")
    print(f"   URI: ...{vote[0][-60:]}")

print("\n" + "-" * 80)
print("RECENT SUGGESTIONS:")
print("-" * 80)
for sugg in suggestions:
    print(f"Type: {sugg[0]:20s} | Status: {sugg[1]:10s} | 👍{sugg[2]:3d} 👎{sugg[3]:3d}")
    print(f"   Text: {sugg[4][:70]}...")

conn.close()

print("\n" + "=" * 80)
print("TESTING API ENDPOINTS...")
print("=" * 80)

import requests

BASE_URL = "http://localhost:5000"

# Test if server is running
try:
    # Test metrics endpoint
    response = requests.get(f"{BASE_URL}/api/feedback/metrics", timeout=2)
    if response.status_code == 200:
        metrics = response.json()
        print("\n✅ Feedback API is WORKING!")
        print(f"\nCommunity Metrics:")
        print(f"  Total Votes: {metrics.get('total_votes', 0)}")
        print(f"  Total Suggestions: {metrics.get('total_suggestions', 0)}")
        print(f"  Active Users: {metrics.get('active_users', 0)}")
        print(f"  Pending Suggestions: {metrics.get('pending_suggestions', 0)}")
    else:
        print(f"\n⚠️ API returned status {response.status_code}")
except requests.exceptions.ConnectionError:
    print("\n⚠️ Flask server is not running!")
    print("   Start it with: python app.py")
except Exception as e:
    print(f"\n❌ Error testing API: {e}")
