"""
Comprehensive Test Suite for GenMentor System with Optimization Benchmarks
Tests multiple scenarios, edge cases, system components, and performance optimizations.
Includes full resource curation testing.
"""

import time
import json
import sys
import asyncio
from typing import Dict, List, Tuple
from datetime import datetime
from ai_engine import GenMentorAI
import numpy as np

# Check available optimizations
try:
    from database_optimizer import ConnectionPool
    DATABASE_OPTIMIZER_AVAILABLE = True
except ImportError:
    DATABASE_OPTIMIZER_AVAILABLE = False

try:
    from faiss_optimizer import FAISSIndex
    FAISS_OPTIMIZER_AVAILABLE = True
except ImportError:
    FAISS_OPTIMIZER_AVAILABLE = False

try:
    from async_resource_curator import AsyncResourceCurator
    ASYNC_RESOURCE_AVAILABLE = True
except ImportError:
    ASYNC_RESOURCE_AVAILABLE = False

try:
    from improved_resource_curator import ImprovedResourceCurator
    RESOURCE_CURATOR_AVAILABLE = True
except ImportError:
    RESOURCE_CURATOR_AVAILABLE = False


class ComprehensiveTestSuite:
    """
    Enhanced testing framework for GenMentor system with optimization benchmarks.
    
    Tests cover:
    - Various career transitions (20+ scenarios)
    - Different skill levels and backgrounds
    - Edge cases and error handling
    - Performance benchmarks for all optimizations
    - Accuracy validation
    - System integration tests
    """
    
    def __init__(self):
        self.test_results = []
        self.benchmark_results = {}
        self.test_users = self._initialize_comprehensive_test_cases()
        
        print("=" * 80)
        print(" GenMentor Comprehensive Test Suite with Optimization Benchmarks")
        print("=" * 80)
        
        # Check available features
        print("\n📦 Available Features:")
        print(f"  • Database Optimizer: {'✅ Available' if DATABASE_OPTIMIZER_AVAILABLE else '❌ Not Available'}")
        print(f"  • FAISS Optimizer: {'✅ Available' if FAISS_OPTIMIZER_AVAILABLE else '❌ Not Available'}")
        print(f"  • Async Resource Curator: {'✅ Available' if ASYNC_RESOURCE_AVAILABLE else '❌ Not Available'}")
    
    def _initialize_comprehensive_test_cases(self) -> List[Dict]:
        """Initialize comprehensive test cases covering various scenarios."""
        return [
            # Tech Career Transitions
            {
                'test_id': 'TC001',
                'name': 'Marketing to Data Science',
                'goal': 'I want to transition from marketing to data science',
                'current_skills': ['excel', 'google analytics', 'basic statistics'],
                'expected_keywords': ['data', 'scientist', 'analyst', 'statistics'],
                'min_skills': 8,
                'category': 'tech_transition'
            },
            {
                'test_id': 'TC002',
                'name': 'Software Engineer to ML Engineer',
                'goal': 'I am a software engineer and want to become a machine learning engineer',
                'current_skills': ['python', 'java', 'algorithms', 'data structures'],
                'expected_keywords': ['machine learning', 'engineer', 'ai'],
                'min_skills': 10,
                'category': 'tech_advancement'
            },
            {
                'test_id': 'TC003',
                'name': 'Beginner Web Developer',
                'goal': 'I want to become a full-stack web developer',
                'current_skills': ['HTML', 'CSS', 'basic JavaScript'],
                'expected_keywords': ['web', 'developer', 'full stack'],
                'min_skills': 12,
                'category': 'beginner_tech'
            },
            {
                'test_id': 'TC004',
                'name': 'Data Analyst to Business Intelligence',
                'goal': 'I am a data analyst and want to move into business intelligence',
                'current_skills': ['SQL', 'Excel', 'Tableau', 'statistics'],
                'expected_keywords': ['business intelligence', 'analyst', 'data'],
                'min_skills': 8,
                'category': 'tech_advancement'
            },
            {
                'test_id': 'TC005',
                'name': 'Cloud Architect AWS',
                'goal': 'I want to become a cloud architect specializing in AWS',
                'current_skills': ['Linux', 'networking', 'basic AWS'],
                'expected_keywords': ['cloud', 'architect', 'aws'],
                'min_skills': 10,
                'category': 'tech_specialization'
            },
            {
                'test_id': 'TC006',
                'name': 'Cybersecurity Analyst',
                'goal': 'I want to become a cybersecurity analyst',
                'current_skills': ['networking basics', 'IT support'],
                'expected_keywords': ['security', 'cybersecurity', 'analyst'],
                'min_skills': 12,
                'category': 'beginner_tech'
            },
            {
                'test_id': 'TC007',
                'name': 'Finance to Data Engineering',
                'goal': 'I want to transition from finance to data engineering',
                'current_skills': ['Excel', 'SQL', 'financial analysis'],
                'expected_keywords': ['data', 'engineer', 'engineering'],
                'min_skills': 10,
                'category': 'tech_transition'
            },
            {
                'test_id': 'TC008',
                'name': 'Product Manager Tech',
                'goal': 'I want to become a product manager in tech',
                'current_skills': ['project management', 'business analysis'],
                'expected_keywords': ['product manager', 'manager', 'product'],
                'min_skills': 8,
                'category': 'management'
            },
            {
                'test_id': 'TC009',
                'name': 'DevOps Engineer',
                'goal': 'I want to become a DevOps engineer',
                'current_skills': ['Linux', 'Python', 'git'],
                'expected_keywords': ['devops', 'engineer', 'operations'],
                'min_skills': 12,
                'category': 'tech_specialization'
            },
            {
                'test_id': 'TC010',
                'name': 'AI Research Scientist',
                'goal': 'I want to become an AI research scientist',
                'current_skills': ['python', 'mathematics', 'statistics', 'machine learning'],
                'expected_keywords': ['ai', 'research', 'scientist', 'intelligence'],
                'min_skills': 8,
                'category': 'tech_advancement'
            },
            
            # Additional Career Paths
            {
                'test_id': 'TC011',
                'name': 'Mobile App Developer',
                'goal': 'I want to become a mobile app developer for iOS and Android',
                'current_skills': ['programming basics', 'UI design'],
                'expected_keywords': ['mobile', 'developer', 'app'],
                'min_skills': 10,
                'category': 'beginner_tech'
            },
            {
                'test_id': 'TC012',
                'name': 'Blockchain Developer',
                'goal': 'I want to become a blockchain developer',
                'current_skills': ['JavaScript', 'cryptography basics'],
                'expected_keywords': ['blockchain', 'developer', 'cryptocurrency'],
                'min_skills': 10,
                'category': 'tech_specialization'
            },
            {
                'test_id': 'TC013',
                'name': 'Game Developer',
                'goal': 'I want to become a game developer',
                'current_skills': ['C++', 'graphics basics'],
                'expected_keywords': ['game', 'developer', 'gaming'],
                'min_skills': 10,
                'category': 'tech_specialization'
            },
            {
                'test_id': 'TC014',
                'name': 'Database Administrator',
                'goal': 'I want to become a database administrator',
                'current_skills': ['SQL', 'basic networking'],
                'expected_keywords': ['database', 'administrator', 'dba'],
                'min_skills': 10,
                'category': 'tech_specialization'
            },
            {
                'test_id': 'TC015',
                'name': 'Network Engineer',
                'goal': 'I want to become a network engineer',
                'current_skills': ['networking basics', 'cisco'],
                'expected_keywords': ['network', 'engineer', 'networking'],
                'min_skills': 10,
                'category': 'tech_specialization'
            },
            
            # Edge Cases
            {
                'test_id': 'TC016',
                'name': 'Minimal Skills Input',
                'goal': 'I want to learn programming',
                'current_skills': [],
                'expected_keywords': ['programming', 'developer', 'software'],
                'min_skills': 5,
                'category': 'edge_case'
            },
            {
                'test_id': 'TC017',
                'name': 'Vague Goal',
                'goal': 'I want to work with computers',
                'current_skills': ['basic computer skills'],
                'expected_keywords': ['computer', 'it', 'technology'],
                'min_skills': 5,
                'category': 'edge_case'
            },
            {
                'test_id': 'TC018',
                'name': 'Many Current Skills',
                'goal': 'I want to advance my data science career',
                'current_skills': ['python', 'R', 'SQL', 'machine learning', 'deep learning', 
                                 'statistics', 'data visualization', 'tableau', 'pandas', 'numpy'],
                'expected_keywords': ['data', 'scientist', 'advanced'],
                'min_skills': 3,
                'category': 'edge_case'
            },
            {
                'test_id': 'TC019',
                'name': 'Long Detailed Goal',
                'goal': 'I am currently working as a business analyst with 5 years of experience in retail industry and I want to transition to a data science role focusing on predictive analytics and machine learning in the e-commerce domain',
                'current_skills': ['excel', 'SQL', 'business intelligence', 'statistics'],
                'expected_keywords': ['data', 'scientist', 'analytics'],
                'min_skills': 8,
                'category': 'edge_case'
            },
            {
                'test_id': 'TC020',
                'name': 'Short Goal',
                'goal': 'AI Engineer',
                'current_skills': ['python'],
                'expected_keywords': ['ai', 'engineer', 'intelligence'],
                'min_skills': 8,
                'category': 'edge_case'
            }
        ]
    
    def print_header(self, text: str, char: str = "="):
        """Print formatted section header."""
        print(f"\n{char * 80}")
        print(f" {text}")
        print(f"{char * 80}")
    
    def print_subheader(self, text: str):
        """Print formatted subsection header."""
        print(f"\n{'─' * 80}")
        print(f" {text}")
        print(f"{'─' * 80}")
    
    def benchmark_occupation_matching(self, ai_engine: GenMentorAI, goal: str, iterations: int = 5) -> Dict:
        """Benchmark occupation matching with and without FAISS."""
        print(f"\n  Testing occupation matching for: '{goal[:50]}...'")
        
        expanded_goal = ai_engine._super_expand_goal_with_domain_knowledge(goal)
        goal_embedding = ai_engine.model.encode([expanded_goal])
        
        results = {
            'with_faiss': None,
            'without_faiss': None,
            'speedup': 0
        }
        
        # Test with FAISS if available
        if ai_engine.faiss_index and ai_engine.faiss_index.index:
            times = []
            for _ in range(iterations):
                start = time.time()
                uri, similarity, raw_sim = ai_engine._faiss_occupation_matching(goal, expanded_goal, goal_embedding)
                times.append(time.time() - start)
            
            results['with_faiss'] = {
                'avg_time': np.mean(times),
                'min_time': np.min(times),
                'max_time': np.max(times),
                'std_time': np.std(times)
            }
            print(f"    ✅ FAISS matching: {results['with_faiss']['avg_time']*1000:.2f}ms (avg)")
        
        # Test without FAISS (simulate linear search)
        times = []
        for _ in range(iterations):
            start = time.time()
            # Simulate linear search through occupations
            best_sim = -1
            for uri, embedding in list(ai_engine.occupation_embeddings.items())[:100]:  # Sample 100 for speed
                from sklearn.metrics.pairwise import cosine_similarity
                sim = cosine_similarity(goal_embedding, [embedding])[0][0]
                if sim > best_sim:
                    best_sim = sim
            times.append(time.time() - start)
        
        results['without_faiss'] = {
            'avg_time': np.mean(times),
            'min_time': np.min(times),
            'max_time': np.max(times),
            'std_time': np.std(times)
        }
        print(f"    ⚠️  Linear search: {results['without_faiss']['avg_time']*1000:.2f}ms (avg)")
        
        if results['with_faiss']:
            results['speedup'] = results['without_faiss']['avg_time'] / results['with_faiss']['avg_time']
            print(f"    🚀 Speedup: {results['speedup']:.2f}x")
        
        return results
    
    def benchmark_database_operations(self, ai_engine: GenMentorAI, iterations: int = 10) -> Dict:
        """Benchmark database operations with and without connection pooling."""
        print(f"\n  Testing database operations...")
        
        results = {
            'with_pool': None,
            'without_pool': None,
            'speedup': 0
        }
        
        # Test with connection pool
        if ai_engine.db_pool:
            times = []
            for _ in range(iterations):
                start = time.time()
                with ai_engine._get_db_connection() as conn:
                    cursor = conn.cursor()
                    cursor.execute("SELECT COUNT(*) FROM skills")
                    cursor.fetchone()
                times.append(time.time() - start)
            
            results['with_pool'] = {
                'avg_time': np.mean(times),
                'min_time': np.min(times),
                'max_time': np.max(times),
                'std_time': np.std(times)
            }
            print(f"    ✅ Connection pool: {results['with_pool']['avg_time']*1000:.2f}ms (avg)")
        
        # Test without pool (direct connection)
        import sqlite3
        times = []
        for _ in range(iterations):
            start = time.time()
            conn = sqlite3.connect('genmentor.db')
            cursor = conn.cursor()
            cursor.execute("SELECT COUNT(*) FROM skills")
            cursor.fetchone()
            conn.close()
            times.append(time.time() - start)
        
        results['without_pool'] = {
            'avg_time': np.mean(times),
            'min_time': np.min(times),
            'max_time': np.max(times),
            'std_time': np.std(times)
        }
        print(f"    ⚠️  Direct connection: {results['without_pool']['avg_time']*1000:.2f}ms (avg)")
        
        if results['with_pool']:
            results['speedup'] = results['without_pool']['avg_time'] / results['with_pool']['avg_time']
            improvement = (1 - results['with_pool']['avg_time'] / results['without_pool']['avg_time']) * 100
            print(f"    🚀 Improvement: {improvement:.1f}% faster")
        
        return results
    
    def run_performance_benchmarks(self):
        """Run comprehensive performance benchmarks for all optimizations."""
        self.print_header("PERFORMANCE BENCHMARKS", "=")
        
        print("\n🔧 Initializing AI Engine for benchmarking...")
        ai_engine = GenMentorAI()
        
        # Benchmark 1: Occupation Matching (FAISS)
        self.print_subheader("1. Occupation Matching Benchmark (FAISS)")
        
        test_goals = [
            "I want to become a data scientist",
            "I want to transition to machine learning engineer",
            "I want to become a full-stack developer"
        ]
        
        occupation_results = []
        for goal in test_goals:
            result = self.benchmark_occupation_matching(ai_engine, goal, iterations=5)
            occupation_results.append(result)
        
        # Calculate average speedup
        avg_speedup = np.mean([r['speedup'] for r in occupation_results if r['speedup'] > 0])
        self.benchmark_results['occupation_matching'] = {
            'avg_speedup': avg_speedup,
            'details': occupation_results
        }
        print(f"\n  📊 Average FAISS Speedup: {avg_speedup:.2f}x")
        
        # Benchmark 2: Database Operations (Connection Pool)
        self.print_subheader("2. Database Operations Benchmark (Connection Pool)")
        
        db_result = self.benchmark_database_operations(ai_engine, iterations=20)
        self.benchmark_results['database_operations'] = db_result
        
        # Benchmark 3: Full Skill Gap Analysis
        self.print_subheader("3. End-to-End Skill Gap Analysis Benchmark")
        
        print("\n  Testing full skill gap analysis pipeline...")
        times = []
        for i in range(3):
            test_case = self.test_users[i]
            start = time.time()
            result = ai_engine.identify_skill_gap(test_case['goal'], test_case['current_skills'])
            elapsed = time.time() - start
            times.append(elapsed)
            print(f"    Test {i+1}: {elapsed:.2f}s - {len(result.get('skill_gap', []))} skills identified")
        
        self.benchmark_results['skill_gap_analysis'] = {
            'avg_time': np.mean(times),
            'min_time': np.min(times),
            'max_time': np.max(times)
        }
        print(f"\n  📊 Average Time: {np.mean(times):.2f}s")
        
        # Benchmark 4: Learning Path Scheduling
        self.print_subheader("4. Learning Path Scheduling Benchmark")
        
        print("\n  Testing learning path generation...")
        scheduling_times = []
        for i in range(3):
            test_case = self.test_users[i]
            result = ai_engine.identify_skill_gap(test_case['goal'], test_case['current_skills'])
            
            if result['skill_gap']:
                start = time.time()
                learning_path = ai_engine.schedule_learning_path(result['skill_gap'][:15])
                elapsed = time.time() - start
                scheduling_times.append(elapsed)
                print(f"    Test {i+1}: {elapsed:.2f}s - {len(learning_path)} sessions created")
        
        self.benchmark_results['learning_path_scheduling'] = {
            'avg_time': np.mean(scheduling_times),
            'min_time': np.min(scheduling_times),
            'max_time': np.max(scheduling_times)
        }
        print(f"\n  📊 Average Time: {np.mean(scheduling_times):.2f}s")
        
        # Summary
        self.print_subheader("Benchmark Summary")
        print("\n  🏆 Performance Improvements:")
        if 'occupation_matching' in self.benchmark_results:
            print(f"    • Occupation Matching (FAISS): {self.benchmark_results['occupation_matching']['avg_speedup']:.2f}x faster")
        if 'database_operations' in self.benchmark_results and self.benchmark_results['database_operations']['speedup'] > 0:
            improvement = (1 - 1/self.benchmark_results['database_operations']['speedup']) * 100
            print(f"    • Database Operations (Pool): {improvement:.1f}% faster")
        print(f"    • Skill Gap Analysis: {self.benchmark_results['skill_gap_analysis']['avg_time']:.2f}s average")
        print(f"    • Learning Path Generation: {self.benchmark_results['learning_path_scheduling']['avg_time']:.2f}s average")
    
    def test_skill_gap_identification(self, test_case: Dict, ai_engine: GenMentorAI) -> Dict:
        """Test skill gap identification for a single test case."""
        start_time = time.time()
        
        try:
            result = ai_engine.identify_skill_gap(
                test_case['goal'],
                test_case['current_skills']
            )
            
            elapsed_time = time.time() - start_time
            
            # Validate results
            occupation = result.get('matched_occupation', {})
            skill_gap = result.get('skill_gap', [])
            
            # Check if occupation matches expected keywords
            occupation_label = occupation.get('label', '').lower()
            keyword_match = any(keyword in occupation_label for keyword in test_case['expected_keywords'])
            
            # Validate skill count
            sufficient_skills = len(skill_gap) >= test_case.get('min_skills', 5)
            
            # Count technical skills (non-soft skills)
            technical_skills = [s for s in skill_gap if not ai_engine._is_soft_or_irrelevant_skill(s.get('label', ''))]
            
            test_result = {
                'test_id': test_case['test_id'],
                'name': test_case['name'],
                'status': 'PASS' if keyword_match and sufficient_skills else 'WARN',
                'elapsed_time': elapsed_time,
                'matched_occupation': occupation.get('label', 'Unknown'),
                'similarity_score': occupation.get('similarity_score', 0),
                'total_skills': len(skill_gap),
                'technical_skills': len(technical_skills),
                'keyword_match': keyword_match,
                'sufficient_skills': sufficient_skills,
                'category': test_case.get('category', 'unknown')
            }
            
            return test_result
            
        except Exception as e:
            return {
                'test_id': test_case['test_id'],
                'name': test_case['name'],
                'status': 'FAIL',
                'error': str(e),
                'elapsed_time': time.time() - start_time,
                'category': test_case.get('category', 'unknown')
            }
    
    def test_learning_path_generation(self, test_case: Dict, ai_engine: GenMentorAI) -> Dict:
        """Test learning path generation for a single test case."""
        try:
            # First get skill gap
            skill_gap_result = ai_engine.identify_skill_gap(
                test_case['goal'],
                test_case['current_skills']
            )
            
            if not skill_gap_result.get('skill_gap'):
                return {
                    'test_id': test_case['test_id'],
                    'status': 'SKIP',
                    'reason': 'No skill gap identified'
                }
            
            start_time = time.time()
            
            # Generate learning path
            learning_path = ai_engine.schedule_learning_path(
                skill_gap_result['skill_gap'][:15]  # Limit to 15 skills for speed
            )
            
            elapsed_time = time.time() - start_time
            
            # Validate learning path
            has_sessions = len(learning_path) > 0
            has_skills = all('skills' in session for session in learning_path)
            has_duration = all('estimated_duration_hours' in session for session in learning_path)
            
            # Calculate total duration
            total_duration = sum(session.get('estimated_duration_hours', 0) for session in learning_path)
            
            # Check skill categorization
            categories_used = set()
            for session in learning_path:
                for skill in session.get('skills', []):
                    if isinstance(skill, dict):
                        label = skill.get('label', '')
                    else:
                        label = skill
                    
                    # Determine category
                    label_lower = label.lower()
                    if any(kw in label_lower for kw in ['python', 'java', 'programming']):
                        categories_used.add('programming')
                    elif any(kw in label_lower for kw in ['data', 'analysis', 'statistics']):
                        categories_used.add('data_analysis')
                    elif any(kw in label_lower for kw in ['machine learning', 'ai', 'neural']):
                        categories_used.add('machine_learning')
            
            return {
                'test_id': test_case['test_id'],
                'status': 'PASS' if has_sessions and has_skills and has_duration else 'WARN',
                'elapsed_time': elapsed_time,
                'total_sessions': len(learning_path),
                'total_duration_hours': total_duration,
                'has_valid_structure': has_sessions and has_skills and has_duration,
                'categories_identified': len(categories_used),
                'category_names': list(categories_used)
            }
            
        except Exception as e:
            return {
                'test_id': test_case['test_id'],
                'status': 'FAIL',
                'error': str(e)
            }
    
    def run_functional_tests(self):
        """Run comprehensive functional tests on all test cases."""
        self.print_header("FUNCTIONAL TESTS - SKILL GAP IDENTIFICATION", "=")
        
        print("\n🔧 Initializing AI Engine...")
        ai_engine = GenMentorAI()
        print("✅ AI Engine initialized\n")
        
        # Group tests by category
        categories = {}
        for test_case in self.test_users:
            cat = test_case.get('category', 'unknown')
            if cat not in categories:
                categories[cat] = []
            categories[cat].append(test_case)
        
        all_results = []
        
        # Run tests by category
        for category, test_cases in categories.items():
            self.print_subheader(f"Category: {category.replace('_', ' ').title()}")
            
            for i, test_case in enumerate(test_cases, 1):
                print(f"\n  [{test_case['test_id']}] {test_case['name']}")
                print(f"  Goal: {test_case['goal'][:60]}...")
                print(f"  Current Skills: {len(test_case['current_skills'])} skills")
                
                result = self.test_skill_gap_identification(test_case, ai_engine)
                all_results.append(result)
                
                if result['status'] == 'PASS':
                    print(f"  ✅ PASS - {result['matched_occupation']} (similarity: {result['similarity_score']:.1%})")
                    print(f"     Skills: {result['technical_skills']} technical / {result['total_skills']} total")
                    print(f"     Time: {result['elapsed_time']:.2f}s")
                elif result['status'] == 'WARN':
                    print(f"  ⚠️  WARN - {result.get('matched_occupation', 'N/A')}")
                    if not result.get('keyword_match'):
                        print(f"     Issue: Occupation doesn't match expected keywords")
                    if not result.get('sufficient_skills'):
                        print(f"     Issue: Insufficient skills ({result.get('total_skills', 0)} < {test_case.get('min_skills', 5)})")
                else:
                    print(f"  ❌ FAIL - {result.get('error', 'Unknown error')}")
        
        # Summary statistics
        self.print_subheader("Test Results Summary")
        
        total_tests = len(all_results)
        passed = len([r for r in all_results if r['status'] == 'PASS'])
        warned = len([r for r in all_results if r['status'] == 'WARN'])
        failed = len([r for r in all_results if r['status'] == 'FAIL'])
        
        print(f"\n  📊 Overall Results:")
        print(f"    • Total Tests: {total_tests}")
        print(f"    • Passed: {passed} ({passed/total_tests*100:.1f}%)")
        print(f"    • Warnings: {warned} ({warned/total_tests*100:.1f}%)")
        print(f"    • Failed: {failed} ({failed/total_tests*100:.1f}%)")
        
        avg_time = np.mean([r['elapsed_time'] for r in all_results if 'elapsed_time' in r])
        avg_skills = np.mean([r['total_skills'] for r in all_results if 'total_skills' in r])
        avg_similarity = np.mean([r['similarity_score'] for r in all_results if 'similarity_score' in r])
        
        print(f"\n  📈 Performance Metrics:")
        print(f"    • Average Time: {avg_time:.2f}s")
        print(f"    • Average Skills Identified: {avg_skills:.1f}")
        print(f"    • Average Similarity Score: {avg_similarity:.1%}")
        
        # Category breakdown
        print(f"\n  📂 Results by Category:")
        for category in categories.keys():
            cat_results = [r for r in all_results if r.get('category') == category]
            cat_passed = len([r for r in cat_results if r['status'] == 'PASS'])
            print(f"    • {category.replace('_', ' ').title()}: {cat_passed}/{len(cat_results)} passed")
        
        self.test_results.extend(all_results)
        
        # Learning Path Tests
        self.print_header("FUNCTIONAL TESTS - LEARNING PATH GENERATION", "=")
        
        print("\n  Testing learning path generation for sample cases...\n")
        
        # Test learning paths for first 5 cases
        path_results = []
        for i, test_case in enumerate(self.test_users[:5], 1):
            print(f"  [{test_case['test_id']}] Generating learning path for: {test_case['name']}")
            result = self.test_learning_path_generation(test_case, ai_engine)
            path_results.append(result)
            
            if result['status'] == 'PASS':
                print(f"  ✅ PASS - {result['total_sessions']} sessions, {result['total_duration_hours']} hours")
                print(f"     Categories: {', '.join(result['category_names'])}")
                print(f"     Time: {result['elapsed_time']:.2f}s")
            elif result['status'] == 'SKIP':
                print(f"  ⏭️  SKIP - {result['reason']}")
            else:
                print(f"  ❌ FAIL - {result.get('error', 'Unknown error')}")
            print()
        
        # Path generation summary
        self.print_subheader("Learning Path Test Summary")
        
        path_passed = len([r for r in path_results if r['status'] == 'PASS'])
        path_skipped = len([r for r in path_results if r['status'] == 'SKIP'])
        path_failed = len([r for r in path_results if r['status'] == 'FAIL'])
        
        print(f"\n  📊 Learning Path Results:")
        print(f"    • Total Tests: {len(path_results)}")
        print(f"    • Passed: {path_passed}")
        print(f"    • Skipped: {path_skipped}")
        print(f"    • Failed: {path_failed}")
        
        if path_passed > 0:
            avg_sessions = np.mean([r['total_sessions'] for r in path_results if 'total_sessions' in r])
            avg_duration = np.mean([r['total_duration_hours'] for r in path_results if 'total_duration_hours' in r])
            avg_categories = np.mean([r['categories_identified'] for r in path_results if 'categories_identified' in r])
            
            print(f"\n  📈 Path Metrics:")
            print(f"    • Average Sessions: {avg_sessions:.1f}")
            print(f"    • Average Duration: {avg_duration:.1f} hours")
            print(f"    • Average Categories: {avg_categories:.1f}")
    
    def generate_report(self):
        """Generate comprehensive test report."""
        self.print_header("TEST REPORT SUMMARY", "=")
        
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        
        print(f"\n  📅 Test Run: {timestamp}")
        print(f"\n  🎯 Test Coverage:")
        print(f"    • Total Test Cases: {len(self.test_users)}")
        print(f"    • Functional Tests: {len(self.test_results)}")
        print(f"    • Benchmark Tests: {len(self.benchmark_results)}")
        
        if self.test_results:
            print(f"\n  ✅ Functional Test Success Rate:")
            passed = len([r for r in self.test_results if r['status'] == 'PASS'])
            print(f"    • {passed}/{len(self.test_results)} ({passed/len(self.test_results)*100:.1f}%)")
        
        if self.benchmark_results:
            print(f"\n  🚀 Performance Benchmarks:")
            if 'occupation_matching' in self.benchmark_results:
                print(f"    • FAISS Occupation Matching: {self.benchmark_results['occupation_matching']['avg_speedup']:.2f}x speedup")
            if 'database_operations' in self.benchmark_results and self.benchmark_results['database_operations']['speedup'] > 0:
                print(f"    • Connection Pool: {self.benchmark_results['database_operations']['speedup']:.2f}x speedup")
            if 'skill_gap_analysis' in self.benchmark_results:
                print(f"    • Skill Gap Analysis: {self.benchmark_results['skill_gap_analysis']['avg_time']:.2f}s average")
            if 'learning_path_scheduling' in self.benchmark_results:
                print(f"    • Learning Path Generation: {self.benchmark_results['learning_path_scheduling']['avg_time']:.2f}s average")
        
        print(f"\n  💾 Saving detailed report to JSON...")
        report = {
            'timestamp': timestamp,
            'test_cases': len(self.test_users),
            'functional_results': self.test_results,
            'benchmark_results': self.benchmark_results,
            'summary': {
                'total_tests': len(self.test_results),
                'passed': len([r for r in self.test_results if r['status'] == 'PASS']),
                'warned': len([r for r in self.test_results if r['status'] == 'WARN']),
                'failed': len([r for r in self.test_results if r['status'] == 'FAIL'])
            }
        }
        
        with open('comprehensive_test_report.json', 'w') as f:
            json.dump(report, f, indent=2)
        
        print(f"  ✅ Report saved: comprehensive_test_report.json")
    
    def test_resource_curation(self):
        """Test complete resource curation for learning paths."""
        self.print_header("RESOURCE CURATION TESTS", "=")
        
        print("  Testing end-to-end learning path with resource curation...\n")
        
        # Initialize AI engine
        print("🔧 Initializing AI Engine...")
        ai_engine = GenMentorAI()
        print("✅ AI Engine initialized\n")
        
        # Initialize resource curator
        if RESOURCE_CURATOR_AVAILABLE:
            resource_curator = ImprovedResourceCurator()
            print("✅ Resource curator initialized\n")
        else:
            print("⚠️  Resource curator not available, skipping tests\n")
            return
        
        # Test case
        test_case = {
            'name': 'Marketing to Data Science (Full System)',
            'goal': 'I want to transition from marketing to data science',
            'current_skills': ['marketing analytics', 'excel', 'basic statistics']
        }
        
        print(f"  📋 Test Case: {test_case['name']}")
        print(f"  Goal: {test_case['goal']}")
        print(f"  Current Skills: {', '.join(test_case['current_skills'])}\n")
        
        print("─" * 80)
        print("  STEP 1: Skill Gap Analysis")
        print("─" * 80)
        
        start_time = time.time()
        result = ai_engine.identify_skill_gap(test_case['goal'], test_case['current_skills'])
        gap_time = time.time() - start_time
        
        print(f"\n  ✅ Matched Occupation: {result['matched_occupation']['label']}")
        print(f"     Similarity: {result['matched_occupation']['similarity_score']*100:.1f}%")
        print(f"     Time: {gap_time:.2f}s")
        print(f"  ✅ Skills to Learn: {len(result['skill_gap'])} skills identified\n")
        
        print("─" * 80)
        print("  STEP 2: Learning Path Generation")
        print("─" * 80)
        
        start_time = time.time()
        learning_path = ai_engine.schedule_learning_path(result['skill_gap'])
        path_time = time.time() - start_time
        
        print(f"\n  ✅ Generated {len(learning_path)} learning sessions")
        print(f"     Total Duration: {sum(s.get('estimated_duration_hours', 0) for s in learning_path)} hours")
        print(f"     Time: {path_time:.2f}s\n")
        
        print("─" * 80)
        print("  STEP 3: Resource Curation for Each Skill")
        print("─" * 80)
        
        total_resources = 0
        skills_with_resources = 0
        resource_details = []
        
        print("\n  Curating resources for each skill...\n")
        
        for session_idx, session in enumerate(learning_path[:3], 1):  # Test first 3 sessions
            print(f"  📚 Session {session_idx}: {session.get('title', 'Untitled')}")
            
            session_skills = session.get('skills', [])
            for skill_idx, skill in enumerate(session_skills[:2], 1):  # Test first 2 skills per session
                if isinstance(skill, dict):
                    skill_name = skill.get('label', str(skill))
                else:
                    skill_name = str(skill)
                
                print(f"     └─ Skill {skill_idx}: {skill_name}")
                
                # Get resources for this skill
                start_time = time.time()
                resources = resource_curator.search_resources(skill_name, limit=10)
                resource_time = time.time() - start_time
                
                if resources and len(resources) > 0:
                    skills_with_resources += 1
                    total_resources += len(resources)
                    
                    print(f"        ✅ Found {len(resources)} resources ({resource_time:.2f}s)")
                    
                    # Show first 3 resources
                    for res_idx, resource in enumerate(resources[:3], 1):
                        print(f"           {res_idx}. [{resource.get('type', 'N/A')}] {resource.get('title', 'Untitled')}")
                        print(f"              URL: {resource.get('url', 'N/A')}")
                        print(f"              Provider: {resource.get('provider', 'N/A')}")
                    
                    if len(resources) > 3:
                        print(f"           ... and {len(resources) - 3} more resources")
                    
                    resource_details.append({
                        'skill': skill_name,
                        'resources_found': len(resources),
                        'time': resource_time,
                        'sample_resources': resources[:3]
                    })
                else:
                    print(f"        ⚠️  No resources found")
            
            print()
        
        print("─" * 80)
        print("  STEP 4: Async Resource Curation (Batch)")
        print("─" * 80)
        
        if ASYNC_RESOURCE_AVAILABLE:
            print("\n  Testing async batch resource fetching...\n")
            
            # Collect all skills from first 3 sessions
            all_skills = []
            for session in learning_path[:3]:
                for skill in session.get('skills', [])[:2]:
                    if isinstance(skill, dict):
                        all_skills.append(skill.get('label', str(skill)))
                    else:
                        all_skills.append(str(skill))
            
            print(f"  Fetching resources for {len(all_skills)} skills in parallel...")
            
            async_curator = AsyncResourceCurator()
            start_time = time.time()
            resources_dict = asyncio.run(async_curator.batch_search(all_skills))
            async_time = time.time() - start_time
            
            async_total = sum(len(resources) for resources in resources_dict.values())
            async_with_resources = len([r for r in resources_dict.values() if len(r) > 0])
            
            print(f"\n  ✅ Async Batch Results:")
            print(f"     Skills Processed: {len(all_skills)}")
            print(f"     Skills with Resources: {async_with_resources}/{len(all_skills)}")
            print(f"     Total Resources: {async_total}")
            print(f"     Time: {async_time:.2f}s")
            print(f"     🚀 Average per skill: {async_time/len(all_skills):.2f}s")
        else:
            print("\n  ⚠️  Async resource curator not available\n")
        
        print("\n" + "─" * 80)
        print("  Resource Curation Summary")
        print("─" * 80)
        
        print(f"\n  📊 Overall Statistics:")
        print(f"     • Skills Processed: {skills_with_resources} skills")
        print(f"     • Total Resources Found: {total_resources}")
        print(f"     • Average Resources per Skill: {total_resources/max(skills_with_resources, 1):.1f}")
        print(f"     • Coverage: {skills_with_resources}/{len(resource_details)*2 if resource_details else 0} ({skills_with_resources/(len(resource_details)*2)*100 if resource_details else 0:.1f}%)")
        
        print(f"\n  💾 Saving sample with resources...")
        
        # Save complete example
        full_output = {
            'test_case': test_case,
            'matched_occupation': result['matched_occupation'],
            'skill_gap_summary': {
                'total_skills': len(result['skill_gap']),
                'skills_to_learn': len(result['skill_gap'])
            },
            'learning_path': learning_path,
            'resource_curation': {
                'skills_processed': skills_with_resources,
                'total_resources': total_resources,
                'resource_details': resource_details
            },
            'timing': {
                'skill_gap_analysis': gap_time,
                'learning_path_generation': path_time
            }
        }
        
        with open('complete_learning_path_with_resources.json', 'w', encoding='utf-8') as f:
            json.dump(full_output, f, indent=2, ensure_ascii=False)
        
        print(f"  ✅ Saved: complete_learning_path_with_resources.json\n")

    def run_all_tests(self):
        """Run complete test suite with benchmarks and functional tests."""
        print("\n🚀 Starting Comprehensive Test Suite...\n")
        
        # Run performance benchmarks first
        self.run_performance_benchmarks()
        
        # Run functional tests
        self.run_functional_tests()
        
        # Test resource curation (NEW)
        self.test_resource_curation()
        
        # Generate final report
        self.generate_report()
        
        print("\n" + "=" * 80)
        print(" ✅ ALL TESTS COMPLETED")
        print("=" * 80)


if __name__ == "__main__":
    # Run comprehensive test suite
    test_suite = ComprehensiveTestSuite()
    test_suite.run_all_tests()
