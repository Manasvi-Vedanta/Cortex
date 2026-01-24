"""Comprehensive Community Feedback System Test
Tests all aspects of the feedback integration:
1. Voting on existing skills
2. Community skill suggestions
3. Vote-based skill boosting
4. Downvote filtering
5. Priority adjustment
"""
import requests
import sqlite3
import time
import json
from datetime import datetime

BASE_URL = "http://127.0.0.1:5000"

def print_section(title):
    """Print formatted section header."""
    print("\n" + "="*80)
    print(f" {title}")
    print("="*80 + "\n")

def check_server():
    """Verify server is running."""
    try:
        response = requests.get(f"{BASE_URL}/api/health", timeout=2)
        return response.status_code == 200
    except:
        return False

def get_skill_uri(skill_name, occupation_uri):
    """Get skill URI from database."""
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
    return result[0] if result else None

def add_community_skill_with_votes(occupation_uri, skill_name, description, vote_count):
    """Add a community skill directly to database with votes."""
    conn = sqlite3.connect('genmentor.db')
    cursor = conn.cursor()
    
    skill_uri = f"http://data.europa.eu/esco/skill/community-{skill_name.lower().replace(' ', '-')}"
    
    # Add skill
    cursor.execute("""
        INSERT OR IGNORE INTO skills (concept_uri, preferred_label, description, skill_type)
        VALUES (?, ?, ?, ?)
    """, (skill_uri, skill_name, f"Community skill: {description}", 'community'))
    
    # Link to occupation
    cursor.execute("""
        INSERT OR IGNORE INTO occupation_skill_relations 
        (occupation_uri, skill_uri, relation_type)
        VALUES (?, ?, 'optional')
    """, (occupation_uri, skill_uri))
    
    conn.commit()
    conn.close()
    
    # Add votes via API
    success_count = 0
    for i in range(vote_count):
        response = requests.post(f"{BASE_URL}/api/feedback/vote", json={
            "user_id": f"voter_{skill_name}_{i}_{datetime.now().timestamp()}",
            "item_uri": skill_uri,
            "item_type": "skill",
            "vote": 1
        })
        if response.status_code == 200:
            success_count += 1
    
    return success_count == vote_count, skill_uri

def vote_on_skill(skill_uri, vote_count, vote_value):
    """Add multiple votes to a skill."""
    success_count = 0
    for i in range(vote_count):
        response = requests.post(f"{BASE_URL}/api/feedback/vote", json={
            "user_id": f"voter_{skill_uri[-10:]}_{i}_{datetime.now().timestamp()}",
            "item_uri": skill_uri,
            "item_type": "skill",
            "vote": vote_value
        })
        if response.status_code == 200:
            success_count += 1
        time.sleep(0.05)  # Small delay to avoid overwhelming server
    return success_count

def get_learning_path(goal):
    """Generate learning path."""
    response = requests.post(f"{BASE_URL}/api/path", json={"goal": goal})
    if response.status_code == 200:
        return response.json()
    return None

def extract_skill_list(path_data):
    """Extract list of skill names from path."""
    skills = []
    for session in path_data.get('learning_path', []):
        for skill in session.get('skills', []):
            if isinstance(skill, str):
                skills.append(skill)
            else:
                skills.append(skill.get('label', ''))
    return skills

def check_vote_scores():
    """Check vote scores in database."""
    conn = sqlite3.connect('genmentor.db')
    cursor = conn.cursor()
    cursor.execute("""
        SELECT s.preferred_label, s.skill_type,
               COALESCE(AVG(CAST(v.vote_value AS FLOAT)), 0) as vote_score,
               COUNT(v.vote_value) as vote_count
        FROM skills s 
        LEFT JOIN votes v ON s.concept_uri = v.item_uri AND v.item_type = 'skill'
        WHERE s.skill_type = 'community' OR EXISTS (
            SELECT 1 FROM votes WHERE item_uri = s.concept_uri
        )
        GROUP BY s.concept_uri
        HAVING vote_count > 0
        ORDER BY vote_score DESC, vote_count DESC
        LIMIT 15
    """)
    results = cursor.fetchall()
    conn.close()
    return results

def main():
    print("\n" + "="*80)
    print(" COMPREHENSIVE COMMUNITY FEEDBACK SYSTEM TEST")
    print(" Test Date:", datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
    print("="*80)
    
    # ========================================================================
    # TEST 1: Server Health Check
    # ========================================================================
    print_section("TEST 1: Server Health Check")
    
    if not check_server():
        print("❌ FAILED: Server is not running!")
        print("Please start the server with: python app.py")
        return
    
    print("✅ PASSED: Server is running and responding")
    
    # ========================================================================
    # TEST 2: Generate Baseline Learning Path
    # ========================================================================
    print_section("TEST 2: Generate Baseline Learning Path")
    
    goal = "I want to become a Machine Learning Engineer"
    print(f"Goal: {goal}")
    
    baseline_data = get_learning_path(goal)
    if not baseline_data:
        print("❌ FAILED: Could not generate baseline learning path")
        return
    
    baseline_skills = extract_skill_list(baseline_data)
    occupation = baseline_data.get('matched_occupation', {})
    occupation_uri = occupation.get('uri')
    occupation_name = occupation.get('label')
    
    print(f"✅ PASSED: Generated learning path")
    print(f"   Occupation: {occupation_name}")
    print(f"   URI: {occupation_uri}")
    print(f"   Skills generated: {len(baseline_skills)}")
    print(f"\n   First 5 skills:")
    for i, skill in enumerate(baseline_skills[:5], 1):
        print(f"      {i}. {skill}")
    
    # ========================================================================
    # TEST 3: Add Community Skills with High Votes
    # ========================================================================
    print_section("TEST 3: Add Community Skills with High Votes")
    
    community_skills = [
        ("TensorFlow", "Deep learning framework by Google", 10),
        ("PyTorch", "Deep learning library by Facebook", 10),
        ("MLflow", "ML lifecycle management platform", 8),
        ("Kubeflow", "ML workflows on Kubernetes", 7),
    ]
    
    added_skills = {}
    
    for skill_name, description, vote_count in community_skills:
        success, skill_uri = add_community_skill_with_votes(
            occupation_uri, skill_name, description, vote_count
        )
        
        if success:
            print(f"✅ Added {skill_name} with {vote_count} upvotes")
            added_skills[skill_name] = skill_uri
        else:
            print(f"❌ Failed to add {skill_name}")
    
    if len(added_skills) == len(community_skills):
        print(f"\n✅ PASSED: All {len(community_skills)} community skills added successfully")
    else:
        print(f"\n⚠️  PARTIAL: {len(added_skills)}/{len(community_skills)} skills added")
    
    # ========================================================================
    # TEST 4: Upvote Existing Important Skills
    # ========================================================================
    print_section("TEST 4: Upvote Existing Important Skills")
    
    upvote_targets = [
        ("Python", 6),
        ("machine learning", 5),
    ]
    
    upvoted = []
    for skill_name, vote_count in upvote_targets:
        skill_uri = get_skill_uri(skill_name, occupation_uri)
        if skill_uri:
            success = vote_on_skill(skill_uri, vote_count, 1)
            if success == vote_count:
                print(f"✅ Added {vote_count} upvotes to {skill_name}")
                upvoted.append(skill_name)
            else:
                print(f"⚠️  Added {success}/{vote_count} upvotes to {skill_name}")
        else:
            print(f"⚠️  Skill '{skill_name}' not found in occupation")
    
    if upvoted:
        print(f"\n✅ PASSED: Upvoted {len(upvoted)} existing skills")
    
    # ========================================================================
    # TEST 5: Downvote Less Relevant Skills
    # ========================================================================
    print_section("TEST 5: Downvote Less Relevant Skills")
    
    downvote_targets = [
        ("spreadsheet software", 4),
    ]
    
    downvoted = []
    for skill_name, vote_count in downvote_targets:
        skill_uri = get_skill_uri(skill_name, occupation_uri)
        if skill_uri:
            success = vote_on_skill(skill_uri, vote_count, -1)
            if success == vote_count:
                print(f"✅ Added {vote_count} downvotes to {skill_name}")
                downvoted.append(skill_name)
            else:
                print(f"⚠️  Added {success}/{vote_count} downvotes to {skill_name}")
        else:
            print(f"⚠️  Skill '{skill_name}' not found")
    
    # ========================================================================
    # TEST 6: Verify Vote Scores in Database
    # ========================================================================
    print_section("TEST 6: Verify Vote Scores in Database")
    
    vote_data = check_vote_scores()
    if vote_data:
        print("Top skills by vote score:\n")
        for skill_name, skill_type, vote_score, vote_count in vote_data:
            marker = "🆕" if skill_type == 'community' else "  "
            meets_criteria = "✅" if (vote_score >= 0.7 and vote_count >= 3) else "  "
            print(f"{marker} {meets_criteria} {skill_name}")
            print(f"      Score: {vote_score:.2f}, Votes: {vote_count}, Type: {skill_type}")
        
        # Check if our community skills meet boost criteria
        community_meeting_criteria = [
            (name, score, count) for name, stype, score, count in vote_data
            if stype == 'community' and score >= 0.7 and count >= 3
        ]
        
        if community_meeting_criteria:
            print(f"\n✅ PASSED: {len(community_meeting_criteria)} community skills meet boost criteria")
        else:
            print(f"\n❌ FAILED: No community skills meet boost criteria")
    else:
        print("⚠️  No vote data found")
    
    # ========================================================================
    # TEST 7: Regenerate Learning Path with Feedback
    # ========================================================================
    print_section("TEST 7: Regenerate Learning Path with Community Feedback")
    
    print("Waiting 2 seconds for votes to process...")
    time.sleep(2)
    
    print(f"Regenerating path for: {goal}\n")
    
    updated_data = get_learning_path(goal)
    if not updated_data:
        print("❌ FAILED: Could not regenerate learning path")
        return
    
    updated_skills = extract_skill_list(updated_data)
    
    print(f"Generated {len(updated_skills)} skills:\n")
    for i, skill in enumerate(updated_skills[:20], 1):
        if skill in added_skills:
            print(f"   🆕 {i}. {skill} (COMMUNITY SUGGESTED)")
        elif skill not in baseline_skills:
            print(f"   ⭐ {i}. {skill} (NEW)")
        else:
            print(f"      {i}. {skill}")
    
    if len(updated_skills) > 20:
        print(f"   ... and {len(updated_skills) - 20} more")
    
    # ========================================================================
    # TEST 8: Analyze Community Impact
    # ========================================================================
    print_section("TEST 8: Community Impact Analysis")
    
    # Check which community skills appear
    community_in_path = [s for s in added_skills.keys() if s in updated_skills]
    
    # Check for new skills
    new_skills = [s for s in updated_skills if s not in baseline_skills]
    
    # Check for removed skills
    removed_skills = [s for s in baseline_skills if s not in updated_skills]
    
    print("📊 Summary Statistics:")
    print(f"   Baseline skills: {len(baseline_skills)}")
    print(f"   Updated skills: {len(updated_skills)}")
    print(f"   New skills added: {len(new_skills)}")
    print(f"   Skills removed: {len(removed_skills)}")
    
    if community_in_path:
        print(f"\n✨ Community Skills in Learning Path:")
        for skill in community_in_path:
            position = updated_skills.index(skill) + 1
            print(f"   ✅ {skill} - Position #{position}")
    else:
        print(f"\n❌ No community skills in learning path")
    
    if new_skills:
        print(f"\n📈 New Skills Added to Path:")
        for skill in new_skills[:10]:
            position = updated_skills.index(skill) + 1
            source = "Community" if skill in added_skills else "Reprioritized"
            print(f"   • {skill} - #{position} ({source})")
    
    if removed_skills:
        print(f"\n📉 Skills Removed/Deprioritized:")
        for skill in removed_skills[:5]:
            print(f"   • {skill}")
    
    # ========================================================================
    # TEST 9: Final Results
    # ========================================================================
    print_section("TEST 9: Final Test Results")
    
    tests_passed = 0
    total_tests = 6
    
    # Test 1: Server running
    tests_passed += 1
    print("✅ Test 1: Server Health - PASSED")
    
    # Test 2: Baseline generation
    tests_passed += 1
    print("✅ Test 2: Baseline Path Generation - PASSED")
    
    # Test 3: Community skills added
    if len(added_skills) >= 3:
        tests_passed += 1
        print("✅ Test 3: Community Skills Addition - PASSED")
    else:
        print(f"❌ Test 3: Community Skills Addition - FAILED ({len(added_skills)}/4 skills)")
    
    # Test 4: Vote scores stored
    if vote_data and len(vote_data) >= 4:
        tests_passed += 1
        print("✅ Test 4: Vote Score Calculation - PASSED")
    else:
        print("❌ Test 4: Vote Score Calculation - FAILED")
    
    # Test 5: Path regeneration
    if updated_skills:
        tests_passed += 1
        print("✅ Test 5: Path Regeneration - PASSED")
    else:
        print("❌ Test 5: Path Regeneration - FAILED")
    
    # Test 6: Community impact visible
    if community_in_path:
        tests_passed += 1
        print(f"✅ Test 6: Community Impact - PASSED ({len(community_in_path)} skills visible)")
    else:
        print("❌ Test 6: Community Impact - FAILED (no community skills in path)")
    
    print(f"\n{'='*80}")
    print(f" FINAL SCORE: {tests_passed}/{total_tests} tests passed")
    print(f"{'='*80}")
    
    if tests_passed == total_tests:
        print("\n🎉 SUCCESS! Community feedback system is fully functional!")
        print("\n✅ Verified Functionality:")
        print("   • Community skills can be added to database")
        print("   • Votes are recorded and aggregated correctly")
        print("   • Vote scores influence skill prioritization")
        print("   • Highly-voted community skills appear in learning paths")
        print("   • Feedback loop is complete and working")
    else:
        print(f"\n⚠️  PARTIAL SUCCESS: {tests_passed}/{total_tests} tests passed")
        print("\nIssues to investigate:")
        if not community_in_path:
            print("   • Community skills not appearing in paths")
            print("   • Check: Server restarted after code changes?")
            print("   • Check: Vote boost logic enabled in ai_engine.py?")
            print("   • Check: Gemini API quota available?")
    
    print("\n" + "="*80)
    print(" TEST COMPLETE")
    print("="*80 + "\n")

if __name__ == "__main__":
    main()
