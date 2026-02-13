"""Test voting on Docker to boost its priority."""
import requests
import sqlite3

BASE_URL = "http://127.0.0.1:5000"

print("\n" + "="*80)
print(" TESTING DOCKER PRIORITY WITH VOTES")
print("="*80)

# Get Docker URI from database
conn = sqlite3.connect('genmentor.db')
cursor = conn.cursor()

cursor.execute("""
    SELECT concept_uri FROM skills
    WHERE preferred_label = 'Docker' AND skill_type = 'community'
    LIMIT 1
""")
result = cursor.fetchone()
conn.close()

if not result:
    print("❌ Docker skill not found in database!")
    exit(1)

docker_uri = result[0]
print(f"\n✓ Docker URI: {docker_uri}")

# Vote for Docker
print(f"\n📊 Adding votes for Docker...")
for i in range(10):
    response = requests.post(
        f"{BASE_URL}/api/feedback/vote",
        json={
            "user_id": f"docker_fan_{i}",
            "item_uri": docker_uri,
            "item_type": "skill",
            "vote": 1
        }
    )
    if response.status_code == 200:
        print(f"  ✓ Vote {i+1}/10")
    else:
        print(f"  ❌ Vote {i+1} failed: {response.status_code}")

print(f"\n✅ Added 10 upvotes for Docker")

# Generate learning path
print(f"\n📚 Generating learning path...")
response = requests.post(
    f"{BASE_URL}/api/path",
    json={"goal": "I want to become a Data Scientist"}
)

if response.status_code == 200:
    path_data = response.json()
    learning_path = path_data.get('learning_path', [])
    
    # Extract all skills
    all_skills = []
    for session in learning_path:
        for skill in session.get('skills', []):
            # Handle both string and dict format
            if isinstance(skill, str):
                all_skills.append(skill)
            else:
                all_skills.append(skill.get('label', ''))
    
    print(f"✓ Generated {len(all_skills)} skills")
    
    # Check if Docker is included
    if 'Docker' in all_skills:
        docker_position = all_skills.index('Docker') + 1
        print(f"\n🎉 SUCCESS! Docker appears at position {docker_position}")
        
        # Show first 20 skills
        print(f"\n📊 First 20 skills:")
        for i, skill in enumerate(all_skills[:20], 1):
            marker = "🆕" if skill == "Docker" else "  "
            print(f"   {marker} {i}. {skill}")
    else:
        print(f"\n❌ Docker NOT in learning path")
        print(f"\n📊 Skills generated:")
        for i, skill in enumerate(all_skills[:15], 1):
            print(f"   {i}. {skill}")
else:
    print(f"❌ Failed to generate path: {response.status_code}")

print("\n" + "="*80)
