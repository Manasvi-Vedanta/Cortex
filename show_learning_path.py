"""
Display a detailed learning path for verification
"""

from ai_engine import GenMentorAI
import json
from datetime import datetime

print("=" * 80)
print(" GenMentor Learning Path Display")
print("=" * 80)

# Initialize AI engine
print("\n🔧 Initializing AI Engine...")
ai_engine = GenMentorAI()
print("✅ AI Engine initialized\n")

# Test case: Marketing to Data Science
goal = "I want to transition from marketing to data science"
current_skills = ["excel", "google analytics", "marketing strategy"]

print(f"📝 Goal: {goal}")
print(f"📚 Current Skills: {', '.join(current_skills)}\n")

print("🔍 Analyzing skill gap...")
result = ai_engine.identify_skill_gap(goal, current_skills)

print(f"\n✅ Matched Occupation: {result['matched_occupation']['label']}")
print(f"📊 Similarity Score: {result['matched_occupation']['similarity_score']:.1%}")
print(f"🎯 Skills Identified: {len(result['skill_gap'])} skills to learn\n")

print("=" * 80)
print(" IDENTIFIED SKILLS GAP")
print("=" * 80)

for i, skill in enumerate(result['skill_gap'][:20], 1):  # Show first 20
    print(f"{i:2}. {skill['label']}")
    if skill.get('description'):
        print(f"    📝 {skill['description'][:100]}...")
    print()

print("\n🗓️ Generating learning path with sessions...")
learning_path = ai_engine.schedule_learning_path(result['skill_gap'])

print("\n" + "=" * 80)
print(" COMPLETE LEARNING PATH")
print("=" * 80)

total_hours = 0
for session in learning_path:
    session_num = session.get('session_number', '?')
    title = session.get('title', 'Untitled Session')
    duration = session.get('estimated_duration_hours', 0)
    difficulty = session.get('difficulty_level', 'unknown')
    skills = session.get('skills', [])
    objectives = session.get('objectives', [])
    
    total_hours += duration
    
    print(f"\n📚 Session {session_num}: {title}")
    print(f"   ⏱️  Duration: {duration} hours")
    print(f"   📊 Difficulty: {difficulty.upper()}")
    
    if objectives:
        print(f"   🎯 Objectives:")
        for obj in objectives[:3]:  # Show first 3 objectives
            print(f"      • {obj}")
    
    print(f"   📖 Skills Covered ({len(skills)}):")
    for skill in skills:
        if isinstance(skill, dict):
            skill_name = skill.get('label', str(skill))
        else:
            skill_name = str(skill)
        print(f"      ✓ {skill_name}")
    
    print("   " + "-" * 76)

print("\n" + "=" * 80)
print(" LEARNING PATH SUMMARY")
print("=" * 80)
print(f"\n📊 Total Sessions: {len(learning_path)}")
print(f"⏱️  Total Duration: {total_hours} hours (~{total_hours//8} days at 8hrs/day)")
print(f"🎯 Total Skills: {sum(len(s.get('skills', [])) for s in learning_path)}")

# Count by difficulty
beginner = sum(1 for s in learning_path if s.get('difficulty_level') == 'beginner')
intermediate = sum(1 for s in learning_path if s.get('difficulty_level') == 'intermediate')
advanced = sum(1 for s in learning_path if s.get('difficulty_level') == 'advanced')

print(f"\n📈 Difficulty Distribution:")
print(f"   • Beginner: {beginner} sessions")
print(f"   • Intermediate: {intermediate} sessions")
print(f"   • Advanced: {advanced} sessions")

# Save detailed path
output_file = f"learning_path_detailed_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
with open(output_file, 'w', encoding='utf-8') as f:
    json.dump({
        'goal': goal,
        'current_skills': current_skills,
        'matched_occupation': result['matched_occupation'],
        'skill_gap': result['skill_gap'],
        'learning_path': learning_path,
        'summary': {
            'total_sessions': len(learning_path),
            'total_hours': total_hours,
            'total_skills': sum(len(s.get('skills', [])) for s in learning_path)
        }
    }, f, indent=2, ensure_ascii=False)

print(f"\n💾 Detailed learning path saved to: {output_file}")
print("\n" + "=" * 80)
