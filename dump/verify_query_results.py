"""Check if votes appear in the occupation query."""
import sqlite3

conn = sqlite3.connect('genmentor.db')
cursor = conn.cursor()

occupation_uri = "http://data.europa.eu/esco/occupation/c40a2919-48a9-40ea-b506-1f34f693496d"

print("\n" + "="*80)
print("CHECKING QUERY FOR WEB DEVELOPER SKILLS")
print("="*80)

# Run the exact query that ai_engine.py uses
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

print(f"\nTotal skills: {len(all_skills)}")

# Find community skills
community_skills = [s for s in all_skills if s[1] in ['Kubernetes', 'Redis', 'MongoDB', 'Docker']]

if community_skills:
    print(f"\n✅ Found {len(community_skills)} community skills in query:")
    for skill in community_skills:
        uri, label, desc, relation, vote_score, vote_count = skill
        print(f"\n  {label}:")
        print(f"    Relation: {relation}")
        print(f"    Vote score: {vote_score}")
        print(f"    Vote count: {vote_count}")
        print(f"    Meets boost criteria: {vote_score >= 0.7 and vote_count >= 3}")
else:
    print(f"\n❌ No community skills found in query results")

# Show top 10 by vote score
print(f"\n" + "="*80)
print("TOP 10 SKILLS BY VOTE SCORE")
print("="*80 + "\n")

for i, skill in enumerate(all_skills[:10], 1):
    uri, label, desc, relation, vote_score, vote_count = skill
    print(f"{i}. {label}")
    print(f"   Votes: {vote_count}, Score: {vote_score:.2f}, Relation: {relation}")

conn.close()
print("\n" + "="*80)
