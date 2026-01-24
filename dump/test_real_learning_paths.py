"""
Real End-to-End Learning Path Generation Tests
Tests actual learning path generation with different career goals and creates comprehensive visualizations.
"""

import asyncio
import json
import time
from datetime import datetime
from ai_engine import GenMentorAI
from improved_resource_curator import ImprovedResourceCurator
from enhanced_visualizations import EnhancedCourseVisualizer

class RealLearningPathTests:
    """Test suite for real learning path generation with multiple career goals."""
    
    def __init__(self):
        print("\n" + "="*80)
        print("REAL END-TO-END LEARNING PATH GENERATION TEST SUITE")
        print("="*80)
        
        # Initialize AI engine
        print("\nInitializing AI Engine...")
        self.ai_engine = GenMentorAI()  # Uses default genmentor.db
        
        # Initialize improved resource curator
        print("Initializing Improved Resource Curator...")
        self.resource_curator = ImprovedResourceCurator(cache_backend='sqlite')
        
        # Initialize visualizer
        print("Initializing Enhanced Visualizer...")
        self.visualizer = EnhancedCourseVisualizer()
        
        # Test scenarios with different career goals
        self.test_scenarios = [
            {
                'name': 'Web Developer',
                'goal': 'I want to become a full-stack web developer',
                'current_skills': []
            },
            {
                'name': 'Data Scientist',
                'goal': 'I want to become a data scientist with machine learning expertise',
                'current_skills': ['Python programming', 'Statistics']
            },
            {
                'name': 'AI Engineer',
                'goal': 'I want to become an AI engineer specializing in deep learning',
                'current_skills': ['Python', 'Machine learning basics']
            },
            {
                'name': 'DevOps Engineer',
                'goal': 'I want to become a DevOps engineer with cloud expertise',
                'current_skills': ['Linux administration', 'Basic networking']
            },
            {
                'name': 'Mobile Developer',
                'goal': 'I want to become a mobile app developer for iOS and Android',
                'current_skills': ['Programming basics', 'UI design']
            }
        ]
        
        self.test_results = []
    
    def run_all_tests(self):
        """Run all test scenarios and generate visualizations."""
        print("\n" + "="*80)
        print("STARTING REAL LEARNING PATH GENERATION TESTS")
        print("="*80)
        
        for i, scenario in enumerate(self.test_scenarios, 1):
            print(f"\n{'='*80}")
            print(f"TEST {i}/{len(self.test_scenarios)}: {scenario['name']}")
            print(f"{'='*80}")
            
            try:
                result = self.test_learning_path_generation(scenario)
                self.test_results.append(result)
                
                # Generate visualization for this test
                if result['status'] == 'success':
                    self.generate_visualization(result, scenario['name'])
                
            except Exception as e:
                print(f" Test failed: {e}")
                self.test_results.append({
                    'scenario': scenario['name'],
                    'status': 'failed',
                    'error': str(e)
                })
        
        # Save summary report
        self.save_test_summary()
        
        print("\n" + "="*80)
        print("ALL TESTS COMPLETE")
        print("="*80)
        print(f" Successful: {sum(1 for r in self.test_results if r['status'] == 'success')}/{len(self.test_results)}")
        print(f" Failed: {sum(1 for r in self.test_results if r['status'] == 'failed')}/{len(self.test_results)}")
    
    def test_learning_path_generation(self, scenario):
        """Test complete learning path generation for a scenario."""
        start_time = time.time()
        
        print(f"\n Goal: {scenario['goal']}")
        print(f" Current Skills: {scenario['current_skills'] if scenario['current_skills'] else 'None (Beginner)'}")
        
        # Step 1: Identify skill gap
        print("\n[1/4] Identifying skill gap...")
        skill_gap_start = time.time()
        skill_gap_result = self.ai_engine.identify_skill_gap(
            scenario['goal'],
            scenario['current_skills']
        )
        skill_gap_time = time.time() - skill_gap_start
        
        print(f"    Matched Occupation: {skill_gap_result['matched_occupation']['label']}")
        print(f"    Skills to Learn: {skill_gap_result['skills_to_learn']}")
        print(f"     Time: {skill_gap_time:.2f}s")
        
        if not skill_gap_result['skill_gap']:
            return {
                'scenario': scenario['name'],
                'status': 'success',
                'message': 'No skill gap found - already qualified!',
                'matched_occupation': skill_gap_result['matched_occupation'],
                'total_time': time.time() - start_time
            }
        
        # Step 2: Schedule learning path
        print("\n[2/4] Scheduling learning path...")
        schedule_start = time.time()
        
        # Limit to 10 skills for manageable learning paths
        limited_skills = skill_gap_result['skill_gap'][:10]
        learning_path = self.ai_engine.schedule_learning_path(limited_skills)
        
        schedule_time = time.time() - schedule_start
        
        print(f"    Learning Sessions: {len(learning_path)}")
        print(f"     Time: {schedule_time:.2f}s")
        
        # Step 3: Fetch resources for all skills
        print("\n[3/4] Fetching learning resources...")
        resources_start = time.time()
        
        all_resources = self.fetch_resources_for_path(learning_path)
        
        resources_time = time.time() - resources_start
        
        total_resources = sum(len(resources) for resources in all_resources.values())
        print(f"    Total Resources: {total_resources}")
        print(f"     Time: {resources_time:.2f}s")
        
        # Step 4: Calculate path statistics
        print("\n[4/4] Calculating path statistics...")
        
        total_hours = sum(session.get('estimated_duration_hours', 0) for session in learning_path)
        total_skills = sum(len(session.get('skills', [])) for session in learning_path)
        duration_days = total_hours // 3  # Assuming 3 hours study per day
        
        print(f"    Total Study Hours: {total_hours}")
        print(f"    Total Skills: {total_skills}")
        print(f"    Estimated Duration: {duration_days} days")
        
        total_time = time.time() - start_time
        
        # Convert resources dict to skill_resources array format for visualization
        skill_resources = []
        for skill_name, resources in all_resources.items():
            skill_resources.append({
                'skill_name': skill_name,
                'resources': resources
            })
        
        # Prepare result
        result = {
            'scenario': scenario['name'],
            'status': 'success',
            'goal': scenario['goal'],
            'current_skills': scenario['current_skills'],
            'matched_occupation': skill_gap_result['matched_occupation'],
            'learning_path': learning_path,
            'resources': all_resources,  # Keep dict format for backward compatibility
            'skill_resources': skill_resources,  # Add array format for visualization
            'statistics': {
                'total_hours': total_hours,
                'total_skills': total_skills,
                'duration_days': duration_days,
                'total_sessions': len(learning_path),
                'total_resources': total_resources
            },
            'performance': {
                'skill_gap_time': skill_gap_time,
                'schedule_time': schedule_time,
                'resources_time': resources_time,
                'total_time': total_time
            }
        }
        
        print(f"\n Test Complete - Total Time: {total_time:.2f}s")
        
        return result
    
    def fetch_resources_for_path(self, learning_path):
        """Fetch resources for all skills in the learning path."""
        # Collect all unique skills
        all_skills = set()
        for session in learning_path:
            for skill in session.get('skills', []):
                skill_label = skill.get('label', skill) if isinstance(skill, dict) else skill
                all_skills.add(skill_label)
        
        # Batch search for all skills
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        
        try:
            resources = loop.run_until_complete(
                self.resource_curator.batch_search(list(all_skills))
            )
            return resources
        finally:
            loop.close()
    
    def generate_visualization(self, result, scenario_name):
        """Generate comprehensive HTML visualization for the test result."""
        print(f"\n Generating visualization for {scenario_name}...")
        
        try:
            # Prepare data for visualization
            vis_data = {
                'goal': result['goal'],
                'matched_occupation': result['matched_occupation'],
                'learning_path': result['learning_path'],
                'resources': result['resources'],
                'statistics': result['statistics'],
                'current_skills': result['current_skills']
            }
            
            # Generate HTML
            html_content = self.visualizer.generate_comprehensive_course_page(vis_data)
            
            # Save to file
            timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
            filename = f"learning_path_{scenario_name.replace(' ', '_')}_{timestamp}.html"
            filepath = self.visualizer.save_comprehensive_visualization(vis_data, filename)
            
            print(f"    Visualization saved: {filepath}")
            
            # Also save as JSON for reference
            json_filename = filename.replace('.html', '.json')
            with open(json_filename, 'w', encoding='utf-8') as f:
                json.dump(result, f, indent=2, ensure_ascii=False)
            print(f"    JSON data saved: {json_filename}")
            
        except Exception as e:
            print(f"    Visualization failed: {e}")
    
    def save_test_summary(self):
        """Save comprehensive test summary."""
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        filename = f"test_results_real_paths_{timestamp}.json"
        
        summary = {
            'timestamp': timestamp,
            'total_tests': len(self.test_results),
            'successful': sum(1 for r in self.test_results if r['status'] == 'success'),
            'failed': sum(1 for r in self.test_results if r['status'] == 'failed'),
            'test_results': self.test_results,
            'performance_summary': {
                'avg_total_time': sum(r.get('performance', {}).get('total_time', 0) 
                                     for r in self.test_results if r['status'] == 'success') / 
                                 max(sum(1 for r in self.test_results if r['status'] == 'success'), 1),
                'avg_resources': sum(r.get('statistics', {}).get('total_resources', 0)
                                    for r in self.test_results if r['status'] == 'success') /
                                max(sum(1 for r in self.test_results if r['status'] == 'success'), 1),
                'avg_hours': sum(r.get('statistics', {}).get('total_hours', 0)
                                for r in self.test_results if r['status'] == 'success') /
                            max(sum(1 for r in self.test_results if r['status'] == 'success'), 1)
            }
        }
        
        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(summary, f, indent=2, ensure_ascii=False)
        
        print(f"\n Test summary saved: {filename}")
        
        # Print summary
        print("\n" + "="*80)
        print("TEST SUMMARY")
        print("="*80)
        print(f"Total Tests: {summary['total_tests']}")
        print(f" Successful: {summary['successful']}")
        print(f" Failed: {summary['failed']}")
        print(f"\n Performance Averages:")
        print(f"   Total Time: {summary['performance_summary']['avg_total_time']:.2f}s")
        print(f"   Resources per Path: {summary['performance_summary']['avg_resources']:.1f}")
        print(f"   Study Hours per Path: {summary['performance_summary']['avg_hours']:.1f}")


if __name__ == '__main__':
    # Run all real learning path tests
    test_suite = RealLearningPathTests()
    test_suite.run_all_tests()
    
    print("\n" + "="*80)
    print(" ALL REAL LEARNING PATH TESTS COMPLETE!")
    print("="*80)
    print("\nCheck the generated HTML files for visualizations:")
    print("  - learning_path_Web_Developer_*.html")
    print("  - learning_path_Data_Scientist_*.html")
    print("  - learning_path_AI_Engineer_*.html")
    print("  - learning_path_DevOps_Engineer_*.html")
    print("  - learning_path_Mobile_Developer_*.html")
    print("\nAnd JSON files for detailed data:")
    print("  - learning_path_*.json")
    print("  - test_results_real_paths_*.json")
