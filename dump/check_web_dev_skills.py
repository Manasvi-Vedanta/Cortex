"""Check if TypeScript has votes and appears in query."""
import sqlite3

conn = sqlite3.connect('genmentor.db')
cursor = conn.cursor()

occupation_uri = "http://data.europa.eu/esco/occupation/c40a2919-48a9-40ea-b506-1f34f693496d"

print("\n" + "="*80)
print(" CHECKING COMMUNITY SKILLS FOR WEB DEVELOPER")
print("="*80)

# Check TypeScript, GraphQL, Next.js
for skill_name in ['TypeScript', 'GraphQL', 'Next.js']:
    print(f"\n{'='*80}")
    print(f" {skill_name.upper()}")
    print('='*80)
    
    # Check if skill exists
    cursor.execute("""
        SELECT concept_uri, preferred_label, skill_type 
        FROM skills 
        WHERE preferred_label = ?
    """, (skill_name,))
    
    skill = cursor.fetchone()
    if not skill:
        print(f"❌ {skill_name} NOT in skills table")
        continue
    
    skill_uri = skill[0]
    print(f"✅ Found in skills table:")
    print(f"   URI: {skill_uri}")
    print(f"   Type: {skill[2]}")
    
    # Check if linked to occupation
    cursor.execute("""
        SELECT relation_type FROM occupation_skill_relations
        WHERE occupation_uri = ? AND skill_uri = ?
    """, (occupation_uri, skill_uri))
    
    relation = cursor.fetchone()
    if relation:
        print(f"✅ Linked to web developer: {relation[0]}")
    else:
        print(f"❌ NOT linked to web developer")
        continue
    
    # Check votes
    cursor.execute("""
        SELECT vote_value FROM votes
        WHERE item_uri = ? AND item_type = 'skill'
    """, (skill_uri,))
    
    votes = cursor.fetchall()
    if votes:
        total = sum(v[0] for v in votes)
        avg = total / len(votes)
        print(f"📊 Votes: {len(votes)} total, sum={total}, avg={avg:.2f}")
    else:
        print(f"❌ NO votes")
    
    # Check what the full query returns
    cursor.execute("""
        SELECT s.preferred_label, osr.relation_type,
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
        WHERE osr.occupation_uri = ? AND s.preferred_label = ?
    """, (occupation_uri, skill_name))
    
    query_result = cursor.fetchone()
    if query_result:
        print(f"✅ Appears in occupation query:")
        print(f"   Relation: {query_result[1]}")
        print(f"   Vote score: {query_result[2]}")
        print(f"   Vote count: {query_result[3]}")
        
        # Check if meets boost criteria
        if query_result[2] >= 0.7 and query_result[3] >= 3:
            print(f"   ✅ MEETS boost criteria (score >= 0.7, count >= 3)")
        else:
            print(f"   ❌ Does NOT meet boost criteria")
            print(f"      Needs: score >= 0.7 AND count >= 3")
            print(f"      Has: score={query_result[2]}, count={query_result[3]}")

conn.close()

print("\n" + "="*80)
