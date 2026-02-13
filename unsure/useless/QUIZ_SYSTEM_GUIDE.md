# Quiz System Guide

## Overview

The GenMentor Quiz System automatically generates comprehensive, AI-powered quizzes for learning paths using the Gemini API. Each quiz consists of 10 multiple-choice questions covering all topics in the learning path, with intelligent difficulty distribution and detailed performance analysis.

## Features

### 1. **Automatic Quiz Generation**
- **10 MCQs per learning path**
- **Difficulty Distribution:**
  - 4 Easy questions (fundamental concepts)
  - 3 Medium questions (application & understanding)
  - 3 Hard questions (analysis & real-world scenarios)
- **Topic Coverage:** Questions span all topics/skills in the learning path
- **AI-Powered:** Uses Gemini 2.0 Flash for intelligent question generation

### 2. **Comprehensive Analysis**
After quiz submission, the system provides:
- **Overall Score:** Percentage, grade, and performance level
- **Difficulty Breakdown:** Performance on easy/medium/hard questions
- **Topic Analysis:** 
  - **Strengths:** Topics with ≥75% accuracy
  - **Needs Improvement:** Topics with 50-74% accuracy
  - **Weaknesses:** Topics with <50% accuracy
- **Personalized Recommendations:** Actionable feedback based on performance

## Installation

The quiz system is already integrated. Ensure you have:

```bash
# Already in requirements.txt
google-generativeai==0.8.5
```

## Usage

### Method 1: Via API (Recommended)

#### Step 1: Start the Flask Server
```bash
python app.py
```

#### Step 2: Generate a Learning Path
```bash
curl -X POST http://localhost:5000/api/path \
  -H "Content-Type: application/json" \
  -d '{
    "goal": "I want to become a Data Scientist",
    "current_skills": ["Python", "Statistics"]
  }'
```

**Note:** The `/api/path` response returns:
```json
{
  "matched_occupation": {...},
  "learning_path": [...sessions...],  // Array of sessions
  "skill_gap_summary": {...}
}
```

#### Step 3: Generate Quiz
To generate a quiz, you need to format the data properly:

```bash
curl -X POST http://localhost:5000/api/quiz/generate \
  -H "Content-Type: application/json" \
  -d '{
    "learning_path": {
      "sessions": [...sessions from step 2...],
      "target_occupation": "Data Scientist",
      "id": "path_12345"
    }
  }'
```

#### Step 4: Submit Answers
```bash
curl -X POST http://localhost:5000/api/quiz/submit \
  -H "Content-Type: application/json" \
  -d '{
    "quiz": {QUIZ_JSON},
    "answers": {
      "1": "A",
      "2": "C",
      "3": "B",
      ...
    }
  }'
```

### Method 2: Direct Python Usage

```python
from quiz_generator import QuizGenerator
from ai_engine import GenMentorAI
from config import GEMINI_API_KEY

# Initialize
ai_engine = GenMentorAI()
quiz_gen = QuizGenerator(GEMINI_API_KEY)

# Generate learning path
learning_path = ai_engine.generate_learning_path(
    "I want to become a Machine Learning Engineer",
    ["Python", "Math"]
)

# Generate quiz
quiz = quiz_gen.generate_quiz(learning_path)

# User takes quiz...
user_answers = {
    1: "A",
    2: "C",
    3: "B",
    # ... etc
}

# Analyze results
analysis = quiz_gen.analyze_quiz_results(quiz, user_answers)

# Display results
print(f"Score: {analysis['score']['percentage']}%")
print(f"Grade: {analysis['score']['grade']}")
print(f"Strengths: {[s['topic'] for s in analysis['strengths']]}")
print(f"Weaknesses: {[w['topic'] for w in analysis['weaknesses']]}")
```

## API Endpoints

### POST `/api/quiz/generate`
Generate a quiz for a learning path.

**Request:**
```json
{
  "learning_path": {
    "sessions": [...],
    "target_occupation": "Data Scientist",
    "skills": [...]
  }
}
```

**Response:**
```json
{
  "success": true,
  "quiz": {
    "questions": [
      {
        "id": 1,
        "question": "What is...",
        "options": {
          "A": "Option A",
          "B": "Option B",
          "C": "Option C",
          "D": "Option D"
        },
        "correct_answer": "A",
        "difficulty": "easy",
        "topic": "Python Basics",
        "explanation": "..."
      }
    ],
    "metadata": {
      "total_questions": 10,
      "difficulty_distribution": {
        "easy": 4,
        "medium": 3,
        "hard": 3
      }
    }
  }
}
```

### POST `/api/quiz/submit`
Submit quiz answers and get analysis.

**Request:**
```json
{
  "quiz": {QUIZ_OBJECT},
  "answers": {
    "1": "A",
    "2": "C",
    "3": "B"
  }
}
```

**Response:**
```json
{
  "success": true,
  "analysis": {
    "score": {
      "correct": 7,
      "incorrect": 3,
      "total": 10,
      "percentage": 70.0,
      "grade": "B"
    },
    "performance_level": "Good",
    "difficulty_analysis": {
      "easy": {"correct": 4, "total": 4, "percentage": 100.0},
      "medium": {"correct": 2, "total": 3, "percentage": 66.7},
      "hard": {"correct": 1, "total": 3, "percentage": 33.3}
    },
    "strengths": [
      {"topic": "Python Basics", "accuracy": 100.0}
    ],
    "weaknesses": [
      {"topic": "Advanced ML", "accuracy": 33.3}
    ],
    "recommendations": [
      "👍 Good job! You understand most concepts...",
      "🎯 Priority topics to review: Advanced ML"
    ]
  }
}
```

## Testing

### Run Test Suite
```bash
python test_quiz_system.py
```

This will:
1. Generate a sample learning path
2. Create a quiz with 10 questions
3. Simulate user answers (~70% accuracy)
4. Analyze results
5. Display comprehensive feedback
6. Save quiz and results to JSON files

### Run API Demo
```bash
# Terminal 1: Start server
python app.py

# Terminal 2: Run demo
python demo_quiz_api.py
```

## Quiz Structure

### Question Object
```json
{
  "id": 1,
  "question": "What is the primary purpose of...",
  "options": {
    "A": "First option",
    "B": "Second option",
    "C": "Third option",
    "D": "Fourth option"
  },
  "correct_answer": "B",
  "difficulty": "medium",
  "topic": "Machine Learning Fundamentals",
  "explanation": "The correct answer is B because..."
}
```

### Analysis Object
```json
{
  "score": {
    "correct": 8,
    "incorrect": 2,
    "total": 10,
    "percentage": 80.0,
    "grade": "A-"
  },
  "performance_level": "Excellent",
  "difficulty_analysis": {...},
  "strengths": [...],
  "needs_improvement": [...],
  "weaknesses": [...],
  "recommendations": [...],
  "detailed_results": [...],
  "analyzed_at": "2025-12-19T10:30:45"
}
```

## Performance Grading

| Score | Grade | Performance Level |
|-------|-------|-------------------|
| 90-100% | A+ | Outstanding |
| 85-89% | A | Outstanding |
| 80-84% | A- | Excellent |
| 75-79% | B+ | Excellent |
| 70-74% | B | Good |
| 65-69% | B- | Good |
| 60-64% | C+ | Satisfactory |
| 55-59% | C | Satisfactory |
| 50-54% | C- | Needs Improvement |
| <50% | F | Requires Significant Review |

## Topic Performance Categories

- **Strengths:** ≥75% accuracy - Topics you've mastered
- **Needs Improvement:** 50-74% accuracy - Topics requiring more practice
- **Weaknesses:** <50% accuracy - Priority areas for review

## Tips for Best Results

1. **Complete the Learning Path First:** Take the quiz after going through all sessions
2. **Take Your Time:** Read each question carefully
3. **Review Explanations:** Learn from both correct and incorrect answers
4. **Focus on Weak Areas:** Use the analysis to guide your study plan
5. **Retake If Needed:** Generate a new quiz after reviewing weak topics

## Troubleshooting

### Quiz Generation Fails
- **Check API Key:** Ensure `GEMINI_API_KEY` is set in `config.py`
- **Network Issues:** Verify internet connection
- **Rate Limits:** Wait a few seconds and try again

### Empty Quiz
- **Learning Path Issue:** Ensure the learning path has sessions with topics
- **API Response:** Check Gemini API response format

### Analysis Errors
- **Answer Format:** Ensure answers are in format `{1: "A", 2: "B", ...}`
- **Question IDs:** Verify question IDs match the quiz

## Files

- **`quiz_generator.py`** - Main quiz generation and analysis logic
- **`app.py`** - Flask API endpoints (updated with quiz routes)
- **`test_quiz_system.py`** - Comprehensive test suite
- **`demo_quiz_api.py`** - API usage demonstration
- **`QUIZ_SYSTEM_GUIDE.md`** - This guide

## Future Enhancements

Potential improvements:
- Quiz difficulty customization
- Timed quizzes
- Question randomization
- Quiz history tracking
- Adaptive difficulty based on performance
- Multi-language support
- Export results to PDF/HTML

---

**Need Help?** Check the test files for working examples or review the API documentation at `http://localhost:5000` when the server is running.
