"""
Learning Path Visualization & Data Cleaning
Generate visual dashboards (Gantt charts, dependency graphs) and clean learning path data.
"""

import json
import sqlite3
from datetime import datetime, timedelta
from typing import Dict, List, Tuple, Optional
import networkx as nx
from collections import defaultdict

class LearningPathVisualizer:
    """Clean, normalize, and visualize learning paths with Gantt charts and dependency graphs."""
    
    def __init__(self, db_path: str = 'genmentor.db'):
        self.db_path = db_path
    
    def _get_db_connection(self):
        """Get database connection."""
        return sqlite3.connect(self.db_path)
    
    # ==================== DATA CLEANING & NORMALIZATION ====================
    
    def clean_learning_path(self, learning_path: List[Dict]) -> List[Dict]:
        """
        Clean and normalize learning path data.
        
        - Normalize durations to hours
        - Validate prerequisites
        - Remove duplicates
        - Ensure proper ordering
        """
        cleaned_path = []
        seen_skills = set()
        session_number = 1
        
        for session in learning_path:
            # Normalize duration
            duration = self._normalize_duration(session.get('estimated_duration_hours', 8))
            
            # Clean skills list (remove duplicates)
            skills = session.get('skills', [])
            if isinstance(skills, list):
                unique_skills = []
                for skill in skills:
                    skill_name = skill if isinstance(skill, str) else skill.get('name', '')
                    if skill_name and skill_name not in seen_skills:
                        unique_skills.append(skill_name)
                        seen_skills.add(skill_name)
                
                if not unique_skills:  # Skip empty sessions
                    continue
            else:
                continue
            
            # Clean prerequisites
            prerequisites = self._clean_prerequisites(
                session.get('prerequisites', []),
                cleaned_path
            )
            
            # Normalize difficulty level
            difficulty = self._normalize_difficulty(
                session.get('difficulty_level', 'intermediate')
            )
            
            cleaned_session = {
                'session_number': session_number,
                'title': session.get('title', f'Learning Session {session_number}'),
                'objectives': session.get('objectives', []),
                'skills': unique_skills,
                'estimated_duration_hours': duration,
                'difficulty_level': difficulty,
                'prerequisites': prerequisites,
                'resources': session.get('resources', [])
            }
            
            cleaned_path.append(cleaned_session)
            session_number += 1
        
        return cleaned_path
    
    def _normalize_duration(self, duration) -> int:
        """Normalize duration to hours (integer)."""
        if isinstance(duration, str):
            # Try to extract number from string
            import re
            numbers = re.findall(r'\d+', duration)
            if numbers:
                duration = int(numbers[0])
            else:
                duration = 8  # Default
        
        duration = int(duration) if duration else 8
        
        # Ensure reasonable bounds (1-100 hours per session)
        return max(1, min(100, duration))
    
    def _clean_prerequisites(self, prerequisites: List, existing_sessions: List[Dict]) -> List[str]:
        """Clean and validate prerequisites."""
        if not prerequisites:
            return []
        
        # Get all valid session titles from existing sessions
        valid_titles = {s['title'] for s in existing_sessions}
        
        # Filter prerequisites to only include valid ones
        cleaned = []
        for prereq in prerequisites:
            if isinstance(prereq, str) and prereq in valid_titles:
                cleaned.append(prereq)
            elif isinstance(prereq, dict) and prereq.get('title') in valid_titles:
                cleaned.append(prereq['title'])
        
        return cleaned
    
    def _normalize_difficulty(self, difficulty: str) -> str:
        """Normalize difficulty level to standard values."""
        difficulty = str(difficulty).lower()
        
        if difficulty in ['beginner', 'easy', 'basic', 'introductory']:
            return 'beginner'
        elif difficulty in ['intermediate', 'medium', 'moderate']:
            return 'intermediate'
        elif difficulty in ['advanced', 'hard', 'expert', 'difficult']:
            return 'advanced'
        else:
            return 'intermediate'
    
    def validate_prerequisites(self, learning_path: List[Dict]) -> Dict:
        """
        Validate that all prerequisites are met and sessions are properly ordered.
        
        Returns:
            Dict with validation results
        """
        issues = []
        session_map = {s['title']: i for i, s in enumerate(learning_path)}
        
        for i, session in enumerate(learning_path):
            for prereq in session.get('prerequisites', []):
                if prereq not in session_map:
                    issues.append({
                        'session': session['title'],
                        'issue': 'missing_prerequisite',
                        'prerequisite': prereq
                    })
                elif session_map[prereq] >= i:
                    issues.append({
                        'session': session['title'],
                        'issue': 'prerequisite_order',
                        'prerequisite': prereq,
                        'message': f'Prerequisite "{prereq}" comes after current session'
                    })
        
        return {
            'valid': len(issues) == 0,
            'total_sessions': len(learning_path),
            'issues': issues
        }
    
    # ==================== VISUALIZATION DATA GENERATION ====================
    
    def generate_gantt_chart_data(self, learning_path: List[Dict], 
                                  start_date: datetime = None) -> Dict:
        """
        Generate data for Gantt chart visualization.
        
        Args:
            learning_path: Cleaned learning path
            start_date: Starting date for the schedule
        
        Returns:
            Dict with Gantt chart data
        """
        if start_date is None:
            start_date = datetime.now()
        
        gantt_data = {
            'title': 'Learning Path Timeline',
            'start_date': start_date.isoformat(),
            'tasks': [],
            'total_duration_hours': 0,
            'total_duration_days': 0
        }
        
        current_date = start_date
        
        for session in learning_path:
            duration_hours = session['estimated_duration_hours']
            duration_days = max(1, duration_hours / 8)  # Assuming 8 hours/day
            
            end_date = current_date + timedelta(days=duration_days)
            
            task = {
                'id': f"session_{session['session_number']}",
                'name': session['title'],
                'start': current_date.isoformat(),
                'end': end_date.isoformat(),
                'duration_hours': duration_hours,
                'duration_days': round(duration_days, 1),
                'progress': 0,  # Can be updated by user
                'dependencies': session.get('prerequisites', []),
                'difficulty': session['difficulty_level'],
                'skills_count': len(session['skills'])
            }
            
            gantt_data['tasks'].append(task)
            gantt_data['total_duration_hours'] += duration_hours
            
            current_date = end_date
        
        gantt_data['total_duration_days'] = round(
            (current_date - start_date).days, 1
        )
        gantt_data['estimated_completion_date'] = current_date.isoformat()
        
        return gantt_data
    
    def generate_dependency_graph_data(self, learning_path: List[Dict]) -> Dict:
        """
        Generate data for dependency graph visualization.
        
        Returns:
            Dict with nodes and edges for graph visualization
        """
        graph_data = {
            'nodes': [],
            'edges': [],
            'levels': []
        }
        
        # Create networkx graph for level calculation
        G = nx.DiGraph()
        
        # Add nodes
        for session in learning_path:
            session_id = f"session_{session['session_number']}"
            G.add_node(session_id)
            
            node = {
                'id': session_id,
                'label': session['title'],
                'session_number': session['session_number'],
                'skills_count': len(session['skills']),
                'duration_hours': session['estimated_duration_hours'],
                'difficulty': session['difficulty_level'],
                'color': self._get_difficulty_color(session['difficulty_level'])
            }
            
            graph_data['nodes'].append(node)
        
        # Add edges (dependencies)
        session_map = {s['title']: f"session_{s['session_number']}" 
                      for s in learning_path}
        
        for session in learning_path:
            session_id = f"session_{session['session_number']}"
            
            for prereq in session.get('prerequisites', []):
                if prereq in session_map:
                    prereq_id = session_map[prereq]
                    G.add_edge(prereq_id, session_id)
                    
                    edge = {
                        'from': prereq_id,
                        'to': session_id,
                        'label': 'requires'
                    }
                    
                    graph_data['edges'].append(edge)
        
        # Calculate levels (topological generations)
        try:
            levels = list(nx.topological_generations(G))
            graph_data['levels'] = [
                {'level': i, 'sessions': list(level)} 
                for i, level in enumerate(levels)
            ]
            graph_data['max_level'] = len(levels) - 1
        except:
            graph_data['levels'] = []
            graph_data['max_level'] = 0
        
        # Calculate graph metrics
        graph_data['metrics'] = {
            'total_sessions': len(graph_data['nodes']),
            'total_dependencies': len(graph_data['edges']),
            'independent_sessions': len([n for n in G.nodes() if G.in_degree(n) == 0]),
            'complexity_score': len(graph_data['edges']) / max(1, len(graph_data['nodes']))
        }
        
        return graph_data
    
    def _get_difficulty_color(self, difficulty: str) -> str:
        """Get color code for difficulty level."""
        colors = {
            'beginner': '#4CAF50',     # Green
            'intermediate': '#FF9800', # Orange
            'advanced': '#F44336'      # Red
        }
        return colors.get(difficulty, '#2196F3')  # Default blue
    
    def generate_skills_timeline(self, learning_path: List[Dict]) -> Dict:
        """Generate a timeline showing when each skill is learned."""
        timeline = {
            'skills': [],
            'sessions': []
        }
        
        skill_first_appearance = {}
        cumulative_hours = 0
        
        for session in learning_path:
            session_start = cumulative_hours
            session_end = cumulative_hours + session['estimated_duration_hours']
            
            timeline['sessions'].append({
                'session_number': session['session_number'],
                'title': session['title'],
                'start_hour': session_start,
                'end_hour': session_end,
                'skills': session['skills']
            })
            
            for skill in session['skills']:
                if skill not in skill_first_appearance:
                    skill_first_appearance[skill] = {
                        'skill_name': skill,
                        'learned_at_hour': session_start,
                        'learned_in_session': session['session_number'],
                        'session_title': session['title']
                    }
            
            cumulative_hours = session_end
        
        timeline['skills'] = list(skill_first_appearance.values())
        timeline['total_hours'] = cumulative_hours
        
        return timeline
    
    # ==================== HTML GENERATION ====================
    
    def generate_gantt_chart_html(self, gantt_data: Dict) -> str:
        """Generate HTML with Gantt chart visualization using Chart.js or similar."""
        html = f"""
<!DOCTYPE html>
<html>
<head>
    <title>Learning Path Gantt Chart</title>
    <style>
        body {{
            font-family: Arial, sans-serif;
            margin: 20px;
            background: #f5f5f5;
        }}
        .container {{
            max-width: 1200px;
            margin: 0 auto;
            background: white;
            padding: 30px;
            border-radius: 10px;
            box-shadow: 0 2px 10px rgba(0,0,0,0.1);
        }}
        h1 {{
            color: #333;
            border-bottom: 3px solid #2196F3;
            padding-bottom: 10px;
        }}
        .summary {{
            background: #e3f2fd;
            padding: 20px;
            border-radius: 5px;
            margin: 20px 0;
        }}
        .summary-item {{
            display: inline-block;
            margin-right: 30px;
        }}
        .summary-label {{
            font-weight: bold;
            color: #666;
        }}
        .summary-value {{
            font-size: 1.3em;
            color: #2196F3;
            font-weight: bold;
        }}
        .task {{
            background: #fff;
            border-left: 5px solid #2196F3;
            padding: 15px;
            margin: 10px 0;
            border-radius: 5px;
            box-shadow: 0 1px 3px rgba(0,0,0,0.1);
        }}
        .task-header {{
            font-weight: bold;
            font-size: 1.1em;
            color: #333;
            margin-bottom: 8px;
        }}
        .task-details {{
            color: #666;
            font-size: 0.9em;
        }}
        .task-bar {{
            background: #2196F3;
            height: 30px;
            border-radius: 3px;
            margin: 10px 0;
            position: relative;
        }}
        .task-bar-label {{
            position: absolute;
            left: 10px;
            top: 50%;
            transform: translateY(-50%);
            color: white;
            font-weight: bold;
        }}
        .difficulty-beginner {{ border-left-color: #4CAF50; }}
        .difficulty-intermediate {{ border-left-color: #FF9800; }}
        .difficulty-advanced {{ border-left-color: #F44336; }}
    </style>
</head>
<body>
    <div class="container">
        <h1>📊 Learning Path Timeline</h1>
        
        <div class="summary">
            <div class="summary-item">
                <div class="summary-label">Total Duration</div>
                <div class="summary-value">{gantt_data['total_duration_hours']} hours</div>
            </div>
            <div class="summary-item">
                <div class="summary-label">Estimated Days</div>
                <div class="summary-value">{gantt_data['total_duration_days']} days</div>
            </div>
            <div class="summary-item">
                <div class="summary-label">Total Sessions</div>
                <div class="summary-value">{len(gantt_data['tasks'])}</div>
            </div>
            <div class="summary-item">
                <div class="summary-label">Start Date</div>
                <div class="summary-value">{gantt_data['start_date'][:10]}</div>
            </div>
        </div>
        
        <h2>📅 Session Timeline</h2>
"""
        
        for task in gantt_data['tasks']:
            html += f"""
        <div class="task difficulty-{task['difficulty']}">
            <div class="task-header">{task['name']}</div>
            <div class="task-details">
                📅 {task['start'][:10]} → {task['end'][:10]} | 
                ⏱️ {task['duration_hours']} hours ({task['duration_days']} days) | 
                🎯 {task['difficulty'].title()} | 
                📚 {task['skills_count']} skills
            </div>
            <div class="task-bar">
                <div class="task-bar-label">{task['name']}</div>
            </div>
            {f"<div style='color: #999; font-size: 0.85em;'>Prerequisites: {', '.join(task['dependencies'])}</div>" if task['dependencies'] else ""}
        </div>
"""
        
        html += """
    </div>
</body>
</html>
"""
        return html
    
    def generate_dependency_graph_html(self, graph_data: Dict) -> str:
        """Generate HTML with dependency graph visualization using vis.js."""
        html = f"""
<!DOCTYPE html>
<html>
<head>
    <title>Learning Path Dependency Graph</title>
    <script type="text/javascript" src="https://unpkg.com/vis-network/standalone/umd/vis-network.min.js"></script>
    <style>
        body {{
            font-family: Arial, sans-serif;
            margin: 0;
            padding: 20px;
            background: #f5f5f5;
        }}
        .container {{
            max-width: 1400px;
            margin: 0 auto;
        }}
        h1 {{
            color: #333;
        }}
        #mynetwork {{
            width: 100%;
            height: 600px;
            background: white;
            border: 1px solid #ddd;
            border-radius: 5px;
        }}
        .metrics {{
            background: white;
            padding: 20px;
            margin: 20px 0;
            border-radius: 5px;
            box-shadow: 0 2px 5px rgba(0,0,0,0.1);
        }}
        .metric {{
            display: inline-block;
            margin-right: 30px;
        }}
        .metric-label {{
            font-weight: bold;
            color: #666;
        }}
        .metric-value {{
            font-size: 1.5em;
            color: #2196F3;
        }}
        .legend {{
            background: white;
            padding: 15px;
            margin: 20px 0;
            border-radius: 5px;
        }}
        .legend-item {{
            display: inline-block;
            margin-right: 20px;
        }}
        .legend-color {{
            display: inline-block;
            width: 20px;
            height: 20px;
            margin-right: 5px;
            vertical-align: middle;
            border-radius: 3px;
        }}
    </style>
</head>
<body>
    <div class="container">
        <h1>🔗 Learning Path Dependency Graph</h1>
        
        <div class="metrics">
            <div class="metric">
                <div class="metric-label">Total Sessions</div>
                <div class="metric-value">{graph_data['metrics']['total_sessions']}</div>
            </div>
            <div class="metric">
                <div class="metric-label">Dependencies</div>
                <div class="metric-value">{graph_data['metrics']['total_dependencies']}</div>
            </div>
            <div class="metric">
                <div class="metric-label">Independent Sessions</div>
                <div class="metric-value">{graph_data['metrics']['independent_sessions']}</div>
            </div>
            <div class="metric">
                <div class="metric-label">Complexity Score</div>
                <div class="metric-value">{graph_data['metrics']['complexity_score']:.2f}</div>
            </div>
        </div>
        
        <div class="legend">
            <strong>Difficulty Levels:</strong>
            <div class="legend-item">
                <span class="legend-color" style="background: #4CAF50;"></span>
                Beginner
            </div>
            <div class="legend-item">
                <span class="legend-color" style="background: #FF9800;"></span>
                Intermediate
            </div>
            <div class="legend-item">
                <span class="legend-color" style="background: #F44336;"></span>
                Advanced
            </div>
        </div>
        
        <div id="mynetwork"></div>
    </div>
    
    <script type="text/javascript">
        var nodes = new vis.DataSet({json.dumps(graph_data['nodes'], indent=2)});
        
        var edges = new vis.DataSet({json.dumps(graph_data['edges'], indent=2)});
        
        var container = document.getElementById('mynetwork');
        var data = {{
            nodes: nodes,
            edges: edges
        }};
        
        var options = {{
            nodes: {{
                shape: 'box',
                margin: 10,
                widthConstraint: {{
                    maximum: 200
                }},
                font: {{
                    size: 14,
                    color: '#ffffff'
                }}
            }},
            edges: {{
                arrows: {{
                    to: {{
                        enabled: true,
                        scaleFactor: 0.5
                    }}
                }},
                smooth: {{
                    type: 'cubicBezier'
                }},
                color: {{
                    color: '#848484',
                    highlight: '#2196F3'
                }}
            }},
            layout: {{
                hierarchical: {{
                    direction: 'UD',
                    sortMethod: 'directed',
                    levelSeparation: 150,
                    nodeSpacing: 200
                }}
            }},
            physics: false
        }};
        
        var network = new vis.Network(container, data, options);
        
        network.on("click", function(params) {{
            if (params.nodes.length > 0) {{
                var nodeId = params.nodes[0];
                var node = nodes.get(nodeId);
                alert('Session: ' + node.label + '\\n' +
                      'Skills: ' + node.skills_count + '\\n' +
                      'Duration: ' + node.duration_hours + ' hours\\n' +
                      'Difficulty: ' + node.difficulty);
            }}
        }});
    </script>
</body>
</html>
"""
        return html
    
    def save_visualizations(self, learning_path: List[Dict], output_dir: str = '.') -> Dict:
        """
        Save all visualizations to HTML files.
        
        Returns:
            Dict with file paths
        """
        import os
        
        # Clean the learning path first
        cleaned_path = self.clean_learning_path(learning_path)
        
        # Generate Gantt chart
        gantt_data = self.generate_gantt_chart_data(cleaned_path)
        gantt_html = self.generate_gantt_chart_html(gantt_data)
        gantt_file = os.path.join(output_dir, 'learning_path_gantt.html')
        with open(gantt_file, 'w', encoding='utf-8') as f:
            f.write(gantt_html)
        
        # Generate dependency graph
        graph_data = self.generate_dependency_graph_data(cleaned_path)
        graph_html = self.generate_dependency_graph_html(graph_data)
        graph_file = os.path.join(output_dir, 'learning_path_dependencies.html')
        with open(graph_file, 'w', encoding='utf-8') as f:
            f.write(graph_html)
        
        # Save cleaned JSON data
        json_file = os.path.join(output_dir, 'learning_path_cleaned.json')
        with open(json_file, 'w', encoding='utf-8') as f:
            json.dump({
                'cleaned_path': cleaned_path,
                'gantt_data': gantt_data,
                'graph_data': graph_data
            }, f, indent=2)
        
        return {
            'gantt_chart': gantt_file,
            'dependency_graph': graph_file,
            'cleaned_data': json_file
        }

if __name__ == "__main__":
    # Example usage
    visualizer = LearningPathVisualizer()
    
    # Sample learning path
    sample_path = [
        {
            "session_number": 1,
            "title": "Python Fundamentals",
            "skills": ["python", "variables", "loops"],
            "estimated_duration_hours": 20,
            "difficulty_level": "beginner",
            "prerequisites": []
        },
        {
            "session_number": 2,
            "title": "Data Structures",
            "skills": ["lists", "dictionaries", "sets"],
            "estimated_duration_hours": 15,
            "difficulty_level": "intermediate",
            "prerequisites": ["Python Fundamentals"]
        }
    ]
    
    # Clean and visualize
    cleaned = visualizer.clean_learning_path(sample_path)
    files = visualizer.save_visualizations(cleaned)
    print(f"Visualizations saved: {files}")
