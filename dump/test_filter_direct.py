"""Direct test of filter function."""
from ai_engine import GenMentorAI
import sqlite3

print("\n" + "="*80)
print(" DIRECT FILTER TEST")
print("="*80)

# Get skills for data scientist
conn = sqlite3.connect('genmentor.db')
cursor = conn.cursor()

occupation_uri = "http://data.europa.eu/esco/occupation/258e46f9-0075-4a2e-adae-1ff0477e0f30"

cursor.execute("""
    SELECT s.concept_uri, s.preferred_label, s.description, osr.relation_type,
           COALESCE(
               (SELECT CAST(SUM(vote_value) AS FLOAT) / COUNT(*)
                FROM votes v
                WHERE v.item_uri = s.concept_uri
                  AND v.item_type = 'skill'),
               0
           ) as vote_score,
           COALESCE(
               (SELECT COUNT(*)
                FROM votes v
                WHERE v.item_uri = s.concept_uri
                  AND v.item_type = 'skill'),
               0
           ) as vote_count
    FROM skills s
    JOIN occupation_skill_relations osr ON s.concept_uri = osr.skill_uri
    WHERE osr.occupation_uri = ?
    ORDER BY 
        CASE osr.relation_type 
            WHEN 'essential' THEN 1 
            WHEN 'optional' THEN 2 
            ELSE 3 
        END,
        vote_score DESC,
        s.relevance_score DESC
""", (occupation_uri,))

all_skills = cursor.fetchall()
conn.close()

print(f"\n📊 Total skills from DB: {len(all_skills)}")

# Find Docker
docker_skills = [s for s in all_skills if s[1] == 'Docker']
if docker_skills:
    docker = docker_skills[0]
    print(f"\n✅ Docker found in skill list:")
    print(f"  Vote score: {docker[4]}, Vote count: {docker[5]}")
else:
    print(f"\n❌ Docker not in skill list")

# Test filter function
engine = GenMentorAI()
goal = "I want to become a Data Scientist"

print(f"\n⚙️ Running filter function...")
filtered_skills = engine._filter_skills_by_goal_relevance(all_skills, goal)

print(f"✓ Filtered to {len(filtered_skills)} skills")

# Check if Docker is in filtered results
docker_in_filtered = any(skill[1] == 'Docker' for skill in filtered_skills)

if docker_in_filtered:
    docker_pos = [i for i, s in enumerate(filtered_skills, 1) if s[1] == 'Docker'][0]
    print(f"\n🎉 SUCCESS! Docker is in filtered skills at position {docker_pos}")
else:
    print(f"\n❌ Docker was filtered OUT")
    
print(f"\n📋 Filtered skills:")
for i, skill in enumerate(filtered_skills[:20], 1):
    marker = "🆕" if skill[1] == "Docker" else "  "
    print(f"   {marker} {i}. {skill[1]}")

print("\n" + "="*80)
