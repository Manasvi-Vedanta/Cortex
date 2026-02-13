"""
Enhanced Learning Path Visualizations
Comprehensive course visualization with topics, resources, time estimates, and progress tracking.
"""

from typing import List, Dict, Any
import json
from datetime import datetime, timedelta


class EnhancedCourseVisualizer:
    """
    Creates rich, interactive visualizations for learning paths with complete course information.
    """
    
    def __init__(self):
        """Initialize enhanced visualizer."""
        self.colors = {
            'beginner': '#4CAF50',
            'intermediate': '#FF9800',
            'advanced': '#F44336',
            'completed': '#2196F3',
            'in_progress': '#FFC107',
            'not_started': '#9E9E9E'
        }
    
    def generate_comprehensive_course_page(self, data: Dict[str, Any]) -> str:
        """
        Generate a comprehensive, beautiful HTML page showing the complete learning journey.
        
        Args:
            data: Dictionary containing:
                - goal: Career goal string
                - matched_occupation: Occupation details
                - learning_path: List of learning sessions
                - resources: Dictionary mapping skill names to resources
                - statistics: Total hours, skills, days
                - current_skills: List of user's current skills (optional)
            
        Returns:
            HTML string for complete course page
        """
        # Extract data
        goal = data.get('goal', 'Your Learning Journey')
        matched_occupation = data.get('matched_occupation', {})
        learning_path = data.get('learning_path', [])
        resources_by_skill = data.get('resources', {})
        statistics = data.get('statistics', {})
        current_skills = data.get('current_skills', [])
        
        # Calculate totals
        total_skills = statistics.get('total_skills', sum(len(session.get('skills', [])) for session in learning_path))
        total_hours = statistics.get('total_hours', sum(session.get('estimated_duration_hours', 0) for session in learning_path))
        total_days = statistics.get('duration_days', round(total_hours / 3, 1))  # Assuming 3 hours per day
        total_sessions = len(learning_path)
        
        occupation_label = matched_occupation.get('label', 'Your Career Goal')
        occupation_desc = matched_occupation.get('description', '')
        
        html = f"""
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Your Complete Learning Journey | GenMentor</title>
    <link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&display=swap" rel="stylesheet">
    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.0/css/all.min.css">
    <style>
        * {{
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }}
        
        body {{
            font-family: 'Inter', system-ui, -apple-system, sans-serif;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: #333;
            line-height: 1.6;
            padding: 20px;
            min-height: 100vh;
        }}
        
        .container {{
            max-width: 1400px;
            margin: 0 auto;
            background: white;
            border-radius: 20px;
            box-shadow: 0 20px 60px rgba(0,0,0,0.3);
            overflow: hidden;
        }}
        
        .header {{
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            padding: 60px 40px;
            text-align: center;
        }}
        
        .header h1 {{
            font-size: 3em;
            font-weight: 700;
            margin-bottom: 20px;
        }}
        
        .header p {{
            font-size: 1.3em;
            opacity: 0.95;
        }}
        
        .stats-grid {{
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
            gap: 30px;
            padding: 40px;
            background: #f8f9fa;
        }}
        
        .stat-card {{
            background: white;
            padding: 30px;
            border-radius: 15px;
            text-align: center;
            box-shadow: 0 4px 15px rgba(0,0,0,0.1);
            transition: transform 0.3s, box-shadow 0.3s;
        }}
        
        .stat-card:hover {{
            transform: translateY(-5px);
            box-shadow: 0 8px 25px rgba(0,0,0,0.15);
        }}
        
        .stat-icon {{
            font-size: 2.5em;
            margin-bottom: 15px;
        }}
        
        .stat-value {{
            font-size: 2.5em;
            font-weight: 700;
            color: #667eea;
            margin-bottom: 5px;
        }}
        
        .stat-label {{
            font-size: 1em;
            color: #666;
            text-transform: uppercase;
            letter-spacing: 1px;
        }}
        
        .timeline-container {{
            padding: 60px 40px;
        }}
        
        .session {{
            margin-bottom: 60px;
            position: relative;
            padding-left: 60px;
            border-left: 4px solid #e0e0e0;
        }}
        
        .session::before {{
            content: '';
            position: absolute;
            left: -15px;
            top: 0;
            width: 30px;
            height: 30px;
            border-radius: 50%;
            background: {self.colors['beginner']};
            border: 4px solid white;
            box-shadow: 0 0 0 4px #e0e0e0;
        }}
        
        .session.intermediate::before {{
            background: {self.colors['intermediate']};
        }}
        
        .session.advanced::before {{
            background: {self.colors['advanced']};
        }}
        
        .session-header {{
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            padding: 30px;
            border-radius: 15px 15px 0 0;
            display: flex;
            justify-content: space-between;
            align-items: center;
        }}
        
        .session-title {{
            font-size: 1.8em;
            font-weight: 600;
        }}
        
        .session-badge {{
            display: inline-block;
            padding: 8px 20px;
            border-radius: 20px;
            background: rgba(255,255,255,0.2);
            font-size: 0.9em;
            text-transform: uppercase;
            letter-spacing: 1px;
        }}
        
        .session-content {{
            background: white;
            border: 2px solid #e0e0e0;
            border-top: none;
            border-radius: 0 0 15px 15px;
            padding: 30px;
        }}
        
        .session-meta {{
            display: flex;
            gap: 30px;
            margin-bottom: 30px;
            padding-bottom: 20px;
            border-bottom: 2px solid #f0f0f0;
        }}
        
        .meta-item {{
            display: flex;
            align-items: center;
            gap: 10px;
        }}
        
        .meta-item i {{
            color: #667eea;
            font-size: 1.2em;
        }}
        
        .objectives {{
            margin-bottom: 30px;
        }}
        
        .objectives h3 {{
            font-size: 1.3em;
            margin-bottom: 15px;
            color: #667eea;
        }}
        
        .objectives ul {{
            list-style: none;
        }}
        
        .objectives li {{
            padding: 10px 0;
            padding-left: 30px;
            position: relative;
        }}
        
        .objectives li::before {{
            content: '✓';
            position: absolute;
            left: 0;
            color: #4CAF50;
            font-weight: bold;
            font-size: 1.2em;
        }}
        
        .skills-grid {{
            display: grid;
            grid-template-columns: repeat(auto-fill, minmax(300px, 1fr));
            gap: 20px;
            margin-top: 20px;
        }}
        
        .skill-card {{
            background: #f8f9fa;
            padding: 20px;
            border-radius: 10px;
            border-left: 4px solid #667eea;
            transition: all 0.3s;
        }}
        
        .skill-card:hover {{
            transform: translateX(5px);
            box-shadow: 0 4px 15px rgba(0,0,0,0.1);
        }}
        
        .skill-name {{
            font-weight: 600;
            font-size: 1.1em;
            margin-bottom: 15px;
            color: #333;
        }}
        
        .resources {{
            margin-top: 15px;
        }}
        
        .resources-label {{
            font-size: 0.9em;
            color: #666;
            margin-bottom: 10px;
            font-weight: 500;
        }}
        
        .resource-item {{
            background: white;
            padding: 12px;
            margin-bottom: 8px;
            border-radius: 8px;
            display: flex;
            align-items: center;
            gap: 12px;
            transition: all 0.2s;
        }}
        
        .resource-item:hover {{
            background: #667eea;
            color: white;
            cursor: pointer;
        }}
        
        .resource-icon {{
            font-size: 1.2em;
            min-width: 30px;
            text-align: center;
        }}
        
        .resource-link {{
            text-decoration: none;
            color: inherit;
            flex: 1;
            display: flex;
            justify-content: space-between;
            align-items: center;
        }}
        
        .resource-info {{
            flex: 1;
        }}
        
        .resource-title {{
            font-weight: 500;
            margin-bottom: 4px;
        }}
        
        .resource-meta {{
            font-size: 0.85em;
            opacity: 0.7;
        }}
        
        .quality-badge {{
            padding: 4px 10px;
            border-radius: 12px;
            font-size: 0.8em;
            font-weight: 600;
            background: #4CAF50;
            color: white;
        }}
        
        .quality-badge.high {{
            background: #4CAF50;
        }}
        
        .quality-badge.medium {{
            background: #FF9800;
        }}
        
        .quality-badge.low {{
            background: #f44336;
        }}
        
        .progress-bar {{
            position: sticky;
            top: 0;
            width: 100%;
            height: 8px;
            background: #e0e0e0;
            z-index: 1000;
        }}
        
        .progress-fill {{
            height: 100%;
            background: linear-gradient(90deg, #667eea 0%, #764ba2 100%);
            width: 0%;
            transition: width 0.3s;
        }}
        
        .download-btn {{
            position: fixed;
            bottom: 30px;
            right: 30px;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            padding: 18px 30px;
            border-radius: 50px;
            box-shadow: 0 8px 25px rgba(102, 126, 234, 0.4);
            text-decoration: none;
            font-weight: 600;
            display: flex;
            align-items: center;
            gap: 10px;
            transition: all 0.3s;
        }}
        
        .download-btn:hover {{
            transform: translateY(-3px);
            box-shadow: 0 12px 35px rgba(102, 126, 234, 0.5);
        }}
        
        @media print {{
            .download-btn, .progress-bar {{
                display: none;
            }}
        }}
    </style>
</head>
<body>
    <div class="progress-bar">
        <div class="progress-fill" id="progressFill"></div>
    </div>
    
    <div class="container">
        <div class="header">
            <h1>🎓 Your Complete Learning Journey</h1>
            <p style="font-size: 1.4em; font-weight: 600; margin: 20px 0;">"{goal}"</p>
            <p style="font-size: 1.1em; opacity: 0.9;">
                <i class="fas fa-briefcase"></i> Target Role: {occupation_label}
            </p>
            {f'<p style="font-size: 0.95em; opacity: 0.85; margin-top: 15px; max-width: 800px; margin-left: auto; margin-right: auto;">{occupation_desc}</p>' if occupation_desc else ''}
            {f'<p style="font-size: 0.9em; opacity: 0.8; margin-top: 15px;"><i class="fas fa-check-circle"></i> Current Skills: {", ".join(current_skills)}</p>' if current_skills else ''}
        </div>
        
        <div class="stats-grid">
            <div class="stat-card">
                <div class="stat-icon">📚</div>
                <div class="stat-value">{total_sessions}</div>
                <div class="stat-label">Learning Sessions</div>
            </div>
            <div class="stat-card">
                <div class="stat-icon">🎯</div>
                <div class="stat-value">{total_skills}</div>
                <div class="stat-label">Skills to Master</div>
            </div>
            <div class="stat-card">
                <div class="stat-icon">⏰</div>
                <div class="stat-value">{total_hours}h</div>
                <div class="stat-label">Total Study Time</div>
            </div>
            <div class="stat-card">
                <div class="stat-icon">📅</div>
                <div class="stat-value">{total_days}</div>
                <div class="stat-label">Days (3h/day)</div>
            </div>
        </div>
        
        <div class="timeline-container">
            <h2 style="text-align: center; margin-bottom: 50px; font-size: 2.5em; color: #667eea;">
                <i class="fas fa-road"></i> Your Learning Path
            </h2>
"""
        
        # Add each session
        for session in learning_path:
            session_num = session['session_number']
            title = session['title']
            difficulty = session['difficulty_level']
            duration = session['estimated_duration_hours']
            skills = session['skills']
            objectives = session.get('objectives', [])
            prerequisites = session.get('prerequisites', [])
            
            html += f"""
            <div class="session {difficulty}">
                <div class="session-header">
                    <div>
                        <span style="opacity: 0.7;">Session {session_num}</span>
                        <div class="session-title">{title}</div>
                    </div>
                    <div class="session-badge">{difficulty}</div>
                </div>
                
                <div class="session-content">
                    <div class="session-meta">
                        <div class="meta-item">
                            <i class="fas fa-clock"></i>
                            <span><strong>{duration} hours</strong> estimated</span>
                        </div>
                        <div class="meta-item">
                            <i class="fas fa-graduation-cap"></i>
                            <span><strong>{len(skills)} skills</strong> to learn</span>
                        </div>
                        {f'<div class="meta-item"><i class="fas fa-link"></i><span><strong>{len(prerequisites)}</strong> prerequisites</span></div>' if prerequisites else ''}
                    </div>
"""
            
            # Add objectives
            if objectives:
                html += """
                    <div class="objectives">
                        <h3><i class="fas fa-bullseye"></i> Learning Objectives</h3>
                        <ul>
"""
                for objective in objectives:
                    html += f"                            <li>{objective}</li>\n"
                
                html += """
                        </ul>
                    </div>
"""
            
            # Add skills with resources
            html += """
                    <div class="skills-section">
                        <h3 style="margin-bottom: 20px; color: #667eea;"><i class="fas fa-list-check"></i> Skills & Resources</h3>
                        <div class="skills-grid">
"""
            
            for skill in skills:
                skill_name = skill if isinstance(skill, str) else skill.get('label', skill.get('uri', 'Unknown'))
                skill_resources = resources_by_skill.get(skill_name, [])
                
                html += f"""
                            <div class="skill-card">
                                <div class="skill-name">📖 {skill_name}</div>
"""
                
                # Add resources if available
                if skill_resources:
                    html += """
                                <div class="resources">
                                    <div class="resources-label">📚 Learning Resources:</div>
"""
                    
                    for resource in skill_resources[:5]:  # Limit to top 5
                        title_text = resource.get('title', 'Resource')
                        url = resource.get('url', '#')
                        provider = resource.get('provider', 'Unknown')
                        res_type = resource.get('type', 'resource')
                        quality = resource.get('quality_score', 0.5)
                        
                        # Determine icon based on type
                        icon = {
                            'video': '🎥',
                            'article': '📄',
                            'documentation': '📘',
                            'repository': '💻',
                            'course': '🎓'
                        }.get(res_type, '🔗')
                        
                        # Determine quality badge
                        if quality >= 0.8:
                            quality_class = 'high'
                            quality_label = 'High'
                        elif quality >= 0.5:
                            quality_class = 'medium'
                            quality_label = 'Good'
                        else:
                            quality_class = 'low'
                            quality_label = 'OK'
                        
                        html += f"""
                                    <div class="resource-item">
                                        <div class="resource-icon">{icon}</div>
                                        <a href="{url}" class="resource-link" target="_blank">
                                            <div class="resource-info">
                                                <div class="resource-title">{title_text[:50]}{'...' if len(title_text) > 50 else ''}</div>
                                                <div class="resource-meta">{provider} • {res_type.title()}</div>
                                            </div>
                                            <span class="quality-badge {quality_class}">{quality_label}</span>
                                        </a>
                                    </div>
"""
                else:
                    html += """
                                    <div class="resources">
                                        <div class="resources-label" style="color: #999;">
                                            <i class="fas fa-search"></i> Search for "{}" on your preferred learning platform
                                        </div>
                                    </div>
""".format(skill_name)
                
                html += """
                                </div>
                            </div>
"""
            
            html += """
                        </div>
                    </div>
                </div>
            </div>
"""
        
        # Close HTML
        html += f"""
        </div>
    </div>
    
    <a href="#" class="download-btn" onclick="window.print(); return false;">
        <i class="fas fa-download"></i>
        Save as PDF
    </a>
    
    <script>
        // Scroll progress indicator
        window.addEventListener('scroll', function() {{
            const winScroll = document.body.scrollTop || document.documentElement.scrollTop;
            const height = document.documentElement.scrollHeight - document.documentElement.clientHeight;
            const scrolled = (winScroll / height) * 100;
            document.getElementById('progressFill').style.width = scrolled + '%';
        }});
        
        // Add click handlers for resource items
        document.querySelectorAll('.resource-item').forEach(item => {{
            item.addEventListener('click', function(e) {{
                if (!e.target.closest('a')) {{
                    const link = this.querySelector('a');
                    if (link) {{
                        window.open(link.href, '_blank');
                    }}
                }}
            }});
        }});
    </script>
</body>
</html>
"""
        
        return html
    
    def save_comprehensive_visualization(self, data: Dict[str, Any], 
                                        filename: str = 'complete_learning_journey.html'):
        """
        Save comprehensive visualization to HTML file.
        
        Args:
            data: Complete learning path data (goal, occupation, sessions, resources, etc.)
            filename: Output filename
        """
        html = self.generate_comprehensive_course_page(data)
        
        with open(filename, 'w', encoding='utf-8') as f:
            f.write(html)
        
        print(f"✅ Saved comprehensive visualization to: {filename}")
        return filename


# Example usage
if __name__ == "__main__":
    # Sample data
    sample_learning_path = [
        {
            "session_number": 1,
            "title": "Programming Fundamentals",
            "difficulty_level": "beginner",
            "estimated_duration_hours": 40,
            "skills": ["python programming", "basic syntax", "data types", "control structures"],
            "objectives": [
                "Understand basic programming concepts",
                "Write simple Python programs",
                "Work with variables and data types"
            ],
            "prerequisites": []
        },
        {
            "session_number": 2,
            "title": "Data Structures & Algorithms",
            "difficulty_level": "intermediate",
            "estimated_duration_hours": 60,
            "skills": ["lists", "dictionaries", "sorting algorithms", "searching algorithms"],
            "objectives": [
                "Master fundamental data structures",
                "Implement common algorithms",
                "Analyze time complexity"
            ],
            "prerequisites": ["Programming Fundamentals"]
        },
        {
            "session_number": 3,
            "title": "Web Development Basics",
            "difficulty_level": "intermediate",
            "estimated_duration_hours": 50,
            "skills": ["HTML", "CSS", "JavaScript", "responsive design"],
            "objectives": [
                "Build responsive web pages",
                "Style with CSS",
                "Add interactivity with JavaScript"
            ],
            "prerequisites": ["Programming Fundamentals"]
        }
    ]
    
    sample_resources = {
        "python programming": [
            {
                "title": "Python Official Tutorial",
                "url": "https://docs.python.org/3/tutorial/",
                "type": "documentation",
                "provider": "Python.org",
                "quality_score": 1.0
            },
            {
                "title": "Python for Beginners - Full Course",
                "url": "https://www.youtube.com/watch?v=example",
                "type": "video",
                "provider": "YouTube",
                "quality_score": 0.9
            }
        ],
        "HTML": [
            {
                "title": "MDN HTML Tutorial",
                "url": "https://developer.mozilla.org/en-US/docs/Web/HTML",
                "type": "documentation",
                "provider": "MDN",
                "quality_score": 1.0
            }
        ]
    }
    
    visualizer = EnhancedCourseVisualizer()
    filename = visualizer.save_comprehensive_visualization(
        sample_learning_path, 
        sample_resources,
        'demo_complete_learning_journey.html'
    )
    
    print(f"\n✅ Open {filename} in your browser to see the complete learning journey!")
