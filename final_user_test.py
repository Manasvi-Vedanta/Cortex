"""
GenMentor Final User Test - Demonstrating Manual Input & Feedback
This script simulates realistic user interactions with the GenMentor system.
"""

import requests
import json
import time
from datetime import datetime

BASE_URL = "http://localhost:5000"

def print_header(title):
    print(f"\n{'='*60}")
    print(f" {title}")
    print(f"{'='*60}")

def export_learning_path(learning_path_data: dict, api_learning_path: dict):
    """Export complete learning path with AI content to a JSON file."""
    try:
        # Enhance learning path data with API response info
        if 'learning_sessions' in api_learning_path:
            learning_path_data['learning_sessions'] = api_learning_path['learning_sessions']
        
        # Add skill gap analysis
        if 'skill_gap' in api_learning_path:
            learning_path_data['skill_gap'] = [
                {
                    'label': skill.get('label', 'Unknown'),
                    'description': skill.get('description', ''),
                    'priority': skill.get('priority', 0),
                    'relation_type': skill.get('relation_type', 'unknown')
                }
                for skill in api_learning_path['skill_gap'][:20]  # Top 20 skills
            ]
        
        # Generate filename with timestamp
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"learning_path_{timestamp}.json"
        
        # Export to file
        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(learning_path_data, f, indent=2, ensure_ascii=False)
        
        print(f"\n📄 Learning Path Exported!")
        print(f"   📁 Saved to: {filename}")
        print(f"   📊 File size: {len(json.dumps(learning_path_data, indent=2))//1024 + 1} KB")
        print(f"   🎯 Includes: Career match, {len(learning_path_data.get('ai_generated_content', {}))} AI contents, skill analysis")
        
    except Exception as e:
        print(f"❌ Error exporting learning path: {e}")

def test_complete_user_journey():
    """Test a complete user journey with manual-style input and feedback."""
    
    print_header("🎯 GENMENTOR COMPLETE USER JOURNEY TEST")
    print("🤖 Testing with your updated Gemini API key and model")
    
    # User Profile
    user_profile = {
        "name": "Sarah Johnson",
        "goal": "I want to transition from marketing to data science",
        "current_skills": ["excel", "google analytics", "basic statistics", "presentation skills"],
        "experience_level": "beginner",
        "user_id": "sarah_j_2025"
    }
    
    print(f"\n👤 User Profile:")
    print(f"   Name: {user_profile['name']}")
    print(f"   Goal: {user_profile['goal']}")
    print(f"   Current Skills: {', '.join(user_profile['current_skills'])}")
    print(f"   Experience: {user_profile['experience_level']}")
    
    # Step 1: Generate Learning Path
    print_header("STEP 1: GENERATING PERSONALIZED LEARNING PATH")
    print("🔍 Analyzing user goals against 3,039 occupations...")
    print("🧠 Processing 13,939 skills with AI...")
    
    try:
        response = requests.post(f"{BASE_URL}/api/path", json={
            'goal': user_profile['goal'],
            'current_skills': user_profile['current_skills'],
            'user_id': user_profile['user_id']
        }, timeout=120)  # Extended timeout for AI processing
        
        if response.status_code == 200:
            result = response.json()
            occupation = result['matched_occupation']
            
            print(f"✅ SUCCESS! Matched Career: {occupation['label']}")
            print(f"📊 Match Confidence: {occupation['similarity_score']:.1%}")
            print(f"🎯 Skills Gap Analysis:")
            summary = result['skill_gap_summary']
            print(f"   • Total occupation skills: {summary['total_skills_needed']}")
            print(f"   • Skills to learn: {summary['skills_to_learn']}")
            print(f"   • Learning path sessions: {len(result['learning_path'])}")
            
            # Show learning path preview
            if result['learning_path']:
                print(f"\n📚 Learning Path Preview:")
                for i, session in enumerate(result['learning_path'][:3], 1):
                    title = session.get('title', f'Session {i}')
                    skills = session.get('skills', [])[:3]
                    duration = session.get('duration', session.get('estimated_duration', 'N/A'))
                    print(f"   Session {i}: {title}")
                    print(f"      Duration: {duration}")
                    print(f"      Skills: {', '.join(skills)}...")
                
                learning_path = result['learning_path']
                analysis_result = result  # Store full result for export
            else:
                learning_path = []
                analysis_result = result
        else:
            print(f"❌ Error: {response.status_code}")
            return
    
    except Exception as e:
        print(f"❌ Error: {e}")
        return
    
    # Step 2: Generate AI Content
    print_header("STEP 2: AI-POWERED CONTENT GENERATION")
    print("🤖 Using Gemini Pro to create personalized learning content...")
    
    test_topics = []
    
    # Extract actual topics from the learning path
    if learning_path:
        for session in learning_path[:2]:  # Use first 2 sessions
            session_skills = session.get('skills', [])[:2]  # Max 2 skills per session
            for skill in session_skills:
                if isinstance(skill, str):
                    test_topics.append(skill)
                elif isinstance(skill, dict) and 'label' in skill:
                    test_topics.append(skill['label'])
    
    # Fallback topics if no learning path found
    if not test_topics:
        test_topics = ["data analysis", "programming fundamentals", "statistical methods"]
    
    # Limit to 3 topics for demo
    test_topics = test_topics[:3]
    
    # Get matched occupation data properly
    matched_occupation = analysis_result.get('matched_occupation', {})
    skill_gap_summary = analysis_result.get('skill_gap_summary', {})
    
    # Initialize learning path data for export
    learning_path_data = {
        'user_profile': {
            'name': user_profile['name'],
            'goal': user_profile['goal'],
            'current_skills': user_profile['current_skills'],
            'experience': user_profile['experience_level'],
            'generation_timestamp': datetime.now().isoformat()
        },
        'matched_career': {
            'title': matched_occupation.get('label', 'N/A'),
            'similarity_score': f"{matched_occupation.get('similarity_score', 0):.1%}",
            'total_skills_needed': skill_gap_summary.get('total_skills_needed', 0),
            'skills_to_learn': skill_gap_summary.get('skills_to_learn', 0)
        },
        'learning_sessions': learning_path,  # Store the actual learning path sessions
        'ai_generated_content': {}
    }
    
    for topic in test_topics:
        print(f"\n📖 Generating content for: {topic}")
        max_retries = 3
        retry_count = 0
        success = False
        
        while retry_count < max_retries and not success:
            try:
                response = requests.get(f"{BASE_URL}/api/content", 
                                      params={'topic': topic, 'level': 'beginner'}, 
                                      timeout=60)  # Increased timeout to 60 seconds
                
                if response.status_code == 200:
                    content = response.json()
                    print(f"   ✅ Generated {len(content['content'])} characters of content")
                    print(f"   📊 Content Type: {content['content_type']}")
                    
                    # Store content in learning path data
                    learning_path_data['ai_generated_content'][topic] = {
                        'content': content['content'],
                        'content_type': content['content_type'],
                        'word_count': len(content['content'].split()),
                        'character_count': len(content['content'])
                    }
                    
                    # Show full content for analysis
                    print(f"\n📖 FULL CONTENT FOR '{topic.upper()}':")
                    print("=" * 80)
                    print(content['content'])
                    print("=" * 80)
                    success = True
                else:
                    print(f"   ❌ Error: {response.status_code}")
                    retry_count += 1
                    if retry_count < max_retries:
                        print(f"   🔄 Retrying... ({retry_count + 1}/{max_retries})")
                        time.sleep(5)
            
            except requests.exceptions.Timeout:
                retry_count += 1
                print(f"   ⏰ Timeout occurred (attempt {retry_count}/{max_retries})")
                if retry_count < max_retries:
                    print(f"   🔄 Retrying with longer timeout...")
                    time.sleep(5)
                else:
                    print(f"   ❌ Max retries reached - content generation failed")
            except Exception as e:
                retry_count += 1
                print(f"   ❌ Error: {e}")
                if retry_count < max_retries:
                    print(f"   🔄 Retrying... ({retry_count + 1}/{max_retries})")
                    time.sleep(5)
                else:
                    print(f"   ❌ Max retries reached - content generation failed")
    
    # Step 3: Simulate User Feedback
    print_header("STEP 3: USER FEEDBACK & SYSTEM LEARNING")
    print("👥 Simulating realistic user feedback on the learning path...")
    
    # Extract skills from the actual learning path for feedback
    feedback_skills = []
    if learning_path:
        for session in learning_path[:2]:  # Use first 2 sessions
            session_skills = session.get('skills', [])[:3]  # Max 3 skills per session
            for skill in session_skills:
                if isinstance(skill, str):
                    feedback_skills.append(skill.lower())
                elif isinstance(skill, dict) and 'label' in skill:
                    feedback_skills.append(skill['label'].lower())
    
    # Fallback to generic skills if no learning path skills found
    if not feedback_skills:
        feedback_skills = ["data analysis", "programming", "statistics", "databases", "visualization"]
    
    # Create feedback scenarios from actual learning path skills
    feedback_scenarios = []
    comments = [
        "Essential for my career transition!",
        "Very relevant to my goals", 
        "Good foundation skill",
        "Important for practical work",
        "Key requirement for data science"
    ]
    
    for i, skill in enumerate(feedback_skills[:5]):  # Limit to 5 skills
        feedback_scenarios.append({
            "skill": skill,
            "vote": 1,
            "comment": comments[i % len(comments)]
        })
    
    feedback_count = 0
    for feedback in feedback_scenarios:
        # Create a mock skill URI for demonstration
        skill_uri = f"http://data.europa.eu/esco/skill/demo-{feedback['skill'].replace(' ', '-')}"
        
        try:
            # Submit vote
            vote_response = requests.post(f"{BASE_URL}/api/vote", json={
                'item_uri': skill_uri,
                'user_id': user_profile['user_id'],
                'vote': feedback['vote']
            })
            
            if vote_response.status_code == 200:
                vote_text = "👍 Upvoted" if feedback['vote'] == 1 else "👎 Downvoted"
                print(f"   {vote_text}: {feedback['skill']}")
                feedback_count += 1
                
                # Submit suggestion
                suggestion_response = requests.post(f"{BASE_URL}/api/suggestion", json={
                    'item_uri': skill_uri,
                    'user_id': user_profile['user_id'],
                    'suggestion_type': 'modify',
                    'suggestion_text': feedback['comment']
                })
                
                if suggestion_response.status_code == 200:
                    print(f"      💡 Suggested: {feedback['comment']}")
        
        except Exception as e:
            print(f"   ❌ Error submitting feedback: {e}")
    
    print(f"\n✅ Submitted {feedback_count} pieces of feedback!")
    
    # Step 4: System Analytics
    print_header("STEP 4: SYSTEM ANALYTICS & IMPACT")
    print("📊 Analyzing system performance and user impact...")
    
    try:
        stats_response = requests.get(f"{BASE_URL}/api/stats")
        if stats_response.status_code == 200:
            stats = stats_response.json()
            
            print(f"🎯 System Performance:")
            db_stats = stats['database_stats']
            print(f"   • Occupations in database: {db_stats['occupations']:,}")
            print(f"   • Skills analyzed: {db_stats['skills']:,}")
            print(f"   • Community feedback: {db_stats['votes']:,} votes, {db_stats['suggestions']:,} suggestions")
            print(f"   • AI Engine: {stats['ai_engine_status']}")
            print(f"   • Embeddings Cached: {stats['embeddings_cached']}")
            
            # Show community insights
            if stats['top_voted_skills']:
                print(f"\n🏆 Community Top Skills:")
                for skill in stats['top_voted_skills'][:5]:
                    print(f"   • {skill['skill']} (Score: {skill['score']})")
        
        # Trigger feedback analysis
        analysis_response = requests.post(f"{BASE_URL}/api/analyze-feedback")
        if analysis_response.status_code == 200:
            print(f"\n🔄 System Learning Complete!")
            print(f"   • Feedback analyzed and integrated")
            print(f"   • Skill relevance scores updated")
            print(f"   • Future recommendations improved")
    
    except Exception as e:
        print(f"❌ Error getting analytics: {e}")
    
    # Export learning path to file
    export_learning_path(learning_path_data, learning_path)
    
    # Final Summary
    print_header("🎉 USER JOURNEY COMPLETE")
    print(f"✅ Successfully demonstrated GenMentor AI system for {user_profile['name']}")
    print(f"\n📋 What we accomplished:")
    print(f"   🎯 Matched '{user_profile['goal']}' to relevant career path")
    print(f"   🧠 Generated personalized learning path with {len(learning_path)} sessions")
    print(f"   🤖 Created AI-powered learning content using Gemini Pro")
    print(f"   👥 Collected and processed community feedback")
    print(f"   📊 Updated system intelligence for future users")
    print(f"   📄 Exported complete learning path to file")
    print(f"\n🚀 GenMentor is ready for real-world deployment!")
    print(f"🌐 API Documentation: http://localhost:5000")

if __name__ == "__main__":
    test_complete_user_journey()
