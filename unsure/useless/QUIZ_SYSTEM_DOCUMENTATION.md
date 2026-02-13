# Quiz System Implementation

## Overview
The quiz system generates personalized 10-question multiple-choice quizzes for each learning path, with difficulty distribution optimized for learning assessment.

## Architecture

### Components
1. **Quiz Generator** (`ai_engine.py`)
   - Uses Gemini 2.5 Flash for intelligent question generation
   - Analyzes learning path sessions to create relevant questions
   
2. **Quiz API Endpoint** (`app.py`)
   - Route: `POST /api/quiz`
   - Accepts learning path data and generates quiz

3. **Demo Script** (`demo_quiz_api.py`)
   - Demonstrates quiz generation workflow
   - Shows proper data formatting

## Technical Implementation

### Quiz Generation Flow
```
User Goal → Learning Path API → Learning Path Data → Quiz API → 10 MCQs
```

### API Request Format
```python
POST /api/quiz
{
    "learning_path": [
        {
            "session_number": 1,
            "session_title": "Foundation Skills",
            "skills": ["Python", "Statistics", "Data Analysis"]
        },
        ...
    ]
}
```

### API Response Format
```python
{
    "quiz": {
        "total_questions": 10,
        "questions": [
            {
                "question_number": 1,
                "question": "What is the primary purpose of...",
                "options": {
                    "A": "Option 1",
                    "B": "Option 2", 
                    "C": "Option 3",
                    "D": "Option 4"
                },
                "correct_answer": "B",
                "difficulty": "easy",
                "skill_assessed": "Python"
            },
            ...
        ]
    }
}
```

## Quiz Characteristics

### Difficulty Distribution
- **4 Easy Questions** (40%): Basic concepts, definitions
- **3 Medium Questions** (30%): Application, understanding
- **3 Hard Questions** (30%): Analysis, complex scenarios

### Question Quality
- All questions are multiple-choice (4 options)
- Each question maps to a specific skill from the learning path
- Difficulty levels ensure comprehensive skill assessment
- Questions test understanding, not just memorization

## Implementation Details

### Key Code Locations

#### 1. Quiz Generator Method (`ai_engine.py` lines ~820-920)
```python
def generate_quiz(self, learning_path_data: Dict) -> Dict:
    """Generate a 10-question quiz based on learning path."""
    # Builds prompt with all sessions and skills
    # Requests Gemini to generate balanced quiz
    # Returns structured quiz data
```

#### 2. Quiz API Endpoint (`app.py` lines ~730-770)
```python
@app.route('/api/quiz', methods=['POST'])
def generate_quiz():
    """Generate quiz for learning path."""
    # Validates input
    # Calls quiz generator
    # Returns formatted quiz
```

#### 3. Data Transformation (`demo_quiz_api.py` lines ~40-60)
```python
# Transform /api/path response to quiz-compatible format
learning_path_for_quiz = {
    "learning_path": [
        {
            "session_number": i + 1,
            "session_title": session.get("title"),
            "skills": [skill if isinstance(skill, str) else skill.get("label") 
                      for skill in session.get("skills", [])]
        }
        for i, session in enumerate(path_data.get("learning_path", []))
    ]
}
```

## Bug Fixes Implemented

### Issue 1: 503 Error - Quiz Generator Not Available
**Problem**: Quiz API returned 503 with message "Quiz generator not available"

**Root Cause**: Data structure mismatch between `/api/path` response and quiz generator expectations
- `/api/path` returns: `{"learning_path": [...], "matched_occupation": {...}}`
- Quiz generator expected: Sessions with specific structure

**Solution**: Transform API response in `demo_quiz_api.py`
```python
# Extract and reformat learning_path array
learning_path_for_quiz = {
    "learning_path": [
        {
            "session_number": session_index + 1,
            "session_title": session.get("title"),
            "skills": extract_skill_labels(session)
        }
        for session_index, session in enumerate(raw_path_data["learning_path"])
    ]
}
```

**Files Modified**: `demo_quiz_api.py` (lines 40-60)

## Usage Example

### Complete Workflow
```python
import requests

BASE_URL = "http://127.0.0.1:5000"

# Step 1: Generate learning path
response = requests.post(f"{BASE_URL}/api/path", 
    json={"goal": "I want to become a Data Scientist"})
path_data = response.json()

# Step 2: Transform data for quiz
learning_path_for_quiz = {
    "learning_path": [
        {
            "session_number": i + 1,
            "session_title": session.get("title"),
            "skills": [
                skill if isinstance(skill, str) else skill.get("label") 
                for skill in session.get("skills", [])
            ]
        }
        for i, session in enumerate(path_data.get("learning_path", []))
    ]
}

# Step 3: Generate quiz
quiz_response = requests.post(f"{BASE_URL}/api/quiz", 
    json=learning_path_for_quiz)
quiz = quiz_response.json()

# Step 4: Display quiz
for q in quiz["quiz"]["questions"]:
    print(f"Q{q['question_number']}. {q['question']} ({q['difficulty']})")
    for option, text in q['options'].items():
        print(f"  {option}. {text}")
    print(f"  Answer: {q['correct_answer']}\n")
```

## Testing

### Test Script: `demo_quiz_api.py`
**Purpose**: Demonstrates end-to-end quiz generation

**Test Cases**:
1. ✅ Learning path generation
2. ✅ Data structure transformation
3. ✅ Quiz generation API call
4. ✅ Quiz display formatting

**Expected Output**:
- 10 questions generated
- Balanced difficulty distribution
- All questions have 4 options
- Each question linked to a skill

## Integration Points

### Frontend Integration
```javascript
// React example
async function generateQuiz(learningPath) {
    const response = await fetch('/api/quiz', {
        method: 'POST',
        headers: {'Content-Type': 'application/json'},
        body: JSON.stringify({learning_path: learningPath})
    });
    
    const {quiz} = await response.json();
    return quiz;
}
```

### Backend Integration
```python
# Use within learning path generation
from ai_engine import GenMentorAI

engine = GenMentorAI()
path = engine.generate_learning_path(goal, user_skills)
quiz = engine.generate_quiz({"learning_path": path})
```

## Performance Considerations

### API Call Costs
- Each quiz generation = 1 Gemini API call
- Average tokens: ~2000-3000 (varies by learning path complexity)
- Rate limits: Subject to Gemini API quotas

### Caching Strategy
- Quiz not currently cached (generates fresh each time)
- Recommendation: Cache quizzes by learning path hash for 24 hours

### Response Times
- Typical: 3-8 seconds (depends on Gemini API response)
- Timeout: 30 seconds configured

## Error Handling

### Common Errors

1. **503 - Quiz Generator Not Available**
   - Cause: Gemini API not configured or unreachable
   - Solution: Check `GEMINI_API_KEY` in config

2. **400 - Invalid Learning Path Data**
   - Cause: Missing required fields in request
   - Solution: Ensure proper data structure transformation

3. **Rate Limit Exceeded**
   - Cause: Too many Gemini API calls
   - Solution: Implement request throttling or caching

## Future Enhancements

### Planned Features
1. **Adaptive Difficulty**: Adjust question difficulty based on user performance
2. **Quiz History**: Store user quiz attempts and scores
3. **Answer Explanations**: Generate detailed explanations for correct answers
4. **Timed Quizzes**: Add time limits per question
5. **Quiz Analytics**: Track which skills users struggle with most

### Optimization Opportunities
1. Batch quiz generation for multiple users
2. Pre-generate quizzes for common learning paths
3. Implement quiz result feedback loop to improve question quality
4. Add question bank for instant quiz generation

## Maintenance

### Monitoring
- Track quiz generation success rate
- Monitor Gemini API usage and costs
- Log failed quiz generations for debugging

### Updates Required
- When learning path structure changes, update quiz generator
- When Gemini API version changes, test quiz quality
- Periodically review quiz difficulty distribution

## Summary

The quiz system successfully integrates with the learning path generation workflow to provide automated skill assessment. The implementation leverages Gemini 2.5 Flash for intelligent question generation, ensuring quizzes are relevant, well-structured, and pedagogically sound.

**Status**: ✅ Fully functional and tested
**Last Updated**: December 19, 2025
