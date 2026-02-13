# 🧠 Cortex - AI-Powered Career Learning Path Generator

[![Python](https://img.shields.io/badge/Python-3.12%2B-blue.svg)](https://www.python.org/)
[![Flask](https://img.shields.io/badge/Flask-2.0%2B-green.svg)](https://flask.palletsprojects.com/)
[![OpenAI](https://img.shields.io/badge/OpenAI-GPT--5.2-412991.svg)](https://openai.com/)
[![Gemini](https://img.shields.io/badge/Google-Gemini%202.5-4285F4.svg)](https://ai.google.dev/)
[![License](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)
[![Status](https://img.shields.io/badge/Status-Production-success.svg)](https://github.com/Manasvi-Vedanta/Hybrid-GenMentor)

> An intelligent career guidance platform combining **Retrieval-Augmented Generation (RAG)**, **ESCO taxonomy**, and **dual LLM support (GPT-5.2 / Gemini)** to generate personalized, skill-based learning paths.

---

## 🌟 Features

### Core Capabilities
- 🎯 **Smart Career Matching**: Match user goals to 3,039+ ESCO occupations using FAISS-based semantic search
- 📚 **Personalized Learning Paths**: Generate structured learning plans with 13,939+ skills
- 🧠 **RAG Architecture**: Retrieval-Augmented Generation for factually grounded content
- 🤖 **Dual LLM Support**: Switchable between OpenAI GPT-5.2 and Google Gemini 2.5
- 📝 **AI Quiz Generation**: Auto-generate 10-question assessments with difficulty distribution
- 📊 **Skill Gap Analysis**: Identify exactly what skills you need to learn
- 🔄 **Dependency-Based Scheduling**: Learn skills in optimal prerequisite order
- 💬 **Community Feedback**: Vote, suggest, and rate learning resources
- 📈 **Performance Analytics**: Comprehensive testing with detailed metrics

### Advanced Features
- **Semantic Embeddings**: 768-dimensional vectors using `all-mpnet-base-v2` Sentence Transformer
- **FAISS Indexing**: Fast approximate nearest neighbor search for occupation matching
- **Graph-Based Scheduling**: NetworkX for skill dependency resolution
- **Multi-Strategy Matching**: Exact, partial, and semantic keyword matching with boost factors
- **Quiz Analysis Engine**: Strengths/weaknesses identification with personalized recommendations
- **RESTful API**: Clean JSON endpoints for frontend integration

---

## 📊 System Performance

### Comprehensive Evaluation Results (20 Test Cases)

| Metric | GPT-5.2 | Gemini 2.5 |
|--------|---------|------------|
| **Success Rate** | 100% (20/20) | 100% (20/20) |
| **Average Similarity Score** | 87.53% | 87.53% |
| **Mean Skills per Path** | 32.8 | 14.0 |
| **Path Generation Time** | 30.5s | 9.1s |
| **Quiz Generation Time** | 29.2s | 24.4s |
| **Total Evaluation Time** | 37 min | 21 min |

### Feature Success Rates

| Feature | Success |
|---------|---------|
| Learning Path Generation | 100% |
| Quiz Generation (10 MCQs) | 100% |
| Community Voting | 100% |
| Skill Suggestions | 100% |
| Path Regeneration | 100% |

### Category Performance (Similarity Scores)

| Category | Avg Similarity | Avg Skills |
|----------|----------------|------------|
| AI/ML | 94.09% | 26.3 |
| Infrastructure | 93.04% | 38.0 |
| Data Engineering | 91.17% | 28.5 |
| Emerging Tech | 96.77% | 29.0 |
| Systems | 94.06% | 40.0 |

---

## 🏗️ Architecture

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                              User Request                                    │
│                    "I want to become a Machine Learning Engineer"           │
└───────────────────────────────────┬─────────────────────────────────────────┘
                                    │
                                    ▼
┌─────────────────────────────────────────────────────────────────────────────┐
│                           Flask API Server                                   │
│  /api/path  │  /api/quiz/generate  │  /api/vote  │  /api/suggestions        │
└───────────────────────────────────┬─────────────────────────────────────────┘
                                    │
                    ┌───────────────┴───────────────┐
                    ▼                               ▼
┌───────────────────────────────┐   ┌───────────────────────────────┐
│      RAG RETRIEVAL (R)        │   │       LLM GENERATION (G)      │
│  ┌─────────────────────────┐  │   │  ┌─────────────────────────┐  │
│  │ Sentence Transformer    │  │   │  │    GPT-5.2 / Gemini     │  │
│  │ (all-mpnet-base-v2)     │  │   │  │    Temperature: 0.2-0.4 │  │
│  │ 768-dim embeddings      │  │   │  │    Max Tokens: 2048-3000│  │
│  └───────────┬─────────────┘  │   │  └───────────┬─────────────┘  │
│              ▼                │   │              │                │
│  ┌─────────────────────────┐  │   │              │                │
│  │    FAISS Index Search   │  │   │              ▼                │
│  │    occupation_faiss.idx │──┼───┼──► Augmented Prompt           │
│  └───────────┬─────────────┘  │   │              │                │
│              ▼                │   │              ▼                │
│  ┌─────────────────────────┐  │   │  ┌─────────────────────────┐  │
│  │   ESCO Skills Retrieval │  │   │  │  Structured Learning    │  │
│  │   13,939+ skills        │  │   │  │  Path with Sessions     │  │
│  └─────────────────────────┘  │   │  └─────────────────────────┘  │
└───────────────────────────────┘   └───────────────────────────────┘
                    │                               │
                    └───────────────┬───────────────┘
                                    ▼
┌─────────────────────────────────────────────────────────────────────────────┐
│                           SQLite Database                                    │
│   • 3,039 ESCO Occupations    • 13,939 Skills    • Skill Hierarchies       │
│   • Community Votes           • User Suggestions  • Learning Resources      │
└─────────────────────────────────────────────────────────────────────────────┘
```

---

## 🚀 Quick Start

### Prerequisites

- Python 3.8 or higher
- pip (Python package manager)
- 4GB RAM minimum
- Internet connection (for Gemini API)

### Installation

1. **Clone the repository**
```bash
git clone https://github.com/Manasvi-Vedanta/Hybrid-GenMentor.git
cd Hybrid-GenMentor
```

2. **Create virtual environment** (recommended)
```bash
python -m venv venv

# Windows
venv\Scripts\activate

# Linux/Mac
source venv/bin/activate
```

3. **Install dependencies**
```bash
pip install -r requirements.txt
```

4. **Configure LLM Provider**

Edit `config.py` to set your preferred LLM:

```python
# For OpenAI GPT-5.2 (default)
OPENAI_API_KEY = "your-openai-key"
OPENAI_MODEL = "gpt-5.2-2025-12-11"

# For Google Gemini
GEMINI_API_KEY = "your-gemini-key"
```

Switch providers by commenting/uncommenting sections marked `--- GEMINI ---` or `--- OPENAI ---` in:
- `ai_engine.py`
- `quiz_generator.py`
- `app.py`

5. **Verify installation**
```bash
python -c "import flask, sentence_transformers, openai; print('✅ All dependencies installed!')"
```

### Running the System

1. **Start the Flask server**
```bash
python app.py
```

You should see:
```
Loading sentence transformer model: all-mpnet-base-v2...
✅ Loaded all-mpnet-base-v2 (dimension: 768)
✅ FAISS index initialized
✅ Quiz generator initialized with OpenAI
Loaded 3039 occupation embeddings
 * Running on http://127.0.0.1:5000 (threaded)
```

2. **Test the API**

Open your browser and visit:
- API Documentation: `http://localhost:5000`
- Health Check: `http://localhost:5000/api/health`

Or use PowerShell:
```powershell
Invoke-WebRequest -Uri http://localhost:5000/api/health
```

3. **Make your first request**

```powershell
$body = @{
    goal = "I want to become a data scientist"
    current_skills = @("python", "statistics")
} | ConvertTo-Json

Invoke-RestMethod -Uri http://localhost:5000/api/path -Method Post -ContentType "application/json" -Body $body
```

---

## 📖 API Documentation

### 1. Health Check
Check if the API is running.

```http
GET /api/health
```

**Response:**
```json
{
    "status": "healthy",
    "message": "Cortex API is running",
    "model": "all-mpnet-base-v2",
    "embedding_dimension": 768,
    "llm_available": true,
    "llm_provider": "openai"
}
```

### 2. Generate Quiz
Auto-generate a 10-question assessment for a learning path.

```http
POST /api/quiz/generate
```

**Request Body:**
```json
{
    "learning_path": {
        "sessions": [...],
        "target_occupation": "Machine Learning Engineer"
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
                "question": "What is the primary purpose of feature scaling in ML?",
                "options": {"A": "...", "B": "...", "C": "...", "D": "..."},
                "correct_answer": "B",
                "difficulty": "easy",
                "topic": "Machine Learning",
                "explanation": "..."
            }
        ],
        "metadata": {
            "total_questions": 10,
            "difficulty_distribution": {"easy": 4, "medium": 3, "hard": 3}
        }
    }
}
```

### 3. Submit Quiz Answers
Submit answers and get performance analysis.

```http
POST /api/quiz/submit
```

**Request:**
```json
{
    "quiz": {...},
    "answers": {"1": "A", "2": "C", "3": "B", ...}
}
```

**Response:**
```json
{
    "analysis": {
        "score": {"percentage": 70.0, "grade": "B"},
        "strengths": [{"topic": "Python", "accuracy": 100.0}],
        "weaknesses": [{"topic": "Deep Learning", "accuracy": 33.3}],
        "recommendations": [
            "🎯 Priority topics to review: Deep Learning",
            "✅ Your strongest areas: Python, Statistics"
        ]
    }
}
```

### 4. Generate Learning Path
Get a personalized learning path based on career goals.

```http
POST /api/path
```

**Request Body:**
```json
{
    "goal": "I want to become a data scientist",
    "current_skills": ["python programming", "basic statistics"],
    "user_id": "user123"
}
```

**Response:**
```json
{
    "matched_occupation": {
        "uri": "http://data.europa.eu/esco/occupation/...",
        "label": "data scientist",
        "description": "Analyze large data sets to extract insights...",
        "similarity_score": 0.856
    },
    "learning_path": [
        {
            "session_number": 1,
            "title": "Foundation Skills",
            "objectives": [
                "Master Python programming fundamentals",
                "Understand statistical concepts"
            ],
            "skills": [
                "Python programming",
                "Statistics",
                "Data structures"
            ],
            "estimated_duration_hours": 8,
            "difficulty_level": "beginner",
            "prerequisites": []
        }
    ],
    "skill_gap_summary": {
        "total_skills_needed": 45,
        "skills_to_learn": 35,
        "recognized_skills": ["python", "statistics"]
    }
}
```

For complete API documentation, visit `http://localhost:5000` when the server is running.

---

## 🧪 Testing

### Run Full System Test (7 Features)

```bash
python full_system_test.py
```

**Expected Output:**
```
✅ Learning Path Generation    PASSED (27.46s)
✅ Community Voting            PASSED (0.52s)
✅ Skill Suggestions           PASSED (0.31s)
✅ Quiz Generation             PASSED (28.42s)
✅ Quiz Submission             PASSED (0.08s)
✅ Feedback Statistics         PASSED (0.12s)
✅ Path Regeneration           PASSED (26.49s)

🎉 Test Success Rate: 100% (7/7)
📊 Total Duration: 106.49 seconds
```

### Run Comprehensive Evaluation (20 Test Cases)

```bash
python comprehensive_evaluation_test.py
```

**Expected Output:**
```
======================================================================
 EVALUATION SUMMARY
======================================================================
✅ Passed: 20/20 (100%)
📊 Avg Similarity: 87.53%
🎯 Avg Skills/Path: 32.8
⏱️  Total Time: 37.0 minutes
📝 Quiz Questions: 200 generated

Results saved to: evaluation_outputs_YYYYMMDD_HHMMSS/
```

---

## 📚 Documentation

- **[COMPLETE_SYSTEM_EXPLANATION.md](COMPLETE_SYSTEM_EXPLANATION.md)** - Detailed technical documentation (1,500+ lines)
- **[QUICK_START.md](QUICK_START.md)** - Quick getting started guide
- **[ADVANCED_FEATURES.md](ADVANCED_FEATURES.md)** - Advanced features documentation
- **[TROUBLESHOOTING.md](TROUBLESHOOTING.md)** - Common issues and solutions
- **[TEST_RESULTS_SUMMARY.md](TEST_RESULTS_SUMMARY.md)** - Test results analysis

---

## 🔧 Configuration

### API Keys

The system supports **dual LLM providers**. Configure in `config.py`:

| Provider | Environment Variable | Model |
|----------|---------------------|-------|
| OpenAI | `OPENAI_API_KEY` | gpt-5.2-2025-12-11 |
| Google | `GOOGLE_API_KEY` | gemini-2.5-flash |

```powershell
# Set OpenAI API key (recommended)
$env:OPENAI_API_KEY = "sk-your-key-here"

# Or set Gemini API key
$env:GOOGLE_API_KEY = "your-gemini-key"
```

### LLM Parameters

| Parameter | OpenAI GPT-5.2 | Gemini 2.5 Flash |
|-----------|----------------|------------------|
| Temperature | 0.2-0.4 | 0.2-0.4 |
| Max Tokens | 500-3000 | 500-3000 |
| Top P | 1.0 | 0.95 |
| Response Format | JSON | JSON |

### Embedding Model Configuration

Switch sentence transformer models in `ai_engine.py`:

```python
GenMentorAI(model_name='all-mpnet-base-v2')      # 768-dim, most accurate (default)
GenMentorAI(model_name='all-MiniLM-L6-v2')       # 384-dim, faster
```

---

## 📊 Similarity Metrics Explained

The system uses **7 different similarity algorithms**:

### Semantic Metrics (Embedding-based)
1. **Cosine Similarity** (76% avg) - Angle between vectors
2. **Euclidean Distance** (72% avg) - Straight-line distance
3. **Manhattan Distance** (68% avg) - L1 norm distance

### Lexical Metrics (Text-based)
4. **Jaccard Similarity** (8% avg) - Word set overlap
5. **Dice Coefficient** (14% avg) - Weighted intersection
6. **Overlap Coefficient** (39% avg) - Subset matching
7. **TF-IDF Similarity** (16% avg) - Term importance

---

## 🗂️ Project Structure

```
Cortex/
├── 📄 Core Application
│   ├── app.py                      # Flask API server
│   ├── ai_engine.py                # AI logic + FAISS RAG (1,700+ lines)
│   ├── quiz_generator.py           # LLM-powered quiz generation
│   ├── similarity_metrics.py       # 7 similarity algorithms
│   └── config.py                   # LLM provider configuration
│
├── 🗄️ Database & Data
│   ├── genmentor.db                # SQLite (99MB, 3,039 occupations)
│   ├── occupation_faiss.index      # FAISS vector index
│   └── *.csv                       # ESCO taxonomy data
│
├── 🧪 Testing
│   ├── full_system_test.py         # 7-feature test suite
│   ├── comprehensive_evaluation_test.py  # 20-case evaluation
│   └── evaluation_outputs_*/       # Test results
│
└── 📚 Documentation
    ├── README.md                   # This file
    └── COMPLETE_SYSTEM_EXPLANATION.md
```

---

## 🐛 Troubleshooting

### Common Issues

**"Module not found" errors**:
```bash
pip install -r requirements.txt
```

**"OpenAI API error" / "Gemini API error"**:
- Verify API key in `config.py` or environment variables
- Check internet connection
- Ensure API quota is not exceeded

**"max_tokens" deprecation (OpenAI)**:
- Use `max_completion_tokens` instead of `max_tokens` for OpenAI SDK v1.0+

**Slow responses**:
- Normal: 15-30 seconds (includes LLM inference time)
- Skill priority caching reduces repeated calls

For more help, see [`TROUBLESHOOTING.md`](TROUBLESHOOTING.md)

---

## 🚀 Deployment

### Production with Gunicorn
```bash
pip install gunicorn
gunicorn -w 4 -b 0.0.0.0:5000 app:app
```

---

## 🤝 Contributing

1. Fork the repository
2. Create feature branch (`git checkout -b feature/`)
3. Commit changes (`git commit -m 'Add '`)
4. Push to branch (`git push origin feature/`)
5. Open Pull Request

---

## 📜 License

MIT License - see [LICENSE](LICENSE) file

---

## 👥 Authors

**Manasvi Vedanta** - [GitHub](https://github.com/Manasvi-Vedanta)

---

## 🙏 Acknowledgments

- **ESCO** for comprehensive skills taxonomy (13,939 skills, 3,039 occupations)
- **Sentence Transformers** team for `all-mpnet-base-v2`
- **OpenAI** for GPT-5.2 API
- **Google** for Gemini 2.5 Flash API
- **FAISS** by Meta for fast vector similarity search
- **Flask** community

---

## 📞 Support

- **Issues**: [GitHub Issues](https://github.com/Manasvi-Vedanta/Hybrid-GenMentor/issues)
- **Documentation**: See `COMPLETE_SYSTEM_EXPLANATION.md`

---

<div align="center">

**Made with ❤️ by Manasvi Vedanta**

⭐ Star this repo if you find it useful!

</div>
