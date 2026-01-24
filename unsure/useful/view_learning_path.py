"""
Quick script to generate and display a detailed learning path
"""

import sys
import os
import json

# Add current directory to path
sys.path.insert(0, os.path.dirname(__file__))

from ai_engine import GenMentorAI

print("=" * 80)
print("GenMentor - Learning Path Generation Demo")
print("=" * 80)

# Initialize AI Engine
print("\n🔧 Initializing AI Engine...")
ai_engine = GenMentorAI()
print("✅ AI Engine initialized\n")

# Test case
goal = "I want to transition from marketing to data science"
current_skills = ["marketing analytics", "excel", "basic statistics"]

print(f"📋 Goal: {goal}")
print(f"📋 Current Skills: {', '.join(current_skills)}")
print("\n" + "=" * 80)

# Step 1: Skill Gap Analysis
print("\n🔍 STEP 1: Skill Gap Analysis")
print("-" * 80)
result = ai_engine.identify_skill_gap(goal, current_skills)

print(f"\n✅ Matched Occupation: {result['matched_occupation']['label']}")
print(f"   Similarity Score: {result['matched_occupation']['similarity_score']*100:.1f}%")
print(f"\n📊 Skills Summary:")
print(f"   Total skills needed: {result.get('total_skills_needed', 0)}")
print(f"   Skills to learn: {len(result['skill_gap'])}")
print(f"   Recognized skills: {len(result.get('recognized_skills', []))}")

print(f"\n📚 Skills to Learn:")
for i, skill in enumerate(result['skill_gap'][:15], 1):  # Show first 15
    print(f"   {i}. {skill['label']}")
if len(result['skill_gap']) > 15:
    print(f"   ... and {len(result['skill_gap']) - 15} more")

# Step 2: Learning Path Generation
print("\n" + "=" * 80)
print("\n🎯 STEP 2: Learning Path Generation")
print("-" * 80)
learning_path = ai_engine.schedule_learning_path(result['skill_gap'])

print(f"\n✅ Generated {len(learning_path)} learning sessions")
print(f"   Total duration: {sum(s.get('estimated_duration_hours', 0) for s in learning_path)} hours")

# Display detailed learning path
print("\n" + "=" * 80)
print("📖 DETAILED LEARNING PATH")
print("=" * 80)

for session in learning_path:
    print(f"\n{'='*80}")
    print(f"Session {session.get('session_number', '?')}: {session.get('title', 'Untitled')}")
    print(f"{'='*80}")
    print(f"⏱️  Duration: {session.get('estimated_duration_hours', 0)} hours")
    print(f"📊 Difficulty: {session.get('difficulty_level', 'N/A')}")
    
    if session.get('objectives'):
        print(f"\n🎯 Objectives:")
        for obj in session['objectives']:
            print(f"   • {obj}")
    
    if session.get('skills'):
        print(f"\n📚 Skills Covered ({len(session['skills'])} skills):")
        for skill in session['skills']:
            if isinstance(skill, dict):
                print(f"   • {skill.get('label', skill)}")
            else:
                print(f"   • {skill}")
    
    if session.get('prerequisites'):
        print(f"\n⚠️  Prerequisites:")
        for prereq in session['prerequisites']:
            print(f"   • {prereq}")
    
    print()

# Save to JSON
output_file = "sample_learning_path.json"
output_data = {
    "goal": goal,
    "current_skills": current_skills,
    "matched_occupation": result['matched_occupation'],
    "skill_gap_summary": {
        "total_skills_needed": result.get('total_skills_needed', 0),
        "skills_to_learn": len(result['skill_gap']),
        "recognized_skills": len(result.get('recognized_skills', []))
    },
    "learning_path": learning_path,
    "total_sessions": len(learning_path),
    "total_hours": sum(s.get('estimated_duration_hours', 0) for s in learning_path)
}

with open(output_file, 'w', encoding='utf-8') as f:
    json.dump(output_data, f, indent=2, ensure_ascii=False)

print("\n" + "=" * 80)
print(f"✅ Full learning path saved to: {output_file}")
print("=" * 80)
