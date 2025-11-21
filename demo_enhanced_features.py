"""
COMPREHENSIVE DEMO - Enhanced Features
Shows actual outputs and visualizations for all three major features
"""

import json
import sys
import io
from datetime import datetime

# Fix encoding for Windows console
if sys.platform == 'win32':
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')

print("=" * 80)
print("ENHANCED FEATURES COMPREHENSIVE DEMO")
print("=" * 80)
print(f"Demo Started: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")

# ============================================================================
# DEMO 1: Community Feedback System
# ============================================================================
print("\n" + "=" * 80)
print("DEMO 1: COMMUNITY FEEDBACK SYSTEM")
print("=" * 80)

from community_feedback import CommunityFeedbackSystem

feedback = CommunityFeedbackSystem()

print("\n[1.1] Adding votes for different skills...")
vote_results = []
test_items = [
    ("http://data.europa.eu/esco/skill/python", "skill", "user1", 1),
    ("http://data.europa.eu/esco/skill/python", "skill", "user2", 1),
    ("http://data.europa.eu/esco/skill/javascript", "skill", "user1", 1),
    ("http://data.europa.eu/esco/skill/sql", "skill", "user3", -1),
]

for item_uri, item_type, user_id, vote in test_items:
    result = feedback.add_vote(item_uri, item_type, user_id, vote)
    skill_name = item_uri.split('/')[-1]
    vote_type = "upvote" if vote == 1 else "downvote"
    print(f"  - {user_id} gave {vote_type} to {skill_name}")
    print(f"    Result: {result}")
    vote_results.append(result)

print("\n[1.2] Getting vote statistics for Python...")
python_stats = feedback.get_vote_statistics("http://data.europa.eu/esco/skill/python", "skill")
print(json.dumps(python_stats, indent=2))

print("\n[1.3] Adding community suggestions...")
suggestion_id = feedback.add_suggestion(
    item_uri="http://data.europa.eu/esco/occupation/data-scientist",
    item_type="occupation",
    user_id="user1",
    suggestion_type="add_skill",
    suggestion_text="Should include Docker and Kubernetes for containerization skills"
)
print(f"  Created suggestion ID: {suggestion_id}")

# Vote on the suggestion
feedback.vote_on_suggestion(suggestion_id, "user2", 1)
feedback.vote_on_suggestion(suggestion_id, "user3", 1)
print(f"  Added 2 supporting votes")

suggestion_result = feedback.vote_on_suggestion(suggestion_id, "user4", 1)
print(f"  Suggestion voting result:")
print(json.dumps(suggestion_result, indent=2))

print("\n[1.4] Getting pending suggestions...")
pending = feedback.get_pending_suggestions(min_community_score=0)
print(f"  Total pending suggestions: {len(pending)}")
if pending:
    print(f"\n  Sample suggestion:")
    print(json.dumps(pending[0], indent=2))

print("\n[1.5] Getting trending items...")
trending = feedback.get_trending_items(item_type="skill", days=30, limit=5)
print(f"  Trending skills (last 30 days):")
for item in trending:
    print(f"    - {item['item_uri'].split('/')[-1]}: {item['vote_count']} votes (score: {item['net_score']})")

print("\n[1.6] Community Metrics Dashboard...")
metrics = feedback.get_community_metrics()
print(json.dumps(metrics, indent=2))

# ============================================================================
# DEMO 2: Learning Path Visualization
# ============================================================================
print("\n" + "=" * 80)
print("DEMO 2: LEARNING PATH VISUALIZATION & DATA CLEANING")
print("=" * 80)

from learning_path_visualizer import LearningPathVisualizer

visualizer = LearningPathVisualizer()

# Create a realistic learning path
demo_learning_path = [
    {
        "session_number": 1,
        "title": "Python Fundamentals",
        "skills": ["Python programming", "Variables", "Data types", "Control flow"],
        "estimated_duration_hours": "25 hours",  # String format (will be cleaned)
        "difficulty_level": "beginner",
        "prerequisites": []
    },
    {
        "session_number": 2,
        "title": "Object-Oriented Programming",
        "skills": ["Classes", "Inheritance", "Polymorphism", "Encapsulation"],
        "estimated_duration_hours": 30,  # Numeric format
        "difficulty_level": "intermediate",
        "prerequisites": ["Python Fundamentals"]
    },
    {
        "session_number": 3,
        "title": "Data Structures & Algorithms",
        "skills": ["Lists", "Dictionaries", "Sets", "Algorithms"],
        "estimated_duration_hours": "35",  # String numeric
        "difficulty_level": "intermediate",
        "prerequisites": ["Object-Oriented Programming"]
    },
    {
        "session_number": 4,
        "title": "Web Development with Flask",
        "skills": ["Flask framework", "REST APIs", "Database integration"],
        "estimated_duration_hours": 40,
        "difficulty_level": "advanced",
        "prerequisites": ["Data Structures & Algorithms"]
    },
    {
        "session_number": 5,
        "title": "Machine Learning Basics",
        "skills": ["NumPy", "Pandas", "Scikit-learn", "ML algorithms"],
        "estimated_duration_hours": 50,
        "difficulty_level": "advanced",
        "prerequisites": ["Data Structures & Algorithms", "Python Fundamentals"]
    }
]

print("\n[2.1] Original Learning Path (before cleaning)...")
print(f"  Total sessions: {len(demo_learning_path)}")
print(f"  Sample session (raw data):")
print(json.dumps(demo_learning_path[0], indent=2))

print("\n[2.2] Data Cleaning & Normalization...")
cleaned_path = visualizer.clean_learning_path(demo_learning_path)
print(f"  After cleaning:")
print(f"  - Duration normalized to hours: {cleaned_path[0]['estimated_duration_hours']}")
print(f"  - Prerequisites validated: {len(cleaned_path[0]['prerequisites'])}")
print(f"  Sample cleaned session:")
print(json.dumps(cleaned_path[0], indent=2))

print("\n[2.3] Generating Gantt Chart Data...")
gantt_data = visualizer.generate_gantt_chart_data(cleaned_path)
print(f"  Gantt Chart Summary:")
print(f"  - Total duration: {gantt_data['total_duration_hours']} hours")
print(f"  - Total days: {gantt_data['total_duration_days']} days")
print(f"  - Start date: {gantt_data['start_date']}")
print(f"  - Estimated completion: {gantt_data['estimated_completion_date']}")
print(f"\n  Task Timeline:")
for task in gantt_data['tasks']:
    print(f"    {task['name']}:")
    print(f"      Start: {task['start']}")
    print(f"      End: {task['end']}")
    print(f"      Duration: {task['duration_hours']} hours ({task['duration_days']} days)")
    print(f"      Difficulty: {task['difficulty']}")
    print(f"      Skills: {task['skills_count']}")
    print()

print("\n[2.4] Generating Dependency Graph...")
graph_data = visualizer.generate_dependency_graph_data(cleaned_path)
print(f"  Graph Metrics:")
print(json.dumps(graph_data['metrics'], indent=2))
print(f"\n  Nodes ({len(graph_data['nodes'])}):")
for node in graph_data['nodes']:
    print(f"    - {node['label']} (Level: {node.get('level', 'N/A')}, Difficulty: {node['difficulty']})")
print(f"\n  Edges ({len(graph_data['edges'])}):")
for edge in graph_data['edges']:
    from_node = next(n['label'] for n in graph_data['nodes'] if n['id'] == edge['from'])
    to_node = next(n['label'] for n in graph_data['nodes'] if n['id'] == edge['to'])
    print(f"    - {from_node} -> {to_node}")

print("\n[2.5] Skills Timeline...")
timeline = visualizer.generate_skills_timeline(cleaned_path)
print(f"  Total duration: {timeline['total_hours']} hours")
print(f"  Skills learned ({len(timeline['skills'])}):")
for skill_info in timeline['skills'][:10]:  # Show first 10
    print(f"    - {skill_info['skill_name']}")
    print(f"      Learned in: Session {skill_info['learned_in_session']} - {skill_info['session_title']}")
    print(f"      At hour: {skill_info['learned_at_hour']}")

print("\n[2.6] Validation Results...")
validation = visualizer.validate_prerequisites(cleaned_path)
print(json.dumps(validation, indent=2))

print("\n[2.7] Generating HTML Visualizations...")
gantt_html = visualizer.generate_gantt_chart_html(gantt_data)
graph_html = visualizer.generate_dependency_graph_html(graph_data)
print(f"  - Gantt chart HTML: {len(gantt_html)} characters")
print(f"  - Dependency graph HTML: {len(graph_html)} characters")

# Save to files
with open("demo_gantt_chart.html", "w", encoding="utf-8") as f:
    f.write(gantt_html)
with open("demo_dependency_graph.html", "w", encoding="utf-8") as f:
    f.write(graph_html)
print(f"  [SAVED] demo_gantt_chart.html")
print(f"  [SAVED] demo_dependency_graph.html")

# ============================================================================
# DEMO 3: Resource Curation System
# ============================================================================
print("\n" + "=" * 80)
print("DEMO 3: RESOURCE CURATION SYSTEM")
print("=" * 80)

from resource_curator import ResourceCurator

curator = ResourceCurator()

print("\n[3.1] Searching for Python resources...")
python_resources = curator.search_resources("Python programming", limit=5)
print(f"  Found {len(python_resources)} resources:")
for i, resource in enumerate(python_resources, 1):
    print(f"\n  Resource {i}:")
    print(f"    Title: {resource['title']}")
    print(f"    Type: {resource['type']}")
    print(f"    Provider: {resource['provider']}")
    print(f"    URL: {resource['url'][:60]}...")
    if 'description' in resource:
        print(f"    Description: {resource['description'][:80]}...")

print("\n[3.2] Adding curated resources to database...")
added_resources = []
for i, resource in enumerate(python_resources[:3], 1):  # Add top 3
    resource_id = curator.add_resource(
        skill_uri="http://data.europa.eu/esco/skill/demo-python",
        resource_url=resource['url'],
        resource_title=resource['title'],
        resource_type=resource['type'],
        provider=resource['provider'],
        description=resource.get('description', ''),
        difficulty_level="beginner",
        is_free=resource.get('is_free', True)
    )
    print(f"  Added resource {i}: ID={resource_id}")
    added_resources.append(resource_id)

print("\n[3.3] Validating resources...")
for resource_id in added_resources[:2]:
    success = curator.validate_resource(resource_id, "demo_validator", "validated")
    print(f"  Resource {resource_id} validated: {success}")

print("\n[3.4] Getting resources for a skill...")
skill_resources = curator.get_resources_for_skill(
    "http://data.europa.eu/esco/skill/demo-python",
    difficulty_level="beginner",
    min_quality=0.0,
    only_validated=False
)
print(f"  Found {len(skill_resources)} resources for Python skill")
if skill_resources:
    print(f"\n  Sample resource:")
    sample = skill_resources[0]
    print(f"    Title: {sample['title']}")
    print(f"    Type: {sample['type']}")
    print(f"    Quality Score: {sample['quality_score']}")
    print(f"    Validation Status: {sample['validation_status']}")

print("\n[3.5] Rating resources...")
if skill_resources:
    resource_url = skill_resources[0]['url']
    feedback.rate_resource(
        resource_url=resource_url,
        skill_uri="http://data.europa.eu/esco/skill/demo-python",
        user_id="demo_user1",
        rating=5,
        quality_score=9,
        review_text="Excellent resource for beginners!"
    )
    feedback.rate_resource(
        resource_url=resource_url,
        skill_uri="http://data.europa.eu/esco/skill/demo-python",
        user_id="demo_user2",
        rating=4,
        quality_score=8,
        review_text="Very helpful"
    )
    
    stats = feedback.get_resource_statistics(resource_url, "http://data.europa.eu/esco/skill/demo-python")
    print(f"  Resource rating statistics:")
    print(json.dumps(stats, indent=2))

print("\n[3.6] Getting resource statistics...")
if added_resources:
    resource_stats = curator.get_resource_statistics(added_resources[0])
    print(f"  Resource statistics:")
    print(json.dumps(resource_stats, indent=2))

print("\n[3.7] Curating resources for entire learning path...")
curated_path = curator.curate_resources_for_learning_path(cleaned_path[:3])  # First 3 sessions
print(f"  Curated resources for {len(curated_path)} sessions")
for session in curated_path:
    resources = session.get('curated_resources', [])
    print(f"\n  Session: {session['title']}")
    print(f"    Resources attached: {len(resources)}")
    for res in resources[:2]:  # Show first 2
        print(f"      - {res['title']} ({res['type']})")

# ============================================================================
# DEMO 4: Integrated Workflow
# ============================================================================
print("\n" + "=" * 80)
print("DEMO 4: INTEGRATED WORKFLOW (All Features Combined)")
print("=" * 80)

print("\n[4.1] Complete workflow: Clean -> Visualize -> Curate -> Rate...")

# Step 1: Clean
workflow_path = visualizer.clean_learning_path(demo_learning_path[:3])
print(f"  [Step 1] Cleaned {len(workflow_path)} sessions")

# Step 2: Visualize
workflow_gantt = visualizer.generate_gantt_chart_data(workflow_path)
workflow_graph = visualizer.generate_dependency_graph_data(workflow_path)
print(f"  [Step 2] Generated visualizations")
print(f"    - Total duration: {workflow_gantt['total_duration_hours']} hours")
print(f"    - Graph complexity: {workflow_graph['metrics']['complexity_score']:.2f}")

# Step 3: Curate resources
workflow_curated = curator.curate_resources_for_learning_path(workflow_path)
print(f"  [Step 3] Curated resources for all sessions")

# Step 4: Community feedback
total_resources = sum(len(s.get('curated_resources', [])) for s in workflow_curated)
print(f"  [Step 4] Total resources curated: {total_resources}")

# Create complete package
complete_package = {
    "learning_path": workflow_curated,
    "visualizations": {
        "gantt_chart": workflow_gantt,
        "dependency_graph": workflow_graph
    },
    "metadata": {
        "total_sessions": len(workflow_curated),
        "total_duration_hours": workflow_gantt['total_duration_hours'],
        "total_skills": sum(len(s['skills']) for s in workflow_curated),
        "total_resources": total_resources,
        "difficulty_progression": [s['difficulty_level'] for s in workflow_curated]
    }
}

print(f"\n[4.2] Complete Package Summary:")
print(json.dumps(complete_package['metadata'], indent=2))

# Save complete package
with open("demo_complete_package.json", "w", encoding="utf-8") as f:
    json.dump(complete_package, f, indent=2)
print(f"\n  [SAVED] demo_complete_package.json")

# ============================================================================
# SUMMARY
# ============================================================================
print("\n" + "=" * 80)
print("DEMO SUMMARY")
print("=" * 80)

print(f"""
Features Demonstrated:

1. Community Feedback System:
   - Voting mechanism (upvotes/downvotes)
   - Suggestion system with community voting
   - Trending items tracking
   - Community metrics dashboard

2. Learning Path Visualizer:
   - Data cleaning & normalization
   - Gantt chart generation (timeline view)
   - Dependency graph (network visualization)
   - Skills timeline
   - Prerequisite validation

3. Resource Curator:
   - Multi-source resource search
   - Resource database management
   - Resource validation & rating
   - Automated curation for learning paths

4. Integrated Workflow:
   - Complete end-to-end workflow
   - Combined all three features
   - Generated complete learning package

Files Created:
  - demo_gantt_chart.html (Interactive timeline)
  - demo_dependency_graph.html (Interactive graph)
  - demo_complete_package.json (Full data package)
""")

print("\n" + "=" * 80)
print(f"Demo Completed: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
print("=" * 80)
print("\nNext Steps:")
print("  1. Open demo_gantt_chart.html in your browser")
print("  2. Open demo_dependency_graph.html in your browser")
print("  3. Review demo_complete_package.json for full data structure")
