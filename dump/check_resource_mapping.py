import json

# Load the test result
with open('test_skill_resources_fix.json', 'r', encoding='utf-8') as f:
    data = json.load(f)

print("=" * 80)
print("SKILLS IN LEARNING SESSIONS vs SKILLS IN SKILL_RESOURCES")
print("=" * 80)

# Get all skills from learning sessions
session_skills = set()
for session in data['learning_path']:
    session_skills.update(session.get('skills', []))

# Get all skills from skill_resources
resource_skills = {r['skill_name']: len(r['resources']) for r in data.get('skill_resources', [])}

print(f"\nTotal skills in learning sessions: {len(session_skills)}")
print(f"Total skills in skill_resources: {len(resource_skills)}")

# Find mismatches
print("\n" + "=" * 80)
print("SKILLS IN SESSIONS BUT NOT IN RESOURCES:")
print("=" * 80)
missing = [s for s in session_skills if s not in resource_skills]
for skill in sorted(missing):
    print(f"  ❌ {skill}")

print("\n" + "=" * 80)
print("SKILLS IN RESOURCES:")
print("=" * 80)
for skill, count in sorted(resource_skills.items())[:30]:
    status = "✅" if count > 0 else "❌"
    print(f"  {status} {skill} ({count} resources)")

print("\n" + "=" * 80)
print("SAMPLE SESSION:")
print("=" * 80)
if data['learning_path']:
    session = data['learning_path'][0]
    print(f"Title: {session.get('title', 'Unknown')}")
    print(f"Skills: {session.get('skills', [])}")
