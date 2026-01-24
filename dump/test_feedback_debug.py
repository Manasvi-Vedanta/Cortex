"""Debug community feedback integration."""
import requests
import json

BASE_URL = "http://127.0.0.1:5000"

print("\n" + "="*80)
print(" DEBUGGING FEEDBACK INTEGRATION")
print("="*80)

# Step 1: Get data scientist occupation
goal = "I want to become a Data Scientist"
response = requests.post(f"{BASE_URL}/api/path", json={"goal": goal})
path_data = response.json()

# Print full response to debug
print(f"\n📊 API Response keys: {list(path_data.keys())}")

# Try to get occupation_uri from different locations
occupation_uri = path_data.get('occupation_uri')
if not occupation_uri and 'metadata' in path_data:
    occupation_uri = path_data['metadata'].get('occupation_uri')
if not occupation_uri and 'matched_occupation' in path_data:
    matched_occ = path_data['matched_occupation']
    print(f"  Matched occupation: {matched_occ}")
    if isinstance(matched_occ, dict):
        occupation_uri = matched_occ.get('uri') or matched_occ.get('concept_uri')
    
print(f"\n✓ Occupation URI: {occupation_uri}")

# Step 2: Submit suggestion
suggestion_data = {
    "user_id": "test_user",
    "item_uri": occupation_uri,
    "item_type": "occupation",
    "suggestion_type": "add_skill",
    "suggestion_text": "Add Docker for containerization"
}

response = requests.post(
    f"{BASE_URL}/api/feedback/suggest",  # Fixed: use /suggest not /suggestions
    json=suggestion_data
)

print(f"\n📝 Suggestion submission status: {response.status_code}")
result = response.json()
suggestion_id = result.get('suggestion_id')
print(f"✓ Created suggestion #{suggestion_id}")
print(f"  Text: {suggestion_data['suggestion_text']}")

# Step 3: Approve suggestion
print(f"\n🔍 Approving suggestion #{suggestion_id}...")
response = requests.post(
    f"{BASE_URL}/api/feedback/suggestions/{suggestion_id}/review",
    json={"reviewer_id": "admin", "status": "approved"}
)

print(f"  Status code: {response.status_code}")
print(f"  Response: {response.json()}")

# Step 4: Implement suggestion
print(f"\n⚙️ Implementing suggestion #{suggestion_id}...")
response = requests.post(
    f"{BASE_URL}/api/feedback/suggestions/{suggestion_id}/implement"
)

print(f"  Status code: {response.status_code}")
result = response.json()
print(f"  Success: {result.get('success')}")
print(f"  Message: {result.get('message')}")
print(f"  Action: {result.get('action')}")

if result.get('error'):
    print(f"  ❌ Error: {result.get('error')}")

# Step 5: Check if skill was added to database
print(f"\n🔍 Checking database for Docker skill...")
import sqlite3
conn = sqlite3.connect('genmentor.db')
cursor = conn.cursor()

# Check skills table
cursor.execute("""
    SELECT concept_uri, preferred_label, skill_type 
    FROM skills 
    WHERE preferred_label LIKE '%Docker%'
""")
docker_skills = cursor.fetchall()

if docker_skills:
    print(f"✓ Found {len(docker_skills)} Docker skill(s):")
    for skill in docker_skills:
        print(f"  - {skill[1]} ({skill[2]})")
        print(f"    URI: {skill[0]}")
        
    # Check if it's linked to occupation
    docker_uri = docker_skills[0][0]
    cursor.execute("""
        SELECT relation_type FROM occupation_skill_relations
        WHERE occupation_uri = ? AND skill_uri = ?
    """, (occupation_uri, docker_uri))
    
    relations = cursor.fetchall()
    if relations:
        print(f"\n✓ Docker is linked to Data Scientist:")
        for rel in relations:
            print(f"  - Relation: {rel[0]}")
    else:
        print(f"\n❌ Docker NOT linked to Data Scientist occupation")
else:
    print("❌ No Docker skill found in database")

conn.close()

print("\n" + "="*80)
