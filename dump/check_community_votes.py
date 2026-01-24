"""Check community skills votes."""
import sqlite3

conn = sqlite3.connect('genmentor.db')
cursor = conn.cursor()

cursor.execute("""
    SELECT s.preferred_label, 
           COUNT(v.vote_value) as vote_count,
           COALESCE(AVG(CAST(v.vote_value AS FLOAT)), 0) as avg_score
    FROM skills s 
    LEFT JOIN votes v ON s.concept_uri = v.item_uri AND v.item_type = 'skill'
    WHERE s.skill_type = 'community'
    GROUP BY s.concept_uri
    ORDER BY vote_count DESC
    LIMIT 10
""")

print("\n" + "="*80)
print("COMMUNITY SKILLS WITH VOTES")
print("="*80 + "\n")

results = cursor.fetchall()
if results:
    for skill_name, vote_count, avg_score in results:
        print(f"  {skill_name}: {vote_count} votes, avg score={avg_score:.2f}")
else:
    print("  No community skills found")

conn.close()
print("\n" + "="*80)
