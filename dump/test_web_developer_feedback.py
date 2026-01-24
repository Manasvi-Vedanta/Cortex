"""Test community feedback integration for Web Developer career path."""
import requests
import time

BASE_URL = "http://127.0.0.1:5000"

def check_server():
    """Check if server is running."""
    try:
        response = requests.get(f"{BASE_URL}/api/health", timeout=2)
        return response.status_code == 200
    except:
        return False

def generate_path(goal):
    """Generate learning path."""
    response = requests.post(f"{BASE_URL}/api/path", json={"goal": goal})
    return response.json() if response.status_code == 200 else None

def extract_skills(path_data):
    """Extract skill names from learning path."""
    skills = []
    if path_data:
        for session in path_data.get('learning_path', []):
            for skill in session.get('skills', []):
                if isinstance(skill, str):
                    skills.append(skill)
                else:
                    skills.append(skill.get('label', ''))
    return skills

def vote_for_skill(skill_name, occupation_uri, votes_count, vote_value=1):
    """Add votes for a specific skill."""
    # Find skill URI from database
    import sqlite3
    conn = sqlite3.connect('genmentor.db')
    cursor = conn.cursor()
    
    cursor.execute("""
        SELECT s.concept_uri FROM skills s
        JOIN occupation_skill_relations osr ON s.concept_uri = osr.skill_uri
        WHERE osr.occupation_uri = ? AND s.preferred_label LIKE ?
        LIMIT 1
    """, (occupation_uri, f"%{skill_name}%"))
    
    result = cursor.fetchone()
    conn.close()
    
    if not result:
        return False
    
    skill_uri = result[0]
    
    # Add votes
    for i in range(votes_count):
        requests.post(f"{BASE_URL}/api/feedback/vote", json={
            "user_id": f"voter_{skill_name}_{i}",
            "item_uri": skill_uri,
            "item_type": "skill",
            "vote": vote_value
        })
    
    return True

def suggest_and_approve_skill(occupation_uri, skill_name, description):
    """Suggest a new skill and approve it."""
    # Submit suggestion
    response = requests.post(f"{BASE_URL}/api/feedback/suggest", json={
        "user_id": "community_contributor",
        "item_uri": occupation_uri,
        "item_type": "occupation",
        "suggestion_type": "add_skill",
        "suggestion_text": f"Add {skill_name} - {description}"
    })
    
    if response.status_code != 200:
        return None
    
    suggestion_id = response.json().get('suggestion_id')
    
    # Vote for the suggestion
    for i in range(5):
        requests.post(f"{BASE_URL}/api/feedback/suggestions/{suggestion_id}/vote", json={
            "user_id": f"supporter_{i}",
            "vote": 1
        })
    
    # Approve
    requests.post(f"{BASE_URL}/api/feedback/suggestions/{suggestion_id}/review", json={
        "reviewer_id": "admin",
        "status": "approved"
    })
    
    # Implement
    response = requests.post(f"{BASE_URL}/api/feedback/suggestions/{suggestion_id}/implement")
    
    return suggestion_id if response.status_code == 200 else None

def main():
    print("\n" + "="*80)
    print(" COMMUNITY FEEDBACK TEST - WEB DEVELOPER")
    print("="*80)
    
    if not check_server():
        print("\n❌ Server not running! Start it with: python app.py")
        return
    
    print("\n✅ Server is running!")
    
    goal = "I want to become a Full Stack Web Developer"
    
    # ========================================================================
    # STEP 1: Generate baseline learning path
    # ========================================================================
    print("\n" + "="*80)
    print(" STEP 1: BASELINE LEARNING PATH (No Community Feedback)")
    print("="*80)
    print(f"\nGoal: {goal}\n")
    
    baseline = generate_path(goal)
    if not baseline:
        print("❌ Failed to generate baseline path")
        return
    
    baseline_skills = extract_skills(baseline)
    occupation_uri = baseline.get('matched_occupation', {}).get('uri')
    occupation_name = baseline.get('matched_occupation', {}).get('label', 'Unknown')
    
    print(f"📋 Occupation: {occupation_name}")
    print(f"🔗 URI: {occupation_uri}\n")
    print(f"📚 Generated {len(baseline_skills)} skills:")
    for i, skill in enumerate(baseline_skills[:10], 1):
        print(f"   {i}. {skill}")
    if len(baseline_skills) > 10:
        print(f"   ... and {len(baseline_skills) - 10} more")
    
    # ========================================================================
    # STEP 2: Apply community feedback
    # ========================================================================
    print("\n" + "="*80)
    print(" STEP 2: APPLYING COMMUNITY FEEDBACK")
    print("="*80)
    
    # Upvote important web dev skills
    print("\n📊 Adding upvotes for key web development skills...")
    
    upvote_skills = [
        ("JavaScript", 8, "Essential for web development"),
        ("React", 6, "Popular frontend framework"),
        ("Node.js", 5, "Backend JavaScript runtime")
    ]
    
    for skill_name, vote_count, reason in upvote_skills:
        if vote_for_skill(skill_name, occupation_uri, vote_count, 1):
            print(f"   ✅ {vote_count} upvotes for {skill_name} ({reason})")
        else:
            print(f"   ⚠️  {skill_name} not found in current skills")
    
    # Downvote less relevant skills
    print("\n👎 Adding downvotes for outdated technologies...")
    
    downvote_skills = [
        ("jQuery", 4, "Outdated, prefer modern frameworks"),
    ]
    
    for skill_name, vote_count, reason in downvote_skills:
        if vote_for_skill(skill_name, occupation_uri, vote_count, -1):
            print(f"   ❌ {vote_count} downvotes for {skill_name} ({reason})")
        else:
            print(f"   ⚠️  {skill_name} not found in current skills")
    
    # Suggest new trending skills
    print("\n💡 Suggesting new community skills...")
    
    new_skills = [
        ("TypeScript", "Adds type safety to JavaScript, industry standard"),
        ("GraphQL", "Modern API query language, alternative to REST"),
        ("Next.js", "Production-ready React framework with SSR")
    ]
    
    implemented = []
    for skill_name, description in new_skills:
        suggestion_id = suggest_and_approve_skill(occupation_uri, skill_name, description)
        if suggestion_id:
            print(f"   ✅ Added {skill_name} (suggestion #{suggestion_id})")
            implemented.append(skill_name)
            # Add votes to boost priority
            time.sleep(0.1)
        else:
            print(f"   ❌ Failed to add {skill_name}")
    
    # ========================================================================
    # STEP 3: Generate updated learning path
    # ========================================================================
    print("\n" + "="*80)
    print(" STEP 3: UPDATED LEARNING PATH (With Community Feedback)")
    print("="*80)
    print(f"\nRegenerating path for: {goal}\n")
    
    time.sleep(1)  # Give server a moment to process
    
    updated = generate_path(goal)
    if not updated:
        print("❌ Failed to generate updated path")
        return
    
    updated_skills = extract_skills(updated)
    
    print(f"📚 Generated {len(updated_skills)} skills:")
    for i, skill in enumerate(updated_skills[:15], 1):
        if skill in implemented:
            print(f"   🆕 {i}. {skill} (COMMUNITY SUGGESTED)")
        elif skill not in baseline_skills:
            print(f"   ⭐ {i}. {skill} (NEW)")
        else:
            print(f"      {i}. {skill}")
    if len(updated_skills) > 15:
        print(f"   ... and {len(updated_skills) - 15} more")
    
    # ========================================================================
    # STEP 4: Analysis
    # ========================================================================
    print("\n" + "="*80)
    print(" STEP 4: COMMUNITY IMPACT ANALYSIS")
    print("="*80)
    
    new_skills_added = [s for s in updated_skills if s not in baseline_skills]
    skills_removed = [s for s in baseline_skills if s not in updated_skills]
    
    print(f"\n📊 Summary:")
    print(f"   Skills before: {len(baseline_skills)}")
    print(f"   Skills after: {len(updated_skills)}")
    print(f"   New skills added: {len(new_skills_added)}")
    print(f"   Skills removed: {len(skills_removed)}")
    
    if new_skills_added:
        print(f"\n✨ New Skills Added:")
        for skill in new_skills_added:
            marker = "🆕" if skill in implemented else "⭐"
            source = "Community Suggestion" if skill in implemented else "Re-prioritized"
            print(f"   {marker} {skill} ({source})")
    
    if skills_removed:
        print(f"\n📤 Skills Removed/Deprioritized:")
        for skill in skills_removed[:5]:
            print(f"   • {skill}")
    
    # Success metrics
    community_skills_included = sum(1 for s in implemented if s in updated_skills)
    
    print(f"\n🎯 Success Metrics:")
    print(f"   Community suggestions implemented: {len(implemented)}")
    print(f"   Community skills in learning path: {community_skills_included}/{len(implemented)}")
    if community_skills_included > 0:
        print(f"   ✅ Community feedback IS affecting learning paths!")
    else:
        print(f"   ⚠️  Community skills not appearing (may need higher votes)")
    
    print("\n" + "="*80)
    print(" TEST COMPLETE")
    print("="*80)

if __name__ == "__main__":
    main()
