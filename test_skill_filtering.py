"""Quick test to check if soft skills are filtered out"""
from ai_engine import GenMentorAI

print("Testing skill filtering...")
engine = GenMentorAI()

# Test 1: Web Developer (should have no soft skills)
print("\n" + "="*80)
print("TEST 1: WEB DEVELOPER")
print("="*80)
result = engine.identify_skill_gap('I want to become a web developer', [])
print(f"\nTotal skills identified: {len(result['skill_gap'])}")
print("\nSkills to learn:")
for s in result['skill_gap'][:25]:
    print(f"  - {s['label']}")

# Test 2: Data Scientist (should have no soft skills)
print("\n" + "="*80)
print("TEST 2: DATA SCIENTIST")
print("="*80)
result2 = engine.identify_skill_gap('I want to become a data scientist', ['Python programming'])
print(f"\nTotal skills identified: {len(result2['skill_gap'])}")
print("\nSkills to learn:")
for s in result2['skill_gap'][:25]:
    print(f"  - {s['label']}")
