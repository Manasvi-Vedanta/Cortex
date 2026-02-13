"""
Comprehensive Evaluation Test Suite for Hybrid GenMentor
Runs 20 different tech career goal tests with detailed metrics and professional visualizations.

"""

import requests
import json
import time
import os
import sys
from datetime import datetime
from typing import Dict, List, Any, Optional, Tuple
from dataclasses import dataclass, field, asdict
from collections import defaultdict
import statistics
import traceback

# Try to import visualization libraries
try:
    import matplotlib.pyplot as plt
    import matplotlib.patches as mpatches
    from matplotlib.gridspec import GridSpec
    import numpy as np
    VISUALIZATION_AVAILABLE = True
except ImportError:
    VISUALIZATION_AVAILABLE = False
    print("Warning: matplotlib/numpy not installed. Install with: pip install matplotlib numpy")

try:
    import seaborn as sns
    SEABORN_AVAILABLE = True
except ImportError:
    SEABORN_AVAILABLE = False
    print("Warning: seaborn not installed. Install with: pip install seaborn")

# Configuration
BASE_URL = "http://localhost:5000"
TIMESTAMP = datetime.now().strftime('%Y%m%d_%H%M%S')
OUTPUT_DIR = f"evaluation_outputs_{TIMESTAMP}"
GRAPHS_DIR = os.path.join(OUTPUT_DIR, "graphs")
LOG_FILE = os.path.join(OUTPUT_DIR, "evaluation_log.txt")

# 20 Different Tech Career Goals for Comprehensive Testing
TEST_CASES = [
    {
        "id": "01",
        "goal": "I want to become a Machine Learning Engineer.",
        "short_name": "ML Engineer",
        "category": "AI/ML",
        "suggestions": [
            ("TensorFlow", "http://data.europa.eu/esco/skill/ml-tensorflow", "Deep learning framework"),
            ("PyTorch", "http://data.europa.eu/esco/skill/ml-pytorch", "Dynamic neural network framework"),
            ("MLOps", "http://data.europa.eu/esco/skill/ml-mlops", "ML operations and deployment")
        ]
    },
    {
        "id": "02",
        "goal": "I want to become a DevOps Engineer.",
        "short_name": "DevOps Engineer",
        "category": "Infrastructure",
        "suggestions": [
            ("Kubernetes", "http://data.europa.eu/esco/skill/devops-kubernetes", "Container orchestration"),
            ("Terraform", "http://data.europa.eu/esco/skill/devops-terraform", "Infrastructure as Code"),
            ("CI/CD Pipelines", "http://data.europa.eu/esco/skill/devops-cicd", "Continuous integration/deployment")
        ]
    },
    {
        "id": "03",
        "goal": "I want to become a Frontend Developer.",
        "short_name": "Frontend Developer",
        "category": "Web Development",
        "suggestions": [
            ("React", "http://data.europa.eu/esco/skill/frontend-react", "Component-based UI library"),
            ("TypeScript", "http://data.europa.eu/esco/skill/frontend-typescript", "Typed JavaScript"),
            ("CSS Frameworks", "http://data.europa.eu/esco/skill/frontend-css", "Tailwind/Bootstrap styling")
        ]
    },
    {
        "id": "04",
        "goal": "I want to become a Backend Developer.",
        "short_name": "Backend Developer",
        "category": "Web Development",
        "suggestions": [
            ("Node.js", "http://data.europa.eu/esco/skill/backend-nodejs", "Server-side JavaScript"),
            ("REST API Design", "http://data.europa.eu/esco/skill/backend-rest", "RESTful API architecture"),
            ("Database Design", "http://data.europa.eu/esco/skill/backend-database", "SQL and NoSQL databases")
        ]
    },
    {
        "id": "05",
        "goal": "I want to become a Data Scientist.",
        "short_name": "Data Scientist",
        "category": "AI/ML",
        "suggestions": [
            ("Statistical Analysis", "http://data.europa.eu/esco/skill/ds-statistics", "Advanced statistics"),
            ("Data Visualization", "http://data.europa.eu/esco/skill/ds-visualization", "Matplotlib/Seaborn/Plotly"),
            ("Feature Engineering", "http://data.europa.eu/esco/skill/ds-features", "Data transformation techniques")
        ]
    },
    {
        "id": "06",
        "goal": "I want to become a Cloud Architect.",
        "short_name": "Cloud Architect",
        "category": "Infrastructure",
        "suggestions": [
            ("AWS Solutions", "http://data.europa.eu/esco/skill/cloud-aws", "Amazon Web Services"),
            ("Azure Architecture", "http://data.europa.eu/esco/skill/cloud-azure", "Microsoft Azure"),
            ("Cloud Security", "http://data.europa.eu/esco/skill/cloud-security", "Cloud security best practices")
        ]
    },
    {
        "id": "07",
        "goal": "I want to become a Cybersecurity Analyst.",
        "short_name": "Cybersecurity Analyst",
        "category": "Security",
        "suggestions": [
            ("Penetration Testing", "http://data.europa.eu/esco/skill/security-pentest", "Ethical hacking"),
            ("SIEM Tools", "http://data.europa.eu/esco/skill/security-siem", "Security monitoring"),
            ("Incident Response", "http://data.europa.eu/esco/skill/security-incident", "Security incident handling")
        ]
    },
    {
        "id": "08",
        "goal": "I want to become a Full Stack Developer.",
        "short_name": "Full Stack Developer",
        "category": "Web Development",
        "suggestions": [
            ("MERN Stack", "http://data.europa.eu/esco/skill/fullstack-mern", "MongoDB/Express/React/Node"),
            ("GraphQL", "http://data.europa.eu/esco/skill/fullstack-graphql", "Query language for APIs"),
            ("Microservices", "http://data.europa.eu/esco/skill/fullstack-microservices", "Distributed architecture")
        ]
    },
    {
        "id": "09",
        "goal": "I want to become an Android App Developer.",
        "short_name": "Android Developer",
        "category": "Mobile Development",
        "suggestions": [
            ("Kotlin", "http://data.europa.eu/esco/skill/android-kotlin", "Primary modern programming language for Android development"),
            ("Jetpack Compose", "http://data.europa.eu/esco/skill/android-jetpack-compose", "Modern declarative UI toolkit for building native Android interfaces"),
            ("Firebase", "http://data.europa.eu/esco/skill/mobile-firebase", "Backend-as-a-Service platform for mobile app development")
        ]
    },
    {
        "id": "10",
        "goal": "I want to become an iOS App Developer.",
        "short_name": "iOS Developer",
        "category": "Mobile Development",
        "suggestions": [
            ("SwiftUI", "http://data.europa.eu/esco/skill/ios-swiftui", "Declarative UI framework"),
            ("Core Data", "http://data.europa.eu/esco/skill/ios-coredata", "Data persistence"),
            ("App Store Optimization", "http://data.europa.eu/esco/skill/ios-aso", "App visibility optimization")
        ]
    },
    {
        "id": "11",
        "goal": "I want to become a Data Engineer.",
        "short_name": "Data Engineer",
        "category": "Data",
        "suggestions": [
            ("Apache Spark", "http://data.europa.eu/esco/skill/de-spark", "Big data processing"),
            ("ETL Pipelines", "http://data.europa.eu/esco/skill/de-etl", "Data transformation"),
            ("Data Warehousing", "http://data.europa.eu/esco/skill/de-warehouse", "Data storage solutions")
        ]
    },
    {
        "id": "12",
        "goal": "I want to become a Blockchain Developer.",
        "short_name": "Blockchain Developer",
        "category": "Emerging Tech",
        "suggestions": [
            ("Solidity", "http://data.europa.eu/esco/skill/blockchain-solidity", "Smart contract language"),
            ("Web3.js", "http://data.europa.eu/esco/skill/blockchain-web3", "Ethereum JavaScript API"),
            ("DeFi Protocols", "http://data.europa.eu/esco/skill/blockchain-defi", "Decentralized finance")
        ]
    },
    {
        "id": "13",
        "goal": "I want to become a Game Developer.",
        "short_name": "Game Developer",
        "category": "Creative Tech",
        "suggestions": [
            ("Unity Engine", "http://data.europa.eu/esco/skill/game-unity", "Game development engine"),
            ("C# for Games", "http://data.europa.eu/esco/skill/game-csharp", "Game programming"),
            ("Game Physics", "http://data.europa.eu/esco/skill/game-physics", "Physics simulation")
        ]
    },
    {
        "id": "14",
        "goal": "I want to become an AI Research Scientist.",
        "short_name": "AI Researcher",
        "category": "AI/ML",
        "suggestions": [
            ("Deep Learning Theory", "http://data.europa.eu/esco/skill/ai-deeplearning", "Neural network fundamentals"),
            ("Research Methodology", "http://data.europa.eu/esco/skill/ai-research", "Academic research skills"),
            ("Natural Language Processing", "http://data.europa.eu/esco/skill/ai-nlp", "Language AI")
        ]
    },
    {
        "id": "15",
        "goal": "I want to become a Site Reliability Engineer.",
        "short_name": "SRE",
        "category": "Infrastructure",
        "suggestions": [
            ("Prometheus/Grafana", "http://data.europa.eu/esco/skill/sre-monitoring", "Monitoring stack"),
            ("Chaos Engineering", "http://data.europa.eu/esco/skill/sre-chaos", "Reliability testing"),
            ("SLO/SLI Management", "http://data.europa.eu/esco/skill/sre-slo", "Service level objectives")
        ]
    },
    {
        "id": "16",
        "goal": "I want to become a Database Administrator.",
        "short_name": "DBA",
        "category": "Data",
        "suggestions": [
            ("PostgreSQL Advanced", "http://data.europa.eu/esco/skill/dba-postgresql", "Advanced PostgreSQL"),
            ("Database Optimization", "http://data.europa.eu/esco/skill/dba-optimization", "Query optimization"),
            ("High Availability", "http://data.europa.eu/esco/skill/dba-ha", "Replication and failover")
        ]
    },
    {
        "id": "17",
        "goal": "I want to become an Embedded Systems Developer.",
        "short_name": "Embedded Developer",
        "category": "Systems",
        "suggestions": [
            ("RTOS", "http://data.europa.eu/esco/skill/embedded-rtos", "Real-time operating systems"),
            ("ARM Architecture", "http://data.europa.eu/esco/skill/embedded-arm", "ARM processor programming"),
            ("IoT Protocols", "http://data.europa.eu/esco/skill/embedded-iot", "MQTT/CoAP protocols")
        ]
    },
    {
        "id": "18",
        "goal": "I want to become a Computer Vision Engineer.",
        "short_name": "CV Engineer",
        "category": "AI/ML",
        "suggestions": [
            ("OpenCV", "http://data.europa.eu/esco/skill/cv-opencv", "Computer vision library"),
            ("Object Detection", "http://data.europa.eu/esco/skill/cv-detection", "YOLO/SSD models"),
            ("Image Segmentation", "http://data.europa.eu/esco/skill/cv-segmentation", "Semantic segmentation")
        ]
    },
    {
        "id": "19",
        "goal": "I want to become a Technical Lead.",
        "short_name": "Tech Lead",
        "category": "Leadership",
        "suggestions": [
            ("System Design", "http://data.europa.eu/esco/skill/lead-systemdesign", "Architecture patterns"),
            ("Code Review", "http://data.europa.eu/esco/skill/lead-codereview", "Review best practices"),
            ("Technical Mentoring", "http://data.europa.eu/esco/skill/lead-mentoring", "Team development")
        ]
    },
    {
        "id": "20",
        "goal": "I want to become a QA Automation Engineer.",
        "short_name": "QA Engineer",
        "category": "Quality",
        "suggestions": [
            ("Selenium/Cypress", "http://data.europa.eu/esco/skill/qa-selenium", "Web automation"),
            ("API Testing", "http://data.europa.eu/esco/skill/qa-api", "REST/GraphQL testing"),
            ("Performance Testing", "http://data.europa.eu/esco/skill/qa-performance", "Load and stress testing")
        ]
    }
]


@dataclass
class TestMetrics:
    """Metrics collected for each test case"""
    test_id: str
    goal: str
    short_name: str
    category: str
    
    # Occupation matching
    matched_occupation: str = ""
    occupation_uri: str = ""
    similarity_score: float = 0.0
    
    # Learning path
    total_skills: int = 0
    total_sessions: int = 0
    skills_list: List[str] = field(default_factory=list)
    session_durations: List[int] = field(default_factory=list)
    
    # Timing
    path_generation_time: float = 0.0
    quiz_generation_time: float = 0.0
    total_test_time: float = 0.0
    
    # Quiz
    quiz_questions_count: int = 0
    quiz_difficulty_distribution: Dict[str, int] = field(default_factory=dict)
    quiz_score_percentage: float = 0.0
    
    # Community
    votes_submitted: int = 0
    suggestions_submitted: int = 0
    
    # Status
    path_generation_success: bool = False
    quiz_generation_success: bool = False
    voting_success: bool = False
    suggestions_success: bool = False
    regeneration_success: bool = False
    overall_success: bool = False
    
    # Error tracking
    errors: List[str] = field(default_factory=list)


class EvaluationLogger:
    """Centralized logging for evaluation"""
    
    def __init__(self, log_file: str):
        self.log_file = log_file
        os.makedirs(os.path.dirname(log_file), exist_ok=True)
        
    def log(self, message: str, level: str = "INFO"):
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        log_entry = f"[{timestamp}] [{level}] {message}"
        print(log_entry)
        with open(self.log_file, 'a', encoding='utf-8') as f:
            f.write(log_entry + "\n")
    
    def success(self, msg): self.log(f"✅ {msg}", "SUCCESS")
    def error(self, msg): self.log(f"❌ {msg}", "ERROR")
    def info(self, msg): self.log(f"ℹ️  {msg}", "INFO")
    def warning(self, msg): self.log(f"⚠️  {msg}", "WARNING")
    def section(self, title):
        self.log("=" * 80)
        self.log(title)
        self.log("=" * 80)


class SingleTestRunner:
    """Runs a single test case and collects metrics"""
    
    def __init__(self, test_case: Dict, output_dir: str, logger: EvaluationLogger):
        self.test_case = test_case
        self.output_dir = output_dir
        self.logger = logger
        self.metrics = TestMetrics(
            test_id=test_case["id"],
            goal=test_case["goal"],
            short_name=test_case["short_name"],
            category=test_case["category"]
        )
        self.learning_path = None
        self.quiz_data = None
        
        os.makedirs(output_dir, exist_ok=True)
    
    def save_json(self, filename: str, data: Any):
        filepath = os.path.join(self.output_dir, filename)
        with open(filepath, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=2, ensure_ascii=False)
    
    def run(self) -> TestMetrics:
        """Run complete test and return metrics"""
        start_time = time.time()
        test_user = f"eval_user_{self.test_case['id']}"
        
        self.logger.info(f"Starting test: {self.test_case['short_name']}")
        
        try:
            # Phase 1: Learning Path Generation
            self.test_learning_path(test_user)
            
            # Phase 2: Community Voting
            if self.metrics.path_generation_success:
                self.test_voting(test_user)
            
            # Phase 3: Community Suggestions
            if self.metrics.path_generation_success:
                self.test_suggestions(test_user)
            
            # Phase 4: Quiz Generation
            if self.metrics.path_generation_success:
                self.test_quiz_generation()
            
            # Phase 5: Quiz Submission
            if self.metrics.quiz_generation_success:
                self.test_quiz_submission()
            
            # Phase 6: Path Regeneration
            if self.metrics.path_generation_success:
                self.test_regeneration(test_user)
            
        except Exception as e:
            self.metrics.errors.append(f"Critical error: {str(e)}")
            self.logger.error(f"Test failed: {str(e)}")
        
        self.metrics.total_test_time = time.time() - start_time
        
        # Determine overall success
        self.metrics.overall_success = (
            self.metrics.path_generation_success and
            self.metrics.quiz_generation_success
        )
        
        # Save metrics
        self.save_json("metrics.json", asdict(self.metrics))
        
        return self.metrics
    
    def test_learning_path(self, user_id: str):
        """Test learning path generation"""
        try:
            start = time.time()
            response = requests.post(
                f"{BASE_URL}/api/path",
                json={"goal": self.test_case["goal"], "user_id": user_id},
                timeout=120
            )
            self.metrics.path_generation_time = time.time() - start
            
            if response.status_code == 200:
                self.learning_path = response.json()
                
                # Extract metrics
                occupation = self.learning_path.get('matched_occupation', {})
                self.metrics.matched_occupation = occupation.get('label', '')
                self.metrics.occupation_uri = occupation.get('uri', '')
                self.metrics.similarity_score = occupation.get('similarity_score', 0)
                
                sessions = self.learning_path.get('learning_path', [])
                self.metrics.total_sessions = len(sessions)
                
                skills = []
                durations = []
                for session in sessions:
                    skills.extend(session.get('skills', []))
                    duration = session.get('duration', '0')
                    if isinstance(duration, str):
                        duration = int(''.join(filter(str.isdigit, duration)) or 0)
                    durations.append(duration)
                
                self.metrics.total_skills = len(skills)
                self.metrics.skills_list = skills
                self.metrics.session_durations = durations
                self.metrics.path_generation_success = True
                
                self.save_json("01_learning_path.json", self.learning_path)
                self.logger.success(f"Learning path: {len(skills)} skills, {self.metrics.similarity_score:.4f} similarity")
            else:
                self.metrics.errors.append(f"Path generation failed: {response.status_code}")
                self.logger.error(f"Path generation failed: {response.status_code}")
                
        except Exception as e:
            self.metrics.errors.append(f"Path generation error: {str(e)}")
            self.logger.error(f"Path generation error: {str(e)}")
    
    def test_voting(self, user_id: str):
        """Test community voting"""
        try:
            votes_success = 0
            skills_to_vote = self.metrics.skills_list[:5]
            
            for skill in skills_to_vote:
                skill_uri = f"http://data.europa.eu/esco/skill/{skill.lower().replace(' ', '-')}"
                response = requests.post(
                    f"{BASE_URL}/api/feedback/vote",
                    json={"item_uri": skill_uri, "item_type": "skill", "vote": 1, "user_id": user_id},
                    timeout=10
                )
                if response.status_code == 200:
                    votes_success += 1
            
            self.metrics.votes_submitted = votes_success
            self.metrics.voting_success = votes_success > 0
            self.save_json("02_voting.json", {"votes_submitted": votes_success})
            
        except Exception as e:
            self.metrics.errors.append(f"Voting error: {str(e)}")
    
    def test_suggestions(self, user_id: str):
        """Test community suggestions"""
        try:
            suggestions_success = 0
            suggestions = self.test_case.get("suggestions", [])
            
            for name, uri, desc in suggestions:
                response = requests.post(
                    f"{BASE_URL}/api/feedback/suggest",
                    json={
                        "item_uri": uri,
                        "item_type": "skill",
                        "suggestion_type": "add_skill",
                        "suggestion_text": f"Add {name}: {desc}",
                        "user_id": user_id
                    },
                    timeout=10
                )
                if response.status_code == 200:
                    suggestions_success += 1
            
            self.metrics.suggestions_submitted = suggestions_success
            self.metrics.suggestions_success = suggestions_success > 0
            self.save_json("03_suggestions.json", {"suggestions_submitted": suggestions_success})
            
        except Exception as e:
            self.metrics.errors.append(f"Suggestions error: {str(e)}")
    
    def test_quiz_generation(self):
        """Test quiz generation"""
        try:
            sessions = self.learning_path.get('learning_path', [])
            quiz_learning_path = {
                'sessions': sessions,
                'target_occupation': self.metrics.matched_occupation,
                'id': f'test_{self.test_case["id"]}'
            }
            
            start = time.time()
            response = requests.post(
                f"{BASE_URL}/api/quiz/generate",
                json={"learning_path": quiz_learning_path},
                timeout=90
            )
            self.metrics.quiz_generation_time = time.time() - start
            
            if response.status_code == 200:
                self.quiz_data = response.json()
                quiz = self.quiz_data.get('quiz', {})
                questions = quiz.get('questions', [])
                
                self.metrics.quiz_questions_count = len(questions)
                
                # Count difficulties
                difficulties = {'easy': 0, 'medium': 0, 'hard': 0}
                for q in questions:
                    diff = q.get('difficulty', 'unknown')
                    if diff in difficulties:
                        difficulties[diff] += 1
                self.metrics.quiz_difficulty_distribution = difficulties
                self.metrics.quiz_generation_success = True
                
                self.save_json("04_quiz.json", self.quiz_data)
                self.logger.success(f"Quiz: {len(questions)} questions")
            else:
                self.metrics.errors.append(f"Quiz generation failed: {response.status_code}")
                
        except Exception as e:
            self.metrics.errors.append(f"Quiz generation error: {str(e)}")
    
    def test_quiz_submission(self):
        """Test quiz submission"""
        try:
            quiz = self.quiz_data.get('quiz', {})
            questions = quiz.get('questions', [])
            
            # Simulate 70% correct answers
            answers = {}
            for i, q in enumerate(questions):
                correct = q.get('correct_answer', 'A')
                if i % 10 < 7:
                    answers[str(i)] = correct
                else:
                    options = q.get('options', {})
                    if isinstance(options, dict):
                        wrong = [k for k in options.keys() if k != correct]
                        answers[str(i)] = wrong[0] if wrong else 'B'
                    else:
                        answers[str(i)] = 'B'
            
            response = requests.post(
                f"{BASE_URL}/api/quiz/submit",
                json={"quiz": quiz, "answers": answers},
                timeout=30
            )
            
            if response.status_code == 200:
                results = response.json()
                analysis = results.get('analysis', {})
                score = analysis.get('score', {})
                self.metrics.quiz_score_percentage = score.get('percentage', 0)
                self.save_json("05_quiz_results.json", results)
                
        except Exception as e:
            self.metrics.errors.append(f"Quiz submission error: {str(e)}")
    
    def test_regeneration(self, user_id: str):
        """Test path regeneration"""
        try:
            time.sleep(1)  # Allow feedback to propagate
            
            response = requests.post(
                f"{BASE_URL}/api/path",
                json={"goal": self.test_case["goal"], "user_id": user_id},
                timeout=120
            )
            
            if response.status_code == 200:
                regenerated = response.json()
                self.metrics.regeneration_success = True
                self.save_json("06_regenerated_path.json", regenerated)
            else:
                self.metrics.errors.append(f"Regeneration failed: {response.status_code}")
                
        except Exception as e:
            self.metrics.errors.append(f"Regeneration error: {str(e)}")


class EvaluationGraphGenerator:
    """Generates professional research-grade visualizations"""
    
    def __init__(self, metrics_list: List[TestMetrics], output_dir: str):
        self.metrics = metrics_list
        self.output_dir = output_dir
        os.makedirs(output_dir, exist_ok=True)
        
        # Set professional style
        if VISUALIZATION_AVAILABLE:
            plt.style.use('seaborn-v0_8-whitegrid' if 'seaborn-v0_8-whitegrid' in plt.style.available else 'ggplot')
            plt.rcParams.update({
                'font.size': 10,
                'axes.titlesize': 12,
                'axes.labelsize': 10,
                'xtick.labelsize': 9,
                'ytick.labelsize': 9,
                'legend.fontsize': 9,
                'figure.titlesize': 14,
                'figure.dpi': 150,
                'savefig.dpi': 300,
                'savefig.bbox': 'tight',
                'axes.spines.top': False,
                'axes.spines.right': False
            })
            
            # Color palette
            self.colors = {
                'primary': '#2E86AB',
                'secondary': '#A23B72',
                'success': '#2ECC71',
                'warning': '#F39C12',
                'danger': '#E74C3C',
                'info': '#3498DB',
                'categories': ['#2E86AB', '#A23B72', '#F18F01', '#C73E1D', '#3A506B', '#5BC0BE', '#6B2737', '#1B998B']
            }
    
    def generate_all_graphs(self):
        """Generate all evaluation graphs"""
        if not VISUALIZATION_AVAILABLE:
            print("Visualization libraries not available. Skipping graph generation.")
            return
        
        print("\n📊 Generating evaluation graphs...")
        
        # 1. Similarity Scores Bar Chart
        self.plot_similarity_scores()
        
        # 2. Skills Count Distribution
        self.plot_skills_distribution()
        
        # 3. Response Times Comparison
        self.plot_response_times()
        
        # 4. Success Rate Overview
        self.plot_success_rates()
        
        # 5. Category-wise Analysis
        self.plot_category_analysis()
        
        # 6. Quiz Metrics
        self.plot_quiz_metrics()
        
        # 7. Session Analysis
        self.plot_session_analysis()
        
        # 8. Comprehensive Dashboard
        self.plot_comprehensive_dashboard()
        
        # 9. Statistical Summary Table
        self.generate_statistical_summary()
        
        # 10. Correlation Heatmap
        self.plot_correlation_heatmap()
        
        print(f"✅ All graphs saved to: {self.output_dir}")
    
    def plot_similarity_scores(self):
        """Plot similarity scores for all test cases"""
        fig, ax = plt.subplots(figsize=(14, 7))
        
        names = [m.short_name for m in self.metrics]
        scores = [m.similarity_score for m in self.metrics]
        categories = [m.category for m in self.metrics]
        
        # Color by category
        unique_cats = list(set(categories))
        cat_colors = {cat: self.colors['categories'][i % len(self.colors['categories'])] 
                     for i, cat in enumerate(unique_cats)}
        bar_colors = [cat_colors[cat] for cat in categories]
        
        bars = ax.barh(names, scores, color=bar_colors, edgecolor='white', linewidth=0.5)
        
        # Add value labels
        for bar, score in zip(bars, scores):
            ax.text(score + 0.01, bar.get_y() + bar.get_height()/2, 
                   f'{score:.3f}', va='center', fontsize=8)
        
        ax.set_xlabel('Similarity Score', fontweight='bold')
        ax.set_title('Occupation Matching Similarity Scores Across Career Goals', fontweight='bold', pad=20)
        ax.set_xlim(0, 1.1)
        
        # Add threshold line
        ax.axvline(x=0.5, color='red', linestyle='--', alpha=0.5, label='Minimum Threshold (0.5)')
        ax.axvline(x=0.8, color='green', linestyle='--', alpha=0.5, label='High Quality (0.8)')
        
        # Legend for categories
        legend_patches = [mpatches.Patch(color=cat_colors[cat], label=cat) for cat in unique_cats]
        ax.legend(handles=legend_patches, loc='lower right', title='Category')
        
        plt.tight_layout()
        plt.savefig(os.path.join(self.output_dir, '01_similarity_scores.png'))
        plt.savefig(os.path.join(self.output_dir, '01_similarity_scores.pdf'))
        plt.close()
    
    def plot_skills_distribution(self):
        """Plot skills count distribution"""
        fig, axes = plt.subplots(1, 2, figsize=(14, 6))
        
        names = [m.short_name for m in self.metrics]
        skills = [m.total_skills for m in self.metrics]
        sessions = [m.total_sessions for m in self.metrics]
        
        # Skills count bar chart
        ax1 = axes[0]
        bars = ax1.bar(range(len(names)), skills, color=self.colors['primary'], edgecolor='white')
        ax1.set_xticks(range(len(names)))
        ax1.set_xticklabels(names, rotation=45, ha='right', fontsize=8)
        ax1.set_ylabel('Number of Skills', fontweight='bold')
        ax1.set_title('Skills Generated per Career Goal', fontweight='bold')
        
        # Add mean line
        mean_skills = statistics.mean(skills)
        ax1.axhline(y=mean_skills, color=self.colors['danger'], linestyle='--', 
                   label=f'Mean: {mean_skills:.1f}')
        ax1.legend()
        
        # Sessions vs Skills scatter
        ax2 = axes[1]
        scatter = ax2.scatter(sessions, skills, c=[self.metrics.index(m) for m in self.metrics],
                             cmap='viridis', s=100, alpha=0.7, edgecolors='white')
        
        # Add labels
        for i, m in enumerate(self.metrics):
            ax2.annotate(m.short_name[:10], (m.total_sessions, m.total_skills), 
                        fontsize=7, alpha=0.7)
        
        ax2.set_xlabel('Number of Sessions', fontweight='bold')
        ax2.set_ylabel('Number of Skills', fontweight='bold')
        ax2.set_title('Sessions vs Skills Relationship', fontweight='bold')
        
        # Add trend line
        if len(sessions) > 1:
            z = np.polyfit(sessions, skills, 1)
            p = np.poly1d(z)
            ax2.plot(sorted(sessions), p(sorted(sessions)), "r--", alpha=0.5, label='Trend')
            ax2.legend()
        
        plt.tight_layout()
        plt.savefig(os.path.join(self.output_dir, '02_skills_distribution.png'))
        plt.savefig(os.path.join(self.output_dir, '02_skills_distribution.pdf'))
        plt.close()
    
    def plot_response_times(self):
        """Plot response times comparison"""
        fig, axes = plt.subplots(1, 2, figsize=(14, 6))
        
        names = [m.short_name for m in self.metrics]
        path_times = [m.path_generation_time for m in self.metrics]
        quiz_times = [m.quiz_generation_time for m in self.metrics]
        
        # Grouped bar chart
        ax1 = axes[0]
        x = np.arange(len(names))
        width = 0.35
        
        bars1 = ax1.bar(x - width/2, path_times, width, label='Path Generation', 
                       color=self.colors['primary'], edgecolor='white')
        bars2 = ax1.bar(x + width/2, quiz_times, width, label='Quiz Generation',
                       color=self.colors['secondary'], edgecolor='white')
        
        ax1.set_ylabel('Time (seconds)', fontweight='bold')
        ax1.set_title('API Response Times by Career Goal', fontweight='bold')
        ax1.set_xticks(x)
        ax1.set_xticklabels(names, rotation=45, ha='right', fontsize=8)
        ax1.legend()
        
        # Box plot
        ax2 = axes[1]
        bp = ax2.boxplot([path_times, quiz_times], labels=['Path Generation', 'Quiz Generation'],
                        patch_artist=True)
        
        bp['boxes'][0].set_facecolor(self.colors['primary'])
        bp['boxes'][1].set_facecolor(self.colors['secondary'])
        
        ax2.set_ylabel('Time (seconds)', fontweight='bold')
        ax2.set_title('Response Time Distribution', fontweight='bold')
        
        # Add statistics
        for i, times in enumerate([path_times, quiz_times], 1):
            if times:
                mean_val = statistics.mean(times)
                ax2.annotate(f'μ={mean_val:.1f}s', (i, mean_val), 
                           xytext=(5, 5), textcoords='offset points', fontsize=9)
        
        plt.tight_layout()
        plt.savefig(os.path.join(self.output_dir, '03_response_times.png'))
        plt.savefig(os.path.join(self.output_dir, '03_response_times.pdf'))
        plt.close()
    
    def plot_success_rates(self):
        """Plot success rates for different features"""
        fig, axes = plt.subplots(1, 2, figsize=(14, 6))
        
        # Feature success rates
        ax1 = axes[0]
        
        features = ['Path Generation', 'Quiz Generation', 'Voting', 'Suggestions', 'Regeneration', 'Overall']
        success_counts = [
            sum(1 for m in self.metrics if m.path_generation_success),
            sum(1 for m in self.metrics if m.quiz_generation_success),
            sum(1 for m in self.metrics if m.voting_success),
            sum(1 for m in self.metrics if m.suggestions_success),
            sum(1 for m in self.metrics if m.regeneration_success),
            sum(1 for m in self.metrics if m.overall_success)
        ]
        total = len(self.metrics)
        success_rates = [count/total * 100 for count in success_counts]
        
        colors_list = [self.colors['success'] if rate >= 80 else 
                      self.colors['warning'] if rate >= 60 else 
                      self.colors['danger'] for rate in success_rates]
        
        bars = ax1.bar(features, success_rates, color=colors_list, edgecolor='white')
        
        # Add value labels
        for bar, rate, count in zip(bars, success_rates, success_counts):
            ax1.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 1,
                    f'{rate:.0f}%\n({count}/{total})', ha='center', fontsize=9)
        
        ax1.set_ylabel('Success Rate (%)', fontweight='bold')
        ax1.set_title('Feature Success Rates', fontweight='bold')
        ax1.set_ylim(0, 110)
        ax1.axhline(y=80, color='green', linestyle='--', alpha=0.3, label='Target (80%)')
        ax1.set_xticklabels(features, rotation=30, ha='right')
        
        # Per-test success overview
        ax2 = axes[1]
        
        test_names = [m.short_name for m in self.metrics]
        success_matrix = np.array([
            [m.path_generation_success, m.quiz_generation_success, 
             m.voting_success, m.suggestions_success, m.regeneration_success]
            for m in self.metrics
        ]).astype(int)
        
        im = ax2.imshow(success_matrix.T, cmap='RdYlGn', aspect='auto', vmin=0, vmax=1)
        
        ax2.set_xticks(range(len(test_names)))
        ax2.set_xticklabels(test_names, rotation=45, ha='right', fontsize=7)
        ax2.set_yticks(range(5))
        ax2.set_yticklabels(['Path', 'Quiz', 'Voting', 'Suggest', 'Regen'], fontsize=9)
        ax2.set_title('Success Matrix (Green=Pass, Red=Fail)', fontweight='bold')
        
        plt.tight_layout()
        plt.savefig(os.path.join(self.output_dir, '04_success_rates.png'))
        plt.savefig(os.path.join(self.output_dir, '04_success_rates.pdf'))
        plt.close()
    
    def plot_category_analysis(self):
        """Plot analysis by category"""
        fig, axes = plt.subplots(2, 2, figsize=(14, 12))
        
        # Group metrics by category
        category_data = defaultdict(list)
        for m in self.metrics:
            category_data[m.category].append(m)
        
        categories = list(category_data.keys())
        
        # Average similarity by category
        ax1 = axes[0, 0]
        avg_similarity = [statistics.mean([m.similarity_score for m in category_data[cat]]) 
                         for cat in categories]
        std_similarity = [statistics.stdev([m.similarity_score for m in category_data[cat]]) 
                         if len(category_data[cat]) > 1 else 0 for cat in categories]
        
        bars = ax1.bar(categories, avg_similarity, yerr=std_similarity, 
                      color=self.colors['categories'][:len(categories)],
                      capsize=5, edgecolor='white')
        ax1.set_ylabel('Average Similarity Score', fontweight='bold')
        ax1.set_title('Similarity Score by Category', fontweight='bold')
        ax1.set_xticklabels(categories, rotation=30, ha='right')
        
        # Skills count by category
        ax2 = axes[0, 1]
        avg_skills = [statistics.mean([m.total_skills for m in category_data[cat]]) 
                     for cat in categories]
        
        ax2.bar(categories, avg_skills, color=self.colors['categories'][:len(categories)],
               edgecolor='white')
        ax2.set_ylabel('Average Skills Count', fontweight='bold')
        ax2.set_title('Skills Generated by Category', fontweight='bold')
        ax2.set_xticklabels(categories, rotation=30, ha='right')
        
        # Response time by category
        ax3 = axes[1, 0]
        avg_time = [statistics.mean([m.path_generation_time for m in category_data[cat]]) 
                   for cat in categories]
        
        ax3.bar(categories, avg_time, color=self.colors['categories'][:len(categories)],
               edgecolor='white')
        ax3.set_ylabel('Average Response Time (s)', fontweight='bold')
        ax3.set_title('Path Generation Time by Category', fontweight='bold')
        ax3.set_xticklabels(categories, rotation=30, ha='right')
        
        # Test count per category (pie chart)
        ax4 = axes[1, 1]
        test_counts = [len(category_data[cat]) for cat in categories]
        
        wedges, texts, autotexts = ax4.pie(test_counts, labels=categories, autopct='%1.0f%%',
                                          colors=self.colors['categories'][:len(categories)],
                                          explode=[0.02]*len(categories))
        ax4.set_title('Test Distribution by Category', fontweight='bold')
        
        plt.tight_layout()
        plt.savefig(os.path.join(self.output_dir, '05_category_analysis.png'))
        plt.savefig(os.path.join(self.output_dir, '05_category_analysis.pdf'))
        plt.close()
    
    def plot_quiz_metrics(self):
        """Plot quiz-related metrics"""
        fig, axes = plt.subplots(1, 3, figsize=(15, 5))
        
        # Quiz questions count
        ax1 = axes[0]
        names = [m.short_name for m in self.metrics]
        q_counts = [m.quiz_questions_count for m in self.metrics]
        
        ax1.bar(range(len(names)), q_counts, color=self.colors['info'], edgecolor='white')
        ax1.set_xticks(range(len(names)))
        ax1.set_xticklabels(names, rotation=45, ha='right', fontsize=7)
        ax1.set_ylabel('Question Count', fontweight='bold')
        ax1.set_title('Quiz Questions Generated', fontweight='bold')
        ax1.axhline(y=10, color='red', linestyle='--', alpha=0.5, label='Target: 10')
        ax1.legend()
        
        # Difficulty distribution (stacked)
        ax2 = axes[1]
        easy = [m.quiz_difficulty_distribution.get('easy', 0) for m in self.metrics]
        medium = [m.quiz_difficulty_distribution.get('medium', 0) for m in self.metrics]
        hard = [m.quiz_difficulty_distribution.get('hard', 0) for m in self.metrics]
        
        x = range(len(names))
        ax2.bar(x, easy, label='Easy', color=self.colors['success'], edgecolor='white')
        ax2.bar(x, medium, bottom=easy, label='Medium', color=self.colors['warning'], edgecolor='white')
        ax2.bar(x, hard, bottom=[e+m for e,m in zip(easy, medium)], label='Hard', 
               color=self.colors['danger'], edgecolor='white')
        
        ax2.set_xticks(range(len(names)))
        ax2.set_xticklabels(names, rotation=45, ha='right', fontsize=7)
        ax2.set_ylabel('Question Count', fontweight='bold')
        ax2.set_title('Quiz Difficulty Distribution', fontweight='bold')
        ax2.legend()
        
        # Quiz generation time histogram
        ax3 = axes[2]
        quiz_times = [m.quiz_generation_time for m in self.metrics if m.quiz_generation_time > 0]
        
        ax3.hist(quiz_times, bins=10, color=self.colors['secondary'], edgecolor='white', alpha=0.7)
        ax3.axvline(x=statistics.mean(quiz_times) if quiz_times else 0, color='red', 
                   linestyle='--', label=f'Mean: {statistics.mean(quiz_times):.1f}s' if quiz_times else 'N/A')
        ax3.set_xlabel('Time (seconds)', fontweight='bold')
        ax3.set_ylabel('Frequency', fontweight='bold')
        ax3.set_title('Quiz Generation Time Distribution', fontweight='bold')
        ax3.legend()
        
        plt.tight_layout()
        plt.savefig(os.path.join(self.output_dir, '06_quiz_metrics.png'))
        plt.savefig(os.path.join(self.output_dir, '06_quiz_metrics.pdf'))
        plt.close()
    
    def plot_session_analysis(self):
        """Plot session-related analysis"""
        fig, axes = plt.subplots(1, 2, figsize=(14, 6))
        
        names = [m.short_name for m in self.metrics]
        sessions = [m.total_sessions for m in self.metrics]
        
        # Session count
        ax1 = axes[0]
        colors_list = [self.colors['success'] if s >= 3 else self.colors['warning'] for s in sessions]
        ax1.bar(range(len(names)), sessions, color=colors_list, edgecolor='white')
        ax1.set_xticks(range(len(names)))
        ax1.set_xticklabels(names, rotation=45, ha='right', fontsize=8)
        ax1.set_ylabel('Number of Sessions', fontweight='bold')
        ax1.set_title('Learning Path Sessions per Goal', fontweight='bold')
        ax1.axhline(y=3, color='blue', linestyle='--', alpha=0.5, label='Target: 3 sessions')
        ax1.legend()
        
        # Skills per session ratio
        ax2 = axes[1]
        ratios = [m.total_skills / m.total_sessions if m.total_sessions > 0 else 0 for m in self.metrics]
        
        ax2.bar(range(len(names)), ratios, color=self.colors['primary'], edgecolor='white')
        ax2.set_xticks(range(len(names)))
        ax2.set_xticklabels(names, rotation=45, ha='right', fontsize=8)
        ax2.set_ylabel('Skills per Session', fontweight='bold')
        ax2.set_title('Average Skills per Session', fontweight='bold')
        
        mean_ratio = statistics.mean(ratios) if ratios else 0
        ax2.axhline(y=mean_ratio, color='red', linestyle='--', 
                   label=f'Mean: {mean_ratio:.1f}')
        ax2.legend()
        
        plt.tight_layout()
        plt.savefig(os.path.join(self.output_dir, '07_session_analysis.png'))
        plt.savefig(os.path.join(self.output_dir, '07_session_analysis.pdf'))
        plt.close()
    
    def plot_comprehensive_dashboard(self):
        """Create a comprehensive dashboard with key metrics"""
        fig = plt.figure(figsize=(20, 16))
        gs = GridSpec(4, 4, figure=fig, hspace=0.3, wspace=0.3)
        
        # Title
        fig.suptitle('Hybrid GenMentor - Comprehensive Evaluation Dashboard', 
                    fontsize=16, fontweight='bold', y=0.98)
        
        # 1. Overall Success Rate (large)
        ax1 = fig.add_subplot(gs[0, 0:2])
        success_rate = sum(1 for m in self.metrics if m.overall_success) / len(self.metrics) * 100
        
        # Create gauge-like visualization
        theta = np.linspace(0, np.pi, 100)
        ax1.fill_between(theta, 0, 1, color='lightgray', alpha=0.3)
        success_theta = np.linspace(0, np.pi * (success_rate/100), 100)
        color = self.colors['success'] if success_rate >= 80 else self.colors['warning'] if success_rate >= 60 else self.colors['danger']
        ax1.fill_between(success_theta, 0, 1, color=color, alpha=0.7)
        ax1.set_xlim(0, np.pi)
        ax1.set_ylim(0, 1.2)
        ax1.text(np.pi/2, 0.5, f'{success_rate:.0f}%', ha='center', va='center', 
                fontsize=32, fontweight='bold')
        ax1.text(np.pi/2, 0.1, 'Overall Success Rate', ha='center', fontsize=12)
        ax1.axis('off')
        ax1.set_title('System Performance', fontweight='bold', pad=20)
        
        # 2. Key Statistics
        ax2 = fig.add_subplot(gs[0, 2:4])
        stats_text = f"""
        Total Tests: {len(self.metrics)}
        Successful: {sum(1 for m in self.metrics if m.overall_success)}
        Failed: {sum(1 for m in self.metrics if not m.overall_success)}
        
        Avg Similarity: {statistics.mean([m.similarity_score for m in self.metrics]):.3f}
        Avg Skills: {statistics.mean([m.total_skills for m in self.metrics]):.1f}
        Avg Sessions: {statistics.mean([m.total_sessions for m in self.metrics]):.1f}
        
        Avg Path Gen Time: {statistics.mean([m.path_generation_time for m in self.metrics]):.1f}s
        Avg Quiz Gen Time: {statistics.mean([m.quiz_generation_time for m in self.metrics if m.quiz_generation_time > 0]):.1f}s
        """
        ax2.text(0.1, 0.5, stats_text, transform=ax2.transAxes, fontsize=11,
                verticalalignment='center', fontfamily='monospace',
                bbox=dict(boxstyle='round', facecolor='wheat', alpha=0.5))
        ax2.axis('off')
        ax2.set_title('Key Statistics', fontweight='bold')
        
        # 3. Similarity Score Distribution
        ax3 = fig.add_subplot(gs[1, 0:2])
        scores = [m.similarity_score for m in self.metrics]
        ax3.hist(scores, bins=10, color=self.colors['primary'], edgecolor='white', alpha=0.7)
        ax3.axvline(x=statistics.mean(scores), color='red', linestyle='--', 
                   label=f'Mean: {statistics.mean(scores):.3f}')
        ax3.set_xlabel('Similarity Score')
        ax3.set_ylabel('Frequency')
        ax3.set_title('Similarity Score Distribution', fontweight='bold')
        ax3.legend()
        
        # 4. Skills vs Time Scatter
        ax4 = fig.add_subplot(gs[1, 2:4])
        skills = [m.total_skills for m in self.metrics]
        times = [m.path_generation_time for m in self.metrics]
        scatter = ax4.scatter(times, skills, c=scores, cmap='viridis', 
                             s=100, alpha=0.7, edgecolors='white')
        plt.colorbar(scatter, ax=ax4, label='Similarity Score')
        ax4.set_xlabel('Generation Time (s)')
        ax4.set_ylabel('Skills Count')
        ax4.set_title('Skills vs Generation Time', fontweight='bold')
        
        # 5. Category Performance
        ax5 = fig.add_subplot(gs[2, 0:2])
        category_data = defaultdict(list)
        for m in self.metrics:
            category_data[m.category].append(m.similarity_score)
        
        categories = list(category_data.keys())
        avg_scores = [statistics.mean(category_data[cat]) for cat in categories]
        
        ax5.barh(categories, avg_scores, color=self.colors['categories'][:len(categories)],
                edgecolor='white')
        ax5.set_xlabel('Average Similarity Score')
        ax5.set_title('Performance by Category', fontweight='bold')
        ax5.set_xlim(0, 1)
        
        # 6. Feature Success Breakdown
        ax6 = fig.add_subplot(gs[2, 2:4])
        features = ['Path Gen', 'Quiz Gen', 'Voting', 'Suggestions', 'Regen']
        success_pcts = [
            sum(1 for m in self.metrics if m.path_generation_success) / len(self.metrics) * 100,
            sum(1 for m in self.metrics if m.quiz_generation_success) / len(self.metrics) * 100,
            sum(1 for m in self.metrics if m.voting_success) / len(self.metrics) * 100,
            sum(1 for m in self.metrics if m.suggestions_success) / len(self.metrics) * 100,
            sum(1 for m in self.metrics if m.regeneration_success) / len(self.metrics) * 100
        ]
        
        colors_list = [self.colors['success'] if p >= 80 else 
                      self.colors['warning'] if p >= 60 else 
                      self.colors['danger'] for p in success_pcts]
        ax6.bar(features, success_pcts, color=colors_list, edgecolor='white')
        ax6.set_ylabel('Success Rate (%)')
        ax6.set_title('Feature Success Rates', fontweight='bold')
        ax6.set_ylim(0, 105)
        
        # 7. Top Performing Goals
        ax7 = fig.add_subplot(gs[3, 0:2])
        sorted_metrics = sorted(self.metrics, key=lambda m: m.similarity_score, reverse=True)[:5]
        names = [m.short_name for m in sorted_metrics]
        scores = [m.similarity_score for m in sorted_metrics]
        
        ax7.barh(names[::-1], scores[::-1], color=self.colors['success'], edgecolor='white')
        ax7.set_xlabel('Similarity Score')
        ax7.set_title('Top 5 Performing Goals', fontweight='bold')
        ax7.set_xlim(0, 1)
        
        # 8. Response Time Summary
        ax8 = fig.add_subplot(gs[3, 2:4])
        path_times = [m.path_generation_time for m in self.metrics]
        quiz_times = [m.quiz_generation_time for m in self.metrics if m.quiz_generation_time > 0]
        
        bp = ax8.boxplot([path_times, quiz_times], labels=['Path Generation', 'Quiz Generation'],
                        patch_artist=True)
        bp['boxes'][0].set_facecolor(self.colors['primary'])
        bp['boxes'][1].set_facecolor(self.colors['secondary'])
        ax8.set_ylabel('Time (seconds)')
        ax8.set_title('Response Time Distribution', fontweight='bold')
        
        plt.savefig(os.path.join(self.output_dir, '08_comprehensive_dashboard.png'))
        plt.savefig(os.path.join(self.output_dir, '08_comprehensive_dashboard.pdf'))
        plt.close()
    
    def generate_statistical_summary(self):
        """Generate statistical summary as image"""
        fig, ax = plt.subplots(figsize=(12, 10))
        ax.axis('off')
        
        # Collect statistics
        similarity_scores = [m.similarity_score for m in self.metrics]
        skills_counts = [m.total_skills for m in self.metrics]
        path_times = [m.path_generation_time for m in self.metrics]
        quiz_times = [m.quiz_generation_time for m in self.metrics if m.quiz_generation_time > 0]
        
        stats_data = [
            ['Metric', 'Mean', 'Std Dev', 'Min', 'Max', 'Median'],
            ['Similarity Score', 
             f'{statistics.mean(similarity_scores):.4f}',
             f'{statistics.stdev(similarity_scores):.4f}' if len(similarity_scores) > 1 else 'N/A',
             f'{min(similarity_scores):.4f}',
             f'{max(similarity_scores):.4f}',
             f'{statistics.median(similarity_scores):.4f}'],
            ['Skills Generated',
             f'{statistics.mean(skills_counts):.1f}',
             f'{statistics.stdev(skills_counts):.1f}' if len(skills_counts) > 1 else 'N/A',
             f'{min(skills_counts)}',
             f'{max(skills_counts)}',
             f'{statistics.median(skills_counts):.1f}'],
            ['Path Gen Time (s)',
             f'{statistics.mean(path_times):.2f}',
             f'{statistics.stdev(path_times):.2f}' if len(path_times) > 1 else 'N/A',
             f'{min(path_times):.2f}',
             f'{max(path_times):.2f}',
             f'{statistics.median(path_times):.2f}'],
            ['Quiz Gen Time (s)',
             f'{statistics.mean(quiz_times):.2f}' if quiz_times else 'N/A',
             f'{statistics.stdev(quiz_times):.2f}' if len(quiz_times) > 1 else 'N/A',
             f'{min(quiz_times):.2f}' if quiz_times else 'N/A',
             f'{max(quiz_times):.2f}' if quiz_times else 'N/A',
             f'{statistics.median(quiz_times):.2f}' if quiz_times else 'N/A']
        ]
        
        table = ax.table(cellText=stats_data[1:], colLabels=stats_data[0],
                        loc='center', cellLoc='center',
                        colColours=[self.colors['primary']]*6)
        table.auto_set_font_size(False)
        table.set_fontsize(11)
        table.scale(1.2, 2)
        
        # Style header
        for i in range(6):
            table[(0, i)].set_text_props(color='white', fontweight='bold')
        
        ax.set_title('Statistical Summary of Evaluation Metrics', 
                    fontsize=14, fontweight='bold', pad=20)
        
        plt.savefig(os.path.join(self.output_dir, '09_statistical_summary.png'))
        plt.savefig(os.path.join(self.output_dir, '09_statistical_summary.pdf'))
        plt.close()
    
    def plot_correlation_heatmap(self):
        """Plot correlation heatmap between metrics"""
        if not SEABORN_AVAILABLE:
            return
        
        fig, ax = plt.subplots(figsize=(10, 8))
        
        # Create correlation matrix
        data = {
            'Similarity': [m.similarity_score for m in self.metrics],
            'Skills': [m.total_skills for m in self.metrics],
            'Sessions': [m.total_sessions for m in self.metrics],
            'Path Time': [m.path_generation_time for m in self.metrics],
            'Quiz Time': [m.quiz_generation_time for m in self.metrics],
            'Quiz Qs': [m.quiz_questions_count for m in self.metrics]
        }
        
        # Calculate correlations
        keys = list(data.keys())
        n = len(keys)
        corr_matrix = np.zeros((n, n))
        
        for i, k1 in enumerate(keys):
            for j, k2 in enumerate(keys):
                if len(data[k1]) > 1 and len(data[k2]) > 1:
                    # Filter out zeros for correlation
                    valid = [(a, b) for a, b in zip(data[k1], data[k2]) if a != 0 and b != 0]
                    if len(valid) > 1:
                        x, y = zip(*valid)
                        corr_matrix[i, j] = np.corrcoef(x, y)[0, 1]
                    else:
                        corr_matrix[i, j] = 0
                else:
                    corr_matrix[i, j] = 0
        
        sns.heatmap(corr_matrix, annot=True, fmt='.2f', cmap='RdYlBu_r',
                   xticklabels=keys, yticklabels=keys, center=0,
                   square=True, linewidths=0.5)
        
        ax.set_title('Correlation Matrix of Evaluation Metrics', fontweight='bold', pad=20)
        
        plt.tight_layout()
        plt.savefig(os.path.join(self.output_dir, '10_correlation_heatmap.png'))
        plt.savefig(os.path.join(self.output_dir, '10_correlation_heatmap.pdf'))
        plt.close()


class ComprehensiveEvaluationRunner:
    """Main runner for comprehensive evaluation"""
    
    def __init__(self):
        self.logger = EvaluationLogger(LOG_FILE)
        self.all_metrics: List[TestMetrics] = []
        
        # Create directories
        os.makedirs(OUTPUT_DIR, exist_ok=True)
        os.makedirs(GRAPHS_DIR, exist_ok=True)
    
    def run_all_tests(self):
        """Run all 20 test cases"""
        self.logger.section("COMPREHENSIVE EVALUATION TEST SUITE")
        self.logger.info(f"Running {len(TEST_CASES)} test cases")
        self.logger.info(f"Output directory: {OUTPUT_DIR}")
        
        start_time = time.time()
        
        for i, test_case in enumerate(TEST_CASES, 1):
            self.logger.section(f"TEST {i}/{len(TEST_CASES)}: {test_case['short_name']}")
            
            # Create test output directory
            test_dir = os.path.join(OUTPUT_DIR, f"test_{test_case['id']}_{test_case['short_name'].lower().replace(' ', '_')}")
            
            # Run single test
            runner = SingleTestRunner(test_case, test_dir, self.logger)
            metrics = runner.run()
            self.all_metrics.append(metrics)
            
            # Progress update
            success_rate = sum(1 for m in self.all_metrics if m.overall_success) / len(self.all_metrics) * 100
            self.logger.info(f"Progress: {i}/{len(TEST_CASES)} tests completed | Current success rate: {success_rate:.1f}%")
            
            # Small delay between tests
            if i < len(TEST_CASES):
                time.sleep(2)
        
        total_time = time.time() - start_time
        
        # Generate summary
        self.generate_summary(total_time)
        
        # Generate graphs
        self.generate_graphs()
        
        return self.all_metrics
    
    def generate_summary(self, total_time: float):
        """Generate evaluation summary"""
        self.logger.section("EVALUATION SUMMARY")
        
        # Calculate overall metrics
        total_tests = len(self.all_metrics)
        successful_tests = sum(1 for m in self.all_metrics if m.overall_success)
        success_rate = successful_tests / total_tests * 100
        
        avg_similarity = statistics.mean([m.similarity_score for m in self.all_metrics])
        avg_skills = statistics.mean([m.total_skills for m in self.all_metrics])
        avg_path_time = statistics.mean([m.path_generation_time for m in self.all_metrics])
        avg_quiz_time = statistics.mean([m.quiz_generation_time for m in self.all_metrics if m.quiz_generation_time > 0])
        
        summary = {
            "evaluation_timestamp": TIMESTAMP,
            "total_test_cases": total_tests,
            "successful_tests": successful_tests,
            "failed_tests": total_tests - successful_tests,
            "overall_success_rate": success_rate,
            "total_evaluation_time_seconds": total_time,
            "total_evaluation_time_minutes": total_time / 60,
            "metrics": {
                "similarity_score": {
                    "mean": avg_similarity,
                    "std": statistics.stdev([m.similarity_score for m in self.all_metrics]) if total_tests > 1 else 0,
                    "min": min(m.similarity_score for m in self.all_metrics),
                    "max": max(m.similarity_score for m in self.all_metrics)
                },
                "skills_generated": {
                    "mean": avg_skills,
                    "std": statistics.stdev([m.total_skills for m in self.all_metrics]) if total_tests > 1 else 0,
                    "min": min(m.total_skills for m in self.all_metrics),
                    "max": max(m.total_skills for m in self.all_metrics)
                },
                "path_generation_time": {
                    "mean": avg_path_time,
                    "std": statistics.stdev([m.path_generation_time for m in self.all_metrics]) if total_tests > 1 else 0
                },
                "quiz_generation_time": {
                    "mean": avg_quiz_time,
                    "std": statistics.stdev([m.quiz_generation_time for m in self.all_metrics if m.quiz_generation_time > 0]) if sum(1 for m in self.all_metrics if m.quiz_generation_time > 0) > 1 else 0
                }
            },
            "feature_success_rates": {
                "path_generation": sum(1 for m in self.all_metrics if m.path_generation_success) / total_tests * 100,
                "quiz_generation": sum(1 for m in self.all_metrics if m.quiz_generation_success) / total_tests * 100,
                "voting": sum(1 for m in self.all_metrics if m.voting_success) / total_tests * 100,
                "suggestions": sum(1 for m in self.all_metrics if m.suggestions_success) / total_tests * 100,
                "regeneration": sum(1 for m in self.all_metrics if m.regeneration_success) / total_tests * 100
            },
            "category_analysis": {},
            "test_results": [asdict(m) for m in self.all_metrics]
        }
        
        # Category analysis
        category_data = defaultdict(list)
        for m in self.all_metrics:
            category_data[m.category].append(m)
        
        for cat, metrics in category_data.items():
            summary["category_analysis"][cat] = {
                "count": len(metrics),
                "success_rate": sum(1 for m in metrics if m.overall_success) / len(metrics) * 100,
                "avg_similarity": statistics.mean([m.similarity_score for m in metrics]),
                "avg_skills": statistics.mean([m.total_skills for m in metrics])
            }
        
        # Save summary
        summary_path = os.path.join(OUTPUT_DIR, "evaluation_summary.json")
        with open(summary_path, 'w', encoding='utf-8') as f:
            json.dump(summary, f, indent=2, ensure_ascii=False)
        
        # Log summary
        self.logger.info(f"Total Tests: {total_tests}")
        self.logger.info(f"Successful: {successful_tests}")
        self.logger.info(f"Failed: {total_tests - successful_tests}")
        self.logger.info(f"Success Rate: {success_rate:.1f}%")
        self.logger.info(f"Average Similarity: {avg_similarity:.4f}")
        self.logger.info(f"Average Skills: {avg_skills:.1f}")
        self.logger.info(f"Total Time: {total_time/60:.1f} minutes")
        
        self.logger.success(f"Summary saved to: {summary_path}")
    
    def generate_graphs(self):
        """Generate all evaluation graphs"""
        self.logger.section("GENERATING EVALUATION GRAPHS")
        
        graph_gen = EvaluationGraphGenerator(self.all_metrics, GRAPHS_DIR)
        graph_gen.generate_all_graphs()
        
        self.logger.success(f"Graphs saved to: {GRAPHS_DIR}")


def main():
    """Main entry point"""
    print("\n" + "=" * 100)
    print(" HYBRID GENMENTOR - COMPREHENSIVE EVALUATION TEST SUITE")
    print(" Running 20 Tech Career Goal Tests with Research-Grade Visualizations")
    print("=" * 100 + "\n")
    
    # Check prerequisites
    if not VISUALIZATION_AVAILABLE:
        print("⚠️  Warning: matplotlib/numpy not installed.")
        print("   Install with: pip install matplotlib numpy seaborn")
        response = input("Continue without visualizations? (y/n): ")
        if response.lower() != 'y':
            return 1
    
    # Run evaluation
    runner = ComprehensiveEvaluationRunner()
    
    try:
        metrics = runner.run_all_tests()
        
        print("\n" + "=" * 100)
        print(" EVALUATION COMPLETED SUCCESSFULLY")
        print(f" Results saved to: {OUTPUT_DIR}")
        print(f" Graphs saved to: {GRAPHS_DIR}")
        print("=" * 100 + "\n")
        
        # Print quick summary
        success_rate = sum(1 for m in metrics if m.overall_success) / len(metrics) * 100
        print(f"📊 Overall Success Rate: {success_rate:.1f}%")
        print(f"📁 Total Output Files: {len(TEST_CASES) * 6 + 10} (approx)")
        
        return 0
        
    except KeyboardInterrupt:
        print("\n\n⚠️  Evaluation interrupted by user")
        return 1
    except Exception as e:
        print(f"\n\n❌ Evaluation failed: {str(e)}")
        traceback.print_exc()
        return 1


if __name__ == "__main__":
    sys.exit(main())
