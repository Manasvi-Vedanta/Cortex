"""
Test Quiz Generation and Analysis System
Demonstrates the complete quiz workflow.
"""

import json
import sys
from datetime import datetime
from ai_engine import GenMentorAI
from quiz_generator import QuizGenerator
from config import GEMINI_API_KEY


def test_quiz_system():
    """Test the complete quiz generation and analysis workflow."""
    print("=" * 80)
    print("GENMENTOR QUIZ SYSTEM TEST")
    print("=" * 80)
    print()
    
    # Initialize systems
    print("1. Initializing AI Engine and Quiz Generator...")
    ai_engine = GenMentorAI()
    quiz_gen = QuizGenerator(GEMINI_API_KEY)
    print("✅ Systems initialized")
    print()
    
    # Generate a learning path
    print("2. Generating sample learning path...")
    goal = "I want to become a Machine Learning Engineer"
    current_skills = ["Python programming", "Basic statistics"]
    
    learning_path = ai_engine.generate_learning_path(goal, current_skills)
    
    if learning_path and 'sessions' in learning_path:
        print(f"✅ Learning path generated with {len(learning_path['sessions'])} sessions")
        print(f"   Target: {learning_path.get('target_occupation', 'Unknown')}")
        print()
        
        # Display sessions
        print("   Sessions:")
        for i, session in enumerate(learning_path['sessions'][:5], 1):
            print(f"   {i}. {session.get('topic', 'Unknown topic')}")
        if len(learning_path['sessions']) > 5:
            print(f"   ... and {len(learning_path['sessions']) - 5} more")
        print()
    else:
        print("❌ Failed to generate learning path")
        return
    
    # Generate quiz
    print("3. Generating comprehensive quiz...")
    print("   (This may take 10-15 seconds as Gemini generates questions)")
    quiz = quiz_gen.generate_quiz(learning_path)
    
    if 'questions' not in quiz or len(quiz['questions']) == 0:
        print("❌ Failed to generate quiz")
        if 'error' in quiz:
            print(f"   Error: {quiz['error']}")
        return
    
    print(f"✅ Quiz generated with {len(quiz['questions'])} questions")
    print()
    
    # Display quiz metadata
    metadata = quiz.get('metadata', {})
    print("   Quiz Metadata:")
    print(f"   - Total Questions: {metadata.get('total_questions', 0)}")
    print(f"   - Easy: {metadata.get('difficulty_distribution', {}).get('easy', 0)}")
    print(f"   - Medium: {metadata.get('difficulty_distribution', {}).get('medium', 0)}")
    print(f"   - Hard: {metadata.get('difficulty_distribution', {}).get('hard', 0)}")
    print(f"   - Topics Covered: {metadata.get('total_topics', 0)}")
    print()
    
    # Display sample questions
    print("4. Sample Questions:")
    print("-" * 80)
    
    for i, question in enumerate(quiz['questions'][:3], 1):
        print(f"\nQuestion {i} [{question.get('difficulty', 'unknown').upper()}]")
        print(f"Topic: {question.get('topic', 'Unknown')}")
        print(f"\n{question.get('question', 'No question text')}")
        print()
        
        options = question.get('options', {})
        for key in ['A', 'B', 'C', 'D']:
            if key in options:
                print(f"   {key}. {options[key]}")
        
        print(f"\nCorrect Answer: {question.get('correct_answer', 'Unknown')}")
        print(f"Explanation: {question.get('explanation', 'No explanation')}")
        print("-" * 80)
    
    if len(quiz['questions']) > 3:
        print(f"\n... and {len(quiz['questions']) - 3} more questions")
    print()
    
    # Simulate user answers
    print("5. Simulating user quiz submission...")
    
    # Create sample answers (mixing correct and incorrect)
    sample_answers = {}
    correct_count = 0
    
    for q in quiz['questions']:
        q_id = q.get('id')
        correct_answer = q.get('correct_answer')
        
        # Simulate 70% accuracy
        import random
        if random.random() < 0.7:
            sample_answers[q_id] = correct_answer
            correct_count += 1
        else:
            # Pick a random wrong answer
            options = ['A', 'B', 'C', 'D']
            options.remove(correct_answer)
            sample_answers[q_id] = random.choice(options)
    
    print(f"✅ Simulated answers for {len(sample_answers)} questions")
    print(f"   (Targeting ~70% accuracy)")
    print()
    
    # Analyze quiz results
    print("6. Analyzing quiz results...")
    analysis = quiz_gen.analyze_quiz_results(quiz, sample_answers)
    
    if 'error' in analysis:
        print(f"❌ Analysis failed: {analysis['error']}")
        return
    
    print("✅ Analysis complete")
    print()
    
    # Display results
    print("=" * 80)
    print("QUIZ RESULTS")
    print("=" * 80)
    print()
    
    score = analysis.get('score', {})
    print(f"📊 SCORE: {score.get('correct', 0)}/{score.get('total', 0)} ({score.get('percentage', 0)}%)")
    print(f"   Grade: {score.get('grade', 'N/A')}")
    print(f"   Performance Level: {analysis.get('performance_level', 'Unknown')}")
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
        print("💪 STRENGTHS:")
        for strength in strengths[:3]:
            print(f"   ✓ {strength['topic']}: {strength['accuracy']}% ({strength['correct']}/{strength['total']})")
        print()
    
    # Needs improvement
    needs_improvement = analysis.get('needs_improvement', [])
    if needs_improvement:
        print("📚 NEEDS IMPROVEMENT:")
        for topic in needs_improvement:
            print(f"   ⚠ {topic['topic']}: {topic['accuracy']}% ({topic['correct']}/{topic['total']})")
        print()
    
    # Weaknesses
    weaknesses = analysis.get('weaknesses', [])
    if weaknesses:
        print("⚠️ WEAKNESSES:")
        for weakness in weaknesses:
            print(f"   ✗ {weakness['topic']}: {weakness['accuracy']}% ({weakness['correct']}/{weakness['total']})")
        print()
    
    # Recommendations
    recommendations = analysis.get('recommendations', [])
    if recommendations:
        print("💡 RECOMMENDATIONS:")
        for rec in recommendations:
            print(f"   {rec}")
        print()
    
    # Save quiz and results
    print("7. Saving quiz and results...")
    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    
    quiz_filename = f"quiz_test_{timestamp}.json"
    results_filename = f"quiz_results_{timestamp}.json"
    
    quiz_gen.save_quiz_to_file(quiz, quiz_filename)
    
    with open(results_filename, 'w', encoding='utf-8') as f:
        json.dump({
            'quiz': quiz,
            'user_answers': sample_answers,
            'analysis': analysis
        }, f, indent=2, ensure_ascii=False)
    
    print(f"✅ Quiz saved to: {quiz_filename}")
    print(f"✅ Results saved to: {results_filename}")
    print()
    
    print("=" * 80)
    print("TEST COMPLETE")
    print("=" * 80)


if __name__ == '__main__':
    try:
        test_quiz_system()
    except KeyboardInterrupt:
        print("\n\nTest interrupted by user")
        sys.exit(0)
    except Exception as e:
        print(f"\n\n❌ Test failed with error: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
