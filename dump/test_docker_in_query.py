"""Test if Docker appears in occupation skills query."""
import sqlite3

conn = sqlite3.connect('genmentor.db')
cursor = conn.cursor()

occupation_uri = "http://data.europa.eu/esco/occupation/258e46f9-0075-4a2e-adae-1ff0477e0f30"

print("\n" + "="*80)
print(" ALL SKILLS FOR DATA SCIENTIST")
print("="*80)

cursor.execute("""
    SELECT s.preferred_label, s.skill_type, osr.relation_type
    FROM skills s
    JOIN occupation_skill_relations osr ON s.concept_uri = osr.skill_uri
    WHERE osr.occupation_uri = ?
    ORDER BY s.preferred_label
""", (occupation_uri,))

all_skills = cursor.fetchall()

print(f"\nTotal skills: {len(all_skills)}")

# Look for community skills
community_skills = [s for s in all_skills if s[1] == 'community']
print(f"Community skills: {len(community_skills)}")

if community_skills:
    print("\n✅ Community Skills Found:")
    for skill in community_skills:
        print(f"  - {skill[0]} ({skill[2]} relation)")
else:
    print("\n❌ No community skills found")

# Look for Docker specifically
docker_skills = [s for s in all_skills if 'docker' in s[0].lower()]
if docker_skills:
    print(f"\n✅ Docker found:")
    for skill in docker_skills:
        print(f"  - {skill[0]} ({skill[1]}, {skill[2]})")
else:
    print(f"\n❌ Docker NOT found in skills")

conn.close()

print("\n" + "="*80)
