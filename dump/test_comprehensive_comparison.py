"""Comprehensive test to compare skill coverage and resource availability"""
import sqlite3
import json
from test_real_learning_paths import RealLearningPathTests

print("=" * 100)
print("COMPREHENSIVE DATABASE UTILIZATION TEST")
print("=" * 100)

# Connect to database
conn = sqlite3.connect('genmentor.db')
cursor = conn.cursor()

# Get database statistics
cursor.execute("SELECT COUNT(*) FROM skills")
total_skills = cursor.fetchone()[0]

cursor.execute("SELECT COUNT(*) FROM occupations")
total_occupations = cursor.fetchone()[0]

cursor.execute("SELECT COUNT(*) FROM occupation_skill_relations")
total_relations = cursor.fetchone()[0]

print(f"\n📊 DATABASE STATISTICS:")
print(f"  Total Skills in Database: {total_skills:,}")
print(f"  Total Occupations: {total_occupations:,}")
print(f"  Total Occupation-Skill Relations: {total_relations:,}")

# Test a comprehensive career path
print("\n" + "=" * 100)
print("TESTING: Full-Stack Web Developer (Comprehensive)")
print("=" * 100)

# Get actual skills for web developer from database
cursor.execute("""
    SELECT COUNT(DISTINCT skill_uri) 
    FROM occupation_skill_relations 
    WHERE occupation_uri = 'http://data.europa.eu/esco/occupation/c40a2919-48a9-40ea-b506-1f34f693496d'
    AND relation_type = 'essential'
""")
db_essential_skills = cursor.fetchone()[0]

print(f"\n📚 Database has {db_essential_skills} essential skills for Web Developer")

conn.close()

# Run actual test
print("\n🔄 Generating learning path...")
tester = RealLearningPathTests()

scenario = {
    'name': 'Full-Stack Web Developer',
    'goal': 'I want to become a full-stack web developer with expertise in modern frameworks',
    'current_skills': []
}

result = tester.test_learning_path_generation(scenario)

# Analyze results
print("\n" + "=" * 100)
print("RESULTS ANALYSIS")
print("=" * 100)

skills_identified = result['statistics']['total_skills']
skills_in_db = db_essential_skills
coverage_percent = (skills_identified / skills_in_db * 100) if skills_in_db > 0 else 0

print(f"\n📈 SKILL COVERAGE:")
print(f"  Skills Available in Database: {skills_in_db}")
print(f"  Skills Identified for Learning: {skills_identified}")
print(f"  Coverage: {coverage_percent:.1f}%")
print(f"  Filtered Out: {skills_in_db - skills_identified} skills")

# Resource coverage
skill_resources = result.get('skill_resources', [])
skills_with_resources = sum(1 for sr in skill_resources if len(sr['resources']) > 0)
resource_coverage = (skills_with_resources / len(skill_resources) * 100) if skill_resources else 0

print(f"\n📚 RESOURCE COVERAGE:")
print(f"  Total Skills in Path: {len(skill_resources)}")
print(f"  Skills with Resources: {skills_with_resources}")
print(f"  Skills without Resources: {len(skill_resources) - skills_with_resources}")
print(f"  Resource Coverage: {resource_coverage:.1f}%")
print(f"  Total Resources Found: {result['statistics']['total_resources']}")

# Learning sessions
print(f"\n📖 LEARNING SESSIONS:")
print(f"  Total Sessions: {len(result['learning_path'])}")
print(f"  Estimated Hours: {result['statistics']['total_hours']}")
print(f"  Estimated Days: {result['statistics']['duration_days']}")

# Show skills without resources
if skill_resources:
    no_resources = [sr['skill_name'] for sr in skill_resources if len(sr['resources']) == 0]
    if no_resources:
        print(f"\n⚠️  SKILLS WITHOUT RESOURCES ({len(no_resources)}):")
        for skill in no_resources[:10]:
            print(f"    - {skill}")
        if len(no_resources) > 10:
            print(f"    ... and {len(no_resources) - 10} more")

print("\n" + "=" * 100)
print("RECOMMENDATIONS FOR IMPROVEMENT")
print("=" * 100)

if coverage_percent < 50:
    print("\n❌ LOW SKILL COVERAGE - Consider:")
    print("  1. Reduce aggressive filtering in _is_soft_or_irrelevant_skill()")
    print("  2. Allow more skills from database to pass through")
    print("  3. Review filter keywords to avoid removing technical skills")

if resource_coverage < 80:
    print("\n⚠️  LOW RESOURCE COVERAGE - Consider:")
    print("  1. Add more curated resources for common skills")
    print("  2. Implement GitHub 'awesome-*' list scraping")
    print("  3. Add RAG-based resource discovery")
    print("  4. Query educational APIs (Coursera, Udemy, YouTube)")

if coverage_percent >= 50 and resource_coverage >= 80:
    print("\n✅ GOOD COVERAGE LEVELS ACHIEVED!")
    print("  - Skill identification is working well")
    print("  - Resource discovery is comprehensive")
    print("  - Learning paths are detailed and actionable")

# Save detailed report
with open('comprehensive_test_report.json', 'w', encoding='utf-8') as f:
    json.dump({
        'database_stats': {
            'total_skills': total_skills,
            'total_occupations': total_occupations,
            'total_relations': total_relations,
            'web_dev_essential_skills': db_essential_skills
        },
        'test_results': {
            'skills_identified': skills_identified,
            'coverage_percent': coverage_percent,
            'resource_coverage': resource_coverage,
            'total_resources': result['statistics']['total_resources'],
            'total_sessions': len(result['learning_path']),
            'total_hours': result['statistics']['total_hours']
        },
        'skills_without_resources': no_resources if 'no_resources' in locals() else []
    }, f, indent=2)

print(f"\n💾 Detailed report saved to: comprehensive_test_report.json")
print("=" * 100)
