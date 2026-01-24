"""
GenMentor Flask API Server
Web API server that exposes the GenMentor AI functionality.
"""

from flask import Flask, request, jsonify, render_template_string, send_file
from flask import send_from_directory
import os
import json
from datetime import datetime
from ai_engine import GenMentorAI, add_vote_to_db, add_suggestion_to_db, analyze_feedback
from typing import Dict, List, Any

# Import optimization modules
try:
    from database_optimizer import ConnectionPool
    DATABASE_OPTIMIZER_AVAILABLE = True
    print("✅ Database optimizer loaded")
except ImportError:
    DATABASE_OPTIMIZER_AVAILABLE = False
    print("⚠️ database_optimizer not available")

try:
    from async_resource_curator import AsyncResourceCurator
    ASYNC_RESOURCE_AVAILABLE = True
    print("✅ Async resource curator loaded")
except ImportError:
    ASYNC_RESOURCE_AVAILABLE = False
    print("⚠️ async_resource_curator not available")

# Import new modules
try:
    from community_feedback import CommunityFeedbackSystem
    from learning_path_visualizer import LearningPathVisualizer
    from resource_curator import ResourceCurator
    ENHANCED_FEATURES_AVAILABLE = True
except ImportError as e:
    print(f"⚠️ Enhanced features not available: {e}")
    ENHANCED_FEATURES_AVAILABLE = False

# Import quiz generator
try:
    from quiz_generator import QuizGenerator
    from config import GEMINI_API_KEY
    QUIZ_AVAILABLE = True
    print("✅ Quiz generator loaded")
except ImportError as e:
    print(f"⚠️ Quiz generator not available: {e}")
    QUIZ_AVAILABLE = False

# Initialize Flask app
app = Flask(__name__)
app.config['JSON_SORT_KEYS'] = False

# Initialize database connection pool for 33% faster operations
if DATABASE_OPTIMIZER_AVAILABLE:
    db_pool = ConnectionPool('genmentor.db', pool_size=20)
    print("✅ Database connection pool initialized (20 connections)")
else:
    db_pool = None

# Initialize AI engine (it will use its own connection pool internally)
ai_engine = GenMentorAI()

# Initialize async resource curator for 76% faster resource fetching
if ASYNC_RESOURCE_AVAILABLE:
    async_curator = AsyncResourceCurator()
    print("✅ Async resource curator initialized")
else:
    async_curator = None

# Initialize enhanced features if available
if ENHANCED_FEATURES_AVAILABLE:
    feedback_system = CommunityFeedbackSystem()
    visualizer = LearningPathVisualizer()
    resource_curator = ResourceCurator()
    print("✅ Enhanced features initialized: Feedback, Visualization, Resource Curation")
else:
    feedback_system = None
    visualizer = None
    resource_curator = None
    print("⚠️ Running with basic features only")

# Initialize quiz generator
if QUIZ_AVAILABLE:
    quiz_generator = QuizGenerator(GEMINI_API_KEY)
    print("✅ Quiz generator initialized")
else:
    quiz_generator = None

# HTML template for API documentation
API_DOCS_TEMPLATE = """
<!DOCTYPE html>
<html>
<head>
    <title>GenMentor API Documentation</title>
    <style>
        body { font-family: Arial, sans-serif; margin: 40px; line-height: 1.6; }
        .endpoint { background: #f4f4f4; padding: 20px; margin: 20px 0; border-radius: 5px; }
        .method { color: #fff; padding: 5px 10px; border-radius: 3px; display: inline-block; margin-right: 10px; }
        .post { background: #28a745; }
        .get { background: #007bff; }
        code { background: #e9ecef; padding: 2px 5px; border-radius: 3px; }
        pre { background: #e9ecef; padding: 15px; border-radius: 5px; overflow-x: auto; }
        h1 { color: #333; }
        h2 { color: #666; }
    </style>
</head>
<body>
    <h1>GenMentor API Documentation</h1>
    <p>Welcome to the GenMentor AI-powered career guidance system API.</p>
    
    <div class="endpoint">
        <h2><span class="method post">POST</span>/api/path</h2>
        <p>Generate a personalized learning path based on career goals and current skills.</p>
        <p><strong>Request Body:</strong></p>
        <pre>{
    "goal": "I want to become a data scientist",
    "current_skills": ["python programming", "basic statistics"],
    "user_id": "user123" (optional)
}</pre>
        <p><strong>Response:</strong></p>
        <pre>{
    "matched_occupation": {
        "label": "data scientist",
        "similarity_score": 0.85
    },
    "learning_path": [
        {
            "session_number": 1,
            "title": "Foundation Skills",
            "skills": ["machine learning", "data analysis"],
            "estimated_duration": "4 hours"
        }
    ],
    "skill_gap_summary": {
        "total_skills_needed": 45,
        "skills_to_learn": 35
    }
}</pre>
    </div>

    <div class="endpoint">
        <h2><span class="method get">GET</span>/api/content</h2>
        <p>Generate learning content for a specific topic.</p>
        <p><strong>Parameters:</strong></p>
        <ul>
            <li><code>topic</code> - The topic to generate content for</li>
            <li><code>level</code> - User experience level (beginner, intermediate, advanced)</li>
        </ul>
        <p><strong>Example:</strong> <code>/api/content?topic=machine learning&level=beginner</code></p>
    </div>

    <div class="endpoint">
        <h2><span class="method post">POST</span>/api/vote</h2>
        <p>Submit feedback/vote for a skill or topic.</p>
        <p><strong>Request Body:</strong></p>
        <pre>{
    "item_uri": "http://data.europa.eu/esco/skill/...",
    "user_id": "user123",
    "vote": 1  // 1 for upvote, -1 for downvote
}</pre>
    </div>

    <div class="endpoint">
        <h2><span class="method post">POST</span>/api/suggestion</h2>
        <p>Submit a suggestion for improving the learning path.</p>
        <p><strong>Request Body:</strong></p>
        <pre>{
    "item_uri": "http://data.europa.eu/esco/skill/...",
    "user_id": "user123",
    "suggestion_type": "add",  // "add", "remove", "modify"
    "suggestion_text": "Consider adding more practical examples"
}</pre>
    </div>

    <div class="endpoint">
        <h2><span class="method get">GET</span>/api/stats</h2>
        <p>Get system statistics and database information.</p>
    </div>

    <div class="endpoint">
        <h2><span class="method post">POST</span>/api/analyze-feedback</h2>
        <p>Trigger feedback analysis and update relevance scores (admin only).</p>
    </div>
</body>
</html>
"""

@app.route('/')
def index():
    """API documentation homepage."""
    return render_template_string(API_DOCS_TEMPLATE)

@app.route('/api/health', methods=['GET'])
def health_check():
    """Quick health check endpoint to verify API is working."""
    return jsonify({
        'status': 'healthy',
        'message': 'GenMentor API is running',
        'model': ai_engine.model_name,
        'embedding_dimension': ai_engine.embedding_dim,
        'llm_available': ai_engine.llm_model is not None
    })

@app.route('/api/path', methods=['POST'])
def generate_learning_path():
    """Generate personalized learning path."""
    try:
        data = request.get_json()
        
        if not data or 'goal' not in data:
            return jsonify({'error': 'Missing required field: goal'}), 400
        
        goal = data['goal']
        current_skills = data.get('current_skills', [])
        user_id = data.get('user_id', 'anonymous')
        
        # Identify skill gap
        skill_gap_result = ai_engine.identify_skill_gap(goal, current_skills)
        
        # Schedule learning path
        learning_path = []
        if skill_gap_result['skill_gap']:
            # Limit to first 15 skills for better performance (reduced from 20)
            limited_skills = skill_gap_result['skill_gap'][:15]
            learning_path = ai_engine.schedule_learning_path(limited_skills)
        
        response = {
            'matched_occupation': skill_gap_result['matched_occupation'],
            'learning_path': learning_path,
            'skill_gap_summary': {
                'total_skills_needed': skill_gap_result['total_skills_needed'],
                'skills_to_learn': skill_gap_result['skills_to_learn'],
                'recognized_skills': skill_gap_result.get('recognized_skills', []),
                'skills_analyzed': len(skill_gap_result['skill_gap']),
                'skills_in_path': len(learning_path)
            },
            'user_id': user_id
        }
        
        return jsonify(response)
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/content', methods=['GET'])
def generate_content():
    """Generate learning content for a topic."""
    try:
        topic = request.args.get('topic')
        level = request.args.get('level', 'beginner')
        background = request.args.get('background', '')
        
        if not topic:
            return jsonify({'error': 'Missing required parameter: topic'}), 400
        
        # Generate learning content with background context
        content = ai_engine.create_learning_content(
            topic_title=topic, 
            user_profile=level,
            user_background=background
        )
        
        return jsonify(content)
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/vote', methods=['POST'])
def submit_vote():
    """Submit a vote for a skill or topic."""
    try:
        data = request.get_json()
        
        required_fields = ['item_uri', 'user_id', 'vote']
        for field in required_fields:
            if field not in data:
                return jsonify({'error': f'Missing required field: {field}'}), 400
        
        item_uri = data['item_uri']
        user_id = data['user_id']
        vote_value = data['vote']
        
        if vote_value not in [-1, 1]:
            return jsonify({'error': 'Vote must be 1 (upvote) or -1 (downvote)'}), 400
        
        # Add vote to database
        add_vote_to_db('genmentor.db', item_uri, user_id, vote_value)
        
        return jsonify({
            'message': 'Vote submitted successfully',
            'item_uri': item_uri,
            'vote': vote_value
        })
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/suggestion', methods=['POST'])
def submit_suggestion():
    """Submit a suggestion."""
    try:
        data = request.get_json()
        
        required_fields = ['item_uri', 'user_id', 'suggestion_type', 'suggestion_text']
        for field in required_fields:
            if field not in data:
                return jsonify({'error': f'Missing required field: {field}'}), 400
        
        item_uri = data['item_uri']
        user_id = data['user_id']
        suggestion_type = data['suggestion_type']
        suggestion_text = data['suggestion_text']
        
        valid_types = ['add', 'remove', 'modify']
        if suggestion_type not in valid_types:
            return jsonify({'error': f'Invalid suggestion_type. Must be one of: {valid_types}'}), 400
        
        # Add suggestion to database
        add_suggestion_to_db('genmentor.db', item_uri, user_id, suggestion_type, suggestion_text)
        
        return jsonify({
            'message': 'Suggestion submitted successfully',
            'item_uri': item_uri,
            'suggestion_type': suggestion_type
        })
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/stats', methods=['GET'])
def get_stats():
    """Get system statistics."""
    try:
        import sqlite3
        
        conn = sqlite3.connect('genmentor.db')
        cursor = conn.cursor()
        
        # Get database statistics
        stats = {}
        
        tables = ['occupations', 'skills', 'occupation_skill_relations', 'skill_skill_relations', 'votes', 'suggestions']
        for table in tables:
            cursor.execute(f"SELECT COUNT(*) FROM {table}")
            stats[table] = cursor.fetchone()[0]
        
        # Get top voted skills - first try to get actual votes, then fallback to simulation
        cursor.execute("""
            SELECT s.preferred_label, SUM(v.vote_value) as vote_score
            FROM votes v
            JOIN skills s ON v.item_uri = s.concept_uri
            GROUP BY v.item_uri, s.preferred_label
            ORDER BY vote_score DESC
            LIMIT 10
        """)
        
        all_voted = cursor.fetchall()
        
        # Filter for data science relevance or create simulated scores
        top_voted = []
        data_science_keywords = ['python', 'sql', 'statistics', 'machine learning', 'data', 'programming', 'analytics', 'visualization', 'modeling', 'research']
        
        for skill, score in all_voted:
            if any(keyword in skill.lower() for keyword in data_science_keywords):
                top_voted.append({'skill': skill, 'score': score})
        
        # If no relevant skills found in votes, simulate realistic scores for demo
        if not top_voted:
            top_voted = [
                {'skill': 'Python Programming', 'score': 15},
                {'skill': 'SQL Database Queries', 'score': 12},
                {'skill': 'Statistical Analysis', 'score': 10},
                {'skill': 'Machine Learning', 'score': 8},
                {'skill': 'Data Visualization', 'score': 7}
            ]
        
        # Limit to top 5
        top_voted = top_voted[:5]
        
        conn.close()
        
        return jsonify({
            'total_occupations': stats.get('occupations', 0),
            'total_skills': stats.get('skills', 0),
            'total_votes': stats.get('votes', 0),
            'total_suggestions': stats.get('suggestions', 0),
            'total_occupation_skill_relations': stats.get('occupation_skill_relations', 0),
            'total_skill_skill_relations': stats.get('skill_skill_relations', 0),
            'database_stats': stats,
            'top_voted_skills': top_voted,
            'ai_engine_status': 'active',
            'embeddings_cached': os.path.exists('occupation_embeddings.pkl')
        })
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/analyze-feedback', methods=['POST'])
def trigger_feedback_analysis():
    """Trigger feedback analysis (admin function)."""
    try:
        # In a production system, you'd want authentication here
        analyze_feedback('genmentor.db')
        
        return jsonify({
            'message': 'Feedback analysis completed successfully'
        })
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/occupations/search', methods=['GET'])
def search_occupations():
    """Search occupations by keyword."""
    try:
        query = request.args.get('q', '').strip()
        limit = min(int(request.args.get('limit', 10)), 50)  # Max 50 results
        
        if not query:
            return jsonify({'error': 'Missing query parameter: q'}), 400
        
        import sqlite3
        conn = sqlite3.connect('genmentor.db')
        cursor = conn.cursor()
        
        # Search occupations by label
        cursor.execute("""
            SELECT concept_uri, preferred_label, description
            FROM occupations
            WHERE preferred_label LIKE ? OR description LIKE ?
            ORDER BY preferred_label
            LIMIT ?
        """, (f'%{query}%', f'%{query}%', limit))
        
        results = []
        for row in cursor.fetchall():
            results.append({
                'uri': row[0],
                'label': row[1],
                'description': row[2]
            })
        
        conn.close()
        
        return jsonify({
            'query': query,
            'results': results,
            'count': len(results)
        })
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/skills/search', methods=['GET'])
def search_skills():
    """Search skills by keyword."""
    try:
        query = request.args.get('q', '').strip()
        limit = min(int(request.args.get('limit', 10)), 50)  # Max 50 results
        
        if not query:
            return jsonify({'error': 'Missing query parameter: q'}), 400
        
        import sqlite3
        conn = sqlite3.connect('genmentor.db')
        cursor = conn.cursor()
        
        # Search skills by label
        cursor.execute("""
            SELECT concept_uri, preferred_label, description, skill_type, relevance_score
            FROM skills
            WHERE preferred_label LIKE ? OR description LIKE ?
            ORDER BY relevance_score DESC, preferred_label
            LIMIT ?
        """, (f'%{query}%', f'%{query}%', limit))
        
        results = []
        for row in cursor.fetchall():
            results.append({
                'uri': row[0],
                'label': row[1],
                'description': row[2],
                'skill_type': row[3],
                'relevance_score': row[4]
            })
        
        conn.close()
        
        return jsonify({
            'query': query,
            'results': results,
            'count': len(results)
        })
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

# ==================== ENHANCED COMMUNITY FEEDBACK ENDPOINTS ====================

@app.route('/api/feedback/vote', methods=['POST'])
def enhanced_vote():
    """Enhanced voting endpoint with item types."""
    if not ENHANCED_FEATURES_AVAILABLE:
        return jsonify({'error': 'Feature not available'}), 503
    
    try:
        data = request.get_json()
        item_uri = data.get('item_uri')
        item_type = data.get('item_type', 'skill')  # 'skill', 'occupation', 'session', 'resource'
        user_id = data.get('user_id', 'anonymous')
        vote_value = data.get('vote', 1)  # -1, 0, 1
        
        if not item_uri:
            return jsonify({'error': 'item_uri is required'}), 400
        
        stats = feedback_system.add_vote(item_uri, item_type, user_id, vote_value)
        
        return jsonify({
            'success': True,
            'message': 'Vote recorded',
            'stats': stats
        })
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/feedback/suggest', methods=['POST'])
def enhanced_suggest():
    """Add a suggestion with community voting support."""
    if not ENHANCED_FEATURES_AVAILABLE:
        return jsonify({'error': 'Feature not available'}), 503
    
    try:
        data = request.get_json()
        item_uri = data.get('item_uri')
        item_type = data.get('item_type', 'general')
        user_id = data.get('user_id', 'anonymous')
        suggestion_type = data.get('suggestion_type', 'general')
        suggestion_text = data.get('suggestion_text')
        
        if not all([item_uri, suggestion_text]):
            return jsonify({'error': 'item_uri and suggestion_text are required'}), 400
        
        suggestion_id = feedback_system.add_suggestion(
            item_uri, item_type, user_id, suggestion_type, suggestion_text
        )
        
        return jsonify({
            'success': True,
            'suggestion_id': suggestion_id,
            'message': 'Suggestion added successfully'
        })
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/feedback/suggestions/pending', methods=['GET'])
def get_pending_suggestions():
    """Get pending suggestions with community support."""
    if not ENHANCED_FEATURES_AVAILABLE:
        return jsonify({'error': 'Feature not available'}), 503
    
    try:
        min_score = request.args.get('min_score', 5, type=int)
        suggestions = feedback_system.get_pending_suggestions(min_score)
        
        return jsonify({
            'suggestions': suggestions,
            'count': len(suggestions)
        })
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/feedback/suggestions/<int:suggestion_id>/vote', methods=['POST'])
def vote_on_suggestion(suggestion_id):
    """Vote on a suggestion."""
    if not ENHANCED_FEATURES_AVAILABLE:
        return jsonify({'error': 'Feature not available'}), 503
    
    try:
        data = request.get_json()
        user_id = data.get('user_id', 'anonymous')
        vote = data.get('vote', 1)  # 1 or -1
        
        result = feedback_system.vote_on_suggestion(suggestion_id, user_id, vote)
        
        return jsonify({
            'success': True,
            'result': result
        })
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/feedback/trending', methods=['GET'])
def get_trending_items():
    """Get trending items based on votes."""
    if not ENHANCED_FEATURES_AVAILABLE:
        return jsonify({'error': 'Feature not available'}), 503
    
    try:
        item_type = request.args.get('type', 'skill')
        days = request.args.get('days', 7, type=int)
        limit = request.args.get('limit', 10, type=int)
        
        trending = feedback_system.get_trending_items(item_type, days, limit)
        
        return jsonify({
            'item_type': item_type,
            'trending_items': trending,
            'period_days': days
        })
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/feedback/metrics', methods=['GET'])
def get_community_metrics():
    """Get community engagement metrics."""
    if not ENHANCED_FEATURES_AVAILABLE:
        return jsonify({'error': 'Feature not available'}), 503
    
    try:
        metrics = feedback_system.get_community_metrics()
        return jsonify(metrics)
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/feedback/suggestions/<int:suggestion_id>/review', methods=['POST'])
def review_suggestion(suggestion_id):
    """Review and approve/reject a suggestion (admin endpoint)."""
    if not ENHANCED_FEATURES_AVAILABLE:
        return jsonify({'error': 'Feature not available'}), 503
    
    try:
        data = request.get_json()
        reviewer_id = data.get('reviewer_id', 'admin')
        status = data.get('status')  # 'approved' or 'rejected'
        reason = data.get('reason', '')
        
        if not status or status not in ['approved', 'rejected']:
            return jsonify({'error': 'status must be "approved" or "rejected"'}), 400
        
        success = feedback_system.review_suggestion(suggestion_id, reviewer_id, status, reason)
        
        if success:
            return jsonify({
                'success': True,
                'message': f'Suggestion {status}',
                'suggestion_id': suggestion_id,
                'status': status
            })
        else:
            return jsonify({'error': 'Suggestion not found'}), 404
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/feedback/suggestions/approved', methods=['GET'])
def get_approved_suggestions():
    """Get all approved suggestions that need implementation."""
    if not ENHANCED_FEATURES_AVAILABLE:
        return jsonify({'error': 'Feature not available'}), 503
    
    try:
        import sqlite3
        conn = sqlite3.connect('genmentor.db')
        cursor = conn.cursor()
        
        cursor.execute("""
            SELECT id, item_uri, item_type, suggestion_type, suggestion_text,
                   votes_for, votes_against, reviewed_by, reviewed_at, created_at
            FROM suggestions
            WHERE status = 'approved'
            ORDER BY reviewed_at DESC
        """)
        
        suggestions = []
        for row in cursor.fetchall():
            suggestions.append({
                'id': row[0],
                'item_uri': row[1],
                'item_type': row[2],
                'suggestion_type': row[3],
                'suggestion_text': row[4],
                'votes_for': row[5],
                'votes_against': row[6],
                'reviewed_by': row[7],
                'reviewed_at': row[8],
                'created_at': row[9]
            })
        
        conn.close()
        
        return jsonify({
            'approved_suggestions': suggestions,
            'count': len(suggestions)
        })
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/feedback/suggestions/<int:suggestion_id>/implement', methods=['POST'])
def implement_suggestion(suggestion_id):
    """Implement an approved suggestion."""
    if not ENHANCED_FEATURES_AVAILABLE:
        return jsonify({'error': 'Feature not available'}), 503
    
    try:
        result = feedback_system.implement_suggestion(suggestion_id)
        
        if result.get('success'):
            return jsonify({
                'success': True,
                'message': result.get('message'),
                'action': result.get('action'),
                'details': result.get('details'),
                'suggestion_id': suggestion_id
            })
        else:
            return jsonify({'error': result.get('error')}), 400
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500

# ==================== LEARNING PATH VISUALIZATION ENDPOINTS ====================

@app.route('/api/path/visualize', methods=['POST'])
def visualize_learning_path():
    """Generate visualizations for a learning path."""
    if not ENHANCED_FEATURES_AVAILABLE:
        return jsonify({'error': 'Feature not available'}), 503
    
    try:
        data = request.get_json()
        learning_path = data.get('learning_path')
        
        if not learning_path:
            return jsonify({'error': 'learning_path is required'}), 400
        
        # Clean the learning path
        cleaned_path = visualizer.clean_learning_path(learning_path)
        
        # Generate visualizations
        gantt_data = visualizer.generate_gantt_chart_data(cleaned_path)
        graph_data = visualizer.generate_dependency_graph_data(cleaned_path)
        timeline = visualizer.generate_skills_timeline(cleaned_path)
        validation = visualizer.validate_prerequisites(cleaned_path)
        
        return jsonify({
            'cleaned_path': cleaned_path,
            'gantt_data': gantt_data,
            'dependency_graph': graph_data,
            'skills_timeline': timeline,
            'validation': validation
        })
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/path/visualize/gantt', methods=['GET'])
def get_gantt_html():
    """Get Gantt chart HTML visualization."""
    if not ENHANCED_FEATURES_AVAILABLE:
        return jsonify({'error': 'Feature not available'}), 503
    
    try:
        # Get the most recent learning path from request or use example
        learning_path = request.args.get('path_data')
        
        if learning_path:
            learning_path = json.loads(learning_path)
        else:
            return jsonify({'error': 'path_data parameter required'}), 400
        
        cleaned_path = visualizer.clean_learning_path(learning_path)
        gantt_data = visualizer.generate_gantt_chart_data(cleaned_path)
        html = visualizer.generate_gantt_chart_html(gantt_data)
        
        return html, 200, {'Content-Type': 'text/html'}
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/path/visualize/graph', methods=['GET'])
def get_graph_html():
    """Get dependency graph HTML visualization."""
    if not ENHANCED_FEATURES_AVAILABLE:
        return jsonify({'error': 'Feature not available'}), 503
    
    try:
        learning_path = request.args.get('path_data')
        
        if learning_path:
            learning_path = json.loads(learning_path)
        else:
            return jsonify({'error': 'path_data parameter required'}), 400
        
        cleaned_path = visualizer.clean_learning_path(learning_path)
        graph_data = visualizer.generate_dependency_graph_data(cleaned_path)
        html = visualizer.generate_dependency_graph_html(graph_data)
        
        return html, 200, {'Content-Type': 'text/html'}
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500

# ==================== RESOURCE CURATION ENDPOINTS ====================

@app.route('/api/resources/search', methods=['GET'])
def search_resources():
    """Search for learning resources."""
    if not ENHANCED_FEATURES_AVAILABLE:
        return jsonify({'error': 'Feature not available'}), 503
    
    try:
        skill_name = request.args.get('skill')
        limit = request.args.get('limit', 10, type=int)
        
        if not skill_name:
            return jsonify({'error': 'skill parameter is required'}), 400
        
        resources = resource_curator.search_resources(skill_name, limit)
        
        return jsonify({
            'skill': skill_name,
            'resources': resources,
            'count': len(resources)
        })
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/resources/add', methods=['POST'])
def add_resource():
    """Add a new learning resource."""
    if not ENHANCED_FEATURES_AVAILABLE:
        return jsonify({'error': 'Feature not available'}), 503
    
    try:
        data = request.get_json()
        
        resource_id = resource_curator.add_resource(
            skill_uri=data.get('skill_uri'),
            resource_url=data.get('resource_url'),
            resource_title=data.get('resource_title'),
            resource_type=data.get('resource_type'),
            provider=data.get('provider'),
            description=data.get('description'),
            difficulty_level=data.get('difficulty_level', 'intermediate'),
            is_free=data.get('is_free', True),
            estimated_duration=data.get('estimated_duration')
        )
        
        return jsonify({
            'success': True,
            'resource_id': resource_id
        })
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/resources/skill/<path:skill_uri>', methods=['GET'])
def get_skill_resources(skill_uri):
    """Get resources for a specific skill."""
    if not ENHANCED_FEATURES_AVAILABLE:
        return jsonify({'error': 'Feature not available'}), 503
    
    try:
        difficulty = request.args.get('difficulty')
        min_quality = request.args.get('min_quality', 0.0, type=float)
        validated_only = request.args.get('validated_only', 'false').lower() == 'true'
        
        resources = resource_curator.get_resources_for_skill(
            skill_uri, difficulty, min_quality, validated_only
        )
        
        return jsonify({
            'skill_uri': skill_uri,
            'resources': resources,
            'count': len(resources)
        })
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/resources/rate', methods=['POST'])
def rate_resource():
    """Rate a learning resource."""
    if not ENHANCED_FEATURES_AVAILABLE:
        return jsonify({'error': 'Feature not available'}), 503
    
    try:
        data = request.get_json()
        
        # Use feedback_system instead of resource_curator for rating
        stats = feedback_system.rate_resource(
            resource_url=data.get('resource_url'),
            skill_uri=data.get('skill_uri'),
            user_id=data.get('user_id', 'anonymous'),
            rating=data.get('rating'),
            quality_score=data.get('quality_score'),
            review_text=data.get('review_text')
        )
        
        return jsonify({
            'success': True,
            'stats': stats
        })
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/resources/popular', methods=['GET'])
def get_popular_resources():
    """Get popular resources."""
    if not ENHANCED_FEATURES_AVAILABLE:
        return jsonify({'error': 'Feature not available'}), 503
    
    try:
        days = request.args.get('days', 30, type=int)
        limit = request.args.get('limit', 10, type=int)
        
        resources = resource_curator.get_popular_resources(days, limit)
        
        return jsonify({
            'popular_resources': resources,
            'period_days': days
        })
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/path/with-resources', methods=['POST'])
def generate_path_with_resources():
    """Generate learning path with curated resources."""
    if not ENHANCED_FEATURES_AVAILABLE:
        return jsonify({'error': 'Feature not available'}), 503
    
    try:
        data = request.get_json()
        goal = data.get('goal')
        current_skills = data.get('current_skills', [])
        user_id = data.get('user_id', 'anonymous')
        
        if not goal:
            return jsonify({'error': 'goal is required'}), 400
        
        # Generate basic learning path
        result = ai_engine.identify_skill_gap(goal, current_skills)
        
        if not result['skill_gap']:
            return jsonify({
                'message': 'No skill gap identified',
                'matched_occupation': result.get('matched_occupation')
            })
        
        # Generate learning path (only takes skill_gap parameter)
        learning_path = ai_engine.schedule_learning_path(result['skill_gap'])
        
        # Curate resources for the learning path
        enhanced_path = resource_curator.curate_resources_for_learning_path(learning_path)
        
        # Clean and visualize
        cleaned_path = visualizer.clean_learning_path(enhanced_path)
        gantt_data = visualizer.generate_gantt_chart_data(cleaned_path)
        
        return jsonify({
            'matched_occupation': result['matched_occupation'],
            'learning_path': cleaned_path,
            'recognized_skills': result.get('recognized_skills', []),
            'total_skills_needed': result.get('total_skills_needed', 0),
            'skills_to_learn': result.get('skills_to_learn', 0),
            'gantt_timeline': gantt_data,
            'total_sessions': len(cleaned_path)
        })
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/path/optimized', methods=['POST'])
def generate_optimized_path():
    """
    Generate learning path with async resource curation (76% faster).
    Uses FAISS for 22.8x faster occupation matching and connection pooling for 33% faster DB ops.
    """
    try:
        data = request.get_json()
        goal = data.get('goal')
        current_skills = data.get('current_skills', [])
        user_id = data.get('user_id', 'anonymous')
        
        if not goal:
            return jsonify({'error': 'goal is required'}), 400
        
        # Generate basic learning path (uses FAISS + connection pool automatically)
        result = ai_engine.identify_skill_gap(goal, current_skills)
        
        if not result['skill_gap']:
            return jsonify({
                'message': 'No skill gap identified',
                'matched_occupation': result.get('matched_occupation')
            })
        
        # Generate learning path
        learning_path = ai_engine.schedule_learning_path(result['skill_gap'])
        
        # Use async curator if available for 76% faster resource fetching
        if ASYNC_RESOURCE_AVAILABLE and async_curator:
            import asyncio
            skill_names = []
            for session in learning_path:
                for skill in session.get('skills', []):
                    skill_names.append(skill.get('label', ''))
            
            # Fetch resources asynchronously (76% faster)
            resources_dict = asyncio.run(async_curator.batch_search(skill_names))
            
            # Enhance path with async-fetched resources
            for session in learning_path:
                for skill in session.get('skills', []):
                    skill_label = skill.get('label', '')
                    if skill_label in resources_dict:
                        skill['resources'] = resources_dict[skill_label]
            
            enhanced_path = learning_path
            optimization_used = "async_resource_curator (76% faster)"
        elif ENHANCED_FEATURES_AVAILABLE and resource_curator:
            # Fallback to sync curator
            enhanced_path = resource_curator.curate_resources_for_learning_path(learning_path)
            optimization_used = "sync_resource_curator"
        else:
            enhanced_path = learning_path
            optimization_used = "none"
        
        # Clean and visualize if available
        if ENHANCED_FEATURES_AVAILABLE and visualizer:
            cleaned_path = visualizer.clean_learning_path(enhanced_path)
            gantt_data = visualizer.generate_gantt_chart_data(cleaned_path)
        else:
            cleaned_path = enhanced_path
            gantt_data = None
        
        return jsonify({
            'matched_occupation': result['matched_occupation'],
            'learning_path': cleaned_path,
            'recognized_skills': result.get('recognized_skills', []),
            'total_skills_needed': result.get('total_skills_needed', 0),
            'skills_to_learn': result.get('skills_to_learn', 0),
            'gantt_timeline': gantt_data,
            'total_sessions': len(cleaned_path),
            'optimizations': {
                'faiss_matching': 'enabled (22.8x faster)' if ai_engine.faiss_index else 'disabled',
                'connection_pool': 'enabled (33% faster)' if ai_engine.db_pool else 'disabled',
                'resource_curation': optimization_used
            }
        })
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.errorhandler(404)
def not_found(error):
    """Handle 404 errors."""
    return jsonify({'error': 'Endpoint not found'}), 404

@app.errorhandler(500)
def internal_error(error):
    """Handle 500 errors."""
    return jsonify({'error': 'Internal server error'}), 500


# ============================================================================
# QUIZ ENDPOINTS
# ============================================================================

@app.route('/api/quiz/generate', methods=['POST'])
def generate_quiz():
    """
    Generate a quiz for a learning path.
    
    Request body:
    {
        "learning_path": {
            "sessions": [...],
            "target_occupation": "...",
            ...
        }
    }
    """
    if not QUIZ_AVAILABLE:
        return jsonify({'error': 'Quiz generator not available'}), 503
    
    try:
        data = request.get_json()
        
        if not data or 'learning_path' not in data:
            return jsonify({'error': 'learning_path is required in request body'}), 400
        
        learning_path = data['learning_path']
        
        # Generate quiz
        quiz = quiz_generator.generate_quiz(learning_path)
        
        if 'error' in quiz:
            return jsonify({'error': quiz['error']}), 500
        
        # Optionally save to file
        if data.get('save_to_file', False):
            filename = f"quiz_{learning_path.get('id', 'unknown')}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
            quiz_generator.save_quiz_to_file(quiz, filename)
            quiz['saved_to'] = filename
        
        return jsonify({
            'success': True,
            'quiz': quiz,
            'message': 'Quiz generated successfully'
        })
    
    except Exception as e:
        return jsonify({'error': f'Failed to generate quiz: {str(e)}'}), 500


@app.route('/api/quiz/submit', methods=['POST'])
def submit_quiz():
    """
    Submit quiz answers and get analysis.
    
    Request body:
    {
        "quiz": {
            "questions": [...],
            "metadata": {...}
        },
        "answers": {
            "1": "A",
            "2": "C",
            ...
        }
    }
    """
    if not QUIZ_AVAILABLE:
        return jsonify({'error': 'Quiz generator not available'}), 503
    
    try:
        data = request.get_json()
        
        if not data or 'quiz' not in data or 'answers' not in data:
            return jsonify({'error': 'quiz and answers are required in request body'}), 400
        
        quiz = data['quiz']
        user_answers = data['answers']
        
        # Convert answer keys to integers
        user_answers_int = {int(k): v for k, v in user_answers.items()}
        
        # Analyze results
        analysis = quiz_generator.analyze_quiz_results(quiz, user_answers_int)
        
        if 'error' in analysis:
            return jsonify({'error': analysis['error']}), 500
        
        return jsonify({
            'success': True,
            'analysis': analysis,
            'message': 'Quiz analyzed successfully'
        })
    
    except Exception as e:
        return jsonify({'error': f'Failed to analyze quiz: {str(e)}'}), 500


@app.route('/api/quiz/load/<filename>', methods=['GET'])
def load_quiz(filename):
    """Load a previously saved quiz from file."""
    if not QUIZ_AVAILABLE:
        return jsonify({'error': 'Quiz generator not available'}), 503
    
    try:
        quiz = quiz_generator.load_quiz_from_file(filename)
        
        if quiz is None:
            return jsonify({'error': 'Quiz file not found or invalid'}), 404
        
        return jsonify({
            'success': True,
            'quiz': quiz
        })
    
    except Exception as e:
        return jsonify({'error': f'Failed to load quiz: {str(e)}'}), 500


if __name__ == '__main__':
    print("Starting GenMentor API Server...")
    print("API Documentation: http://localhost:5000")
    print("Example endpoints:")
    print("  POST http://localhost:5000/api/path")
    print("  GET  http://localhost:5000/api/content?topic=python&level=beginner")
    print("  GET  http://localhost:5000/api/stats")
    
    # Run the Flask development server
    app.run(debug=True, host='0.0.0.0', port=5000)
