"""Debug why Docker isn't appearing."""
import sqlite3

conn = sqlite3.connect('genmentor.db')
cursor = conn.cursor()

docker_uri = "http://data.europa.eu/esco/skill/community-docker"
occupation_uri = "http://data.europa.eu/esco/occupation/258e46f9-0075-4a2e-adae-1ff0477e0f30"

print("\n" + "="*80)
print(" DOCKER SKILL DEBUG")
print("="*80)

# Check votes for Docker
cursor.execute("""
    SELECT vote_value FROM votes
    WHERE item_uri = ? AND item_type = 'skill'
""", (docker_uri,))

votes = cursor.fetchall()
print(f"\n📊 Docker votes: {len(votes)}")
if votes:
    total = sum(v[0] for v in votes)
    avg = total / len(votes)
    print(f"  Total: {total}, Average: {avg}")

# Check what the query returns for Docker
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
    WHERE osr.occupation_uri = ? AND s.preferred_label = 'Docker'
""", (occupation_uri,))

docker_data = cursor.fetchone()

if docker_data:
    print(f"\n✅ Docker in query results:")
    print(f"  URI: {docker_data[0]}")
    print(f"  Label: {docker_data[1]}")
    print(f"  Relation: {docker_data[3]}")
    print(f"  Vote score: {docker_data[4]}")
    print(f"  Vote count: {docker_data[5]}")
    
    # Check if it meets criteria
    vote_score = docker_data[4]
    vote_count = docker_data[5]
    
    if vote_score >= 0.7 and vote_count >= 3:
        print(f"\n✅ Meets community boost criteria (score >= 0.7, count >= 3)")
    else:
        print(f"\n❌ Does NOT meet criteria (needs score >= 0.7 and count >= 3)")
        print(f"   Current: score={vote_score}, count={vote_count}")
else:
    print(f"\n❌ Docker not found in query")

conn.close()

print("\n" + "="*80)
