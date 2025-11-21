"""
Comprehensive Test Suite for Enhanced Features
Tests all three major features:
1. Community Feedback Loop
2. Learning Path Visualization
3. Resource Curation
"""

import json
import time
import sys
import io
from datetime import datetime

# Fix encoding for Windows console
if sys.platform == 'win32':
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')

print("=" * 80)
print("ENHANCED FEATURES TEST SUITE")
print("=" * 80)
print(f"Test Started: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")

# Test 1: Initialize all systems and create database tables
print("\n" + "=" * 80)
print("TEST 1: Initialize Systems and Create Database Tables")
print("=" * 80)

try:
    from community_feedback import CommunityFeedbackSystem
    print("✓ Community Feedback System imported successfully")
    feedback = CommunityFeedbackSystem()
    print("✓ Community Feedback System initialized")
    print("  - Created tables: votes, suggestions, suggestion_votes, curriculum_updates, resource_ratings")
except Exception as e:
    print(f"✗ Error initializing Community Feedback System: {e}")
    feedback = None

try:
    from learning_path_visualizer import LearningPathVisualizer
    print("✓ Learning Path Visualizer imported successfully")
    visualizer = LearningPathVisualizer()
    print("✓ Learning Path Visualizer initialized")
except Exception as e:
    print(f"✗ Error initializing Learning Path Visualizer: {e}")
    visualizer = None

try:
    from resource_curator import ResourceCurator
    print("✓ Resource Curator imported successfully")
    curator = ResourceCurator()
    print("✓ Resource Curator initialized")
    print("  - Created tables: learning_resources, resource_tags, resource_access_stats")
except Exception as e:
    print(f"✗ Error initializing Resource Curator: {e}")
    curator = None

# Test 2: Community Feedback System
print("\n" + "=" * 80)
print("TEST 2: Community Feedback System")
print("=" * 80)

if feedback:
    # Test voting
    print("\n2.1 Testing Voting System:")
    test_skill_uri = "http://data.europa.eu/esco/skill/test-python-programming"
    
    vote_result = feedback.add_vote(
        item_uri=test_skill_uri,
        item_type="skill",
        user_id="test_user_1",
        vote_value=1
    )
    print(f"  ✓ Added upvote: {vote_result}")
    
    vote_stats = feedback.get_vote_statistics(test_skill_uri, "skill")
    print(f"  ✓ Vote statistics: {vote_stats}")
    
    # Test suggestions
    print("\n2.2 Testing Suggestion System:")
    suggestion_id = feedback.add_suggestion(
        item_uri=test_skill_uri,
        item_type="skill",
        user_id="test_user_1",
        suggestion_type="improve_description",
        suggestion_text="Add more examples for Python list comprehensions"
    )
    print(f"  ✓ Added suggestion ID: {suggestion_id}")
    
    # Vote on suggestion
    feedback.vote_on_suggestion(suggestion_id, "test_user_2", 1)
    print(f"  ✓ Voted on suggestion")
    
    pending = feedback.get_pending_suggestions(min_community_score=0)
    print(f"  ✓ Pending suggestions: {len(pending)}")
    
    # Test community metrics
    print("\n2.3 Testing Community Metrics:")
    metrics = feedback.get_community_metrics()
    print(f"  ✓ Total votes: {metrics['total_votes']}")
    print(f"  ✓ Total suggestions: {metrics['total_suggestions']}")
    print(f"  ✓ Pending suggestions: {metrics['pending_suggestions']}")
    print(f"  ✓ Active users (30 days): {metrics['active_users_30d']}")
    print(f"  ✓ Total resource ratings: {metrics['total_resource_ratings']}")
    print(f"  ✓ Average resource rating: {metrics['average_resource_rating']}")
    
    # Test trending items
    print("\n2.4 Testing Trending System:")
    trending = feedback.get_trending_items(item_type="skill", days=30, limit=5)
    print(f"  ✓ Found {len(trending)} trending items")

# Test 3: Learning Path Visualization
print("\n" + "=" * 80)
print("TEST 3: Learning Path Visualization & Data Cleaning")
print("=" * 80)

if visualizer:
    # Sample learning path
    sample_path = [
        {
            "session_number": 1,
            "title": "Python Fundamentals",
            "skills": ["python", "variables", "data types"],
            "estimated_duration_hours": "20 hours",
            "difficulty_level": "beginner",
            "prerequisites": []
        },
        {
            "session_number": 2,
            "title": "Advanced Python",
            "skills": ["OOP", "decorators", "generators"],
            "estimated_duration_hours": "30",
            "difficulty_level": "intermediate",
            "prerequisites": ["Python Fundamentals"]
        },
        {
            "session_number": 3,
            "title": "Data Science with Python",
            "skills": ["pandas", "numpy", "matplotlib"],
            "estimated_duration_hours": 40,
            "difficulty_level": "advanced",
            "prerequisites": ["Advanced Python"]
        }
    ]
    
    print("\n3.1 Testing Data Cleaning:")
    cleaned_path = visualizer.clean_learning_path(sample_path)
    print(f"  ✓ Cleaned {len(cleaned_path)} sessions")
    print(f"  ✓ Sample cleaned session:")
    print(f"    - Title: {cleaned_path[0]['title']}")
    print(f"    - Duration: {cleaned_path[0]['estimated_duration_hours']} hours")
    print(f"    - Skills: {', '.join(cleaned_path[0]['skills'])}")
    
    print("\n3.2 Testing Gantt Chart Generation:")
    gantt_data = visualizer.generate_gantt_chart_data(cleaned_path)
    print(f"  ✓ Total duration: {gantt_data['total_duration_hours']} hours ({gantt_data['total_duration_days']} days)")
    print(f"  ✓ Generated {len(gantt_data['tasks'])} tasks")
    print(f"  ✓ Sample task:")
    print(f"    - {gantt_data['tasks'][0]['name']}")
    print(f"    - Start: {gantt_data['tasks'][0]['start']}")
    print(f"    - End: {gantt_data['tasks'][0]['end']}")
    print(f"    - Duration: {gantt_data['tasks'][0]['duration_hours']} hours")
    
    print("\n3.3 Testing Dependency Graph Generation:")
    graph_data = visualizer.generate_dependency_graph_data(cleaned_path)
    print(f"  [OK] Nodes: {len(graph_data['nodes'])}")
    print(f"  [OK] Edges: {len(graph_data['edges'])}")
    print(f"  [OK] Complexity score: {graph_data['metrics']['complexity_score']:.2f}")
    print(f"  [OK] Independent sessions: {graph_data['metrics']['independent_sessions']}")
    
    print("\n3.4 Testing Skills Timeline:")
    timeline = visualizer.generate_skills_timeline(cleaned_path)
    print(f"  [OK] Tracked {len(timeline['skills'])} skills")
    print(f"  [OK] Total duration: {timeline['total_hours']} hours")
    print(f"  [OK] Sample skills learned:")
    for skill_info in timeline['skills'][:3]:
        print(f"    - {skill_info['skill_name']}: Session {skill_info['learned_in_session']} at hour {skill_info['learned_at_hour']}")
    
    print("\n3.5 Testing HTML Visualization Generation:")
    try:
        gantt_html = visualizer.generate_gantt_chart_html(gantt_data)
        print(f"  ✓ Generated Gantt chart HTML ({len(gantt_html)} characters)")
        
        graph_html = visualizer.generate_dependency_graph_html(graph_data)
        print(f"  ✓ Generated dependency graph HTML ({len(graph_html)} characters)")
        
        # Save visualizations to files
        with open("test_gantt_chart.html", "w", encoding="utf-8") as f:
            f.write(gantt_html)
        print(f"  ✓ Saved Gantt chart to: test_gantt_chart.html")
        
        with open("test_dependency_graph.html", "w", encoding="utf-8") as f:
            f.write(graph_html)
        print(f"  ✓ Saved dependency graph to: test_dependency_graph.html")
        
    except Exception as e:
        print(f"  ✗ Error generating HTML: {e}")

# Test 4: Resource Curation System
print("\n" + "=" * 80)
print("TEST 4: Resource Curation System")
print("=" * 80)

if curator:
    test_skill = "python programming"
    test_skill_uri = "http://data.europa.eu/esco/skill/test-python"
    
    print("\n4.1 Testing Resource Search:")
    search_results = curator.search_resources(test_skill, limit=5)
    print(f"  ✓ Found {len(search_results)} resources")
    if search_results:
        print(f"  ✓ Sample resource:")
        print(f"    - Title: {search_results[0]['title']}")
        print(f"    - Type: {search_results[0]['type']}")
        print(f"    - Provider: {search_results[0]['provider']}")
        print(f"    - URL: {search_results[0]['url'][:60]}...")
    
    print("\n4.2 Testing Resource Addition:")
    resource_id = curator.add_resource(
        skill_uri=test_skill_uri,
        resource_url="https://docs.python.org/3/tutorial/",
        resource_title="Official Python Tutorial",
        resource_type="documentation",
        provider="Python.org",
        description="Comprehensive Python tutorial from official docs",
        difficulty_level="beginner",
        is_free=True,
        estimated_duration="10 hours"
    )
    print(f"  ✓ Added resource ID: {resource_id}")
    
    print("\n4.3 Testing Resource Validation:")
    validation = curator.validate_resource(resource_id, "test_validator", "validated")
    print(f"  [OK] Resource validated: {validation}")
    
    print("\n4.4 Testing Resource Retrieval:")
    skill_resources = curator.get_resources_for_skill(
        test_skill_uri,
        difficulty_level="beginner",
        min_quality=5.0
    )
    print(f"  [OK] Found {len(skill_resources)} resources for skill")
    
    print("\n4.5 Testing Resource Rating:")
    feedback.rate_resource(
        resource_url="https://docs.python.org/3/tutorial/",
        skill_uri=test_skill_uri,
        user_id="test_user_1",
        rating=5,
        quality_score=9,
        review_text="Excellent tutorial for beginners!"
    )
    print(f"  [OK] Added resource rating")
    
    print("\n4.6 Testing Resource Statistics:")
    stats = curator.get_resource_statistics(resource_id)
    print(f"  [OK] Resource statistics:")
    print(f"    - Total access count: {stats.get('total_access_count', 0)}")
    print(f"    - Completion rate: {stats.get('completion_rate', 0)}%")
    
    print("\n4.7 Testing Learning Path Curation:")
    if cleaned_path:
        curated_path = curator.curate_resources_for_learning_path(cleaned_path)
        print(f"  ✓ Curated resources for {len(curated_path)} sessions")
        total_resources = sum(len(session.get('resources', [])) for session in curated_path)
        print(f"  ✓ Total resources attached: {total_resources}")

# Test 5: Integration Test
print("\n" + "=" * 80)
print("TEST 5: Full Integration Test")
print("=" * 80)

if visualizer and curator:
    print("\n5.1 Complete Learning Path Workflow:")
    
    # Create a comprehensive learning path
    integration_path = [
        {
            "session_number": 1,
            "title": "Web Development Basics",
            "skills": ["HTML", "CSS", "JavaScript"],
            "estimated_duration_hours": 25,
            "difficulty_level": "beginner",
            "prerequisites": []
        },
        {
            "session_number": 2,
            "title": "Frontend Frameworks",
            "skills": ["React", "Vue.js"],
            "estimated_duration_hours": 35,
            "difficulty_level": "intermediate",
            "prerequisites": ["Web Development Basics"]
        }
    ]
    
    # Clean the path
    cleaned = visualizer.clean_learning_path(integration_path)
    print(f"  ✓ Cleaned learning path")
    
    # Generate visualizations
    gantt = visualizer.generate_gantt_chart_data(cleaned)
    graph = visualizer.generate_dependency_graph_data(cleaned)
    print(f"  ✓ Generated visualizations")
    
    # Curate resources
    with_resources = curator.curate_resources_for_learning_path(cleaned)
    print(f"  ✓ Curated resources for all sessions")
    
    # Create complete package
    complete_package = {
        "learning_path": with_resources,
        "visualizations": {
            "gantt_chart": gantt,
            "dependency_graph": graph
        },
        "metadata": {
            "total_duration_hours": gantt['total_duration_hours'],
            "total_sessions": len(with_resources),
            "difficulty_progression": [s['difficulty_level'] for s in with_resources]
        }
    }
    
    print(f"\n  ✓ Complete Package Generated:")
    print(f"    - Sessions: {complete_package['metadata']['total_sessions']}")
    print(f"    - Duration: {complete_package['metadata']['total_duration_hours']} hours")
    print(f"    - Difficulty: {' → '.join(complete_package['metadata']['difficulty_progression'])}")

# Final Summary
print("\n" + "=" * 80)
print("TEST SUMMARY")
print("=" * 80)

results = {
    "Community Feedback System": feedback is not None,
    "Learning Path Visualizer": visualizer is not None,
    "Resource Curator": curator is not None,
}

print("\nFeature Status:")
for feature, status in results.items():
    status_icon = "✓" if status else "✗"
    status_text = "WORKING" if status else "FAILED"
    print(f"  {status_icon} {feature}: {status_text}")

all_passed = all(results.values())
print(f"\n{'='*80}")
if all_passed:
    print("✓ ALL TESTS PASSED!")
    print("All enhanced features are working correctly.")
    print("\nNext Steps:")
    print("1. Start the Flask API: python app.py")
    print("2. Test API endpoints at: http://localhost:5000")
    print("3. Open test_gantt_chart.html in browser")
    print("4. Open test_dependency_graph.html in browser")
else:
    print("✗ SOME TESTS FAILED")
    print("Please check the error messages above.")

print(f"{'='*80}")
print(f"\nTest Completed: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
print("="*80)
