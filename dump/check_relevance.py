"""Check what relevance scores community skills are getting."""
import sqlite3

occupation_uri = "http://data.europa.eu/esco/occupation/1c5a45b9-440e-4726-b565-16a952abd341"

print("\n" + "="*80)
print(" CHECKING COMMUNITY SKILL RELEVANCE SCORES")
print("="*80 + "\n")

# Check if TensorFlow, PyTorch match any keywords
data_science_priority_skills = {
    'python': 10, 'sql': 10, 'r': 9, 'statistics': 10, 'machine learning': 10,
    'data analysis': 10, 'statistical analysis': 9, 'programming': 9,
    'data visualization': 8, 'data mining': 8, 'predictive modeling': 8,
    'statistical modeling': 8, 'artificial intelligence': 8, 'deep learning': 7,
}

high_value_keywords = ['python', 'sql', 'statistics', 'machine learning', 'data']
medium_value_keywords = ['analytic', 'model', 'algorithm', 'programming', 'research', 'quantitative']

test_skills = ['TensorFlow', 'PyTorch', 'MLflow', 'Kubeflow', 'Docker', 'Kubernetes']

for skill in test_skills:
    label_lower = skill.lower()
    relevance_score = 0
    
    # Check priority skills
    for priority_skill, score in data_science_priority_skills.items():
        if priority_skill in label_lower:
            relevance_score = score
            print(f"{skill}: Matched '{priority_skill}' → relevance_score = {score}")
            break
    
    if relevance_score == 0:
        # Check high value keywords
        for keyword in high_value_keywords:
            if keyword in label_lower:
                relevance_score = 8
                print(f"{skill}: Matched high keyword '{keyword}' → relevance_score = 8")
                break
    
    if relevance_score == 0:
        # Check medium value keywords
        for keyword in medium_value_keywords:
            if keyword in label_lower:
                relevance_score = 6
                print(f"{skill}: Matched medium keyword '{keyword}' → relevance_score = 6")
                break
    
    if relevance_score == 0:
        print(f"{skill}: NO keyword match → relevance_score = 0 → ELIGIBLE FOR BOOST!")

print("\n" + "="*80)
print(" CONCLUSION")
print("="*80 + "\n")

print("If skills show 'relevance_score = 0', they should be boosted by community votes.")
print("If they have a relevance_score > 0, the boost logic won't apply!")
print("\nThis is the issue: boost only applies when relevance_score == 0")

print("\n" + "="*80 + "\n")
