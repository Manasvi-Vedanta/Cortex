"""
AI-Powered Quiz Generator and Analyzer
Generates comprehensive quizzes for learning paths using Gemini API.
"""

import json
import google.generativeai as genai
from typing import Dict, List, Any, Optional
from datetime import datetime
import re


class QuizGenerator:
    """Generates and analyzes quizzes for learning paths using Gemini API."""
    
    def __init__(self, api_key: str):
        """
        Initialize quiz generator with Gemini API.
        
        Args:
            api_key: Google Gemini API key
        """
        genai.configure(api_key=api_key)
        self.model = genai.GenerativeModel('gemini-2.5-flash')
    
    def generate_quiz(self, learning_path: Dict[str, Any]) -> Dict[str, Any]:
        """
        Generate a comprehensive quiz for the entire learning path.
        
        Args:
            learning_path: Complete learning path with sessions and skills
            
        Returns:
            Dictionary containing quiz questions with metadata
        """
        # Extract all topics/skills from the learning path
        all_topics = self._extract_topics_from_path(learning_path)
        
        # Create prompt for Gemini
        prompt = self._create_quiz_prompt(all_topics, learning_path)
        
        # Generate quiz using Gemini
        try:
            response = self.model.generate_content(prompt)
            quiz_data = self._parse_quiz_response(response.text)
            
            # Add metadata
            quiz_data['metadata'] = {
                'learning_path_id': learning_path.get('id', 'unknown'),
                'target_occupation': learning_path.get('target_occupation', 'unknown'),
                'total_topics': len(all_topics),
                'generated_at': datetime.now().isoformat(),
                'total_questions': 10,
                'difficulty_distribution': {
                    'easy': 4,
                    'medium': 3,
                    'hard': 3
                }
            }
            
            quiz_data['topics_covered'] = all_topics
            
            return quiz_data
            
        except Exception as e:
            print(f"Error generating quiz: {e}")
            return self._create_fallback_quiz(all_topics)
    
    def _extract_topics_from_path(self, learning_path: Dict[str, Any]) -> List[str]:
        """Extract all unique topics/skills from the learning path."""
        topics = []
        
        # Extract from sessions
        sessions = learning_path.get('sessions', [])
        for session in sessions:
            # Get session topic
            if 'topic' in session:
                topics.append(session['topic'])
            
            # Get skills from session
            if 'skills' in session:
                for skill in session['skills']:
                    if isinstance(skill, dict):
                        skill_name = skill.get('preferredLabel', skill.get('name', ''))
                    else:
                        skill_name = str(skill)
                    
                    if skill_name and skill_name not in topics:
                        topics.append(skill_name)
        
        # Also check top-level skills if present
        if 'skills' in learning_path:
            for skill in learning_path['skills']:
                if isinstance(skill, dict):
                    skill_name = skill.get('preferredLabel', skill.get('name', ''))
                else:
                    skill_name = str(skill)
                
                if skill_name and skill_name not in topics:
                    topics.append(skill_name)
        
        return topics[:15]  # Limit to top 15 topics to keep quiz focused
    
    def _create_quiz_prompt(self, topics: List[str], learning_path: Dict[str, Any]) -> str:
        """Create a detailed prompt for Gemini to generate the quiz."""
        target_occupation = learning_path.get('target_occupation', 'the target role')
        
        prompt = f"""You are an expert educational assessment creator. Generate a comprehensive quiz for a learning path aimed at becoming a {target_occupation}.

TOPICS TO COVER:
{chr(10).join([f"- {topic}" for topic in topics])}

REQUIREMENTS:
1. Create EXACTLY 10 multiple choice questions (MCQs)
2. Difficulty distribution:
   - 4 EASY questions (fundamental concepts, definitions)
   - 3 MEDIUM questions (application, understanding)
   - 3 HARD questions (analysis, synthesis, real-world scenarios)
3. Each question must have:
   - A clear, concise question statement
   - Exactly 4 answer options (A, B, C, D)
   - Only ONE correct answer
   - The topic/skill being tested
   - Difficulty level
4. Cover diverse topics from the list above
5. Questions should be practical and relevant to {target_occupation}

OUTPUT FORMAT (strict JSON):
{{
  "questions": [
    {{
      "id": 1,
      "question": "Question text here?",
      "options": {{
        "A": "Option A text",
        "B": "Option B text",
        "C": "Option C text",
        "D": "Option D text"
      }},
      "correct_answer": "A",
      "difficulty": "easy",
      "topic": "Topic name from the list",
      "explanation": "Brief explanation of why this answer is correct"
    }}
  ]
}}

Generate the quiz now in valid JSON format:"""
        
        return prompt
    
    def _parse_quiz_response(self, response_text: str) -> Dict[str, Any]:
        """Parse Gemini's response and extract quiz JSON."""
        # Try to extract JSON from response
        json_match = re.search(r'\{[\s\S]*\}', response_text)
        
        if json_match:
            try:
                quiz_data = json.loads(json_match.group())
                
                # Validate structure
                if 'questions' in quiz_data and len(quiz_data['questions']) > 0:
                    # Ensure we have exactly 10 questions
                    questions = quiz_data['questions'][:10]
                    
                    # Validate each question
                    validated_questions = []
                    for q in questions:
                        if all(key in q for key in ['question', 'options', 'correct_answer', 'difficulty', 'topic']):
                            validated_questions.append(q)
                    
                    quiz_data['questions'] = validated_questions
                    return quiz_data
            except json.JSONDecodeError:
                pass
        
        # If parsing fails, return empty structure
        return {"questions": []}
    
    def _create_fallback_quiz(self, topics: List[str]) -> Dict[str, Any]:
        """Create a basic fallback quiz if generation fails."""
        return {
            "questions": [],
            "metadata": {
                "generated_at": datetime.now().isoformat(),
                "status": "generation_failed",
                "total_questions": 0
            },
            "topics_covered": topics,
            "error": "Failed to generate quiz. Please try again."
        }
    
    def analyze_quiz_results(self, quiz: Dict[str, Any], user_answers: Dict[int, str]) -> Dict[str, Any]:
        """
        Analyze user's quiz results and provide detailed feedback.
        
        Args:
            quiz: The quiz dictionary with questions
            user_answers: Dictionary mapping question_id to user's answer (A/B/C/D)
            
        Returns:
            Dictionary with analysis, score, strengths, weaknesses
        """
        questions = quiz.get('questions', [])
        total_questions = len(questions)
        
        if total_questions == 0:
            return {"error": "No questions in quiz"}
        
        # Initialize analysis
        correct_count = 0
        incorrect_count = 0
        topic_performance = {}
        difficulty_performance = {'easy': {'correct': 0, 'total': 0},
                                 'medium': {'correct': 0, 'total': 0},
                                 'hard': {'correct': 0, 'total': 0}}
        
        detailed_results = []
        
        # Analyze each question
        for question in questions:
            q_id = question.get('id')
            correct_answer = question.get('correct_answer')
            user_answer = user_answers.get(q_id, '')
            topic = question.get('topic', 'Unknown')
            difficulty = question.get('difficulty', 'medium')
            
            is_correct = (user_answer.upper() == correct_answer.upper())
            
            # Update counters
            if is_correct:
                correct_count += 1
            else:
                incorrect_count += 1
            
            # Track topic performance
            if topic not in topic_performance:
                topic_performance[topic] = {'correct': 0, 'total': 0, 'questions': []}
            
            topic_performance[topic]['total'] += 1
            topic_performance[topic]['questions'].append(q_id)
            
            if is_correct:
                topic_performance[topic]['correct'] += 1
            
            # Track difficulty performance
            if difficulty in difficulty_performance:
                difficulty_performance[difficulty]['total'] += 1
                if is_correct:
                    difficulty_performance[difficulty]['correct'] += 1
            
            # Store detailed result
            detailed_results.append({
                'question_id': q_id,
                'question': question.get('question'),
                'user_answer': user_answer,
                'correct_answer': correct_answer,
                'is_correct': is_correct,
                'topic': topic,
                'difficulty': difficulty,
                'explanation': question.get('explanation', '')
            })
        
        # Calculate score
        score_percentage = (correct_count / total_questions) * 100
        
        # Identify strengths and weaknesses
        strengths = []
        weaknesses = []
        needs_improvement = []
        
        for topic, performance in topic_performance.items():
            accuracy = (performance['correct'] / performance['total']) * 100
            
            if accuracy >= 75:
                strengths.append({
                    'topic': topic,
                    'accuracy': round(accuracy, 1),
                    'correct': performance['correct'],
                    'total': performance['total']
                })
            elif accuracy >= 50:
                needs_improvement.append({
                    'topic': topic,
                    'accuracy': round(accuracy, 1),
                    'correct': performance['correct'],
                    'total': performance['total']
                })
            else:
                weaknesses.append({
                    'topic': topic,
                    'accuracy': round(accuracy, 1),
                    'correct': performance['correct'],
                    'total': performance['total']
                })
        
        # Sort by accuracy
        strengths.sort(key=lambda x: x['accuracy'], reverse=True)
        weaknesses.sort(key=lambda x: x['accuracy'])
        needs_improvement.sort(key=lambda x: x['accuracy'])
        
        # Generate recommendations
        recommendations = self._generate_recommendations(
            score_percentage, strengths, weaknesses, needs_improvement, difficulty_performance
        )
        
        # Create performance summary
        performance_level = self._get_performance_level(score_percentage)
        
        return {
            'score': {
                'correct': correct_count,
                'incorrect': incorrect_count,
                'total': total_questions,
                'percentage': round(score_percentage, 1),
                'grade': self._calculate_grade(score_percentage)
            },
            'performance_level': performance_level,
            'difficulty_analysis': {
                'easy': {
                    'correct': difficulty_performance['easy']['correct'],
                    'total': difficulty_performance['easy']['total'],
                    'percentage': round((difficulty_performance['easy']['correct'] / difficulty_performance['easy']['total'] * 100) if difficulty_performance['easy']['total'] > 0 else 0, 1)
                },
                'medium': {
                    'correct': difficulty_performance['medium']['correct'],
                    'total': difficulty_performance['medium']['total'],
                    'percentage': round((difficulty_performance['medium']['correct'] / difficulty_performance['medium']['total'] * 100) if difficulty_performance['medium']['total'] > 0 else 0, 1)
                },
                'hard': {
                    'correct': difficulty_performance['hard']['correct'],
                    'total': difficulty_performance['hard']['total'],
                    'percentage': round((difficulty_performance['hard']['correct'] / difficulty_performance['hard']['total'] * 100) if difficulty_performance['hard']['total'] > 0 else 0, 1)
                }
            },
            'strengths': strengths,
            'needs_improvement': needs_improvement,
            'weaknesses': weaknesses,
            'recommendations': recommendations,
            'detailed_results': detailed_results,
            'analyzed_at': datetime.now().isoformat()
        }
    
    def _generate_recommendations(self, score: float, strengths: List, weaknesses: List, 
                                  needs_improvement: List, difficulty_perf: Dict) -> List[str]:
        """Generate personalized recommendations based on performance."""
        recommendations = []
        
        # Overall performance recommendations
        if score >= 80:
            recommendations.append("🎉 Excellent performance! You have a strong grasp of the material.")
        elif score >= 60:
            recommendations.append("👍 Good job! You understand most concepts but have room for improvement.")
        else:
            recommendations.append("📚 Consider reviewing the learning path materials more thoroughly.")
        
        # Difficulty-based recommendations
        easy_perf = difficulty_perf['easy']
        medium_perf = difficulty_perf['medium']
        hard_perf = difficulty_perf['hard']
        
        if easy_perf['total'] > 0 and (easy_perf['correct'] / easy_perf['total']) < 0.75:
            recommendations.append("⚠️ Focus on mastering fundamental concepts - you struggled with basic questions.")
        
        if medium_perf['total'] > 0 and (medium_perf['correct'] / medium_perf['total']) < 0.6:
            recommendations.append("💡 Practice applying concepts to different scenarios to improve your understanding.")
        
        if hard_perf['total'] > 0 and (hard_perf['correct'] / hard_perf['total']) >= 0.67:
            recommendations.append("🌟 Great critical thinking! You excel at complex problem-solving.")
        
        # Topic-specific recommendations
        if weaknesses:
            weak_topics = [w['topic'] for w in weaknesses[:3]]
            recommendations.append(f"🎯 Priority topics to review: {', '.join(weak_topics)}")
        
        if strengths:
            strong_topics = [s['topic'] for s in strengths[:2]]
            recommendations.append(f"✅ Your strongest areas: {', '.join(strong_topics)}")
        
        if needs_improvement:
            improve_topics = [n['topic'] for n in needs_improvement[:2]]
            recommendations.append(f"📖 Topics needing more practice: {', '.join(improve_topics)}")
        
        return recommendations
    
    def _get_performance_level(self, score: float) -> str:
        """Determine performance level based on score."""
        if score >= 90:
            return "Outstanding"
        elif score >= 80:
            return "Excellent"
        elif score >= 70:
            return "Good"
        elif score >= 60:
            return "Satisfactory"
        elif score >= 50:
            return "Needs Improvement"
        else:
            return "Requires Significant Review"
    
    def _calculate_grade(self, score: float) -> str:
        """Calculate letter grade from percentage."""
        if score >= 90:
            return "A+"
        elif score >= 85:
            return "A"
        elif score >= 80:
            return "A-"
        elif score >= 75:
            return "B+"
        elif score >= 70:
            return "B"
        elif score >= 65:
            return "B-"
        elif score >= 60:
            return "C+"
        elif score >= 55:
            return "C"
        elif score >= 50:
            return "C-"
        else:
            return "F"
    
    def save_quiz_to_file(self, quiz: Dict[str, Any], filename: str) -> bool:
        """Save quiz to JSON file."""
        try:
            with open(filename, 'w', encoding='utf-8') as f:
                json.dump(quiz, f, indent=2, ensure_ascii=False)
            return True
        except Exception as e:
            print(f"Error saving quiz: {e}")
            return False
    
    def load_quiz_from_file(self, filename: str) -> Optional[Dict[str, Any]]:
        """Load quiz from JSON file."""
        try:
            with open(filename, 'r', encoding='utf-8') as f:
                return json.load(f)
        except Exception as e:
            print(f"Error loading quiz: {e}")
            return None
