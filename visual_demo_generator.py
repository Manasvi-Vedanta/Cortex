"""
Visual Demo Generator for GenMentor System
Creates professional webpages for multiple use cases to demonstrate system capabilities
"""

import os
import json
import time
from datetime import datetime
from ai_engine import GenMentorAI
from improved_resource_curator import ImprovedResourceCurator
import sys
import io

# Fix encoding
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')


class VisualDemoGenerator:
    """Generate professional demonstration webpages for various use cases."""
    
    def __init__(self, output_dir="demo_outputs"):
        self.output_dir = output_dir
        self.ai_engine = GenMentorAI()
        self.resource_curator = ImprovedResourceCurator()
        
        # Create output directory
        if not os.path.exists(output_dir):
            os.makedirs(output_dir)
            print(f"✓ Created output directory: {output_dir}")
    
    def get_showcase_cases(self):
        """Get diverse showcase cases for visual demonstration."""
        return [
            {
                'id': 'demo_01',
                'title': 'Marketing Professional to Data Scientist',
                'goal': 'I am a marketing professional with 5 years of experience and I want to transition to data science',
                'current_skills': ['Marketing Analytics', 'Excel', 'Google Analytics', 'Basic Statistics', 'Presentation Skills'],
                'description': 'Career transition from marketing to technical role',
                'category': 'Career Transition'
            },
            {
                'id': 'demo_02',
                'title': 'Software Engineer to Machine Learning Engineer',
                'goal': 'I am a software engineer who wants to specialize in machine learning and AI',
                'current_skills': ['Python', 'Java', 'Git', 'Algorithms', 'Data Structures', 'REST APIs'],
                'description': 'Technical specialization within software engineering',
                'category': 'Career Advancement'
            },
            {
                'id': 'demo_03',
                'title': 'Complete Beginner to Web Developer',
                'goal': 'I want to become a full-stack web developer and build modern web applications',
                'current_skills': ['Basic Computer Skills', 'HTML Basics'],
                'description': 'Starting from scratch in web development',
                'category': 'Beginner Journey'
            },
            {
                'id': 'demo_04',
                'title': 'Finance Analyst to Data Engineer',
                'goal': 'I work in finance and want to become a data engineer working with big data systems',
                'current_skills': ['Excel', 'SQL', 'Financial Modeling', 'VBA', 'Python Basics'],
                'description': 'Cross-domain transition with technical skills',
                'category': 'Career Transition'
            },
            {
                'id': 'demo_05',
                'title': 'Junior Developer to Senior Software Engineer',
                'goal': 'I am a junior developer and want to advance to senior software engineer level',
                'current_skills': ['JavaScript', 'React', 'Node.js', 'Git', 'MongoDB', 'REST APIs'],
                'description': 'Career progression within same role',
                'category': 'Career Advancement'
            },
            {
                'id': 'demo_06',
                'title': 'IT Support to Cybersecurity Specialist',
                'goal': 'I work in IT support and want to specialize in cybersecurity and network security',
                'current_skills': ['Windows Administration', 'Networking Basics', 'Troubleshooting', 'Linux Basics'],
                'description': 'Specialization in security domain',
                'category': 'Tech Specialization'
            },
            {
                'id': 'demo_07',
                'title': 'Data Analyst to Business Intelligence Specialist',
                'goal': 'I want to advance from data analyst to business intelligence specialist role',
                'current_skills': ['SQL', 'Excel', 'Tableau', 'Power BI', 'Statistics', 'Data Visualization'],
                'description': 'Natural career progression in analytics',
                'category': 'Career Advancement'
            },
            {
                'id': 'demo_08',
                'title': 'Teacher to UX/UI Designer',
                'goal': 'I am a teacher who wants to transition into UX/UI design and product design',
                'current_skills': ['Communication', 'Presentation', 'Basic Design', 'User Research'],
                'description': 'Creative career transition',
                'category': 'Career Transition'
            },
            {
                'id': 'demo_09',
                'title': 'Cloud Engineer AWS Specialist',
                'goal': 'I want to become an AWS cloud architect and design scalable cloud solutions',
                'current_skills': ['Linux', 'Docker', 'Networking', 'Basic AWS', 'Python'],
                'description': 'Cloud specialization focus',
                'category': 'Tech Specialization'
            },
            {
                'id': 'demo_10',
                'title': 'DevOps Engineer Journey',
                'goal': 'I want to become a DevOps engineer working with CI/CD and infrastructure automation',
                'current_skills': ['Linux', 'Git', 'Python', 'Bash Scripting', 'Docker'],
                'description': 'Modern DevOps role preparation',
                'category': 'Tech Specialization'
            },
            {
                'id': 'demo_11',
                'title': 'AI Research Scientist',
                'goal': 'I want to become an AI research scientist working on cutting-edge AI models',
                'current_skills': ['Python', 'Machine Learning', 'Deep Learning', 'Mathematics', 'Statistics', 'PyTorch'],
                'description': 'Advanced AI research path',
                'category': 'Advanced Tech'
            },
            {
                'id': 'demo_12',
                'title': 'Mobile App Developer (iOS & Android)',
                'goal': 'I want to develop mobile applications for both iOS and Android platforms',
                'current_skills': ['Programming Basics', 'UI Design', 'JavaScript'],
                'description': 'Mobile development specialization',
                'category': 'Tech Specialization'
            }
        ]
    
    def generate_demo_page(self, demo_case):
        """Generate a professional demo page for a specific use case."""
        
        demo_id = demo_case['id']
        title = demo_case['title']
        goal = demo_case['goal']
        current_skills = demo_case['current_skills']
        description = demo_case['description']
        category = demo_case['category']
        
        print(f"\n{'='*100}")
        print(f"Generating Demo: {title}")
        print(f"{'='*100}")
        print(f"Goal: {goal}")
        print(f"Skills: {', '.join(current_skills)}")
        
        # Step 1: Skill Gap Analysis
        print(f"\n[1/3] Analyzing skill gap...")
        try:
            skill_gap = self.ai_engine.identify_skill_gap(goal, current_skills)
            matched_occ = skill_gap['matched_occupation']
            
            print(f"  ✓ Matched: {matched_occ['label']} ({matched_occ['similarity_score']*100:.1f}% match)")
            print(f"  ✓ Skills needed: {skill_gap['skills_to_learn']}")
        except Exception as e:
            print(f"  ✗ Error: {str(e)}")
            return None
        
        # Step 2: Generate Learning Path
        print(f"\n[2/3] Generating learning path...")
        try:
            limited_skills = skill_gap['skill_gap'][:12]
            learning_path = self.ai_engine.schedule_learning_path(limited_skills)
            
            total_hours = sum(s.get('estimated_duration_hours', 0) or s.get('duration', 0) 
                            for s in learning_path)
            
            print(f"  ✓ Sessions: {len(learning_path)}")
            print(f"  ✓ Duration: {total_hours} hours")
        except Exception as e:
            print(f"  ✗ Error: {str(e)}")
            return None
        
        # Step 3: Curate Resources
        print(f"\n[3/3] Curating resources...")
        sessions_with_resources = []
        total_resources = 0
        
        for i, session in enumerate(learning_path, 1):
            session_title = session.get('title', f'Session {i}')
            duration = session.get('estimated_duration_hours', 0) or session.get('duration', 0)
            difficulty = session.get('difficulty_level', 'intermediate')
            objectives = session.get('objectives', [])[:4]
            
            session_data = {
                'session_number': i,
                'title': session_title,
                'duration': duration,
                'difficulty': difficulty,
                'objectives': objectives,
                'skills': []
            }
            
            skills_list = session.get('skills', []) or session.get('skills_covered', [])
            for skill_uri in skills_list[:4]:
                skill_name = skill_uri.split('/')[-1].replace('_', ' ').replace('-', ' ')
                resources = self.resource_curator.search_resources(skill_name, limit=6)
                
                valid_resources = []
                for res in resources:
                    url = res.get('url') or res.get('resource_url')
                    if url and url.startswith('http'):
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
                    session_data['skills'].append({
                        'name': skill_name.title(),
                        'uri': skill_uri,
                        'resources': valid_resources
                    })
                    total_resources += len(valid_resources)
            
            if session_data['skills']:
                sessions_with_resources.append(session_data)
        
        print(f"  ✓ Resources: {total_resources}")
        print(f"  ✓ Sessions with resources: {len(sessions_with_resources)}")
        
        # Generate HTML
        html = self.generate_html(
            demo_id, title, description, category, goal, current_skills,
            matched_occ, skill_gap, sessions_with_resources, total_hours
        )
        
        # Save files
        html_filename = os.path.join(self.output_dir, f"{demo_id}.html")
        with open(html_filename, 'w', encoding='utf-8') as f:
            f.write(html)
        
        # Save JSON metadata
        json_data = {
            'id': demo_id,
            'title': title,
            'description': description,
            'category': category,
            'goal': goal,
            'current_skills': current_skills,
            'matched_occupation': matched_occ,
            'total_hours': total_hours,
            'total_sessions': len(sessions_with_resources),
            'total_resources': total_resources,
            'generated_at': datetime.now().isoformat()
        }
        
        json_filename = os.path.join(self.output_dir, f"{demo_id}.json")
        with open(json_filename, 'w', encoding='utf-8') as f:
            json.dump(json_data, f, indent=2, ensure_ascii=False)
        
        print(f"\n✓ Generated: {html_filename}")
        
        return {
            'html_file': html_filename,
            'json_file': json_filename,
            'stats': json_data
        }
    
    def generate_html(self, demo_id, title, description, category, goal, current_skills,
                     matched_occ, skill_gap, sessions, total_hours):
        """Generate professional HTML page."""
        
        occupation_name = matched_occ.get('label', 'Professional')
        similarity = matched_occ.get('similarity_score', 0) * 100
        total_resources = sum(len(skill['resources']) for session in sessions for skill in session['skills'])
        total_skills = sum(len(session['skills']) for session in sessions)
        
        html = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{title} - GenMentor Learning Path</title>
    <style>
        * {{
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }}
        
        body {{
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Oxygen, Ubuntu, sans-serif;
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
        
        .demo-badge {{
            position: absolute;
            top: 20px;
            right: 20px;
            background: rgba(255,255,255,0.2);
            padding: 8px 20px;
            border-radius: 25px;
            font-size: 0.85em;
            font-weight: 600;
            backdrop-filter: blur(10px);
        }}
        
        .header h1 {{
            font-size: 2.5em;
            margin-bottom: 15px;
            font-weight: 700;
        }}
        
        .header .subtitle {{
            font-size: 1.2em;
            opacity: 0.95;
            font-weight: 300;
            margin-bottom: 10px;
        }}
        
        .header .category {{
            display: inline-block;
            background: rgba(255,255,255,0.25);
            padding: 8px 20px;
            border-radius: 25px;
            font-size: 0.9em;
            margin-top: 10px;
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
            background: rgba(255,255,255,0.95);
        }}
        
        .badge-duration {{ color: #667eea; }}
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
        }}
        
        .objectives ul {{
            list-style: none;
            padding: 0;
        }}
        
        .objectives li {{
            padding: 10px 0 10px 30px;
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
        
        .resource-title a {{
            color: #333;
            text-decoration: none;
            font-weight: 600;
            font-size: 1.1em;
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
            margin-top: 8px;
        }}
        
        .resource-description {{
            color: #555;
            font-size: 0.95em;
            line-height: 1.6;
            margin-top: 10px;
        }}
        
        .resource-meta {{
            display: flex;
            gap: 15px;
            flex-wrap: wrap;
            margin-top: 10px;
            font-size: 0.9em;
        }}
        
        .meta-badge {{
            padding: 4px 10px;
            border-radius: 15px;
            font-weight: 600;
            font-size: 0.85em;
        }}
        
        .meta-badge.free {{ background: #d1fae5; color: #065f46; }}
        .meta-badge.quality {{ background: #fef3c7; color: #92400e; }}
        .meta-badge.stars {{ background: #dbeafe; color: #1e40af; }}
        
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
        
        @media (max-width: 768px) {{
            .header h1 {{ font-size: 2em; }}
            .stats {{ grid-template-columns: repeat(2, 1fr); }}
            .content {{ padding: 30px 20px; }}
        }}
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <div class="demo-badge">DEMO {demo_id.upper()}</div>
            <h1>{title}</h1>
            <p class="subtitle">{description}</p>
            <span class="category">{category}</span>
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
                    <p>{', '.join(current_skills) if current_skills else 'Starting fresh'}</p>
                </div>
                <div class="profile-item">
                    <strong>🎯 Best Career Match</strong>
                    <p><strong style="color: #667eea; font-size: 1.2em;">{occupation_name.title()}</strong></p>
                    <span class="match-badge">✓ {similarity:.1f}% Match</span>
                </div>
            </div>
            
            <h2 class="section-title">🚀 Your Learning Path</h2>
"""
        
        # Add sessions
        for session in sessions:
            html += f"""
            <div class="session">
                <div class="session-header">
                    <div style="display: flex; align-items: center;">
                        <div class="session-number">{session['session_number']}</div>
                        <div class="session-title">{session['title']}</div>
                    </div>
                    <div class="session-badges">
                        <span class="badge badge-duration">⏱️ {session['duration']} hours</span>
                        <span class="badge badge-difficulty {session['difficulty']}">📊 {session['difficulty'].title()}</span>
                    </div>
                </div>
                
                <div class="session-body">
"""
            
            if session['objectives']:
                html += """
                    <div class="objectives">
                        <h4>🎯 Learning Objectives</h4>
                        <ul>
"""
                for obj in session['objectives']:
                    html += f"                            <li>{obj}</li>\n"
                html += """                        </ul>
                    </div>
"""
            
            html += """
                    <div class="skills-grid">
"""
            
            for skill in session['skills']:
                html += f"""
                        <div class="skill-card">
                            <div class="skill-name">📚 {skill['name']}</div>
                            <div class="resources-list">
"""
                
                for res in skill['resources']:
                    html += f"""
                                <div class="resource-item">
                                    <div class="resource-header">
                                        <div class="resource-title">
                                            <a href="{res['url']}" target="_blank" rel="noopener">{res['title']}</a>
                                        </div>
                                        <span class="resource-type-badge {res['type']}">{res['type']}</span>
                                    </div>
                                    <div class="resource-provider">📍 {res['provider']}</div>
"""
                    
                    if res.get('description'):
                        html += f"""                                    <div class="resource-description">{res['description']}</div>\n"""
                    
                    html += """                                    <div class="resource-meta">
"""
                    
                    if res.get('is_free'):
                        html += """                                        <span class="meta-badge free">✓ FREE</span>\n"""
                    if res.get('quality_score', 0) > 0:
                        html += f"""                                        <span class="meta-badge quality">⭐ {res['quality_score']:.2f}</span>\n"""
                    if res.get('stars', 0) > 0:
                        html += f"""                                        <span class="meta-badge stars">⭐ {res['stars']:,}</span>\n"""
                    
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
        
        html += f"""
        </div>
        
        <div class="footer">
            <h3>🎓 GenMentor AI</h3>
            <p>Personalized learning paths powered by artificial intelligence</p>
            <p style="margin-top: 15px;">Generated on {datetime.now().strftime("%B %d, %Y at %I:%M %p")}</p>
            <p style="margin-top: 10px; opacity: 0.8;">
                {total_hours} hours • {len(sessions)} sessions • {total_resources} resources
            </p>
        </div>
    </div>
</body>
</html>
"""
        
        return html
    
    def generate_index_page(self, demo_results):
        """Generate an index page linking to all demos."""
        
        html = """<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>GenMentor Visual Demos - Index</title>
    <style>
        * {
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }
        
        body {
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            min-height: 100vh;
            padding: 40px 20px;
        }
        
        .container {
            max-width: 1400px;
            margin: 0 auto;
        }
        
        .header {
            text-align: center;
            color: white;
            margin-bottom: 50px;
        }
        
        .header h1 {
            font-size: 3.5em;
            margin-bottom: 20px;
            text-shadow: 0 2px 10px rgba(0,0,0,0.2);
        }
        
        .header p {
            font-size: 1.3em;
            opacity: 0.9;
        }
        
        .stats-bar {
            background: rgba(255,255,255,0.15);
            backdrop-filter: blur(10px);
            border-radius: 15px;
            padding: 25px;
            margin: 30px 0;
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
            gap: 30px;
            text-align: center;
            color: white;
        }
        
        .stat-item .number {
            font-size: 3em;
            font-weight: 700;
            display: block;
        }
        
        .stat-item .label {
            font-size: 1.1em;
            opacity: 0.9;
            margin-top: 5px;
        }
        
        .demos-grid {
            display: grid;
            grid-template-columns: repeat(auto-fill, minmax(350px, 1fr));
            gap: 30px;
        }
        
        .demo-card {
            background: white;
            border-radius: 15px;
            overflow: hidden;
            box-shadow: 0 10px 30px rgba(0,0,0,0.2);
            transition: all 0.3s;
            text-decoration: none;
            color: inherit;
            display: block;
        }
        
        .demo-card:hover {
            transform: translateY(-10px);
            box-shadow: 0 20px 40px rgba(0,0,0,0.3);
        }
        
        .demo-header {
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            padding: 25px;
            position: relative;
        }
        
        .demo-id {
            position: absolute;
            top: 15px;
            right: 15px;
            background: rgba(255,255,255,0.2);
            padding: 5px 12px;
            border-radius: 15px;
            font-size: 0.8em;
            font-weight: 600;
        }
        
        .demo-header h3 {
            font-size: 1.5em;
            margin-bottom: 10px;
            padding-right: 80px;
        }
        
        .demo-category {
            background: rgba(255,255,255,0.2);
            display: inline-block;
            padding: 5px 15px;
            border-radius: 20px;
            font-size: 0.85em;
        }
        
        .demo-body {
            padding: 25px;
        }
        
        .demo-description {
            color: #666;
            margin-bottom: 20px;
            line-height: 1.6;
        }
        
        .demo-stats {
            display: grid;
            grid-template-columns: repeat(2, 1fr);
            gap: 15px;
            margin-top: 20px;
        }
        
        .demo-stat {
            text-align: center;
            padding: 15px;
            background: #f8f9fa;
            border-radius: 10px;
        }
        
        .demo-stat .value {
            font-size: 2em;
            font-weight: 700;
            color: #667eea;
            display: block;
        }
        
        .demo-stat .label {
            font-size: 0.9em;
            color: #666;
            margin-top: 5px;
        }
        
        .view-button {
            display: block;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            text-align: center;
            padding: 15px;
            border-radius: 10px;
            margin-top: 20px;
            font-weight: 600;
            transition: all 0.3s;
        }
        
        .view-button:hover {
            transform: scale(1.05);
        }
        
        .footer {
            text-align: center;
            color: white;
            margin-top: 60px;
            padding: 30px;
            background: rgba(255,255,255,0.1);
            backdrop-filter: blur(10px);
            border-radius: 15px;
        }
        
        @media (max-width: 768px) {
            .header h1 { font-size: 2.5em; }
            .demos-grid { grid-template-columns: 1fr; }
        }
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h1>🎓 GenMentor Visual Demos</h1>
            <p>Explore diverse learning paths powered by AI</p>
            
            <div class="stats-bar">
                <div class="stat-item">
                    <span class="number">""" + str(len(demo_results)) + """</span>
                    <span class="label">Demo Cases</span>
                </div>
                <div class="stat-item">
                    <span class="number">""" + str(sum(r['stats']['total_sessions'] for r in demo_results)) + """</span>
                    <span class="label">Total Sessions</span>
                </div>
                <div class="stat-item">
                    <span class="number">""" + str(sum(r['stats']['total_hours'] for r in demo_results)) + """</span>
                    <span class="label">Learning Hours</span>
                </div>
                <div class="stat-item">
                    <span class="number">""" + str(sum(r['stats']['total_resources'] for r in demo_results)) + """</span>
                    <span class="label">Resources</span>
                </div>
            </div>
        </div>
        
        <div class="demos-grid">
"""
        
        for result in demo_results:
            stats = result['stats']
            html += f"""
            <a href="{os.path.basename(result['html_file'])}" class="demo-card">
                <div class="demo-header">
                    <div class="demo-id">{stats['id'].upper()}</div>
                    <h3>{stats['title']}</h3>
                    <span class="demo-category">{stats['category']}</span>
                </div>
                <div class="demo-body">
                    <div class="demo-description">{stats['description']}</div>
                    <div class="demo-stats">
                        <div class="demo-stat">
                            <span class="value">{stats['total_sessions']}</span>
                            <span class="label">Sessions</span>
                        </div>
                        <div class="demo-stat">
                            <span class="value">{stats['total_hours']}</span>
                            <span class="label">Hours</span>
                        </div>
                    </div>
                    <div class="view-button">View Learning Path →</div>
                </div>
            </a>
"""
        
        html += """
        </div>
        
        <div class="footer">
            <h3>GenMentor AI System</h3>
            <p style="margin-top: 10px;">Personalized learning paths powered by advanced AI algorithms</p>
            <p style="margin-top: 15px; opacity: 0.8;">Generated on """ + datetime.now().strftime("%B %d, %Y") + """</p>
        </div>
    </div>
</body>
</html>
"""
        
        index_filename = os.path.join(self.output_dir, "index.html")
        with open(index_filename, 'w', encoding='utf-8') as f:
            f.write(html)
        
        return index_filename
    
    def generate_all_demos(self):
        """Generate all demonstration pages."""
        
        print("\n" + "="*100)
        print(" GENMENTOR VISUAL DEMO GENERATOR")
        print("="*100)
        print(f" Output Directory: {self.output_dir}")
        print("="*100)
        
        showcase_cases = self.get_showcase_cases()
        demo_results = []
        
        print(f"\nGenerating {len(showcase_cases)} demonstration pages...\n")
        
        for i, demo_case in enumerate(showcase_cases, 1):
            print(f"\n[{i}/{len(showcase_cases)}] Processing...")
            result = self.generate_demo_page(demo_case)
            
            if result:
                demo_results.append(result)
            
            # Small delay between generations
            time.sleep(0.5)
        
        # Generate index page
        print(f"\n{'='*100}")
        print(" Generating Index Page")
        print(f"{'='*100}")
        
        index_file = self.generate_index_page(demo_results)
        print(f"\n✓ Index page: {index_file}")
        
        # Summary
        print(f"\n{'='*100}")
        print(" GENERATION COMPLETE")
        print(f"{'='*100}")
        print(f"\n✓ Successfully generated {len(demo_results)} demonstration pages")
        print(f"✓ Total sessions: {sum(r['stats']['total_sessions'] for r in demo_results)}")
        print(f"✓ Total hours: {sum(r['stats']['total_hours'] for r in demo_results)}")
        print(f"✓ Total resources: {sum(r['stats']['total_resources'] for r in demo_results)}")
        print(f"\n📂 All files saved in: {self.output_dir}")
        print(f"\n💡 Open '{os.path.basename(index_file)}' in your browser to view all demos!")
        print(f"{'='*100}\n")
        
        return demo_results, index_file


if __name__ == "__main__":
    generator = VisualDemoGenerator()
    results, index_file = generator.generate_all_demos()
    
    print("\n✅ Ready to showcase to your project advisor!")
    print(f"✅ Open: {index_file}")
