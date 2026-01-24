"""
Test to compare skill coverage before and after fixes
"""
from test_real_learning_paths import RealLearningPathTests
import json

print("=" * 80)
print("TESTING COMPREHENSIVE SKILL COVERAGE WITH FIXES")
print("=" * 80)

tester = RealLearningPathTests()

# Test Mobile Developer (had most skills in database: 149)
scenario = {
    'name': 'Mobile Developer Comprehensive',
    'goal': 'I want to become a mobile app developer for iOS and Android',
    'current_skills': []
}

print("\n🎯 Testing Mobile Developer (Database has 149 skills for this occupation)")
print("=" * 80)

result = tester.test_learning_path_generation(scenario)

print("\n" + "=" * 80)
print("RESULTS SUMMARY")
print("=" * 80)
print(f"✅ Matched Occupation: {result['matched_occupation']['label']}")
print(f"✅ Skills Identified: {len(result.get('skill_resources', []))}")
print(f"✅ Total Resources Found: {result['statistics']['total_resources']}")
print(f"✅ Learning Sessions: {len(result['learning_path'])}")
print(f"✅ Total Study Hours: {result['statistics']['total_hours']}")

# Check resource coverage
skills_with_resources = sum(1 for sr in result.get('skill_resources', []) if len(sr['resources']) > 0)
skills_without_resources = len(result.get('skill_resources', [])) - skills_with_resources

print(f"\n📊 Resource Coverage:")
print(f"  - Skills with resources: {skills_with_resources}/{len(result.get('skill_resources', []))} ({skills_with_resources*100//max(len(result.get('skill_resources', [])), 1)}%)")
print(f"  - Skills without resources: {skills_without_resources}")

# Save detailed result
with open('mobile_developer_comprehensive_test.json', 'w', encoding='utf-8') as f:
    json.dump(result, f, indent=2, ensure_ascii=False)

print(f"\n✅ Detailed results saved to: mobile_developer_comprehensive_test.json")

# Show sample skills
print("\n" + "=" * 80)
print("SAMPLE SKILLS (First 20)")
print("=" * 80)
for i, sr in enumerate(result.get('skill_resources', [])[:20], 1):
    status = "✅" if len(sr['resources']) > 0 else "❌"
    print(f"{i:2}. {status} {sr['skill_name']} ({len(sr['resources'])} resources)")
