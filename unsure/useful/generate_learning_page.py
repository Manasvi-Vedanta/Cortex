"""
Generate Complete Learning Path Webpage
Creates an interactive HTML page showing the full learning journey with resources
"""

import json
from datetime import datetime
from ai_engine import GenMentorAI
from improved_resource_curator import ImprovedResourceCurator

def generate_complete_learning_page(goal, current_skills):
    """Generate a complete learning path with resources and save as HTML."""
    
    print("=" * 80)
    print("GENMENTOR - COMPLETE LEARNING PATH GENERATOR")
    print("=" * 80)
    print(f"\n🎯 Goal: {goal}")
    print(f"📚 Current Skills: {', '.join(current_skills)}\n")
    
    # Initialize components
    print("Initializing AI Engine...")
    ai_engine = GenMentorAI()
    resource_curator = ImprovedResourceCurator()
    
    # Step 1: Analyze skill gap
    print("\n[1/3] Analyzing skill gap...")
    skill_gap = ai_engine.identify_skill_gap(goal, current_skills)
    
    print(f"   ✓ Matched Occupation: {skill_gap['matched_occupation']}")
    print(f"   ✓ Skills Needed: {skill_gap['skills_to_learn']}")
    print(f"   ✓ Total Skills to Learn: {len(skill_gap['skill_gap'])}")
    
    # Step 2: Generate learning path
    print("\n[2/3] Generating learning path...")
    learning_path = ai_engine.schedule_learning_path(skill_gap['skill_gap'][:15])
    
    print(f"   ✓ Created {len(learning_path)} learning sessions")
    total_hours = sum(session.get('duration', 0) for session in learning_path)
    print(f"   ✓ Total Duration: {total_hours} hours")
    
    # Step 3: Curate resources for each skill
    print("\n[3/3] Curating learning resources...")
    sessions_with_resources = []
    
    for i, session in enumerate(learning_path, 1):
        # Handle both old and new session structures
        title = session.get('title') or session.get('session_title', f'Session {i}')
        print(f"\n   Session {i}: {title}")
        
        session_data = {
            'session_number': i,
            'title': title,
            'duration': session.get('estimated_duration_hours') or session.get('duration', 0),
            'difficulty': session.get('difficulty_level') or session.get('difficulty', 'intermediate'),
            'objectives': session.get('objectives') or session.get('learning_objectives', []),
            'skills': []
        }
        
        # Get skills from either 'skills' or 'skills_covered'
        skills_list = session.get('skills') or session.get('skills_covered', [])
        for skill in skills_list[:3]:  # Limit to 3 skills per session for demo
            skill_name = skill.split('/')[-1].replace('_', ' ')
            print(f"      🔍 Finding resources for: {skill_name}")
            
            resources = resource_curator.search_resources(skill_name, limit=5)
            
            skill_data = {
                'name': skill_name,
                'uri': skill,
                'resources': resources
            }
            session_data['skills'].append(skill_data)
            print(f"         ✓ Found {len(resources)} resources")
        
        sessions_with_resources.append(session_data)
    
    # Generate HTML
    print("\n[4/4] Generating interactive webpage...")
    html = generate_html(goal, current_skills, skill_gap, sessions_with_resources, total_hours)
    
    # Save HTML file
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"complete_learning_journey_{timestamp}.html"
    
    with open(filename, 'w', encoding='utf-8') as f:
        f.write(html)
    
    print(f"\n✅ SUCCESS! Webpage generated: {filename}")
    print(f"\n📖 Open this file in your browser to see your complete learning journey!")
    print("=" * 80)
    
    return filename

def generate_html(goal, current_skills, skill_gap, sessions, total_hours):
    """Generate the complete HTML page."""
    
    html = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Your Learning Journey - GenMentor</title>
    <style>
        * {{
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }}
        
        body {{
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            padding: 20px;
            line-height: 1.6;
        }}
        
        .container {{
            max-width: 1200px;
            margin: 0 auto;
            background: white;
            border-radius: 20px;
            box-shadow: 0 20px 60px rgba(0,0,0,0.3);
            overflow: hidden;
        }}
        
        .header {{
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            padding: 40px;
            text-align: center;
        }}
        
        .header h1 {{
            font-size: 2.5em;
            margin-bottom: 10px;
        }}
        
        .header p {{
            font-size: 1.2em;
            opacity: 0.9;
        }}
        
        .summary {{
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
            gap: 20px;
            padding: 30px 40px;
            background: #f8f9fa;
            border-bottom: 2px solid #e9ecef;
        }}
        
        .summary-card {{
            text-align: center;
            padding: 20px;
            background: white;
            border-radius: 10px;
            box-shadow: 0 2px 10px rgba(0,0,0,0.1);
        }}
        
        .summary-card .number {{
            font-size: 2.5em;
            font-weight: bold;
            color: #667eea;
            display: block;
        }}
        
        .summary-card .label {{
            color: #666;
            font-size: 0.9em;
            margin-top: 5px;
        }}
        
        .content {{
            padding: 40px;
        }}
        
        .section {{
            margin-bottom: 40px;
        }}
        
        .section h2 {{
            color: #333;
            margin-bottom: 20px;
            padding-bottom: 10px;
            border-bottom: 3px solid #667eea;
            font-size: 1.8em;
        }}
        
        .occupation-match {{
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            padding: 20px 30px;
            border-radius: 10px;
            font-size: 1.2em;
            margin-bottom: 20px;
        }}
        
        .session {{
            background: #f8f9fa;
            border-radius: 15px;
            padding: 30px;
            margin-bottom: 30px;
            border-left: 5px solid #667eea;
            box-shadow: 0 2px 10px rgba(0,0,0,0.05);
        }}
        
        .session-header {{
            display: flex;
            justify-content: space-between;
            align-items: center;
            margin-bottom: 20px;
        }}
        
        .session-title {{
            font-size: 1.5em;
            color: #333;
            font-weight: bold;
        }}
        
        .session-meta {{
            display: flex;
            gap: 15px;
        }}
        
        .badge {{
            padding: 5px 15px;
            border-radius: 20px;
            font-size: 0.85em;
            font-weight: 600;
        }}
        
        .badge-duration {{
            background: #e3f2fd;
            color: #1976d2;
        }}
        
        .badge-difficulty {{
            background: #fff3e0;
            color: #f57c00;
        }}
        
        .badge-beginner {{ background: #c8e6c9; color: #388e3c; }}
        .badge-intermediate {{ background: #fff3e0; color: #f57c00; }}
        .badge-advanced {{ background: #ffcdd2; color: #d32f2f; }}
        
        .objectives {{
            background: white;
            padding: 15px;
            border-radius: 8px;
            margin-bottom: 20px;
        }}
        
        .objectives h4 {{
            color: #667eea;
            margin-bottom: 10px;
        }}
        
        .objectives ul {{
            list-style-position: inside;
            color: #555;
        }}
        
        .objectives li {{
            padding: 5px 0;
        }}
        
        .skills {{
            display: grid;
            gap: 20px;
        }}
        
        .skill {{
            background: white;
            border-radius: 10px;
            padding: 20px;
            box-shadow: 0 2px 5px rgba(0,0,0,0.1);
        }}
        
        .skill-name {{
            font-size: 1.2em;
            font-weight: bold;
            color: #667eea;
            margin-bottom: 15px;
            text-transform: capitalize;
        }}
        
        .resources {{
            display: grid;
            gap: 10px;
        }}
        
        .resource {{
            background: #f8f9fa;
            padding: 15px;
            border-radius: 8px;
            border-left: 4px solid #667eea;
            transition: transform 0.2s;
        }}
        
        .resource:hover {{
            transform: translateX(5px);
            box-shadow: 0 2px 8px rgba(0,0,0,0.1);
        }}
        
        .resource-header {{
            display: flex;
            justify-content: space-between;
            align-items: start;
            margin-bottom: 8px;
        }}
        
        .resource-title {{
            font-weight: 600;
            color: #333;
            flex: 1;
        }}
        
        .resource-title a {{
            color: #667eea;
            text-decoration: none;
        }}
        
        .resource-title a:hover {{
            text-decoration: underline;
        }}
        
        .resource-type {{
            background: #667eea;
            color: white;
            padding: 3px 10px;
            border-radius: 15px;
            font-size: 0.75em;
            font-weight: 600;
            text-transform: uppercase;
            margin-left: 10px;
        }}
        
        .resource-type.course {{ background: #4caf50; }}
        .resource-type.video {{ background: #f44336; }}
        .resource-type.documentation {{ background: #2196f3; }}
        .resource-type.repository {{ background: #9c27b0; }}
        .resource-type.practice {{ background: #ff9800; }}
        
        .resource-provider {{
            font-size: 0.85em;
            color: #666;
            margin-bottom: 5px;
        }}
        
        .resource-description {{
            font-size: 0.9em;
            color: #555;
            margin-top: 8px;
        }}
        
        .resource-meta {{
            display: flex;
            gap: 15px;
            margin-top: 8px;
            font-size: 0.85em;
            color: #777;
        }}
        
        .free-badge {{
            background: #4caf50;
            color: white;
            padding: 2px 8px;
            border-radius: 10px;
            font-size: 0.8em;
            font-weight: 600;
        }}
        
        .quality-score {{
            color: #ff9800;
        }}
        
        .footer {{
            background: #2c3e50;
            color: white;
            text-align: center;
            padding: 20px;
            margin-top: 40px;
        }}
        
        .no-resources {{
            padding: 20px;
            text-align: center;
            color: #999;
            font-style: italic;
        }}
        
        @media print {{
            body {{
                background: white;
            }}
            .container {{
                box-shadow: none;
            }}
        }}
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h1>🎓 Your Personalized Learning Journey</h1>
            <p>Generated by GenMentor AI - {datetime.now().strftime("%B %d, %Y")}</p>
        </div>
        
        <div class="summary">
            <div class="summary-card">
                <span class="number">{len(sessions)}</span>
                <span class="label">Learning Sessions</span>
            </div>
            <div class="summary-card">
                <span class="number">{total_hours}</span>
                <span class="label">Total Hours</span>
            </div>
            <div class="summary-card">
                <span class="number">{skill_gap['skills_to_learn']}</span>
                <span class="label">Skills to Learn</span>
            </div>
            <div class="summary-card">
                <span class="number">{sum(len(s['skills']) for s in sessions)}</span>
                <span class="label">Skills with Resources</span>
            </div>
        </div>
        
        <div class="content">
            <div class="section">
                <h2>📋 Your Profile</h2>
                <div style="background: #f8f9fa; padding: 20px; border-radius: 10px;">
                    <p style="margin-bottom: 10px;"><strong>Goal:</strong> {goal}</p>
                    <p style="margin-bottom: 10px;"><strong>Current Skills:</strong> {', '.join(current_skills) if current_skills else 'Starting fresh'}</p>
                </div>
                <div class="occupation-match">
                    🎯 <strong>Best Match:</strong> {skill_gap['matched_occupation']}
                </div>
            </div>
            
            <div class="section">
                <h2>🚀 Your Learning Path</h2>
"""
    
    # Add each session
    for session in sessions:
        difficulty_class = f"badge-{session['difficulty'].lower()}"
        
        html += f"""
                <div class="session">
                    <div class="session-header">
                        <div class="session-title">
                            Session {session['session_number']}: {session['title']}
                        </div>
                        <div class="session-meta">
                            <span class="badge badge-duration">⏱️ {session['duration']} hours</span>
                            <span class="badge {difficulty_class}">📊 {session['difficulty']}</span>
                        </div>
                    </div>
"""
        
        # Add objectives if available
        if session.get('objectives'):
            html += """
                    <div class="objectives">
                        <h4>Learning Objectives:</h4>
                        <ul>
"""
            for obj in session['objectives'][:5]:  # Limit to 5 objectives
                html += f"                            <li>{obj}</li>\n"
            html += """                        </ul>
                    </div>
"""
        
        # Add skills and resources
        html += """
                    <div class="skills">
"""
        
        for skill in session['skills']:
            html += f"""
                        <div class="skill">
                            <div class="skill-name">📚 {skill['name']}</div>
                            <div class="resources">
"""
            
            if skill['resources']:
                for resource in skill['resources']:
                    resource_type = resource.get('type', 'resource')
                    provider = resource.get('provider', 'Unknown')
                    description = resource.get('description', '')
                    is_free = resource.get('is_free', False)
                    quality_score = resource.get('quality_score', 0)
                    stars = resource.get('stars', 0)
                    title = resource.get('title', 'Resource')
                    url = resource.get('url') or resource.get('resource_url', '#')
                    
                    html += f"""
                                <div class="resource">
                                    <div class="resource-header">
                                        <div class="resource-title">
                                            <a href="{url}" target="_blank">{title}</a>
                                        </div>
                                        <span class="resource-type {resource_type}">{resource_type}</span>
                                    </div>
                                    <div class="resource-provider">📍 Provider: {provider}</div>
"""
                    
                    if description:
                        html += f"""                                    <div class="resource-description">{description}</div>\n"""
                    
                    html += """                                    <div class="resource-meta">
"""
                    
                    if is_free:
                        html += """                                        <span class="free-badge">FREE</span>\n"""
                    
                    if quality_score > 0:
                        html += f"""                                        <span class="quality-score">⭐ Quality: {quality_score:.2f}</span>\n"""
                    
                    if stars > 0:
                        html += f"""                                        <span>⭐ {stars:,} stars</span>\n"""
                    
                    html += """                                    </div>
                                </div>
"""
            else:
                html += """
                                <div class="no-resources">
                                    No resources available yet. Check back soon!
                                </div>
"""
            
            html += """
                            </div>
                        </div>
"""
        
        html += """
                    </div>
                </div>
"""
    
    # Close HTML
    html += f"""
            </div>
        </div>
        
        <div class="footer">
            <p>Generated by <strong>GenMentor AI</strong> - Your Personalized Learning Companion</p>
            <p style="margin-top: 5px; opacity: 0.8;">Start your journey today and achieve your career goals! 🚀</p>
        </div>
    </div>
</body>
</html>
"""
    
    return html

if __name__ == "__main__":
    # Example usage
    goal = "I want to become a data scientist"
    current_skills = ["Marketing", "Excel", "Presentation"]
    
    # You can customize these:
    # goal = input("What's your career goal? ")
    # skills_input = input("What skills do you already have? (comma-separated) ")
    # current_skills = [s.strip() for s in skills_input.split(',')] if skills_input else []
    
    filename = generate_complete_learning_page(goal, current_skills)
    
    print(f"\n💡 Tip: Right-click the file and select 'Open with' → Your preferred browser")
    print(f"     Or drag and drop the file into your browser window!")
