# 🎓 GenMentor - AI-Powered Career Guidance System

[![Python](https://img.shields.io/badge/Python-3.8%2B-blue.svg)](https://www.python.org/)
[![Flask](https://img.shields.io/badge/Flask-2.0%2B-green.svg)](https://flask.palletsprojects.com/)
[![License](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)
[![Status](https://img.shields.io/badge/Status-Production-success.svg)](https://github.com/Manasvi-Vedanta/Hybrid-GenMentor)

> An intelligent career guidance platform that uses advanced NLP and AI to generate personalized learning paths based on your career goals and current skills.

---

## 🌟 Features

### Core Capabilities
- 🎯 **Smart Career Matching**: Match user goals to 3,039+ occupations using semantic understanding
- 📚 **Personalized Learning Paths**: Generate structured learning plans with 13,939+ skills
- 🧠 **Multiple Similarity Metrics**: 7 different algorithms for robust career matching
- 🤖 **AI-Powered Content**: Intelligent content generation using Google Gemini 2.5 Pro
- 📊 **Skill Gap Analysis**: Identify exactly what skills you need to learn
- 🔄 **Dependency-Based Scheduling**: Learn skills in the optimal order
- 💬 **User Feedback System**: Vote and suggest improvements to learning paths
- 📈 **Performance Tracking**: Comprehensive testing and validation

### Advanced Features
- **Semantic Embeddings**: 768-dimensional vectors using all-mpnet-base-v2
- **Graph-Based Scheduling**: NetworkX for skill dependency resolution
- **Multi-Strategy Matching**: Exact, partial, and semantic keyword matching
- **Dynamic Boost Factors**: Domain-specific, keyword density, and career transition boosting
- **LLM Integration**: Real-time session creation with Gemini 2.5 Pro
- **RESTful API**: Clean JSON endpoints for easy integration

---

## 📊 System Performance

Based on comprehensive testing (15 test cases):

| Metric | Value |
|--------|-------|
| **Success Rate** | 93.3% (14/15 passed) |
| **Average Similarity Score** | 76.0% |
| **Average Response Time** | 22.91 seconds |
| **Timeout Rate** | 0% |
| **Semantic Similarity (Cosine)** | 76.0% average |
| **Weighted Average (7 metrics)** | 51.0% average |

---

## 🏗️ Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                        User Request                          │
└──────────────────────┬──────────────────────────────────────┘
                       │
                       ▼
┌─────────────────────────────────────────────────────────────┐
│                     Flask API Server                         │
│  • /api/health  • /api/path  • /api/content  • /api/vote   │
└──────────────────────┬──────────────────────────────────────┘
                       │
                       ▼
┌─────────────────────────────────────────────────────────────┐
│                      AI Engine Core                          │
│  ┌──────────────────────────────────────────────────────┐  │
│  │  1. Goal Embedding (768-dim vectors)                 │  │
│  │  2. Occupation Matching (3,039 careers)              │  │
│  │  3. Similarity Calculation (7 algorithms)            │  │
│  │  4. Skill Gap Analysis (13,939 skills)               │  │
│  │  5. Dependency Graph (NetworkX)                      │  │
│  │  6. LLM Session Creation (Gemini 2.5 Pro)            │  │
│  └──────────────────────────────────────────────────────┘  │
└──────────────────────┬──────────────────────────────────────┘
                       │
                       ▼
┌─────────────────────────────────────────────────────────────┐
│                  SQLite Database (ESCO)                      │
│  • 3,039 Occupations  • 13,939 Skills  • 134,895 Relations │
└─────────────────────────────────────────────────────────────┘
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
git clone https://github.com/Manasvi-Vedanta/Cortex.git
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

4. **Verify installation**
```bash
python -c "import flask, sentence_transformers, google.generativeai; print('✅ All dependencies installed!')"
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
✅ Gemini 2.5 Pro API configured successfully!
✅ Advanced similarity metrics initialized
Loaded 3039 occupation embeddings
 * Running on http://127.0.0.1:5000
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
    "message": "GenMentor API is running",
    "model": "all-mpnet-base-v2",
    "embedding_dimension": 768,
    "llm_available": true
}
```

### 2. Generate Learning Path
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

### Run Comprehensive Test Suite

```bash
python comprehensive_test_suite.py
```

This will run:
- **10 main test cases** (various career goals)
- **5 edge cases** (empty skills, vague goals, special characters)
- **5 performance tests** (response time benchmarking)

**Expected Output:**
```
======================================================================
 TEST SUITE SUMMARY
======================================================================
✅ Passed: 14
❌ Failed: 0
⚠️  Warnings: 1
📊 Success Rate: 93.3%
🎯 Avg Similarity: 76.0%
⏱️  Avg Response Time: 22.91s
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

The system requires a Google Gemini API key. You can:

1. **Use the default key** (already configured in `config.py`)
2. **Set your own key** as an environment variable:
   ```powershell
   $env:GOOGLE_API_KEY = "your-api-key-here"
   ```

### Model Configuration

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
Hybrid-GenMentor/
├── 📄 Core Application
│   ├── app.py                      # Flask API server (449 lines)
│   ├── ai_engine.py                # AI logic (1,713 lines)
│   ├── similarity_metrics.py       # 7 algorithms (262 lines)
│   └── config.py                   # Configuration
│
├── 🗄️ Database & Data
│   ├── genmentor.db                # SQLite (151,895 records)
│   ├── occupation_embeddings_all-mpnet-base-v2.pkl
│   └── *.csv                       # ESCO data files
│
├── 🧪 Testing
│   ├── comprehensive_test_suite.py # Test suite (589 lines)
│   └── test_results_*.json         # Test outputs
│
└── 📚 Documentation
    ├── README.md                   # This file
    ├── COMPLETE_SYSTEM_EXPLANATION.md
    └── *.md                        # Other docs
```

---

## 🐛 Troubleshooting

### Common Issues

**"Module not found" errors**:
```bash
pip install -r requirements.txt
```

**"Gemini API error"**:
- Check API key in `config.py`
- Verify internet connection

**Slow responses**:
- Normal: 15-25 seconds
- Reduce skill limit in `app.py` for faster responses

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

- **ESCO** for skills taxonomy
- **Sentence Transformers** team
- **Google** for Gemini 2.5 Pro API
- **Flask** community

---

## 📞 Support

- **Issues**: [GitHub Issues](https://github.com/Manasvi-Vedanta/Cortex/issues)
- **Documentation**: See `COMPLETE_SYSTEM_EXPLANATION.md`

---

<div align="center">

**Made with ❤️ by Manasvi Vedanta**

⭐ Star this repo if you find it useful!

</div>
