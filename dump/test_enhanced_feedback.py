"""Enhanced test that adds votes directly to community skills."""
import requests
import sqlite3
import time

BASE_URL = "http://127.0.0.1:5000"

def add_votes_to_skill_uri(skill_uri, vote_count, vote_value=1):
    """Add votes directly to a skill URI."""
    for i in range(vote_count):
        response = requests.post(f"{BASE_URL}/api/feedback/vote", json={
            "user_id": f"voter_{skill_uri}_{i}",
            "item_uri": skill_uri,
            "item_type": "skill",
            "vote": vote_value
        })
        if response.status_code != 200:
            return False
    return True

def main():
    print("\n" + "="*80)
    print(" ENHANCED COMMUNITY FEEDBACK TEST")
    print("="*80)
    
    # Get occupation URI
    goal = "I want to become a Full Stack Web Developer"
    response = requests.post(f"{BASE_URL}/api/path", json={"goal": goal})
    data = response.json()
    occupation_uri = data.get('matched_occupation', {}).get('uri')
    
    print(f"\n✅ Occupation: {data.get('matched_occupation', {}).get('label')}")
    print(f"🔗 URI: {occupation_uri}")
    
    # Get baseline skills
    baseline_skills = []
    for session in data.get('learning_path', []):
        for skill in session.get('skills', []):
            if isinstance(skill, str):
                baseline_skills.append(skill)
            else:
                baseline_skills.append(skill.get('label', ''))
    
    print(f"\n📚 Baseline: {len(baseline_skills)} skills")
    
    # ========================================================================
    # Add community skills manually to database
    # ========================================================================
    print("\n" + "="*80)
    print(" ADDING COMMUNITY SKILLS WITH VOTES")
    print("="*80)
    
    conn = sqlite3.connect('genmentor.db')
    cursor = conn.cursor()
    
    community_skills = [
        ("Kubernetes", "Container orchestration platform for deploying web apps", 10),
        ("Redis", "In-memory data store for caching and sessions", 8),
        ("MongoDB", "NoSQL database popular in modern web development", 7)
    ]
    
    added_skills = []
    
    for skill_name, description, vote_count in community_skills:
        skill_uri = f"http://data.europa.eu/esco/skill/community-{skill_name.lower()}"
        
        # Add skill
        cursor.execute("""
            INSERT OR IGNORE INTO skills (concept_uri, preferred_label, description, skill_type)
            VALUES (?, ?, ?, ?)
        """, (skill_uri, skill_name, f"Community-suggested: {description}", 'community'))
        
        # Link to occupation
        cursor.execute("""
            INSERT OR IGNORE INTO occupation_skill_relations 
            (occupation_uri, skill_uri, relation_type)
            VALUES (?, ?, 'optional')
        """, (occupation_uri, skill_uri))
        
        conn.commit()
        
        # Add votes via API
        if add_votes_to_skill_uri(skill_uri, vote_count, 1):
            print(f"✅ Added {skill_name} with {vote_count} upvotes")
            added_skills.append(skill_name)
        else:
            print(f"❌ Failed to add votes for {skill_name}")
    
    conn.close()
    
    # ========================================================================
    # Generate new learning path
    # ========================================================================
    print("\n" + "="*80)
    print(" REGENERATING LEARNING PATH")
    print("="*80)
    
    time.sleep(1)
    
    response = requests.post(f"{BASE_URL}/api/path", json={"goal": goal})
    data = response.json()
    
    updated_skills = []
    for session in data.get('learning_path', []):
        for skill in session.get('skills', []):
            if isinstance(skill, str):
                updated_skills.append(skill)
            else:
                updated_skills.append(skill.get('label', ''))
    
    print(f"\n📚 Generated {len(updated_skills)} skills:")
    for i, skill in enumerate(updated_skills[:20], 1):
        if skill in added_skills:
            print(f"   🆕 {i}. {skill} (COMMUNITY)")
        else:
            print(f"      {i}. {skill}")
    
    # Analysis
    print("\n" + "="*80)
    print(" RESULTS")
    print("="*80)
    
    community_in_path = [s for s in added_skills if s in updated_skills]
    
    print(f"\n📊 Community Skills Status:")
    for skill in added_skills:
        if skill in updated_skills:
            pos = updated_skills.index(skill) + 1
            print(f"   ✅ {skill} - Position {pos}")
        else:
            print(f"   ❌ {skill} - Not included")
    
    if community_in_path:
        print(f"\n🎉 SUCCESS! {len(community_in_path)}/{len(added_skills)} community skills appearing!")
    else:
        print(f"\n⚠️  No community skills in path - may need server restart")
    
    print("\n" + "="*80)

if __name__ == "__main__":
    main()
