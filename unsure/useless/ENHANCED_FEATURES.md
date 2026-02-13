# 🚀 GenMentor Enhanced Features

## New Features Implementation

This document describes the three major enhancements added to the GenMentor system:

### 1. 🗳️ Community Feedback Loop System
### 2. 📊 Learning Path Visualization & Data Cleaning
### 3. 📚 Resource Curation System

---

## 🗳️ 1. Community Feedback Loop

**Module**: `community_feedback.py`

### Features:
- **Enhanced Voting System**: Vote on skills, occupations, sessions, and resources
- **Suggestion Management**: Propose curriculum updates with community voting
- **Curriculum Updates**: Track and implement community-approved changes
- **Resource Ratings**: Rate learning resources with quality scores
- **Community Analytics**: Track engagement metrics and trending items

### API Endpoints:

#### Vote on Items
```http
POST /api/feedback/vote
Content-Type: application/json

{
    "item_uri": "http://data.europa.eu/esco/skill/...",
    "item_type": "skill",  // 'skill', 'occupation', 'session', 'resource'
    "user_id": "user123",
    "vote": 1  // -1 (downvote), 0 (neutral), 1 (upvote)
}
```

#### Add Suggestion
```http
POST /api/feedback/suggest
Content-Type: application/json

{
    "item_uri": "http://data.europa.eu/esco/occupation/...",
    "item_type": "occupation",
    "user_id": "user123",
    "suggestion_type": "add_skill",
    "suggestion_text": "Should include TensorFlow as required skill"
}
```

#### Get Pending Suggestions
```http
GET /api/feedback/suggestions/pending?min_score=5
```

#### Vote on Suggestion
```http
POST /api/feedback/suggestions/123/vote
Content-Type: application/json

{
    "user_id": "user123",
    "vote": 1  // 1 (support), -1 (oppose)
}
```

#### Get Trending Items
```http
GET /api/feedback/trending?type=skill&days=7&limit=10
```

#### Get Community Metrics
```http
GET /api/feedback/metrics
```

### Database Tables:
- `votes` - User votes on items
- `suggestions` - Community suggestions
- `suggestion_votes` - Votes on suggestions
- `curriculum_updates` - Proposed curriculum changes
- `resource_ratings` - Resource quality ratings

---

## 📊 2. Learning Path Visualization & Data Cleaning

**Module**: `learning_path_visualizer.py`

### Features:
- **Data Cleaning**: Normalize durations, validate prerequisites, remove duplicates
- **Gantt Chart Generation**: Timeline visualization with dependencies
- **Dependency Graph**: Visual graph of skill dependencies
- **Skills Timeline**: Track when each skill is learned
- **Validation**: Ensure learning path integrity

### API Endpoints:

#### Visualize Learning Path
```http
POST /api/path/visualize
Content-Type: application/json

{
    "learning_path": [
        {
            "session_number": 1,
            "title": "Python Basics",
            "skills": ["python", "variables"],
            "estimated_duration_hours": 20,
            "difficulty_level": "beginner",
            "prerequisites": []
        }
    ]
}
```

**Response**:
```json
{
    "cleaned_path": [...],
    "gantt_data": {
        "total_duration_hours": 120,
        "total_duration_days": 15,
        "tasks": [...]
    },
    "dependency_graph": {
        "nodes": [...],
        "edges": [...],
        "metrics": {...}
    },
    "skills_timeline": {...},
    "validation": {
        "valid": true,
        "issues": []
    }
}
```

#### Get Gantt Chart HTML
```http
GET /api/path/visualize/gantt?path_data=[...]
```

Returns interactive HTML Gantt chart.

#### Get Dependency Graph HTML
```http
GET /api/path/visualize/graph?path_data=[...]
```

Returns interactive HTML dependency graph using vis.js.

### Visualization Features:

#### Gantt Chart:
- Session timelines
- Duration estimates
- Difficulty levels (color-coded)
- Prerequisite tracking
- Total duration calculations

#### Dependency Graph:
- Visual node network
- Hierarchical layout
- Color-coded difficulty
- Interactive nodes
- Complexity metrics

---

## 📚 3. Resource Curation System

**Module**: `resource_curator.py`

### Features:
- **Multi-Source Search**: GitHub, YouTube, Medium, Official Docs
- **Resource Management**: Add, validate, and rate resources
- **Quality Scoring**: Community ratings and validation
- **Automated Curation**: Attach resources to learning paths
- **Access Tracking**: Monitor resource usage and completion

### API Endpoints:

#### Search Resources
```http
GET /api/resources/search?skill=python+programming&limit=10
```

#### Add Resource
```http
POST /api/resources/add
Content-Type: application/json

{
    "skill_uri": "http://data.europa.eu/esco/skill/...",
    "resource_url": "https://docs.python.org/3/tutorial/",
    "resource_title": "Python Tutorial",
    "resource_type": "documentation",  // 'course', 'tutorial', 'documentation', 'video', 'article', 'book'
    "provider": "Python.org",
    "description": "Official Python tutorial",
    "difficulty_level": "beginner",
    "is_free": true,
    "estimated_duration": "10 hours"
}
```

#### Get Resources for Skill
```http
GET /api/resources/skill/http%3A%2F%2Fdata.europa.eu%2Fesco%2Fskill%2F...
    ?difficulty=beginner
    &min_quality=5.0
    &validated_only=true
```

#### Rate Resource
```http
POST /api/resources/rate
Content-Type: application/json

{
    "resource_url": "https://docs.python.org/3/tutorial/",
    "skill_uri": "http://data.europa.eu/esco/skill/...",
    "user_id": "user123",
    "rating": 5,  // 1-5 stars
    "quality_score": 9,  // 1-10
    "review_text": "Excellent tutorial for beginners"
}
```

#### Get Popular Resources
```http
GET /api/resources/popular?days=30&limit=10
```

#### Generate Path with Resources
```http
POST /api/path/with-resources
Content-Type: application/json

{
    "goal": "I want to become a data scientist",
    "current_skills": ["python", "statistics"],
    "user_id": "user123"
}
```

**Response**: Complete learning path with curated resources for each session.

### Database Tables:
- `learning_resources` - Curated learning resources
- `resource_tags` - Resource categorization
- `resource_access_stats` - Usage tracking
- `resource_ratings` - Community ratings (inherited from feedback system)

---

## 🔧 Installation

1. **Ensure all dependencies are installed**:
```bash
pip install networkx vis-network requests beautifulsoup4
```

2. **Initialize the database tables**:
```python
from community_feedback import CommunityFeedbackSystem
from resource_curator import ResourceCurator

# Initialize systems (creates tables automatically)
feedback = CommunityFeedbackSystem()
curator = ResourceCurator()
```

3. **Run the enhanced API server**:
```bash
python app.py
```

---

## 📖 Usage Examples

### Example 1: Generate Complete Learning Path with Visualizations

```python
import requests
import json

# Generate path with resources
response = requests.post('http://localhost:5000/api/path/with-resources', 
    json={
        "goal": "Become a full-stack developer",
        "current_skills": ["HTML", "CSS"],
        "user_id": "user123"
    }
)

result = response.json()

# Save visualization files
from learning_path_visualizer import LearningPathVisualizer

visualizer = LearningPathVisualizer()
files = visualizer.save_visualizations(result['learning_path'])

print(f"Gantt chart: {files['gantt_chart']}")
print(f"Dependency graph: {files['dependency_graph']}")
```

### Example 2: Community Feedback Workflow

```python
import requests

# Vote on a skill
requests.post('http://localhost:5000/api/feedback/vote',
    json={
        "item_uri": "http://data.europa.eu/esco/skill/python",
        "item_type": "skill",
        "user_id": "user123",
        "vote": 1
    }
)

# Add suggestion
requests.post('http://localhost:5000/api/feedback/suggest',
    json={
        "item_uri": "http://data.europa.eu/esco/occupation/data-scientist",
        "item_type": "occupation",
        "user_id": "user123",
        "suggestion_type": "add_skill",
        "suggestion_text": "Should include Docker for deployment"
    }
)

# Check community metrics
response = requests.get('http://localhost:5000/api/feedback/metrics')
print(response.json())
```

### Example 3: Resource Curation

```python
import requests

# Search for resources
response = requests.get('http://localhost:5000/api/resources/search',
    params={'skill': 'machine learning', 'limit': 5}
)

resources = response.json()['resources']

# Rate a resource
requests.post('http://localhost:5000/api/resources/rate',
    json={
        "resource_url": resources[0]['url'],
        "skill_uri": "http://data.europa.eu/esco/skill/ml",
        "user_id": "user123",
        "rating": 5,
        "quality_score": 9,
        "review_text": "Excellent resource!"
    }
)
```

---

## 🎨 Visualization Examples

### Gantt Chart Features:
- Color-coded by difficulty level
- Session timelines with dates
- Prerequisite indicators
- Total duration summary
- Interactive HTML output

### Dependency Graph Features:
- Hierarchical layout
- Node colors by difficulty
- Directed edges for dependencies
- Interactive node information
- Complexity metrics

---

## 📊 Community Metrics

The system tracks:
- **Total Votes**: All votes across all items
- **Total Suggestions**: Community-submitted suggestions
- **Pending Suggestions**: Awaiting review
- **Active Users**: Users active in last 30 days
- **Resource Ratings**: Quality scores from community
- **Trending Items**: Most voted items in recent period

---

## 🔐 Security Considerations

- User IDs should be properly authenticated in production
- Implement rate limiting for voting/suggestions
- Validate all user inputs
- Use HTTPS in production
- Implement CORS properly for web clients

---

## 🚀 Future Enhancements

1. **ML-based Resource Recommendations**: Personalized resource suggestions
2. **Automated Quality Assessment**: AI-driven resource validation
3. **Gamification**: Badges and points for community contributions
4. **Export Options**: PDF, PNG exports of visualizations
5. **Real-time Collaboration**: Live learning path editing
6. **Mobile App Integration**: Native mobile clients

---

## 📝 API Summary

### Community Feedback (7 endpoints):
- POST `/api/feedback/vote`
- POST `/api/feedback/suggest`
- GET `/api/feedback/suggestions/pending`
- POST `/api/feedback/suggestions/:id/vote`
- GET `/api/feedback/trending`
- GET `/api/feedback/metrics`

### Visualization (3 endpoints):
- POST `/api/path/visualize`
- GET `/api/path/visualize/gantt`
- GET `/api/path/visualize/graph`

### Resource Curation (6 endpoints):
- GET `/api/resources/search`
- POST `/api/resources/add`
- GET `/api/resources/skill/:uri`
- POST `/api/resources/rate`
- GET `/api/resources/popular`
- POST `/api/path/with-resources`

**Total: 16 new API endpoints**

---

## 🐛 Troubleshooting

### Issue: "Feature not available" error
**Solution**: Ensure all modules are imported correctly:
```python
from community_feedback import CommunityFeedbackSystem
from learning_path_visualizer import LearningPathVisualizer
from resource_curator import ResourceCurator
```

### Issue: Database tables not created
**Solution**: Initialize systems manually:
```python
feedback = CommunityFeedbackSystem()  # Creates tables
curator = ResourceCurator()  # Creates tables
```

### Issue: Visualization not rendering
**Solution**: Check that vis.js CDN is accessible and browser supports ES6.

---

## 📞 Support

For issues or questions:
1. Check the main `COMPLETE_SYSTEM_EXPLANATION.md`
2. Review API documentation at `http://localhost:5000`
3. Check database schema in respective modules

---

**Made with ❤️ for GenMentor Enhanced Features**
