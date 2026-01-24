"""Diagnostic: Test the filter function directly to see why boost isn't working."""
import sqlite3
import sys

# Import the ai_engine module
sys.path.insert(0, '.')
from ai_engine import GenMentorAI

occupation_uri = "http://data.europa.eu/esco/occupation/1c5a45b9-440e-4726-b565-16a952abd341"

print("\n" + "="*80)
print(" DIAGNOSTIC: Direct Filter Function Test")
print("="*80)

# Get skills from database with the EXACT query ai_engine uses
conn = sqlite3.connect('genmentor.db')
cursor = conn.cursor()

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

print(f"\n📊 Total skills from database query: {len(all_skills)}")

# Find community skills
community_skills = [(s[1], s[4], s[5]) for s in all_skills if 'community' in s[1].lower() 
                    or s[1] in ['TensorFlow', 'PyTorch', 'MLflow', 'Kubeflow']]

print(f"\n🔍 Community skills in query results:")
for name, vote_score, vote_count in community_skills:
    meets = "✅" if (vote_score >= 0.7 and vote_count >= 3) else "❌"
    print(f"   {meets} {name}: score={vote_score:.2f}, count={vote_count}")

# Now test the filter function
print(f"\n⚙️  Testing _filter_skills_by_goal_relevance() function...")

engine = GenMentorAI()
goal = "I want to become a Machine Learning Engineer"

# Call the filter function directly
filtered_skills = engine._filter_skills_by_goal_relevance(all_skills, goal)

print(f"✓ Filtered to {len(filtered_skills)} skills")

# Check if community skills made it through
community_in_filtered = [s for s in filtered_skills if s[1] in ['TensorFlow', 'PyTorch', 'MLflow', 'Kubeflow']]

print(f"\n📋 Community skills in filtered results:")
if community_in_filtered:
    for skill in community_in_filtered:
        print(f"   ✅ {skill[1]}")
else:
    print("   ❌ No community skills in filtered results")

print(f"\n📝 First 15 filtered skills:")
for i, skill in enumerate(filtered_skills[:15], 1):
    uri, label, desc, relation = skill[:4]
    marker = "🆕" if label in ['TensorFlow', 'PyTorch', 'MLflow', 'Kubeflow'] else "  "
    print(f"   {marker} {i}. {label}")

# Detailed analysis
print(f"\n" + "="*80)
print(" ANALYSIS")
print("="*80 + "\n")

if community_in_filtered:
    print(f"✅ BOOST LOGIC IS WORKING!")
    print(f"   {len(community_in_filtered)} community skills passed through filter")
else:
    print("❌ BOOST LOGIC NOT WORKING")
    print("\nPossible reasons:")
    print("1. Skills not meeting boost criteria (vote_score >= 0.7 AND vote_count >= 3)")
    print("2. Boost code not executing (wrong code path)")
    print("3. Skills boosted but filtered out later in the process")
    
    # Check if skills are in the raw query
    if community_skills:
        print(f"\n   Skills ARE in database query ({len(community_skills)} found)")
        for name, score, count in community_skills:
            if score >= 0.7 and count >= 3:
                print(f"   ✅ {name} meets criteria but still filtered out!")
            else:
                print(f"   ❌ {name} doesn't meet criteria (needs score>=0.7 AND count>=3)")
    else:
        print("   Skills NOT in database query (wrong occupation?)")

print("\n" + "="*80 + "\n")
