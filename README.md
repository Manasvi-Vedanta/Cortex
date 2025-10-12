# Cortex: AI-Powered Career Guidance System

Cortex is an intelligent career guidance system that combines AI-powered recommendations with community feedback to create personalized learning paths. Built on the ESCO (European Skills, Competences and Occupations) framework, it helps users identify skill gaps and provides structured learning plans to achieve their career goals.

## Features

- **🎯 Goal-to-Occupation Matching**: Uses semantic similarity to match user career goals with relevant occupations
- **📚 Skill Gap Analysis**: Identifies missing skills based on occupation requirements and user's current abilities
- **🛤️ Learning Path Generation**: Creates structured, dependency-aware learning paths with topological sorting
- **🤖 AI-Powered Content Creation**: Generates personalized learning materials using RAG (Retrieval-Augmented Generation)
- **👥 Community Feedback**: Incorporates user votes and suggestions to improve recommendation quality
- **🔄 Adaptive Learning**: System learns from feedback to improve future recommendations
- **🔍 Explainable AI**: Provides clear explanations for why skills are recommended

## Architecture

The system follows a hybrid approach combining:
- **ESCO Data Processing**: Structured occupation and skill data
- **Semantic Search**: Sentence transformers for goal-occupation matching
- **Graph Analysis**: NetworkX for dependency resolution
- **LLM Integration**: Google Gemini for content generation and path refinement
- **Community Intelligence**: Crowdsourced feedback for continuous improvement

## Installation

### Prerequisites

- Python 3.8+
- pip package manager

### Setup

1. **Clone the repository:**
   ```bash
   git clone <repository-url>
   cd Hybrid-Cortex
   ```

2. **Install dependencies:**
   ```bash
   pip install pandas Flask sentence-transformers networkx google-generativeai openai google-api-python-client beautifulsoup4 requests tf-keras
   ```

3. **Set up the database:**
   ```bash
   python setup_database.py
   ```
   This will create `Cortex.db` and populate it with ESCO data from the CSV files.

4. **Configure API keys (optional but recommended):**
   - Get a Google API key for Gemini
   - Set it in the AI engine initialization or as an environment variable

## Usage

### Starting the API Server

```bash
python app.py
```

The server will start on `http://localhost:5000` with API documentation available at the root URL.

### API Endpoints

#### Generate Learning Path
```bash
POST /api/path
Content-Type: application/json

{
    "goal": "I want to become a data scientist",
    "current_skills": ["python programming", "basic statistics"],
    "user_id": "user123"
}
```

#### Generate Learning Content
```bash
GET /api/content?topic=machine learning&level=beginner
```

#### Submit Feedback
```bash
POST /api/vote
Content-Type: application/json

{
    "item_uri": "http://data.europa.eu/esco/skill/...",
    "user_id": "user123",
    "vote": 1
}
```

#### Search Occupations/Skills
```bash
GET /api/occupations/search?q=data&limit=10
GET /api/skills/search?q=python&limit=10
```

### Testing the System

Run the test client to verify all endpoints:

```bash
python test_client.py
```

## Database Schema

The system uses SQLite with the following main tables:

- **occupations**: ESCO occupation data
- **skills**: ESCO skill data with relevance scores
- **occupation_skill_relations**: Links between occupations and required skills
- **skill_skill_relations**: Dependencies between skills
- **votes**: Community feedback on skills/topics
- **suggestions**: User suggestions for improvements

## AI Components

### 1. Skill Identifier (`identify_skill_gap`)
- Uses sentence transformers to match goals to occupations
- Retrieves required skills from ESCO database
- Calculates skill gaps by comparing with user's current skills

### 2. Path Scheduler (`schedule_learning_path`)
- Builds dependency graphs using NetworkX
- Performs topological sorting for optimal learning order
- Integrates community feedback for prioritization
- Uses LLM for human-friendly session organization

### 3. Content Creator (`create_learning_content`)
- Implements RAG (Retrieval-Augmented Generation)
- Searches for relevant content sources
- Generates personalized learning materials
- Adapts content to user experience level

### 4. Feedback Analyzer (`analyze_feedback`)
- Processes community votes and suggestions
- Updates skill relevance scores based on feedback
- Implements adaptive learning mechanisms

## Project Structure

```
Hybrid-Cortex/
├── setup_database.py      # Database initialization
├── ai_engine.py          # Core AI functionality
├── app.py               # Flask API server
├── test_client.py       # API testing client
├── Cortex.db         # SQLite database (created after setup)
├── occupation_embeddings.pkl  # Cached embeddings (created after first run)
├── occupations_en.csv   # ESCO occupation data
├── skills_en.csv        # ESCO skill data
├── occupationSkillRelations_en.csv  # Occupation-skill mappings
├── skillSkillRelations_en.csv       # Skill dependencies
└── README.md           # This file
```

## Development Phases

The project was developed following a structured approach:

### Phase 0: Foundation & Setup ✅
- Installed essential Python libraries
- Set up development environment

### Phase 1: Building the ESCO Data Core ✅
- Created SQLite database schema
- Ingested ESCO CSV data
- Implemented efficient indexing

### Phase 2: Implementing the Cortex AI Engine ✅
- Built skill identifier with semantic matching
- Created path scheduler with dependency resolution
- Implemented RAG-based content creator

### Phase 3: Integrating Hybrid Human Feedback ✅
- Extended database for votes and suggestions
- Created feedback collection functions
- Implemented adaptive learning mechanisms

### Phase 4: Algorithmic Improvements ✅
- Added explainable AI features
- Implemented relevance score decay system
- Enhanced recommendation quality

### Phase 5: API Server Integration ✅
- Built Flask web API
- Created comprehensive endpoint documentation
- Implemented error handling and validation

## Configuration

### Environment Variables (Optional)
- `GOOGLE_API_KEY`: For Gemini LLM integration
- `SEARCH_API_KEY`: For web search functionality

### Performance Tuning
- Embedding computation: ~20 seconds for 3,000+ occupations
- Database queries: Optimized with indexes
- Memory usage: ~200MB for full embedding cache

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests if applicable
5. Submit a pull request

## Future Enhancements

- [ ] Real-time learning progress tracking
- [ ] Integration with external learning platforms
- [ ] Advanced NLP for better goal understanding
- [ ] Mobile application interface
- [ ] Multi-language support
- [ ] Integration with job market data
- [ ] Machine learning model for success prediction

## License

This project is part of academic research. Please refer to the institution's policies for usage rights.

## Acknowledgments

- **ESCO Framework**: European Skills, Competences and Occupations taxonomy
- **Sentence Transformers**: For semantic similarity computation
- **NetworkX**: For graph-based dependency analysis
- **Google Gemini**: For advanced language model capabilities

---

**Cortex**: *Guiding careers through intelligent learning paths*
