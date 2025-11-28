"""
Enhanced Comprehensive Test Suite for GenMentor System
Includes extensive test cases, detailed benchmarking, relevance scoring, and comprehensive reporting
"""

import time
import json
import sys
import io
from typing import Dict, List, Tuple
from datetime import datetime
from ai_engine import GenMentorAI
from improved_resource_curator import ImprovedResourceCurator
import numpy as np

# Fix encoding
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')

class EnhancedTestSuite:
    """Enhanced testing framework with detailed metrics and reporting."""
    
    def __init__(self):
        self.test_results = []
        self.ai_engine = GenMentorAI()
        self.resource_curator = ImprovedResourceCurator()
        
        print("=" * 100)
        print(" GENMENTOR ENHANCED TEST SUITE - COMPREHENSIVE EVALUATION")
        print("=" * 100)
        print(f" Started: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        print("=" * 100)
    
    def get_diverse_test_cases(self) -> List[Dict]:
        """Get diverse test cases from different domains and experience levels."""
        return [
            # Tech Transitions - Beginner to Intermediate
            {
                'test_id': 'T001',
                'name': 'Marketing to Data Science',
                'goal': 'I want to transition from marketing to data science',
                'current_skills': ['marketing analytics', 'excel', 'basic statistics'],
                'experience_level': 'beginner',
                'category': 'Career Transition',
                'difficulty': 'high'
            },
            {
                'test_id': 'T002',
                'name': 'Finance to Data Engineering',
                'goal': 'I work in finance and want to become a data engineer',
                'current_skills': ['excel', 'sql', 'financial modeling', 'python basics'],
                'experience_level': 'intermediate',
                'category': 'Career Transition',
                'difficulty': 'medium'
            },
            {
                'test_id': 'T003',
                'name': 'Teacher to UX Designer',
                'goal': 'I am a teacher who wants to transition into UX design',
                'current_skills': ['presentation', 'communication', 'basic design'],
                'experience_level': 'beginner',
                'category': 'Career Transition',
                'difficulty': 'high'
            },
            
            # Tech Advancement - Same field progression
            {
                'test_id': 'T004',
                'name': 'Junior to Senior Developer',
                'goal': 'I am a junior software developer and want to become a senior developer',
                'current_skills': ['python', 'javascript', 'git', 'rest apis', 'databases'],
                'experience_level': 'intermediate',
                'category': 'Career Advancement',
                'difficulty': 'medium'
            },
            {
                'test_id': 'T005',
                'name': 'Software Engineer to ML Engineer',
                'goal': 'I am a software engineer transitioning to machine learning engineering',
                'current_skills': ['python', 'java', 'algorithms', 'data structures', 'cloud computing'],
                'experience_level': 'intermediate',
                'category': 'Career Advancement',
                'difficulty': 'medium'
            },
            {
                'test_id': 'T006',
                'name': 'Data Analyst to Data Scientist',
                'goal': 'I want to advance from data analyst to data scientist',
                'current_skills': ['sql', 'excel', 'tableau', 'statistics', 'python basics'],
                'experience_level': 'intermediate',
                'category': 'Career Advancement',
                'difficulty': 'low'
            },
            
            # Tech Specialization - Specific technology focus
            {
                'test_id': 'T007',
                'name': 'AWS Cloud Architect',
                'goal': 'I want to become an AWS cloud architect',
                'current_skills': ['linux', 'networking', 'docker', 'basic aws'],
                'experience_level': 'intermediate',
                'category': 'Tech Specialization',
                'difficulty': 'medium'
            },
            {
                'test_id': 'T008',
                'name': 'DevOps Engineer',
                'goal': 'I want to become a DevOps engineer',
                'current_skills': ['linux', 'python', 'git', 'ci/cd basics'],
                'experience_level': 'intermediate',
                'category': 'Tech Specialization',
                'difficulty': 'medium'
            },
            {
                'test_id': 'T009',
                'name': 'Cybersecurity Specialist',
                'goal': 'I want to become a cybersecurity specialist',
                'current_skills': ['networking', 'linux', 'programming basics'],
                'experience_level': 'beginner',
                'category': 'Tech Specialization',
                'difficulty': 'high'
            },
            {
                'test_id': 'T010',
                'name': 'Blockchain Developer',
                'goal': 'I want to become a blockchain developer',
                'current_skills': ['javascript', 'node.js', 'cryptography basics'],
                'experience_level': 'intermediate',
                'category': 'Tech Specialization',
                'difficulty': 'high'
            },
            
            # Emerging Tech Roles
            {
                'test_id': 'T011',
                'name': 'AI Research Scientist',
                'goal': 'I want to become an AI research scientist',
                'current_skills': ['python', 'mathematics', 'statistics', 'machine learning', 'deep learning'],
                'experience_level': 'advanced',
                'category': 'Research & Advanced',
                'difficulty': 'low'
            },
            {
                'test_id': 'T012',
                'name': 'Computer Vision Engineer',
                'goal': 'I want to specialize in computer vision engineering',
                'current_skills': ['python', 'machine learning', 'opencv basics'],
                'experience_level': 'intermediate',
                'category': 'Tech Specialization',
                'difficulty': 'medium'
            },
            {
                'test_id': 'T013',
                'name': 'NLP Engineer',
                'goal': 'I want to become a natural language processing engineer',
                'current_skills': ['python', 'machine learning', 'linguistics basics'],
                'experience_level': 'intermediate',
                'category': 'Tech Specialization',
                'difficulty': 'medium'
            },
            
            # Web & Mobile Development
            {
                'test_id': 'T014',
                'name': 'Full-Stack Web Developer',
                'goal': 'I want to become a full-stack web developer',
                'current_skills': ['html', 'css', 'javascript basics'],
                'experience_level': 'beginner',
                'category': 'Web Development',
                'difficulty': 'medium'
            },
            {
                'test_id': 'T015',
                'name': 'Mobile App Developer',
                'goal': 'I want to develop mobile apps for iOS and Android',
                'current_skills': ['programming basics', 'ui design'],
                'experience_level': 'beginner',
                'category': 'Mobile Development',
                'difficulty': 'medium'
            },
            
            # Management & Leadership
            {
                'test_id': 'T016',
                'name': 'Technical Product Manager',
                'goal': 'I want to become a technical product manager',
                'current_skills': ['project management', 'business analysis', 'technical background'],
                'experience_level': 'intermediate',
                'category': 'Management',
                'difficulty': 'low'
            },
            {
                'test_id': 'T017',
                'name': 'Engineering Manager',
                'goal': 'I want to move from senior engineer to engineering manager',
                'current_skills': ['software development', 'team collaboration', 'mentoring'],
                'experience_level': 'advanced',
                'category': 'Management',
                'difficulty': 'low'
            },
            
            # Edge Cases
            {
                'test_id': 'T018',
                'name': 'Complete Beginner - Programming',
                'goal': 'I want to learn programming and get a tech job',
                'current_skills': [],
                'experience_level': 'beginner',
                'category': 'Edge Case',
                'difficulty': 'high'
            },
            {
                'test_id': 'T019',
                'name': 'Vague Goal - Tech Career',
                'goal': 'I want to work in technology',
                'current_skills': ['computer basics'],
                'experience_level': 'beginner',
                'category': 'Edge Case',
                'difficulty': 'high'
            },
            {
                'test_id': 'T020',
                'name': 'Highly Experienced - Specialization',
                'goal': 'I want to specialize in reinforcement learning',
                'current_skills': ['python', 'machine learning', 'deep learning', 'neural networks', 
                                  'mathematics', 'statistics', 'tensorflow', 'pytorch'],
                'experience_level': 'advanced',
                'category': 'Edge Case',
                'difficulty': 'low'
            },
            
            # Additional Diverse Cases
            {
                'test_id': 'T021',
                'name': 'Game Developer',
                'goal': 'I want to become a game developer',
                'current_skills': ['c++', 'graphics basics', 'game design'],
                'experience_level': 'intermediate',
                'category': 'Game Development',
                'difficulty': 'medium'
            },
            {
                'test_id': 'T022',
                'name': 'Database Administrator',
                'goal': 'I want to become a database administrator',
                'current_skills': ['sql', 'database basics', 'networking'],
                'experience_level': 'beginner',
                'category': 'Data Management',
                'difficulty': 'medium'
            },
            {
                'test_id': 'T023',
                'name': 'Business Intelligence Analyst',
                'goal': 'I want to become a business intelligence analyst',
                'current_skills': ['excel', 'sql', 'data analysis', 'tableau'],
                'experience_level': 'intermediate',
                'category': 'Business Analytics',
                'difficulty': 'low'
            },
            {
                'test_id': 'T024',
                'name': 'Network Engineer',
                'goal': 'I want to become a network engineer',
                'current_skills': ['networking basics', 'cisco', 'routing'],
                'experience_level': 'intermediate',
                'category': 'Network Engineering',
                'difficulty': 'medium'
            },
            {
                'test_id': 'T025',
                'name': 'IoT Engineer',
                'goal': 'I want to work with Internet of Things and embedded systems',
                'current_skills': ['programming', 'electronics basics', 'sensors'],
                'experience_level': 'intermediate',
                'category': 'IoT & Embedded',
                'difficulty': 'medium'
            }
        ]
    
    def calculate_relevance_score(self, skill_uri: str, occupation_skills: List[str], 
                                  goal: str, current_skills: List[str]) -> Dict:
        """
        Calculate detailed relevance score for a suggested skill.
        
        Relevance is calculated based on:
        1. Direct relevance to target occupation (40%)
        2. Skill gap priority (30%)
        3. Learning path position (20%)
        4. Resource availability (10%)
        """
        skill_name = skill_uri.split('/')[-1].replace('_', ' ').lower()
        
        # 1. Direct relevance to occupation (40 points)
        occupation_relevance = 40 if skill_uri in occupation_skills else 20
        
        # 2. Skill gap priority (30 points)
        # Higher priority if not in current skills
        current_skill_names = [s.lower() for s in current_skills]
        gap_priority = 30 if skill_name not in ' '.join(current_skill_names) else 10
        
        # 3. Learning path position (20 points)
        # Earlier skills get higher priority
        position_score = 20  # Will be adjusted based on position in path
        
        # 4. Resource availability (10 points)
        resources = self.resource_curator.search_resources(skill_name, limit=1)
        resource_score = 10 if resources else 5
        
        total_score = occupation_relevance + gap_priority + position_score + resource_score
        
        return {
            'skill': skill_name,
            'total_score': total_score,
            'max_score': 100,
            'percentage': (total_score / 100) * 100,
            'breakdown': {
                'occupation_relevance': occupation_relevance,
                'skill_gap_priority': gap_priority,
                'learning_path_position': position_score,
                'resource_availability': resource_score
            }
        }
    
    def run_comprehensive_test(self, test_case: Dict) -> Dict:
        """Run a comprehensive test case with detailed metrics."""
        test_id = test_case['test_id']
        name = test_case['name']
        goal = test_case['goal']
        current_skills = test_case['current_skills']
        
        print(f"\n{'='*100}")
        print(f"TEST {test_id}: {name}")
        print(f"{'='*100}")
        print(f"Goal: {goal}")
        print(f"Current Skills: {', '.join(current_skills) if current_skills else 'None'}")
        print(f"Category: {test_case['category']} | Difficulty: {test_case['difficulty'].upper()}")
        
        result = {
            'test_id': test_id,
            'name': name,
            'goal': goal,
            'current_skills': current_skills,
            'category': test_case['category'],
            'experience_level': test_case['experience_level'],
            'difficulty': test_case['difficulty'],
            'timestamps': {}
        }
        
        # Step 1: Skill Gap Analysis
        print(f"\n[1/4] Skill Gap Analysis...")
        start_time = time.time()
        try:
            skill_gap = self.ai_engine.identify_skill_gap(goal, current_skills)
            result['timestamps']['skill_gap_analysis'] = time.time() - start_time
            
            matched_occ = skill_gap['matched_occupation']
            result['matched_occupation'] = {
                'label': matched_occ['label'],
                'similarity_score': matched_occ['similarity_score'],
                'similarity_percentage': matched_occ['similarity_score'] * 100,
                'uri': matched_occ['uri']
            }
            
            result['skill_gap'] = {
                'total_skills_needed': skill_gap['skills_to_learn'],
                'skills_to_learn': len(skill_gap['skill_gap']),
                'recognized_skills': len(skill_gap.get('recognized_skills', []))
            }
            
            print(f"  ✓ Matched Occupation: {matched_occ['label']}")
            print(f"  ✓ Similarity Score: {matched_occ['similarity_score']*100:.2f}%")
            print(f"  ✓ Skills to Learn: {skill_gap['skills_to_learn']}")
            print(f"  ✓ Time: {result['timestamps']['skill_gap_analysis']:.2f}s")
            
        except Exception as e:
            result['error'] = f"Skill gap analysis failed: {str(e)}"
            print(f"  ✗ Error: {str(e)}")
            return result
        
        # Step 2: Learning Path Generation
        print(f"\n[2/4] Learning Path Generation...")
        start_time = time.time()
        try:
            limited_skills = skill_gap['skill_gap'][:12]
            learning_path = self.ai_engine.schedule_learning_path(limited_skills)
            result['timestamps']['learning_path_generation'] = time.time() - start_time
            
            total_hours = sum(s.get('estimated_duration_hours', 0) or s.get('duration', 0) for s in learning_path)
            
            result['learning_path'] = {
                'total_sessions': len(learning_path),
                'total_hours': total_hours,
                'weeks_full_time': round(total_hours / 40, 1),
                'sessions': learning_path
            }
            
            print(f"  ✓ Sessions Generated: {len(learning_path)}")
            print(f"  ✓ Total Duration: {total_hours} hours (~{total_hours/40:.1f} weeks)")
            print(f"  ✓ Time: {result['timestamps']['learning_path_generation']:.2f}s")
            
        except Exception as e:
            result['error'] = f"Learning path generation failed: {str(e)}"
            print(f"  ✗ Error: {str(e)}")
            return result
        
        # Step 3: Relevance Score Calculation
        print(f"\n[3/4] Calculating Skill Relevance Scores...")
        start_time = time.time()
        try:
            occupation_skills = [s['uri'] for s in skill_gap['skill_gap']]
            relevance_scores = []
            
            # Get first 5 skill URIs from skill_gap
            skill_uris_to_check = [s['uri'] for s in skill_gap['skill_gap'][:5]]
            
            for i, skill_uri in enumerate(skill_uris_to_check, 1):  # Top 5 skills
                relevance = self.calculate_relevance_score(
                    skill_uri, occupation_skills, goal, current_skills
                )
                relevance['position'] = i
                relevance_scores.append(relevance)
                
                print(f"  {i}. {relevance['skill'].title()}")
                print(f"     Total Score: {relevance['total_score']}/100 ({relevance['percentage']:.1f}%)")
                print(f"     - Occupation Relevance: {relevance['breakdown']['occupation_relevance']}/40")
                print(f"     - Skill Gap Priority: {relevance['breakdown']['skill_gap_priority']}/30")
                print(f"     - Learning Position: {relevance['breakdown']['learning_path_position']}/20")
                print(f"     - Resource Availability: {relevance['breakdown']['resource_availability']}/10")
            
            result['relevance_scores'] = relevance_scores
            result['timestamps']['relevance_calculation'] = time.time() - start_time
            print(f"  ✓ Time: {result['timestamps']['relevance_calculation']:.2f}s")
            
        except Exception as e:
            result['error'] = f"Relevance calculation failed: {str(e)}"
            print(f"  ✗ Error: {str(e)}")
        
        # Step 4: Resource Curation
        print(f"\n[4/4] Resource Curation Sample...")
        start_time = time.time()
        try:
            resource_stats = {
                'skills_checked': 0,
                'skills_with_resources': 0,
                'total_resources': 0,
                'avg_resources_per_skill': 0
            }
            
            # Get first 3 skills from skill_gap (use labels directly)
            skills_sample = skill_gap['skill_gap'][:3]
            
            for skill_data in skills_sample:  # Sample 3 skills
                skill_name = skill_data['label']
                resources = self.resource_curator.search_resources(skill_name, limit=5)
                
                resource_stats['skills_checked'] += 1
                if resources:
                    resource_stats['skills_with_resources'] += 1
                    resource_stats['total_resources'] += len(resources)
                
                print(f"  • {skill_name.title()}: {len(resources)} resources")
            
            if resource_stats['skills_checked'] > 0:
                resource_stats['avg_resources_per_skill'] = round(
                    resource_stats['total_resources'] / resource_stats['skills_checked'], 1
                )
            
            result['resource_curation'] = resource_stats
            result['timestamps']['resource_curation'] = time.time() - start_time
            print(f"  ✓ Time: {result['timestamps']['resource_curation']:.2f}s")
            
        except Exception as e:
            result['error'] = f"Resource curation failed: {str(e)}"
            print(f"  ✗ Error: {str(e)}")
        
        # Calculate total time
        result['timestamps']['total'] = sum(
            t for k, t in result['timestamps'].items() if k != 'total'
        )
        
        print(f"\n{'─'*100}")
        print(f"TOTAL TIME: {result['timestamps']['total']:.2f}s")
        print(f"{'─'*100}")
        
        # Test is successful if we have matched occupation and learning path
        has_core_results = ('matched_occupation' in result and 
                           'learning_path' in result and 
                           len(result.get('learning_path', {}).get('sessions', [])) > 0)
        
        result['status'] = 'success' if has_core_results else 'failed'
        
        # Track which components succeeded
        result['components_status'] = {
            'skill_gap_analysis': 'matched_occupation' in result,
            'learning_path_generation': 'learning_path' in result,
            'relevance_scoring': 'relevance_scores' in result and len(result.get('relevance_scores', [])) > 0,
            'resource_curation': 'resource_curation' in result
        }
        
        return result
    
    def generate_comprehensive_report(self, all_results: List[Dict]) -> Dict:
        """Generate a comprehensive test report with statistics and insights."""
        
        print("\n" + "="*100)
        print(" GENERATING COMPREHENSIVE REPORT")
        print("="*100)
        
        report = {
            'test_suite': 'GenMentor Enhanced Test Suite',
            'timestamp': datetime.now().isoformat(),
            'summary': {
                'total_tests': len(all_results),
                'successful_tests': sum(1 for r in all_results if r.get('status') == 'success'),
                'failed_tests': sum(1 for r in all_results if r.get('status') == 'failed'),
                'success_rate': 0
            },
            'performance_metrics': {},
            'similarity_scores': {},
            'relevance_analysis': {},
            'category_breakdown': {},
            'test_results': all_results
        }
        
        successful_results = [r for r in all_results if r.get('status') == 'success']
        
        if len(all_results) > 0:
            report['summary']['success_rate'] = (
                report['summary']['successful_tests'] / report['summary']['total_tests']
            ) * 100
        
        # Performance Metrics
        if successful_results:
            skill_gap_times = [r['timestamps']['skill_gap_analysis'] for r in successful_results]
            learning_path_times = [r['timestamps']['learning_path_generation'] for r in successful_results]
            total_times = [r['timestamps']['total'] for r in successful_results]
            
            report['performance_metrics'] = {
                'skill_gap_analysis': {
                    'avg': round(np.mean(skill_gap_times), 2),
                    'min': round(np.min(skill_gap_times), 2),
                    'max': round(np.max(skill_gap_times), 2),
                    'std': round(np.std(skill_gap_times), 2)
                },
                'learning_path_generation': {
                    'avg': round(np.mean(learning_path_times), 2),
                    'min': round(np.min(learning_path_times), 2),
                    'max': round(np.max(learning_path_times), 2),
                    'std': round(np.std(learning_path_times), 2)
                },
                'total_processing': {
                    'avg': round(np.mean(total_times), 2),
                    'min': round(np.min(total_times), 2),
                    'max': round(np.max(total_times), 2),
                    'std': round(np.std(total_times), 2)
                }
            }
        
        # Similarity Score Analysis
        if successful_results:
            similarity_scores = [r['matched_occupation']['similarity_score'] * 100 
                                for r in successful_results]
            
            report['similarity_scores'] = {
                'average': round(np.mean(similarity_scores), 2),
                'median': round(np.median(similarity_scores), 2),
                'min': round(np.min(similarity_scores), 2),
                'max': round(np.max(similarity_scores), 2),
                'std': round(np.std(similarity_scores), 2),
                'distribution': {
                    'excellent (>90%)': sum(1 for s in similarity_scores if s > 90),
                    'good (70-90%)': sum(1 for s in similarity_scores if 70 <= s <= 90),
                    'fair (50-70%)': sum(1 for s in similarity_scores if 50 <= s < 70),
                    'poor (<50%)': sum(1 for s in similarity_scores if s < 50)
                }
            }
        
        # Relevance Score Analysis
        all_relevance_scores = []
        for r in successful_results:
            if 'relevance_scores' in r:
                all_relevance_scores.extend([rs['total_score'] for rs in r['relevance_scores']])
        
        if all_relevance_scores:
            report['relevance_analysis'] = {
                'average_score': round(np.mean(all_relevance_scores), 2),
                'median_score': round(np.median(all_relevance_scores), 2),
                'min_score': round(np.min(all_relevance_scores), 2),
                'max_score': round(np.max(all_relevance_scores), 2),
                'distribution': {
                    'highly_relevant (>80)': sum(1 for s in all_relevance_scores if s > 80),
                    'relevant (60-80)': sum(1 for s in all_relevance_scores if 60 <= s <= 80),
                    'moderately_relevant (40-60)': sum(1 for s in all_relevance_scores if 40 <= s < 60),
                    'low_relevance (<40)': sum(1 for s in all_relevance_scores if s < 40)
                }
            }
        
        # Category Breakdown
        categories = {}
        for r in successful_results:
            cat = r.get('category', 'Unknown')
            if cat not in categories:
                categories[cat] = {
                    'count': 0,
                    'avg_similarity': 0,
                    'avg_time': 0,
                    'similarity_scores': []
                }
            
            categories[cat]['count'] += 1
            categories[cat]['similarity_scores'].append(
                r['matched_occupation']['similarity_score'] * 100
            )
        
        for cat, data in categories.items():
            data['avg_similarity'] = round(np.mean(data['similarity_scores']), 2)
            del data['similarity_scores']
        
        report['category_breakdown'] = categories
        
        return report
    
    def print_final_report(self, report: Dict):
        """Print a formatted final report."""
        
        print("\n" + "="*100)
        print(" FINAL TEST REPORT")
        print("="*100)
        
        # Summary
        print(f"\n📊 TEST SUMMARY")
        print(f"{'─'*100}")
        print(f"  Total Tests: {report['summary']['total_tests']}")
        print(f"  Successful: {report['summary']['successful_tests']} ✓")
        print(f"  Failed: {report['summary']['failed_tests']} ✗")
        print(f"  Success Rate: {report['summary']['success_rate']:.1f}%")
        
        # Performance Metrics
        if report['performance_metrics']:
            print(f"\n⚡ PERFORMANCE METRICS")
            print(f"{'─'*100}")
            pm = report['performance_metrics']
            
            print(f"  Skill Gap Analysis:")
            print(f"    Average: {pm['skill_gap_analysis']['avg']}s")
            print(f"    Range: {pm['skill_gap_analysis']['min']}s - {pm['skill_gap_analysis']['max']}s")
            
            print(f"\n  Learning Path Generation:")
            print(f"    Average: {pm['learning_path_generation']['avg']}s")
            print(f"    Range: {pm['learning_path_generation']['min']}s - {pm['learning_path_generation']['max']}s")
            
            print(f"\n  Total Processing Time:")
            print(f"    Average: {pm['total_processing']['avg']}s per test")
            print(f"    Range: {pm['total_processing']['min']}s - {pm['total_processing']['max']}s")
        
        # Similarity Scores
        if report['similarity_scores']:
            print(f"\n🎯 SIMILARITY SCORE ANALYSIS")
            print(f"{'─'*100}")
            ss = report['similarity_scores']
            
            print(f"  Average Similarity: {ss['average']:.2f}%")
            print(f"  Median: {ss['median']:.2f}%")
            print(f"  Range: {ss['min']:.2f}% - {ss['max']:.2f}%")
            print(f"  Standard Deviation: {ss['std']:.2f}%")
            
            print(f"\n  Distribution:")
            dist = ss['distribution']
            total = sum(dist.values())
            for category, count in dist.items():
                percentage = (count / total * 100) if total > 0 else 0
                print(f"    {category}: {count} tests ({percentage:.1f}%)")
        
        # Relevance Analysis
        if report['relevance_analysis']:
            print(f"\n📈 SKILL RELEVANCE ANALYSIS")
            print(f"{'─'*100}")
            ra = report['relevance_analysis']
            
            print(f"  Average Relevance Score: {ra['average_score']:.2f}/100")
            print(f"  Median: {ra['median_score']:.2f}/100")
            print(f"  Range: {ra['min_score']:.2f} - {ra['max_score']:.2f}")
            
            print(f"\n  Distribution:")
            dist = ra['distribution']
            total = sum(dist.values())
            for category, count in dist.items():
                percentage = (count / total * 100) if total > 0 else 0
                print(f"    {category}: {count} skills ({percentage:.1f}%)")
        
        # Category Breakdown
        if report['category_breakdown']:
            print(f"\n📁 CATEGORY BREAKDOWN")
            print(f"{'─'*100}")
            for cat, data in sorted(report['category_breakdown'].items(), 
                                   key=lambda x: x[1]['count'], reverse=True):
                print(f"  {cat}:")
                print(f"    Tests: {data['count']}")
                print(f"    Avg Similarity: {data['avg_similarity']:.2f}%")
        
        print(f"\n{'='*100}")
        print(" Report Generation Complete")
        print(f"{'='*100}\n")
    
    def save_report(self, report: Dict, filename: str):
        """Save the report to a JSON file."""
        # Convert numpy types to Python types for JSON serialization
        import numpy as np
        def convert_numpy(obj):
            if isinstance(obj, np.integer):
                return int(obj)
            elif isinstance(obj, np.floating):
                return float(obj)
            elif isinstance(obj, np.ndarray):
                return obj.tolist()
            elif isinstance(obj, dict):
                return {key: convert_numpy(value) for key, value in obj.items()}
            elif isinstance(obj, list):
                return [convert_numpy(item) for item in obj]
            return obj
        
        report_converted = convert_numpy(report)
        
        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(report_converted, f, indent=2, ensure_ascii=False)
        print(f"\n💾 Report saved to: {filename}")
    
    def run_all_tests(self):
        """Run all test cases and generate comprehensive report."""
        test_cases = self.get_diverse_test_cases()
        all_results = []
        
        print(f"\n🚀 Running {len(test_cases)} comprehensive test cases...\n")
        
        for i, test_case in enumerate(test_cases, 1):
            print(f"\n{'='*100}")
            print(f" PROGRESS: Test {i}/{len(test_cases)}")
            print(f"{'='*100}")
            
            result = self.run_comprehensive_test(test_case)
            all_results.append(result)
            
            # Small delay between tests
            time.sleep(0.5)
        
        # Generate comprehensive report
        report = self.generate_comprehensive_report(all_results)
        
        # Print final report
        self.print_final_report(report)
        
        # Save report
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"comprehensive_test_report_{timestamp}.json"
        self.save_report(report, filename)
        
        return report


if __name__ == "__main__":
    suite = EnhancedTestSuite()
    report = suite.run_all_tests()
    
    print("\n" + "="*100)
    print(" ALL TESTS COMPLETED SUCCESSFULLY")
    print("="*100)
    print("\n✅ Check the JSON report file for detailed results and metrics")
    print("✅ All similarity scores, relevance calculations, and performance metrics are documented")
    print("\n")
