"""
Demo: Quiz System API Usage
Shows how to use the quiz endpoints via the Flask API.
"""

import requests
import json
from datetime import datetime


def demo_quiz_api():
    """Demonstrate the quiz API workflow."""
    
    BASE_URL = "http://localhost:5000"
    
    print("=" * 80)
    print("QUIZ API DEMO")
    print("=" * 80)
    print("\nNOTE: Make sure the Flask server is running (python app.py)")
    print()
    
    # Step 1: Generate a learning path
    print("1. Generating learning path...")
    
    path_data = {
        "goal": "I want to become a Full Stack Web Developer",
        "current_skills": ["HTML", "CSS", "Basic JavaScript"]
    }
    
    response = requests.post(f"{BASE_URL}/api/path", json=path_data)
    
    if response.status_code != 200:
        print(f"❌ Failed to generate learning path: {response.status_code}")
        print(response.text)
        return
    
    path_response = response.json()
    
    # Extract the learning path array and format it properly for quiz generation
    sessions = path_response.get('learning_path', [])
    learning_path = {
        'sessions': sessions,
        'target_occupation': path_response.get('matched_occupation', {}).get('label', 'Unknown'),
        'id': f"path_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
    }
    
    print("✅ Learning path generated")
    print(f"   Sessions: {len(sessions)}")
    print()
    
    # Step 2: Generate quiz for the learning path
    print("2. Generating quiz for learning path...")
    print("   (This may take 10-15 seconds)")
    
    quiz_data = {
        "learning_path": learning_path
    }
    
    response = requests.post(f"{BASE_URL}/api/quiz/generate", json=quiz_data)
    
    if response.status_code != 200:
        print(f"❌ Failed to generate quiz: {response.status_code}")
        print(response.text)
        return
    
    quiz_response = response.json()
    quiz = quiz_response.get('quiz', {})
    
    print("✅ Quiz generated")
    print(f"   Questions: {len(quiz.get('questions', []))}")
    
    metadata = quiz.get('metadata', {})
    diff_dist = metadata.get('difficulty_distribution', {})
    print(f"   Difficulty: {diff_dist.get('easy', 0)} easy, {diff_dist.get('medium', 0)} medium, {diff_dist.get('hard', 0)} hard")
    print()
    
    # Display questions
    print("3. Quiz Questions:")
    print("-" * 80)
    
    for i, q in enumerate(quiz.get('questions', []), 1):
        print(f"\nQ{i}. [{q.get('difficulty', 'unknown').upper()}] {q.get('question', 'No question')}")
        print(f"    Topic: {q.get('topic', 'Unknown')}")
        print()
        
        options = q.get('options', {})
        for key in ['A', 'B', 'C', 'D']:
            if key in options:
                print(f"    {key}. {options[key]}")
        
        print()
    
    print("-" * 80)
    print()
    
    # Step 3: Simulate user answers
    print("4. Simulating user answers...")
    
    # Create sample answers (you would get these from user input)
    user_answers = {}
    
    for q in quiz.get('questions', []):
        q_id = q.get('id')
        # For demo, let's answer some correctly and some incorrectly
        if q_id % 3 == 0:
            # Wrong answer
            options = ['A', 'B', 'C', 'D']
            correct = q.get('correct_answer')
            options.remove(correct)
            user_answers[str(q_id)] = options[0]
        else:
            # Correct answer
            user_answers[str(q_id)] = q.get('correct_answer')
    
    print(f"✅ Generated {len(user_answers)} answers")
    print()
    
    # Step 4: Submit quiz and get analysis
    print("5. Submitting quiz for analysis...")
    
    submit_data = {
        "quiz": quiz,
        "answers": user_answers
    }
    
    response = requests.post(f"{BASE_URL}/api/quiz/submit", json=submit_data)
    
    if response.status_code != 200:
        print(f"❌ Failed to submit quiz: {response.status_code}")
        print(response.text)
        return
    
    result = response.json()
    analysis = result.get('analysis', {})
    
    print("✅ Quiz analyzed")
    print()
    
    # Display results
    print("=" * 80)
    print("QUIZ RESULTS")
    print("=" * 80)
    print()
    
    score = analysis.get('score', {})
    print(f"📊 SCORE: {score.get('correct', 0)}/{score.get('total', 0)} ({score.get('percentage', 0)}%)")
    print(f"   Grade: {score.get('grade', 'N/A')}")
    print(f"   Performance: {analysis.get('performance_level', 'Unknown')}")
    print()
    
    # Difficulty breakdown
    diff_analysis = analysis.get('difficulty_analysis', {})
    print("📈 DIFFICULTY BREAKDOWN:")
    for level in ['easy', 'medium', 'hard']:
        level_data = diff_analysis.get(level, {})
        print(f"   {level.capitalize()}: {level_data.get('correct', 0)}/{level_data.get('total', 0)} ({level_data.get('percentage', 0)}%)")
    print()
    
    # Strengths
    strengths = analysis.get('strengths', [])
    if strengths:
        print("💪 YOUR STRENGTHS:")
        for s in strengths:
            print(f"   ✓ {s['topic']} - {s['accuracy']}% accuracy")
        print()
    
    # Weaknesses
    weaknesses = analysis.get('weaknesses', [])
    if weaknesses:
        print("⚠️ AREAS TO IMPROVE:")
        for w in weaknesses:
            print(f"   ✗ {w['topic']} - {w['accuracy']}% accuracy")
        print()
    
    # Needs improvement
    needs_improvement = analysis.get('needs_improvement', [])
    if needs_improvement:
        print("📚 NEEDS MORE PRACTICE:")
        for n in needs_improvement:
            print(f"   • {n['topic']} - {n['accuracy']}% accuracy")
        print()
    
    # Recommendations
    recommendations = analysis.get('recommendations', [])
    if recommendations:
        print("💡 RECOMMENDATIONS:")
        for rec in recommendations:
            print(f"   {rec}")
        print()
    
    # Save results
    filename = f"quiz_demo_results_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
    with open(filename, 'w', encoding='utf-8') as f:
        json.dump({
            'learning_path': learning_path,
            'quiz': quiz,
            'user_answers': user_answers,
            'analysis': analysis
        }, f, indent=2, ensure_ascii=False)
    
    print(f"💾 Results saved to: {filename}")
    print()
    print("=" * 80)
    print("DEMO COMPLETE")
    print("=" * 80)


if __name__ == '__main__':
    try:
        demo_quiz_api()
    except requests.exceptions.ConnectionError:
        print("\n❌ Error: Could not connect to Flask server")
        print("Please make sure the server is running:")
        print("   python app.py")
    except KeyboardInterrupt:
        print("\n\nDemo interrupted by user")
    except Exception as e:
        print(f"\n❌ Demo failed: {e}")
        import traceback
        traceback.print_exc()
