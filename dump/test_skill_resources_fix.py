"""Quick test to verify skill_resources are properly included"""
from test_real_learning_paths import RealLearningPathTests
import json

print("Running quick test...")
tester = RealLearningPathTests()

scenario = {
    'name': 'Web Developer Test',
    'goal': 'I want to become a web developer',
    'current_skills': []
}

print("\n" + "=" * 80)
print("Testing Web Developer path with skill_resources fix")
print("=" * 80)

result = tester.test_learning_path_generation(scenario)

print(f"\nResult keys: {list(result.keys())}")
print(f"Skill resources count: {len(result.get('skill_resources', []))}")

if result.get('skill_resources'):
    print("\nFirst 5 skills with resources:")
    for sr in result['skill_resources'][:5]:
        print(f"  - {sr['skill_name']}: {len(sr['resources'])} resources")
else:
    print("\n❌ No skill_resources found!")

# Save to JSON to verify structure
with open('test_skill_resources_fix.json', 'w', encoding='utf-8') as f:
    json.dump(result, f, indent=2, ensure_ascii=False)

print("\n✅ Test result saved to: test_skill_resources_fix.json")
