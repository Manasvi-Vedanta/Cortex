"""
Live System Demonstration for Final Report Screenshots
"""

from ai_engine import GenMentorAI
import json

print('='*70)
print('LIVE SYSTEM DEMONSTRATION - Data Scientist Career Path')
print('='*70)

ai = GenMentorAI()

print()
print('INPUT:')
print('  Goal: I want to become a data scientist')
print('  Current Skills: [Python, Excel, Basic Statistics]')
print()

result = ai.identify_skill_gap(
    'I want to become a data scientist',
    ['Python', 'Excel', 'Basic Statistics']
)

print('='*70)
print('OUTPUT:')
print('='*70)
print()
print('MATCHED OCCUPATION:')
occ = result['matched_occupation']
print(f"  Title: {occ['label']}")
print(f"  Similarity Score: {occ['similarity_score']*100:.1f}%")
print()
print('SKILL GAP ANALYSIS:')
print(f"  Total Skills Required: {result['total_skills_needed']}")
print(f"  Skills to Learn: {result['skills_to_learn']}")
print(f"  Recognized User Skills: {len(result['recognized_skills'])}")
print()
print('TOP 10 SKILLS TO LEARN:')
for i, skill in enumerate(result['skill_gap'][:10], 1):
    label = skill['label']
    rel_type = skill['relation_type']
    priority = skill['priority']
    difficulty = skill.get('difficulty', 'N/A')
    print(f"  {i}. {label}")
    print(f"     Type: {rel_type}, Priority: {priority}, Difficulty: {difficulty}")
print()

# Generate learning path
print('='*70)
print('LEARNING PATH GENERATION')
print('='*70)
path = ai.schedule_learning_path(result['skill_gap'][:15])
print(f"Generated {len(path)} learning sessions")
print()
for session in path[:5]:
    num = session.get('session_number', '?')
    title = session.get('title', 'Untitled')
    duration = session.get('estimated_duration_hours', 0)
    difficulty = session.get('difficulty_level', 'N/A')
    skills_list = session.get('skills', [])[:3]
    
    print(f"Session {num}:")
    print(f"  Title: {title}")
    print(f"  Duration: {duration} hours")
    print(f"  Difficulty: {difficulty}")
    print(f"  Skills: {skills_list}")
    print()

print('='*70)
print('DEMONSTRATION COMPLETE')
print('='*70)
