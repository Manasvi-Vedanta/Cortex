"""
High-Quality Learning Path Generator
Creates a professional, working webpage with proper resources and calculation
"""

import json
from datetime import datetime
from ai_engine import GenMentorAI
from improved_resource_curator import ImprovedResourceCurator
import sys
import io

# Fix encoding
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')

def generate_proper_learning_page(goal, current_skills):
    """Generate a high-quality learning path with validated resources."""
    
    print("=" * 80)
    print("GENMENTOR - HIGH-QUALITY LEARNING PATH GENERATOR")
    print("=" * 80)
    print(f"\nGoal: {goal}")
    print(f"Current Skills: {', '.join(current_skills) if current_skills else 'None'}\n")
    
    # Initialize
    ai_engine = GenMentorAI()
    resource_curator = ImprovedResourceCurator()
    
    # Step 1: Skill Gap Analysis
    print("[1/4] Analyzing skill gap and matching occupation...")
    skill_gap = ai_engine.identify_skill_gap(goal, current_skills)
    
    matched_occ = skill_gap['matched_occupation']
    print(f"  ✓ Best Match: {matched_occ['label']}")
    print(f"  ✓ Similarity: {matched_occ['similarity_score']*100:.1f}%")
    print(f"  ✓ Skills to Learn: {skill_gap['skills_to_learn']}")
    
    # Step 2: Generate Learning Path
    print("\n[2/4] Generating structured learning path...")
    # Limit to 12 skills for quality
    limited_skills = skill_gap['skill_gap'][:12]
    learning_path = ai_engine.schedule_learning_path(limited_skills)
    
    # Calculate total hours properly
    total_hours = 0
    for session in learning_path:
        duration = session.get('estimated_duration_hours', 0) or session.get('duration', 0)
        if duration:
            total_hours += duration
    
    print(f"  ✓ Sessions: {len(learning_path)}")
    print(f"  ✓ Total Duration: {total_hours} hours ({total_hours/40:.1f} weeks at 40hrs/week)")
    
    # Step 3: Curate Quality Resources
    print("\n[3/4] Curating high-quality learning resources...")
    sessions_with_resources = []
    total_resources = 0
    
    for i, session in enumerate(learning_path, 1):
        title = session.get('title', f'Session {i}')
        duration = session.get('estimated_duration_hours', 0) or session.get('duration', 0)
        difficulty = session.get('difficulty_level', 'intermediate')
        objectives = session.get('objectives', [])[:4]  # Limit objectives
        
        print(f"\n  Session {i}: {title}")
        print(f"    Duration: {duration}h | Difficulty: {difficulty}")
        
        session_data = {
            'session_number': i,
            'title': title,
            'duration': duration,
            'difficulty': difficulty,
            'objectives': objectives,
            'skills': []
        }
        
        # Get skills (limit to 4 per session for quality)
        skills_list = session.get('skills', []) or session.get('skills_covered', [])
        for skill_uri in skills_list[:4]:
            skill_name = skill_uri.split('/')[-1].replace('_', ' ').replace('-', ' ')
            
            # Search for resources
            resources = resource_curator.search_resources(skill_name, limit=6)
            
            # Validate resources
            valid_resources = []
            for res in resources:
                if res.get('url') or res.get('resource_url'):
                    # Ensure URL is present
                    url = res.get('url') or res.get('resource_url')
                    if url and url != '#' and url.startswith('http'):
                        valid_resources.append({
                            'title': res.get('title', 'Resource'),
                            'url': url,
                            'type': res.get('type', 'resource'),
                            'provider': res.get('provider', 'Web'),
                            'description': res.get('description', ''),
                            'is_free': res.get('is_free', True),
                            'quality_score': res.get('quality_score', 0.5),
                            'stars': res.get('stars', 0)
                        })
            
            if valid_resources:
                skill_data = {
                    'name': skill_name.title(),
                    'uri': skill_uri,
                    'resources': valid_resources
                }
                session_data['skills'].append(skill_data)
                total_resources += len(valid_resources)
                print(f"      ✓ {skill_name.title()}: {len(valid_resources)} resources")
            else:
                print(f"      ⚠ {skill_name.title()}: No quality resources found (skipped)")
        
        if session_data['skills']:  # Only add if has resources
            sessions_with_resources.append(session_data)
    
    print(f"\n  Total Quality Resources: {total_resources}")
    print(f"  Sessions with Resources: {len(sessions_with_resources)}")
    
    # Step 4: Generate HTML
    print("\n[4/4] Generating professional webpage...")
    html = generate_professional_html(
        goal, 
        current_skills, 
        matched_occ,
        skill_gap,
        sessions_with_resources, 
        total_hours
    )
    
    # Save
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"professional_learning_path_{timestamp}.html"
    
    with open(filename, 'w', encoding='utf-8') as f:
        f.write(html)
    
    # Also save as JSON
    json_filename = f"professional_learning_path_{timestamp}.json"
    with open(json_filename, 'w', encoding='utf-8') as f:
        json.dump({
            'goal': goal,
            'current_skills': current_skills,
            'matched_occupation': matched_occ,
            'total_hours': total_hours,
            'sessions': sessions_with_resources
        }, f, indent=2, ensure_ascii=False)
    
    print("\n" + "=" * 80)
    print("SUCCESS!")
    print("=" * 80)
    print(f"\nHTML File: {filename}")
    print(f"JSON File: {json_filename}")
    print(f"\nTotal Resources: {total_resources}")
    print(f"Total Duration: {total_hours} hours")
    print(f"Sessions: {len(sessions_with_resources)}")
    print("\nOpen the HTML file in your browser to view your learning path!")
    print("=" * 80)
    
    return filename

def generate_professional_html(goal, current_skills, matched_occ, skill_gap, sessions, total_hours):
    """Generate a professional, working HTML page."""
    
    occupation_name = matched_occ.get('label', 'Professional')
    occupation_desc = matched_occ.get('description', '')
    similarity = matched_occ.get('similarity_score', 0) * 100
    
    total_resources = sum(len(skill['resources']) for session in sessions for skill in session['skills'])
    total_skills = sum(len(session['skills']) for session in sessions)
    
    html = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Learning Path: {occupation_name.title()} - GenMentor</title>
    <style>
        * {{
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }}
        
        body {{
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Oxygen, Ubuntu, Cantarell, sans-serif;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            min-height: 100vh;
            padding: 20px;
            line-height: 1.6;
        }}
        
        .container {{
            max-width: 1400px;
            margin: 0 auto;
            background: white;
            border-radius: 20px;
            box-shadow: 0 20px 60px rgba(0,0,0,0.4);
            overflow: hidden;
        }}
        
        .header {{
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            padding: 60px 40px;
            text-align: center;
            position: relative;
        }}
        
        .header::before {{
            content: '';
            position: absolute;
            top: 0;
            left: 0;
            right: 0;
            bottom: 0;
            background: url('data:image/svg+xml,<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1440 320"><path fill="rgba(255,255,255,0.1)" d="M0,96L48,112C96,128,192,160,288,160C384,160,480,128,576,112C672,96,768,96,864,112C960,128,1056,160,1152,160C1248,160,1344,128,1392,112L1440,96L1440,320L1392,320C1344,320,1248,320,1152,320C1056,320,960,320,864,320C768,320,672,320,576,320C480,320,384,320,288,320C192,320,96,320,48,320L0,320Z"></path></svg>') bottom center no-repeat;
            opacity: 0.3;
        }}
        
        .header-content {{
            position: relative;
            z-index: 1;
        }}
        
        .header h1 {{
            font-size: 3em;
            margin-bottom: 15px;
            font-weight: 700;
            text-shadow: 0 2px 10px rgba(0,0,0,0.2);
        }}
        
        .header .subtitle {{
            font-size: 1.3em;
            opacity: 0.95;
            font-weight: 300;
        }}
        
        .header .date {{
            margin-top: 10px;
            font-size: 0.9em;
            opacity: 0.8;
        }}
        
        .stats {{
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
            gap: 0;
            background: #f8f9fa;
            border-bottom: 3px solid #e9ecef;
        }}
        
        .stat-card {{
            text-align: center;
            padding: 30px 20px;
            background: white;
            border-right: 1px solid #e9ecef;
            transition: all 0.3s;
        }}
        
        .stat-card:last-child {{
            border-right: none;
        }}
        
        .stat-card:hover {{
            background: #f8f9fa;
            transform: translateY(-2px);
        }}
        
        .stat-card .icon {{
            font-size: 2.5em;
            margin-bottom: 10px;
        }}
        
        .stat-card .number {{
            font-size: 2.8em;
            font-weight: 700;
            color: #667eea;
            display: block;
            line-height: 1;
        }}
        
        .stat-card .label {{
            color: #666;
            font-size: 0.95em;
            margin-top: 8px;
            font-weight: 500;
        }}
        
        .content {{
            padding: 50px 40px;
        }}
        
        .profile-section {{
            background: linear-gradient(135deg, #f5f7fa 0%, #c3cfe2 100%);
            border-radius: 15px;
            padding: 30px;
            margin-bottom: 40px;
            border-left: 5px solid #667eea;
        }}
        
        .profile-section h2 {{
            color: #333;
            margin-bottom: 20px;
            font-size: 1.8em;
        }}
        
        .profile-item {{
            background: white;
            padding: 20px;
            border-radius: 10px;
            margin-bottom: 15px;
            box-shadow: 0 2px 5px rgba(0,0,0,0.1);
        }}
        
        .profile-item strong {{
            color: #667eea;
            display: block;
            margin-bottom: 8px;
            font-size: 1.1em;
        }}
        
        .profile-item p {{
            color: #555;
            line-height: 1.8;
        }}
        
        .match-badge {{
            display: inline-block;
            background: linear-gradient(135deg, #11998e 0%, #38ef7d 100%);
            color: white;
            padding: 8px 20px;
            border-radius: 25px;
            font-weight: 600;
            margin-top: 10px;
            font-size: 1.1em;
        }}
        
        .section-title {{
            color: #333;
            font-size: 2.2em;
            margin: 50px 0 30px 0;
            padding-bottom: 15px;
            border-bottom: 4px solid #667eea;
            font-weight: 700;
        }}
        
        .session {{
            background: #ffffff;
            border-radius: 20px;
            padding: 0;
            margin-bottom: 40px;
            box-shadow: 0 10px 30px rgba(0,0,0,0.1);
            overflow: hidden;
            border: 1px solid #e9ecef;
            transition: all 0.3s;
        }}
        
        .session:hover {{
            box-shadow: 0 15px 40px rgba(0,0,0,0.15);
            transform: translateY(-5px);
        }}
        
        .session-header {{
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            padding: 30px 35px;
            display: flex;
            justify-content: space-between;
            align-items: center;
            flex-wrap: wrap;
            gap: 15px;
        }}
        
        .session-number {{
            background: rgba(255,255,255,0.2);
            width: 50px;
            height: 50px;
            border-radius: 50%;
            display: flex;
            align-items: center;
            justify-content: center;
            font-size: 1.5em;
            font-weight: 700;
            margin-right: 20px;
        }}
        
        .session-title {{
            flex: 1;
            font-size: 1.8em;
            font-weight: 600;
        }}
        
        .session-badges {{
            display: flex;
            gap: 12px;
            flex-wrap: wrap;
        }}
        
        .badge {{
            padding: 8px 18px;
            border-radius: 25px;
            font-size: 0.9em;
            font-weight: 600;
            display: flex;
            align-items: center;
            gap: 6px;
            white-space: nowrap;
        }}
        
        .badge-duration {{
            background: rgba(255,255,255,0.95);
            color: #667eea;
        }}
        
        .badge-difficulty {{
            background: rgba(255,255,255,0.95);
        }}
        
        .badge-difficulty.beginner {{ color: #38ef7d; }}
        .badge-difficulty.intermediate {{ color: #f59e0b; }}
        .badge-difficulty.advanced {{ color: #ef4444; }}
        
        .session-body {{
            padding: 35px;
        }}
        
        .objectives {{
            background: #f8f9fa;
            padding: 25px;
            border-radius: 12px;
            margin-bottom: 30px;
            border-left: 4px solid #667eea;
        }}
        
        .objectives h4 {{
            color: #667eea;
            margin-bottom: 15px;
            font-size: 1.3em;
            font-weight: 600;
        }}
        
        .objectives ul {{
            list-style: none;
            padding: 0;
        }}
        
        .objectives li {{
            padding: 10px 0;
            padding-left: 30px;
            position: relative;
            color: #555;
        }}
        
        .objectives li::before {{
            content: '✓';
            position: absolute;
            left: 0;
            color: #38ef7d;
            font-weight: bold;
            font-size: 1.2em;
        }}
        
        .skills-grid {{
            display: grid;
            gap: 25px;
        }}
        
        .skill-card {{
            background: #f8f9fa;
            border-radius: 15px;
            padding: 25px;
            border: 2px solid #e9ecef;
            transition: all 0.3s;
        }}
        
        .skill-card:hover {{
            border-color: #667eea;
            box-shadow: 0 5px 15px rgba(102, 126, 234, 0.1);
        }}
        
        .skill-name {{
            font-size: 1.5em;
            font-weight: 600;
            color: #667eea;
            margin-bottom: 20px;
            display: flex;
            align-items: center;
            gap: 10px;
        }}
        
        .resources-list {{
            display: grid;
            gap: 15px;
        }}
        
        .resource-item {{
            background: white;
            padding: 20px;
            border-radius: 10px;
            border-left: 4px solid #667eea;
            transition: all 0.3s;
            display: flex;
            flex-direction: column;
            gap: 10px;
        }}
        
        .resource-item:hover {{
            transform: translateX(8px);
            box-shadow: 0 5px 15px rgba(0,0,0,0.1);
        }}
        
        .resource-header {{
            display: flex;
            justify-content: space-between;
            align-items: start;
            gap: 15px;
        }}
        
        .resource-title {{
            flex: 1;
        }}
        
        .resource-title a {{
            color: #333;
            text-decoration: none;
            font-weight: 600;
            font-size: 1.1em;
            transition: color 0.3s;
        }}
        
        .resource-title a:hover {{
            color: #667eea;
            text-decoration: underline;
        }}
        
        .resource-type-badge {{
            padding: 5px 12px;
            border-radius: 20px;
            font-size: 0.75em;
            font-weight: 700;
            text-transform: uppercase;
            letter-spacing: 0.5px;
            color: white;
        }}
        
        .resource-type-badge.course {{ background: linear-gradient(135deg, #11998e 0%, #38ef7d 100%); }}
        .resource-type-badge.video {{ background: linear-gradient(135deg, #eb3349 0%, #f45c43 100%); }}
        .resource-type-badge.documentation {{ background: linear-gradient(135deg, #2196f3 0%, #21cbf3 100%); }}
        .resource-type-badge.repository {{ background: linear-gradient(135deg, #9c27b0 0%, #ba68c8 100%); }}
        .resource-type-badge.practice {{ background: linear-gradient(135deg, #f59e0b 0%, #fbbf24 100%); }}
        .resource-type-badge.tutorial {{ background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); }}
        
        .resource-provider {{
            color: #666;
            font-size: 0.9em;
            display: flex;
            align-items: center;
            gap: 5px;
        }}
        
        .resource-description {{
            color: #555;
            font-size: 0.95em;
            line-height: 1.6;
        }}
        
        .resource-meta {{
            display: flex;
            gap: 15px;
            flex-wrap: wrap;
            align-items: center;
            font-size: 0.9em;
        }}
        
        .meta-badge {{
            padding: 4px 10px;
            border-radius: 15px;
            font-weight: 600;
            font-size: 0.85em;
            display: flex;
            align-items: center;
            gap: 4px;
        }}
        
        .meta-badge.free {{
            background: #d1fae5;
            color: #065f46;
        }}
        
        .meta-badge.quality {{
            background: #fef3c7;
            color: #92400e;
        }}
        
        .meta-badge.stars {{
            background: #dbeafe;
            color: #1e40af;
        }}
        
        .footer {{
            background: #2c3e50;
            color: white;
            text-align: center;
            padding: 40px;
        }}
        
        .footer h3 {{
            margin-bottom: 10px;
            font-size: 1.5em;
        }}
        
        .footer p {{
            opacity: 0.9;
            line-height: 1.8;
        }}
        
        .no-resources {{
            text-align: center;
            padding: 30px;
            color: #999;
            font-style: italic;
        }}
        
        @media (max-width: 768px) {{
            .header h1 {{
                font-size: 2em;
            }}
            
            .stats {{
                grid-template-columns: repeat(2, 1fr);
            }}
            
            .session-header {{
                flex-direction: column;
                align-items: flex-start;
            }}
            
            .session-title {{
                font-size: 1.4em;
            }}
            
            .content {{
                padding: 30px 20px;
            }}
        }}
        
        @media print {{
            body {{
                background: white;
            }}
            
            .session {{
                page-break-inside: avoid;
            }}
        }}
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <div class="header-content">
                <h1>🎓 Your Learning Journey</h1>
                <p class="subtitle">Personalized Path to Become a {occupation_name.title()}</p>
                <p class="date">Generated on {datetime.now().strftime("%B %d, %Y at %I:%M %p")}</p>
            </div>
        </div>
        
        <div class="stats">
            <div class="stat-card">
                <div class="icon">📚</div>
                <span class="number">{len(sessions)}</span>
                <span class="label">Learning Sessions</span>
            </div>
            <div class="stat-card">
                <div class="icon">⏱️</div>
                <span class="number">{total_hours}</span>
                <span class="label">Total Hours</span>
            </div>
            <div class="stat-card">
                <div class="icon">🎯</div>
                <span class="number">{total_skills}</span>
                <span class="label">Skills to Master</span>
            </div>
            <div class="stat-card">
                <div class="icon">🔗</div>
                <span class="number">{total_resources}</span>
                <span class="label">Quality Resources</span>
            </div>
        </div>
        
        <div class="content">
            <div class="profile-section">
                <h2>👤 Your Profile</h2>
                <div class="profile-item">
                    <strong>🎯 Career Goal</strong>
                    <p>{goal}</p>
                </div>
                <div class="profile-item">
                    <strong>📋 Current Skills</strong>
                    <p>{', '.join(current_skills) if current_skills else 'Starting your journey from the beginning'}</p>
                </div>
                <div class="profile-item">
                    <strong>🎯 Best Career Match</strong>
                    <p><strong style="color: #667eea; font-size: 1.2em;">{occupation_name.title()}</strong></p>
                    <p style="margin-top: 8px;">{occupation_desc}</p>
                    <span class="match-badge">✓ {similarity:.1f}% Match</span>
                </div>
            </div>
            
            <h2 class="section-title">🚀 Your Learning Path</h2>
"""
    
    # Add sessions
    for session in sessions:
        session_num = session['session_number']
        title = session['title']
        duration = session['duration']
        difficulty = session['difficulty']
        objectives = session['objectives']
        
        html += f"""
            <div class="session">
                <div class="session-header">
                    <div style="display: flex; align-items: center;">
                        <div class="session-number">{session_num}</div>
                        <div class="session-title">{title}</div>
                    </div>
                    <div class="session-badges">
                        <span class="badge badge-duration">⏱️ {duration} hours</span>
                        <span class="badge badge-difficulty {difficulty}">📊 {difficulty.title()}</span>
                    </div>
                </div>
                
                <div class="session-body">
"""
        
        # Add objectives
        if objectives:
            html += """
                    <div class="objectives">
                        <h4>🎯 Learning Objectives</h4>
                        <ul>
"""
            for obj in objectives:
                html += f"                            <li>{obj}</li>\n"
            html += """                        </ul>
                    </div>
"""
        
        # Add skills and resources
        html += """
                    <div class="skills-grid">
"""
        
        for skill in session['skills']:
            skill_name = skill['name']
            resources = skill['resources']
            
            html += f"""
                        <div class="skill-card">
                            <div class="skill-name">📚 {skill_name}</div>
                            <div class="resources-list">
"""
            
            for res in resources:
                res_type = res['type']
                provider = res['provider']
                title_text = res['title']
                url = res['url']
                description = res.get('description', '')
                is_free = res.get('is_free', False)
                quality = res.get('quality_score', 0)
                stars = res.get('stars', 0)
                
                html += f"""
                                <div class="resource-item">
                                    <div class="resource-header">
                                        <div class="resource-title">
                                            <a href="{url}" target="_blank" rel="noopener noreferrer">{title_text}</a>
                                        </div>
                                        <span class="resource-type-badge {res_type}">{res_type}</span>
                                    </div>
                                    <div class="resource-provider">📍 {provider}</div>
"""
                
                if description:
                    html += f"""                                    <div class="resource-description">{description}</div>\n"""
                
                html += """                                    <div class="resource-meta">
"""
                
                if is_free:
                    html += """                                        <span class="meta-badge free">✓ FREE</span>\n"""
                
                if quality > 0:
                    html += f"""                                        <span class="meta-badge quality">⭐ Quality: {quality:.2f}</span>\n"""
                
                if stars > 0:
                    html += f"""                                        <span class="meta-badge stars">⭐ {stars:,} stars</span>\n"""
                
                html += """                                    </div>
                                </div>
"""
            
            html += """
                            </div>
                        </div>
"""
        
        html += """
                    </div>
                </div>
            </div>
"""
    
    # Footer
    html += f"""
        </div>
        
        <div class="footer">
            <h3>🎓 GenMentor AI</h3>
            <p>Your personalized learning companion powered by artificial intelligence</p>
            <p style="margin-top: 15px;">Ready to start your journey? Click on any resource link to begin learning!</p>
            <p style="margin-top: 10px; font-size: 0.9em; opacity: 0.8;">
                Total Learning Time: {total_hours} hours (~{total_hours/40:.1f} weeks at full-time)
            </p>
        </div>
    </div>
</body>
</html>
"""
    
    return html

if __name__ == "__main__":
    # High-quality example
    goal = "I want to become a data scientist"
    current_skills = ["Marketing", "Excel", "Basic Statistics"]
    
    generate_proper_learning_page(goal, current_skills)
