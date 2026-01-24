import json
import glob

# Load all test results  
test_files = glob.glob('learning_path_*_20251116_*.json')
# Get the newest test results (161237, 161314, 161347 etc)
test_files = [f for f in test_files if '161237' in f or '161314' in f or '161347' in f or '161425' in f or '161501' in f]

for test_file in test_files[:5]:  # Check all 5 paths
    print("\n" + "=" * 80)
    print(f"ANALYZING: {test_file}")
    print("=" * 80)
    
    with open(test_file, 'r', encoding='utf-8') as f:
        data = json.load(f)

    # Find skills with 0 resources
    print("\nSKILLS WITH 0 RESOURCES:")
    zero_resources = [r for r in data.get('skill_resources', []) if len(r.get('resources', [])) == 0]
    for r in zero_resources[:15]:
        print(f"  ❌ {r['skill_name']}")
    
    if not zero_resources:
        print("  ✅ All skills have resources!")
    else:
        print(f"\n  Total: {len(zero_resources)} skills with 0 resources")
    
    # Check for potentially irrelevant skills
    print("\nPOTENTIALLY IRRELEVANT SKILLS:")
    all_skills = []
    for session in data.get('learning_path', []):
        all_skills.extend(session.get('skills', []))
    
    # Expanded list of irrelevant keywords for technical careers
    irrelevant_keywords = [
        'literature', 'W3C', 'DNS', 'governance', 'preservation',
        'metadata management', 'infrastructure management', 'process improvement',
        'content creation', 'digital literacy', 'ethical reasoning',
        'visual communication', 'creative thinking', 'design thinking',
        'critical thinking', 'logical thinking', 'analytical thinking',
        'research and analysis', 'tool proficiency'
    ]
    
    potentially_irrelevant = []
    for skill in all_skills:
        for keyword in irrelevant_keywords:
            if keyword.lower() in skill.lower():
                potentially_irrelevant.append(skill)
                break
    
    for skill in set(potentially_irrelevant):
        print(f"  ⚠️  {skill}")
    
    if not potentially_irrelevant:
        print("  ✅ No obviously irrelevant skills found!")
    else:
        print(f"\n  Total: {len(set(potentially_irrelevant))} potentially irrelevant skills")
    
    # Show total unique skills
    print(f"\nTOTAL UNIQUE SKILLS: {len(set(all_skills))}")
