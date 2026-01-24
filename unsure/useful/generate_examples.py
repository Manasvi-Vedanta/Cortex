"""
Generate example JSON files from actual API responses
This script calls each endpoint and saves the response to examples/ folder
"""

import requests
import json
import os
from datetime import datetime

BASE_URL = "http://localhost:5000"
EXAMPLES_DIR = "examples"

# Create examples directory if it doesn't exist
os.makedirs(EXAMPLES_DIR, exist_ok=True)

print("=" * 80)
print("GENERATING API RESPONSE EXAMPLES")
print("=" * 80)
print(f"Started: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
print(f"Saving to: {EXAMPLES_DIR}/\n")

def save_response(filename, data):
    """Save JSON response to file"""
    filepath = os.path.join(EXAMPLES_DIR, filename)
    with open(filepath, 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=2, ensure_ascii=False)
    print(f"[SAVED] {filename}")
    return filepath

# 1. Vote Response
print("\n1. Capturing vote response...")
vote_response = requests.post(f"{BASE_URL}/api/feedback/vote", json={
    "item_uri": "http://data.europa.eu/esco/skill/example-python",
    "item_type": "skill",
    "user_id": "example_user",
    "vote": 1
})
if vote_response.status_code == 200:
    save_response("vote_response.json", vote_response.json())

# 2. Suggest Response
print("2. Capturing suggestion response...")
suggest_response = requests.post(f"{BASE_URL}/api/feedback/suggest", json={
    "item_uri": "http://data.europa.eu/esco/skill/example-python",
    "item_type": "skill",
    "user_id": "example_user",
    "suggestion_type": "improve_description",
    "suggestion_text": "Add more practical examples for beginners"
})
if suggest_response.status_code == 200:
    suggestion_data = suggest_response.json()
    save_response("suggest_response.json", suggestion_data)
    suggestion_id = suggestion_data.get('suggestion_id')
    
    # 3. Vote on Suggestion
    if suggestion_id:
        print("3. Capturing vote on suggestion response...")
        vote_suggest_response = requests.post(
            f"{BASE_URL}/api/feedback/suggestions/{suggestion_id}/vote",
            json={"user_id": "example_user_2", "vote": 1}
        )
        if vote_suggest_response.status_code == 200:
            save_response("vote_on_suggestion_response.json", vote_suggest_response.json())

# 4. Pending Suggestions
print("4. Capturing pending suggestions...")
pending_response = requests.get(f"{BASE_URL}/api/feedback/suggestions/pending", params={"min_score": 0})
if pending_response.status_code == 200:
    save_response("pending_suggestions_response.json", pending_response.json())

# 5. Trending Items
print("5. Capturing trending items...")
trending_response = requests.get(f"{BASE_URL}/api/feedback/trending", params={
    "type": "skill",
    "days": 30,
    "limit": 10
})
if trending_response.status_code == 200:
    save_response("trending_response.json", trending_response.json())

# 6. Community Metrics
print("6. Capturing community metrics...")
metrics_response = requests.get(f"{BASE_URL}/api/feedback/metrics")
if metrics_response.status_code == 200:
    save_response("metrics_response.json", metrics_response.json())

# 7. Visualize Learning Path
print("7. Capturing visualization data...")
sample_path = [
    {
        "session_number": 1,
        "title": "Python Fundamentals",
        "skills": ["python", "variables", "data types", "control flow"],
        "estimated_duration_hours": 25,
        "difficulty_level": "beginner",
        "prerequisites": []
    },
    {
        "session_number": 2,
        "title": "Object-Oriented Programming",
        "skills": ["classes", "inheritance", "polymorphism", "encapsulation"],
        "estimated_duration_hours": 30,
        "difficulty_level": "intermediate",
        "prerequisites": ["Python Fundamentals"]
    },
    {
        "session_number": 3,
        "title": "Data Science with Python",
        "skills": ["pandas", "numpy", "matplotlib", "data analysis"],
        "estimated_duration_hours": 40,
        "difficulty_level": "advanced",
        "prerequisites": ["Object-Oriented Programming"]
    }
]

visualize_response = requests.post(f"{BASE_URL}/api/path/visualize", json={
    "learning_path": sample_path
})
if visualize_response.status_code == 200:
    viz_data = visualize_response.json()
    save_response("visualize_response.json", viz_data)
    
    # Also save individual components
    if 'gantt_data' in viz_data:
        save_response("gantt_sample.json", viz_data['gantt_data'])
    if 'dependency_graph' in viz_data:
        save_response("dependency_graph_sample.json", viz_data['dependency_graph'])

# 8. Search Resources
print("8. Capturing resource search...")
search_response = requests.get(f"{BASE_URL}/api/resources/search", params={
    "skill": "python programming",
    "limit": 5
})
if search_response.status_code == 200:
    save_response("search_resources_response.json", search_response.json())

# 9. Add Resource
print("9. Capturing add resource response...")
add_resource_response = requests.post(f"{BASE_URL}/api/resources/add", json={
    "skill_uri": "http://data.europa.eu/esco/skill/example-python",
    "resource_url": "https://docs.python.org/3/tutorial/",
    "resource_title": "Official Python Tutorial",
    "resource_type": "documentation",
    "provider": "Python.org",
    "description": "Comprehensive Python tutorial from official docs",
    "difficulty_level": "beginner",
    "is_free": True,
    "estimated_duration": "10 hours"
})
if add_resource_response.status_code == 200:
    save_response("add_resource_response.json", add_resource_response.json())

# 10. Get Resources for Skill
print("10. Capturing skill resources...")
skill_resources_response = requests.get(
    f"{BASE_URL}/api/resources/skill/http%3A%2F%2Fdata.europa.eu%2Fesco%2Fskill%2Fexample-python",
    params={"difficulty": "beginner", "min_quality": 0, "validated_only": False}
)
if skill_resources_response.status_code == 200:
    save_response("get_skill_resources_response.json", skill_resources_response.json())

# 11. Rate Resource
print("11. Capturing resource rating...")
rate_response = requests.post(f"{BASE_URL}/api/resources/rate", json={
    "resource_url": "https://docs.python.org/3/tutorial/",
    "skill_uri": "http://data.europa.eu/esco/skill/example-python",
    "user_id": "example_user",
    "rating": 5,
    "quality_score": 9,
    "review_text": "Excellent resource for beginners!"
})
if rate_response.status_code == 200:
    save_response("rate_resource_response.json", rate_response.json())

# 12. Popular Resources
print("12. Capturing popular resources...")
popular_response = requests.get(f"{BASE_URL}/api/resources/popular", params={
    "days": 30,
    "limit": 10
})
if popular_response.status_code == 200:
    save_response("popular_resources_response.json", popular_response.json())

# 13. Integrated: Path with Resources
print("13. Capturing integrated path with resources...")
print("    (This may take 30-60 seconds...)")
integrated_response = requests.post(f"{BASE_URL}/api/path/with-resources", json={
    "goal": "I want to become a Python developer specializing in web applications",
    "current_skills": ["HTML", "CSS", "JavaScript basics"],
    "user_id": "example_user"
}, timeout=60)
if integrated_response.status_code == 200:
    save_response("path_with_resources_response.json", integrated_response.json())

print("\n" + "=" * 80)
print("GENERATION COMPLETE!")
print("=" * 80)
print(f"\nAll example JSON files have been saved to: {EXAMPLES_DIR}/")
print("You can now inspect these files to see the exact structure of API responses.")
print("\nFiles created:")
for filename in sorted(os.listdir(EXAMPLES_DIR)):
    if filename.endswith('.json'):
        filepath = os.path.join(EXAMPLES_DIR, filename)
        size = os.path.getsize(filepath)
        print(f"  - {filename} ({size} bytes)")
