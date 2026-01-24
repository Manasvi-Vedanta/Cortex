"""Minimal test."""
import sys

# Check if Docker is in the skill data
all_skills = [
    ('uri1', 'Python', 'desc', 'essential', 0.8, 5),
    ('uri2', 'Docker', 'Community-suggested skill', 'optional', 1.0, 10),
    ('uri3', 'SQL', 'desc', 'essential', 0.5, 3),
]

print("\n" + "="*80)
print("Testing filter logic")
print("="*80)

for skill_data in all_skills:
    if len(skill_data) == 6:
        uri, label, description, relation_type, vote_score, vote_count = skill_data
    else:
        uri, label, description, relation_type = skill_data
        vote_score, vote_count = 0.0, 0
    
    print(f"\nProcessing: {label}")
    print(f"  Vote score: {vote_score}, count: {vote_count}")
    
    relevance_score = 0
    
    # Check Docker specifically
    if label == 'Docker':
        print(f"  Docker found! Checking boost criteria...")
        if relevance_score == 0 and vote_score >= 0.7 and vote_count >= 3:
            relevance_score = 7
            print(f"  ✅ Boosted to relevance {relevance_score}")
        else:
            print(f"  ❌ Not boosted (relevance={relevance_score}, score={vote_score}, count={vote_count})")
    
    print(f"  Final relevance: {relevance_score}")
    
    if relevance_score > 0 or relation_type == 'essential':
        print(f"  ✅ INCLUDED")
    else:
        print(f"  ❌ FILTERED OUT")

print("\n" + "="*80)
