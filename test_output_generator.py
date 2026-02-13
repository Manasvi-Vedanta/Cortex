"""
Test Output HTML Generator
Generates a professional, interactive HTML report from full_system_test.py output.
Includes learning path with resource links and quiz analysis.
"""

import json
import os
from datetime import datetime
from typing import Dict, List, Any, Optional


class TestOutputHTMLGenerator:
    """Generates professional HTML output from system test results."""
    
    def __init__(self, output_dir: str):
        self.output_dir = output_dir
        self.data = {}
        self._load_test_data()
        
        # Curated resources for common skills
        self.curated_resources = self._get_curated_resources()
    
    def _load_test_data(self):
        """Load all test output JSON files."""
        json_files = {
            'learning_path': '01_learning_path.json',
            'community_voting': '02_community_voting.json',
            'skill_suggestions': '03_skill_suggestions.json',
            'quiz_questions': '04_quiz_questions.json',
            'quiz_results': '05_quiz_results.json',
            'feedback_stats': '06_feedback_statistics.json',
            'regenerated_path': '07_regenerated_learning_path.json',
            'final_summary': '08_final_summary.json'
        }
        
        for key, filename in json_files.items():
            filepath = os.path.join(self.output_dir, filename)
            if os.path.exists(filepath):
                with open(filepath, 'r', encoding='utf-8') as f:
                    self.data[key] = json.load(f)
            else:
                self.data[key] = None
    
    def _get_curated_resources(self) -> Dict[str, Dict]:
        """Get curated high-quality resources for skills."""
        return {
            # === MOBILE DEVELOPMENT ===
            'android': {
                'official': {'title': 'Android Developers Official Guide', 'url': 'https://developer.android.com/guide', 'type': 'documentation', 'provider': 'Google', 'icon': '📚'},
                'course': {'title': 'Android Basics with Compose', 'url': 'https://developer.android.com/courses/android-basics-compose/course', 'type': 'course', 'provider': 'Google', 'icon': '🎓'},
                'video': {'title': 'Android Development Full Course', 'url': 'https://www.youtube.com/watch?v=fis26HvvDII', 'type': 'video', 'provider': 'freeCodeCamp', 'icon': '🎬'},
                'practice': {'title': 'Android Codelabs', 'url': 'https://developer.android.com/codelabs', 'type': 'practice', 'provider': 'Google', 'icon': '💻'}
            },
            'kotlin': {
                'official': {'title': 'Kotlin Official Documentation', 'url': 'https://kotlinlang.org/docs/home.html', 'type': 'documentation', 'provider': 'JetBrains', 'icon': '📚'},
                'course': {'title': 'Kotlin Bootcamp for Programmers', 'url': 'https://developer.android.com/courses/kotlin-bootcamp/overview', 'type': 'course', 'provider': 'Google', 'icon': '🎓'},
                'video': {'title': 'Kotlin Course for Beginners', 'url': 'https://www.youtube.com/watch?v=F9UC9DY-vIU', 'type': 'video', 'provider': 'freeCodeCamp', 'icon': '🎬'},
                'practice': {'title': 'Kotlin Koans', 'url': 'https://play.kotlinlang.org/koans/overview', 'type': 'practice', 'provider': 'JetBrains', 'icon': '💻'}
            },
            'jetpack compose': {
                'official': {'title': 'Jetpack Compose Documentation', 'url': 'https://developer.android.com/jetpack/compose/documentation', 'type': 'documentation', 'provider': 'Google', 'icon': '📚'},
                'course': {'title': 'Jetpack Compose for Android', 'url': 'https://developer.android.com/courses/jetpack-compose/course', 'type': 'course', 'provider': 'Google', 'icon': '🎓'},
                'video': {'title': 'Jetpack Compose Full Course', 'url': 'https://www.youtube.com/watch?v=6_wK_Ud8--0', 'type': 'video', 'provider': 'Philipp Lackner', 'icon': '🎬'},
                'practice': {'title': 'Compose Codelabs', 'url': 'https://developer.android.com/codelabs/jetpack-compose-basics', 'type': 'practice', 'provider': 'Google', 'icon': '💻'}
            },
            'firebase': {
                'official': {'title': 'Firebase Documentation', 'url': 'https://firebase.google.com/docs', 'type': 'documentation', 'provider': 'Google', 'icon': '📚'},
                'course': {'title': 'Firebase Fundamentals', 'url': 'https://firebase.google.com/codelabs/firebase-android', 'type': 'course', 'provider': 'Google', 'icon': '🎓'},
                'video': {'title': 'Firebase Android Tutorial', 'url': 'https://www.youtube.com/watch?v=dRYnm_k3w1w', 'type': 'video', 'provider': 'Philipp Lackner', 'icon': '🎬'},
                'practice': {'title': 'Firebase Codelabs', 'url': 'https://firebase.google.com/codelabs', 'type': 'practice', 'provider': 'Google', 'icon': '💻'}
            },
            'gradle': {
                'official': {'title': 'Gradle User Manual', 'url': 'https://docs.gradle.org/current/userguide/userguide.html', 'type': 'documentation', 'provider': 'Gradle', 'icon': '📚'},
                'course': {'title': 'Configure Android Builds', 'url': 'https://developer.android.com/build', 'type': 'course', 'provider': 'Google', 'icon': '🎓'},
                'video': {'title': 'Gradle Tutorial for Android', 'url': 'https://www.youtube.com/watch?v=o0M4f5djJTQ', 'type': 'video', 'provider': 'Coding in Flow', 'icon': '🎬'},
                'practice': {'title': 'Build Configuration Samples', 'url': 'https://github.com/android/gradle-recipes', 'type': 'practice', 'provider': 'GitHub', 'icon': '💻'}
            },
            'flutter': {
                'official': {'title': 'Flutter Documentation', 'url': 'https://docs.flutter.dev/', 'type': 'documentation', 'provider': 'Google', 'icon': '📚'},
                'course': {'title': 'Flutter Codelabs', 'url': 'https://docs.flutter.dev/codelabs', 'type': 'course', 'provider': 'Google', 'icon': '🎓'},
                'video': {'title': 'Flutter Course for Beginners', 'url': 'https://www.youtube.com/watch?v=VPvVD8t02U8', 'type': 'video', 'provider': 'freeCodeCamp', 'icon': '🎬'},
                'practice': {'title': 'Flutter Cookbook', 'url': 'https://docs.flutter.dev/cookbook', 'type': 'practice', 'provider': 'Google', 'icon': '💻'}
            },
            'react native': {
                'official': {'title': 'React Native Documentation', 'url': 'https://reactnative.dev/docs/getting-started', 'type': 'documentation', 'provider': 'Meta', 'icon': '📚'},
                'course': {'title': 'React Native Tutorial', 'url': 'https://reactnative.dev/docs/tutorial', 'type': 'course', 'provider': 'Meta', 'icon': '🎓'},
                'video': {'title': 'React Native Full Course', 'url': 'https://www.youtube.com/watch?v=obH0Po_RdWk', 'type': 'video', 'provider': 'freeCodeCamp', 'icon': '🎬'},
                'practice': {'title': 'Expo Snack', 'url': 'https://snack.expo.dev/', 'type': 'practice', 'provider': 'Expo', 'icon': '💻'}
            },
            
            # === DATA SCIENCE & ML ===
            'tensorflow': {
                'official': {'title': 'TensorFlow Documentation', 'url': 'https://www.tensorflow.org/learn', 'type': 'documentation', 'provider': 'Google', 'icon': '📚'},
                'course': {'title': 'TensorFlow Developer Certificate', 'url': 'https://www.tensorflow.org/certificate', 'type': 'course', 'provider': 'Google', 'icon': '🎓'},
                'video': {'title': 'TensorFlow 2.0 Full Course', 'url': 'https://www.youtube.com/watch?v=tPYj3fFJGjk', 'type': 'video', 'provider': 'freeCodeCamp', 'icon': '🎬'},
                'practice': {'title': 'TensorFlow Tutorials', 'url': 'https://www.tensorflow.org/tutorials', 'type': 'practice', 'provider': 'Google', 'icon': '💻'}
            },
            'pytorch': {
                'official': {'title': 'PyTorch Documentation', 'url': 'https://pytorch.org/docs/stable/index.html', 'type': 'documentation', 'provider': 'Meta', 'icon': '📚'},
                'course': {'title': 'PyTorch Tutorials', 'url': 'https://pytorch.org/tutorials/', 'type': 'course', 'provider': 'Meta', 'icon': '🎓'},
                'video': {'title': 'PyTorch Full Course', 'url': 'https://www.youtube.com/watch?v=c36lUUr864M', 'type': 'video', 'provider': 'Patrick Loeber', 'icon': '🎬'},
                'practice': {'title': 'PyTorch Examples', 'url': 'https://github.com/pytorch/examples', 'type': 'practice', 'provider': 'GitHub', 'icon': '💻'}
            },
            'pandas': {
                'official': {'title': 'Pandas Documentation', 'url': 'https://pandas.pydata.org/docs/', 'type': 'documentation', 'provider': 'Pandas', 'icon': '📚'},
                'course': {'title': 'Data Analysis with Pandas', 'url': 'https://www.kaggle.com/learn/pandas', 'type': 'course', 'provider': 'Kaggle', 'icon': '🎓'},
                'video': {'title': 'Pandas Tutorial', 'url': 'https://www.youtube.com/watch?v=vmEHCJofslg', 'type': 'video', 'provider': 'Keith Galli', 'icon': '🎬'},
                'practice': {'title': 'Pandas Exercises', 'url': 'https://github.com/guipsamora/pandas_exercises', 'type': 'practice', 'provider': 'GitHub', 'icon': '💻'}
            },
            'numpy': {
                'official': {'title': 'NumPy Documentation', 'url': 'https://numpy.org/doc/stable/', 'type': 'documentation', 'provider': 'NumPy', 'icon': '📚'},
                'course': {'title': 'NumPy Tutorial', 'url': 'https://numpy.org/doc/stable/user/quickstart.html', 'type': 'course', 'provider': 'NumPy', 'icon': '🎓'},
                'video': {'title': 'NumPy Full Course', 'url': 'https://www.youtube.com/watch?v=QUT1VHiLmmI', 'type': 'video', 'provider': 'freeCodeCamp', 'icon': '🎬'},
                'practice': {'title': 'NumPy 100 Exercises', 'url': 'https://github.com/rougier/numpy-100', 'type': 'practice', 'provider': 'GitHub', 'icon': '💻'}
            },
            'deep learning': {
                'official': {'title': 'Deep Learning Book', 'url': 'https://www.deeplearningbook.org/', 'type': 'documentation', 'provider': 'MIT Press', 'icon': '📚'},
                'course': {'title': 'Deep Learning Specialization', 'url': 'https://www.coursera.org/specializations/deep-learning', 'type': 'course', 'provider': 'deeplearning.ai', 'icon': '🎓'},
                'video': {'title': 'Deep Learning Full Course', 'url': 'https://www.youtube.com/watch?v=VyWAvY2CF9c', 'type': 'video', 'provider': 'freeCodeCamp', 'icon': '🎬'},
                'practice': {'title': 'Fast.ai Practical Deep Learning', 'url': 'https://course.fast.ai/', 'type': 'practice', 'provider': 'fast.ai', 'icon': '💻'}
            },
            'data analysis': {
                'official': {'title': 'Data Analysis Guide', 'url': 'https://pandas.pydata.org/docs/user_guide/index.html', 'type': 'documentation', 'provider': 'Pandas', 'icon': '📚'},
                'course': {'title': 'Data Analysis with Python', 'url': 'https://www.freecodecamp.org/learn/data-analysis-with-python/', 'type': 'course', 'provider': 'freeCodeCamp', 'icon': '🎓'},
                'video': {'title': 'Data Analysis Full Course', 'url': 'https://www.youtube.com/watch?v=GPVsHOlRBBI', 'type': 'video', 'provider': 'freeCodeCamp', 'icon': '🎬'},
                'practice': {'title': 'Kaggle Learn', 'url': 'https://www.kaggle.com/learn', 'type': 'practice', 'provider': 'Kaggle', 'icon': '💻'}
            },
            
            # === PROGRAMMING LANGUAGES (ordered by specificity) ===
            'javascript': {
                'official': {'title': 'MDN JavaScript Guide', 'url': 'https://developer.mozilla.org/en-US/docs/Web/JavaScript/Guide', 'type': 'documentation', 'provider': 'MDN', 'icon': '📚'},
                'course': {'title': 'JavaScript Algorithms & Data Structures', 'url': 'https://www.freecodecamp.org/learn/javascript-algorithms-and-data-structures/', 'type': 'course', 'provider': 'freeCodeCamp', 'icon': '🎓'},
                'video': {'title': 'JavaScript Full Course for Beginners', 'url': 'https://www.youtube.com/watch?v=PkZNo7MFNFg', 'type': 'video', 'provider': 'freeCodeCamp', 'icon': '🎬'},
                'practice': {'title': 'JavaScript30 - 30 Day Challenge', 'url': 'https://javascript30.com/', 'type': 'practice', 'provider': 'Wes Bos', 'icon': '💻'}
            },
            'java': {
                'official': {'title': 'Java Documentation', 'url': 'https://docs.oracle.com/en/java/', 'type': 'documentation', 'provider': 'Oracle', 'icon': '📚'},
                'course': {'title': 'Java Programming MOOC', 'url': 'https://java-programming.mooc.fi/', 'type': 'course', 'provider': 'University of Helsinki', 'icon': '🎓'},
                'video': {'title': 'Java Tutorial for Beginners', 'url': 'https://www.youtube.com/watch?v=eIrMbAQSU34', 'type': 'video', 'provider': 'Programming with Mosh', 'icon': '🎬'},
                'practice': {'title': 'Exercism Java Track', 'url': 'https://exercism.org/tracks/java', 'type': 'practice', 'provider': 'Exercism', 'icon': '💻'}
            },
            'python': {
                'official': {'title': 'Python Official Tutorial', 'url': 'https://docs.python.org/3/tutorial/', 'type': 'documentation', 'provider': 'Python.org', 'icon': '📚'},
                'course': {'title': 'Python for Everybody', 'url': 'https://www.py4e.com/', 'type': 'course', 'provider': 'Dr. Chuck', 'icon': '🎓'},
                'video': {'title': 'Python Tutorial for Beginners', 'url': 'https://www.youtube.com/watch?v=_uQrJ0TkZlc', 'type': 'video', 'provider': 'Programming with Mosh', 'icon': '🎬'},
                'practice': {'title': 'Python Exercises', 'url': 'https://www.w3schools.com/python/python_exercises.asp', 'type': 'practice', 'provider': 'W3Schools', 'icon': '💻'}
            },
            
            # === SOFTWARE DEVELOPMENT CONCEPTS ===
            'ide': {
                'official': {'title': 'Android Studio User Guide', 'url': 'https://developer.android.com/studio/intro', 'type': 'documentation', 'provider': 'Google', 'icon': '📚'},
                'course': {'title': 'Android Studio Essential Training', 'url': 'https://developer.android.com/studio/intro', 'type': 'course', 'provider': 'Google', 'icon': '🎓'},
                'video': {'title': 'Android Studio Tutorial for Beginners', 'url': 'https://www.youtube.com/watch?v=4M0hNugPJV8', 'type': 'video', 'provider': 'Coding in Flow', 'icon': '🎬'},
                'practice': {'title': 'Android Studio Codelabs', 'url': 'https://developer.android.com/codelabs/basic-android-kotlin-compose-first-app', 'type': 'practice', 'provider': 'Google', 'icon': '💻'}
            },
            'integrated development environment': {
                'official': {'title': 'Android Studio User Guide', 'url': 'https://developer.android.com/studio/intro', 'type': 'documentation', 'provider': 'Google', 'icon': '📚'},
                'course': {'title': 'IntelliJ IDEA Guide', 'url': 'https://www.jetbrains.com/idea/guide/', 'type': 'course', 'provider': 'JetBrains', 'icon': '🎓'},
                'video': {'title': 'How to Use Android Studio', 'url': 'https://www.youtube.com/watch?v=4M0hNugPJV8', 'type': 'video', 'provider': 'Coding in Flow', 'icon': '🎬'},
                'practice': {'title': 'Build Your First App', 'url': 'https://developer.android.com/training/basics/firstapp', 'type': 'practice', 'provider': 'Google', 'icon': '💻'}
            },
            'debug': {
                'official': {'title': 'Android Debugging Guide', 'url': 'https://developer.android.com/studio/debug', 'type': 'documentation', 'provider': 'Google', 'icon': '📚'},
                'course': {'title': 'Debugging Techniques', 'url': 'https://developer.android.com/studio/debug', 'type': 'course', 'provider': 'Google', 'icon': '🎓'},
                'video': {'title': 'How to Debug Android Apps', 'url': 'https://www.youtube.com/watch?v=Wn_P3kbGNl8', 'type': 'video', 'provider': 'CodingWithMitch', 'icon': '🎬'},
                'practice': {'title': 'Debug Codelabs', 'url': 'https://developer.android.com/codelabs/basic-android-kotlin-compose-first-app', 'type': 'practice', 'provider': 'Google', 'icon': '💻'}
            },
            'object-oriented': {
                'official': {'title': 'OOP Concepts in Java', 'url': 'https://docs.oracle.com/javase/tutorial/java/concepts/', 'type': 'documentation', 'provider': 'Oracle', 'icon': '📚'},
                'course': {'title': 'Object-Oriented Programming in Java', 'url': 'https://www.coursera.org/learn/object-oriented-java', 'type': 'course', 'provider': 'Duke/Coursera', 'icon': '🎓'},
                'video': {'title': 'OOP in Java - Full Course', 'url': 'https://www.youtube.com/watch?v=6T_HgnjoYwM', 'type': 'video', 'provider': 'Bro Code', 'icon': '🎬'},
                'practice': {'title': 'OOP Practice Problems', 'url': 'https://exercism.org/tracks/java/concepts/classes', 'type': 'practice', 'provider': 'Exercism', 'icon': '💻'}
            },
            'oop': {
                'official': {'title': 'OOP Concepts in Java', 'url': 'https://docs.oracle.com/javase/tutorial/java/concepts/', 'type': 'documentation', 'provider': 'Oracle', 'icon': '📚'},
                'course': {'title': 'Object-Oriented Programming in Java', 'url': 'https://www.coursera.org/learn/object-oriented-java', 'type': 'course', 'provider': 'Duke/Coursera', 'icon': '🎓'},
                'video': {'title': 'OOP Concepts Explained', 'url': 'https://www.youtube.com/watch?v=6T_HgnjoYwM', 'type': 'video', 'provider': 'Bro Code', 'icon': '🎬'},
                'practice': {'title': 'OOP Practice Problems', 'url': 'https://exercism.org/tracks/java/concepts/classes', 'type': 'practice', 'provider': 'Exercism', 'icon': '💻'}
            },
            'logic programming': {
                'official': {'title': 'Programming Logic Fundamentals', 'url': 'https://www.khanacademy.org/computing/computer-programming/programming', 'type': 'documentation', 'provider': 'Khan Academy', 'icon': '📚'},
                'course': {'title': 'CS50 Introduction to Programming', 'url': 'https://cs50.harvard.edu/x/', 'type': 'course', 'provider': 'Harvard', 'icon': '🎓'},
                'video': {'title': 'Programming Logic Tutorial', 'url': 'https://www.youtube.com/watch?v=azcrPFhaY9k', 'type': 'video', 'provider': 'freeCodeCamp', 'icon': '🎬'},
                'practice': {'title': 'Logic Exercises', 'url': 'https://www.hackerrank.com/domains/algorithms', 'type': 'practice', 'provider': 'HackerRank', 'icon': '💻'}
            },
            'flowchart': {
                'official': {'title': 'Flowchart Guide', 'url': 'https://www.lucidchart.com/pages/what-is-a-flowchart-tutorial', 'type': 'documentation', 'provider': 'Lucidchart', 'icon': '📚'},
                'course': {'title': 'Algorithm Design with Flowcharts', 'url': 'https://www.khanacademy.org/computing/computer-science/algorithms', 'type': 'course', 'provider': 'Khan Academy', 'icon': '🎓'},
                'video': {'title': 'Flowcharts Explained', 'url': 'https://www.youtube.com/watch?v=6hfOvs8pY1k', 'type': 'video', 'provider': 'CS Dojo', 'icon': '🎬'},
                'practice': {'title': 'Draw.io Flowchart Tool', 'url': 'https://app.diagrams.net/', 'type': 'practice', 'provider': 'draw.io', 'icon': '💻'}
            },
            'design pattern': {
                'official': {'title': 'Design Patterns in Java', 'url': 'https://refactoring.guru/design-patterns', 'type': 'documentation', 'provider': 'Refactoring Guru', 'icon': '📚'},
                'course': {'title': 'Design Patterns Course', 'url': 'https://www.coursera.org/learn/design-patterns', 'type': 'course', 'provider': 'Coursera', 'icon': '🎓'},
                'video': {'title': 'Design Patterns in Android', 'url': 'https://www.youtube.com/watch?v=v9ejT8FO-7I', 'type': 'video', 'provider': 'Derek Banas', 'icon': '🎬'},
                'practice': {'title': 'Design Patterns Examples', 'url': 'https://refactoring.guru/design-patterns/examples', 'type': 'practice', 'provider': 'Refactoring Guru', 'icon': '💻'}
            },
            'software design': {
                'official': {'title': 'Software Design Principles', 'url': 'https://refactoring.guru/design-patterns', 'type': 'documentation', 'provider': 'Refactoring Guru', 'icon': '📚'},
                'course': {'title': 'Software Design and Architecture', 'url': 'https://www.coursera.org/specializations/software-design-architecture', 'type': 'course', 'provider': 'Coursera', 'icon': '🎓'},
                'video': {'title': 'Software Design Tutorial', 'url': 'https://www.youtube.com/watch?v=v9ejT8FO-7I', 'type': 'video', 'provider': 'Derek Banas', 'icon': '🎬'},
                'practice': {'title': 'Design Patterns Examples', 'url': 'https://refactoring.guru/design-patterns/examples', 'type': 'practice', 'provider': 'Refactoring Guru', 'icon': '💻'}
            },
            'version control': {
                'official': {'title': 'Pro Git Book', 'url': 'https://git-scm.com/book/en/v2', 'type': 'documentation', 'provider': 'Git', 'icon': '📚'},
                'course': {'title': 'Version Control with Git', 'url': 'https://www.atlassian.com/git/tutorials', 'type': 'course', 'provider': 'Atlassian', 'icon': '🎓'},
                'video': {'title': 'Git and GitHub for Beginners', 'url': 'https://www.youtube.com/watch?v=RGOj5yH7evk', 'type': 'video', 'provider': 'freeCodeCamp', 'icon': '🎬'},
                'practice': {'title': 'Learn Git Branching', 'url': 'https://learngitbranching.js.org/', 'type': 'practice', 'provider': 'Learn Git Branching', 'icon': '💻'}
            },
            'configuration management': {
                'official': {'title': 'Git Documentation', 'url': 'https://git-scm.com/doc', 'type': 'documentation', 'provider': 'Git', 'icon': '📚'},
                'course': {'title': 'Git Essentials', 'url': 'https://www.atlassian.com/git/tutorials', 'type': 'course', 'provider': 'Atlassian', 'icon': '🎓'},
                'video': {'title': 'Git Tutorial for Beginners', 'url': 'https://www.youtube.com/watch?v=8JJ101D3knE', 'type': 'video', 'provider': 'Programming with Mosh', 'icon': '🎬'},
                'practice': {'title': 'Learn Git Branching', 'url': 'https://learngitbranching.js.org/', 'type': 'practice', 'provider': 'Learn Git Branching', 'icon': '💻'}
            },
            'git': {
                'official': {'title': 'Pro Git Book', 'url': 'https://git-scm.com/book/en/v2', 'type': 'documentation', 'provider': 'Git', 'icon': '📚'},
                'course': {'title': 'Git & GitHub Course', 'url': 'https://www.atlassian.com/git/tutorials', 'type': 'course', 'provider': 'Atlassian', 'icon': '🎓'},
                'video': {'title': 'Git and GitHub for Beginners', 'url': 'https://www.youtube.com/watch?v=RGOj5yH7evk', 'type': 'video', 'provider': 'freeCodeCamp', 'icon': '🎬'},
                'practice': {'title': 'Learn Git Branching', 'url': 'https://learngitbranching.js.org/', 'type': 'practice', 'provider': 'Learn Git Branching', 'icon': '💻'}
            },
            
            # === DATABASE ===
            'sql': {
                'official': {'title': 'SQL Tutorial', 'url': 'https://www.w3schools.com/sql/', 'type': 'documentation', 'provider': 'W3Schools', 'icon': '📚'},
                'course': {'title': 'SQL for Data Science', 'url': 'https://www.coursera.org/learn/sql-for-data-science', 'type': 'course', 'provider': 'Coursera', 'icon': '🎓'},
                'video': {'title': 'SQL Full Course', 'url': 'https://www.youtube.com/watch?v=HXV3zeQKqGY', 'type': 'video', 'provider': 'freeCodeCamp', 'icon': '🎬'},
                'practice': {'title': 'SQLBolt Interactive', 'url': 'https://sqlbolt.com/', 'type': 'practice', 'provider': 'SQLBolt', 'icon': '💻'}
            },
            'database': {
                'official': {'title': 'Database Fundamentals', 'url': 'https://www.w3schools.com/sql/sql_intro.asp', 'type': 'documentation', 'provider': 'W3Schools', 'icon': '📚'},
                'course': {'title': 'Databases: Relational Databases', 'url': 'https://www.edx.org/course/databases-5-sql', 'type': 'course', 'provider': 'Stanford/edX', 'icon': '🎓'},
                'video': {'title': 'Database Design Course', 'url': 'https://www.youtube.com/watch?v=ztHopE5Wnpc', 'type': 'video', 'provider': 'freeCodeCamp', 'icon': '🎬'},
                'practice': {'title': 'SQLite Tutorial', 'url': 'https://www.sqlitetutorial.net/', 'type': 'practice', 'provider': 'SQLite Tutorial', 'icon': '💻'}
            },
            
            # === WEB & API ===
            'api': {
                'official': {'title': 'REST API Tutorial', 'url': 'https://restfulapi.net/', 'type': 'documentation', 'provider': 'RESTful API', 'icon': '📚'},
                'course': {'title': 'APIs for Beginners', 'url': 'https://www.freecodecamp.org/news/apis-for-beginners/', 'type': 'course', 'provider': 'freeCodeCamp', 'icon': '🎓'},
                'video': {'title': 'REST API Explained', 'url': 'https://www.youtube.com/watch?v=lsMQRaeKNDk', 'type': 'video', 'provider': 'Programming with Mosh', 'icon': '🎬'},
                'practice': {'title': 'Postman Learning Center', 'url': 'https://learning.postman.com/', 'type': 'practice', 'provider': 'Postman', 'icon': '💻'}
            },
            'web development': {
                'official': {'title': 'MDN Web Docs', 'url': 'https://developer.mozilla.org/en-US/docs/Learn', 'type': 'documentation', 'provider': 'MDN', 'icon': '📚'},
                'course': {'title': 'The Odin Project', 'url': 'https://www.theodinproject.com/', 'type': 'course', 'provider': 'The Odin Project', 'icon': '🎓'},
                'video': {'title': 'Web Development Full Course', 'url': 'https://www.youtube.com/watch?v=G3e-cpL7ofc', 'type': 'video', 'provider': 'SuperSimpleDev', 'icon': '🎬'},
                'practice': {'title': 'Frontend Mentor', 'url': 'https://www.frontendmentor.io/', 'type': 'practice', 'provider': 'Frontend Mentor', 'icon': '💻'}
            },
            
            # === MACHINE LEARNING & AI ===
            'machine learning': {
                'official': {'title': 'TensorFlow Documentation', 'url': 'https://www.tensorflow.org/learn', 'type': 'documentation', 'provider': 'Google', 'icon': '📚'},
                'course': {'title': 'Machine Learning by Andrew Ng', 'url': 'https://www.coursera.org/specializations/machine-learning-introduction', 'type': 'course', 'provider': 'Stanford/Coursera', 'icon': '🎓'},
                'video': {'title': 'Machine Learning Course', 'url': 'https://www.youtube.com/watch?v=NWONeJKn6kc', 'type': 'video', 'provider': 'freeCodeCamp', 'icon': '🎬'},
                'practice': {'title': 'Kaggle Learn', 'url': 'https://www.kaggle.com/learn', 'type': 'practice', 'provider': 'Kaggle', 'icon': '💻'}
            },
            
            # === DEVOPS & TOOLS ===
            'docker': {
                'official': {'title': 'Docker Documentation', 'url': 'https://docs.docker.com/get-started/', 'type': 'documentation', 'provider': 'Docker', 'icon': '📚'},
                'course': {'title': 'Docker for Beginners', 'url': 'https://docker-curriculum.com/', 'type': 'course', 'provider': 'Docker Curriculum', 'icon': '🎓'},
                'video': {'title': 'Docker Tutorial', 'url': 'https://www.youtube.com/watch?v=fqMOX6JJhGo', 'type': 'video', 'provider': 'freeCodeCamp', 'icon': '🎬'},
                'practice': {'title': 'Play with Docker', 'url': 'https://labs.play-with-docker.com/', 'type': 'practice', 'provider': 'Docker', 'icon': '💻'}
            },
            'testing': {
                'official': {'title': 'Android Testing Guide', 'url': 'https://developer.android.com/training/testing', 'type': 'documentation', 'provider': 'Google', 'icon': '📚'},
                'course': {'title': 'Software Testing Fundamentals', 'url': 'https://www.udacity.com/course/software-testing--cs258', 'type': 'course', 'provider': 'Udacity', 'icon': '🎓'},
                'video': {'title': 'Android Testing Tutorial', 'url': 'https://www.youtube.com/watch?v=EkfVL5vCDmo', 'type': 'video', 'provider': 'Philipp Lackner', 'icon': '🎬'},
                'practice': {'title': 'Testing Codelabs', 'url': 'https://developer.android.com/codelabs/advanced-android-kotlin-training-testing-basics', 'type': 'practice', 'provider': 'Google', 'icon': '💻'}
            },
            
            # === UI/UX ===
            'ui design': {
                'official': {'title': 'Material Design Guidelines', 'url': 'https://m3.material.io/', 'type': 'documentation', 'provider': 'Google', 'icon': '📚'},
                'course': {'title': 'UI Design Fundamentals', 'url': 'https://www.coursera.org/learn/ui-design', 'type': 'course', 'provider': 'Coursera', 'icon': '🎓'},
                'video': {'title': 'UI Design for Beginners', 'url': 'https://www.youtube.com/watch?v=_Hp_dI0DzY4', 'type': 'video', 'provider': 'Envato Tuts+', 'icon': '🎬'},
                'practice': {'title': 'Figma Learn', 'url': 'https://www.figma.com/resources/learn-design/', 'type': 'practice', 'provider': 'Figma', 'icon': '💻'}
            },
            
            # === GENERIC PROGRAMMING CONCEPTS ===
            'programming': {
                'official': {'title': 'Programming Fundamentals', 'url': 'https://www.khanacademy.org/computing/computer-programming', 'type': 'documentation', 'provider': 'Khan Academy', 'icon': '📚'},
                'course': {'title': 'CS50: Introduction to Computer Science', 'url': 'https://cs50.harvard.edu/x/', 'type': 'course', 'provider': 'Harvard', 'icon': '🎓'},
                'video': {'title': 'Programming Basics', 'url': 'https://www.youtube.com/watch?v=zOjov-2OZ0E', 'type': 'video', 'provider': 'freeCodeCamp', 'icon': '🎬'},
                'practice': {'title': 'Codecademy', 'url': 'https://www.codecademy.com/', 'type': 'practice', 'provider': 'Codecademy', 'icon': '💻'}
            }
        }
    
    def _get_skill_resources(self, skill_name: str) -> List[Dict]:
        """Get curated resources for a skill with precise matching."""
        skill_lower = skill_name.lower().strip()
        
        # Define matching priority - exact matches first, then partial
        # This prevents 'java' from matching 'javascript'
        exact_matches = {
            'javascript': 'javascript',
            'java': 'java',
            'python': 'python',
            'kotlin': 'kotlin',
            'android': 'android',
        }
        
        # Check for exact word matches first (avoid java matching javascript)
        for exact_key, resource_key in exact_matches.items():
            # Check if it's an exact match or exact word in phrase
            words = skill_lower.split()
            if exact_key == skill_lower or exact_key in words:
                # Make sure we're not matching 'java' when skill is 'javascript'
                if exact_key == 'java' and 'javascript' in skill_lower:
                    continue
                if resource_key in self.curated_resources:
                    resources = self.curated_resources[resource_key]
                    return [
                        {**resources.get('official', {}), 'category': 'Documentation'},
                        {**resources.get('course', {}), 'category': 'Course'},
                        {**resources.get('video', {}), 'category': 'Video'},
                        {**resources.get('practice', {}), 'category': 'Practice'}
                    ]
        
        # Keyword mapping for common skill patterns
        keyword_mapping = {
            'integrated development environment': 'integrated development environment',
            'ide': 'ide',
            'debug': 'debug',
            'object-oriented': 'object-oriented',
            'object oriented': 'object-oriented',
            'oop': 'oop',
            'logic programming': 'logic programming',
            'flowchart': 'flowchart',
            'design pattern': 'design pattern',
            'software design': 'software design',
            'version control': 'version control',
            'configuration management': 'configuration management',
            'git': 'git',
            'sql': 'sql',
            'database': 'database',
            'api': 'api',
            'web development': 'web development',
            'machine learning': 'machine learning',
            'docker': 'docker',
            'testing': 'testing',
            'test': 'testing',
            'ui design': 'ui design',
            'programming': 'programming',
            'mobile': 'android',
        }
        
        # Find best matching keyword
        for keyword, resource_key in keyword_mapping.items():
            if keyword in skill_lower:
                if resource_key in self.curated_resources:
                    resources = self.curated_resources[resource_key]
                    return [
                        {**resources.get('official', {}), 'category': 'Documentation'},
                        {**resources.get('course', {}), 'category': 'Course'},
                        {**resources.get('video', {}), 'category': 'Video'},
                        {**resources.get('practice', {}), 'category': 'Practice'}
                    ]
        
        # Fallback to programming basics for generic skills
        resources = self.curated_resources['programming']
        return [
            {**resources.get('official', {}), 'category': 'Documentation'},
            {**resources.get('course', {}), 'category': 'Course'},
            {**resources.get('video', {}), 'category': 'Video'},
            {**resources.get('practice', {}), 'category': 'Practice'}
        ]
    
    def generate_html(self) -> str:
        """Generate complete HTML report."""
        learning_path = self.data.get('regenerated_path') or self.data.get('learning_path') or {}
        quiz_questions = self.data.get('quiz_questions') or {}
        quiz_results = self.data.get('quiz_results') or {}
        final_summary = self.data.get('final_summary') or {}
        
        occupation = learning_path.get('matched_occupation', {})
        sessions = learning_path.get('learning_path', [])
        
        # Get quiz data - handle None/missing quiz data gracefully
        quiz_obj = quiz_questions.get('quiz', {}) if quiz_questions else {}
        questions = quiz_obj.get('questions', []) if isinstance(quiz_obj, dict) else []
        analysis = quiz_results.get('analysis', {}) if quiz_results else {}
        score_data = analysis.get('score', {}) if analysis else {}
        
        html = f'''<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Learning Path Report - Hybrid GenMentor</title>
    <link href="https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800&display=swap" rel="stylesheet">
    <style>
        * {{
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }}
        
        :root {{
            --primary: #6366f1;
            --primary-dark: #4f46e5;
            --primary-light: #818cf8;
            --secondary: #8b5cf6;
            --success: #10b981;
            --warning: #f59e0b;
            --danger: #ef4444;
            --info: #3b82f6;
            --dark: #1e293b;
            --light: #f8fafc;
            --gray: #64748b;
            --border: #e2e8f0;
        }}
        
        body {{
            font-family: 'Inter', -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            min-height: 100vh;
            line-height: 1.6;
            color: var(--dark);
        }}
        
        .container {{
            max-width: 1400px;
            margin: 0 auto;
            padding: 20px;
        }}
        
        .main-card {{
            background: white;
            border-radius: 24px;
            box-shadow: 0 25px 80px rgba(0,0,0,0.3);
            overflow: hidden;
        }}
        
        /* Header Styles */
        .header {{
            background: linear-gradient(135deg, #1e293b 0%, #334155 100%);
            color: white;
            padding: 50px;
            position: relative;
            overflow: hidden;
        }}
        
        .header::before {{
            content: '';
            position: absolute;
            top: -50%;
            right: -20%;
            width: 60%;
            height: 200%;
            background: linear-gradient(135deg, rgba(99, 102, 241, 0.3), rgba(139, 92, 246, 0.3));
            transform: rotate(15deg);
            pointer-events: none;
        }}
        
        .header-content {{
            position: relative;
            z-index: 1;
        }}
        
        .badge {{
            display: inline-block;
            background: rgba(99, 102, 241, 0.3);
            color: #a5b4fc;
            padding: 6px 16px;
            border-radius: 20px;
            font-size: 0.85em;
            font-weight: 600;
            margin-bottom: 15px;
            backdrop-filter: blur(10px);
        }}
        
        .header h1 {{
            font-size: 2.8em;
            font-weight: 800;
            margin-bottom: 10px;
            line-height: 1.2;
        }}
        
        .header .subtitle {{
            font-size: 1.15em;
            opacity: 0.9;
            font-weight: 400;
        }}
        
        .occupation-match {{
            margin-top: 25px;
            display: flex;
            align-items: center;
            gap: 15px;
            flex-wrap: wrap;
        }}
        
        .match-score {{
            background: linear-gradient(135deg, var(--success), #059669);
            padding: 12px 25px;
            border-radius: 30px;
            font-weight: 700;
            font-size: 1.1em;
        }}
        
        .occupation-label {{
            background: rgba(255,255,255,0.1);
            padding: 10px 20px;
            border-radius: 10px;
            font-weight: 500;
        }}
        
        /* Stats Bar */
        .stats-bar {{
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(180px, 1fr));
            background: var(--light);
            border-bottom: 1px solid var(--border);
        }}
        
        .stat-item {{
            padding: 30px 25px;
            text-align: center;
            border-right: 1px solid var(--border);
            transition: all 0.3s;
        }}
        
        .stat-item:last-child {{
            border-right: none;
        }}
        
        .stat-item:hover {{
            background: white;
        }}
        
        .stat-icon {{
            font-size: 2.2em;
            margin-bottom: 8px;
        }}
        
        .stat-value {{
            font-size: 2.5em;
            font-weight: 800;
            color: var(--primary);
            line-height: 1;
        }}
        
        .stat-label {{
            color: var(--gray);
            font-size: 0.9em;
            margin-top: 5px;
            font-weight: 500;
        }}
        
        /* Navigation Tabs */
        .nav-tabs {{
            display: flex;
            background: white;
            border-bottom: 2px solid var(--border);
            padding: 0 30px;
            overflow-x: auto;
        }}
        
        .nav-tab {{
            padding: 20px 30px;
            font-weight: 600;
            color: var(--gray);
            cursor: pointer;
            border-bottom: 3px solid transparent;
            margin-bottom: -2px;
            transition: all 0.3s;
            white-space: nowrap;
        }}
        
        .nav-tab:hover {{
            color: var(--primary);
        }}
        
        .nav-tab.active {{
            color: var(--primary);
            border-bottom-color: var(--primary);
        }}
        
        .nav-tab .tab-icon {{
            margin-right: 8px;
        }}
        
        /* Tab Content */
        .tab-content {{
            display: none;
            padding: 40px;
            animation: fadeIn 0.4s ease;
        }}
        
        .tab-content.active {{
            display: block;
        }}
        
        @keyframes fadeIn {{
            from {{ opacity: 0; transform: translateY(10px); }}
            to {{ opacity: 1; transform: translateY(0); }}
        }}
        
        /* Section Titles */
        .section-title {{
            font-size: 1.8em;
            font-weight: 700;
            color: var(--dark);
            margin-bottom: 25px;
            display: flex;
            align-items: center;
            gap: 12px;
        }}
        
        .section-title .icon {{
            font-size: 1.2em;
        }}
        
        /* Session Cards */
        .session-card {{
            background: white;
            border-radius: 16px;
            margin-bottom: 30px;
            box-shadow: 0 4px 20px rgba(0,0,0,0.08);
            overflow: hidden;
            border: 1px solid var(--border);
            transition: all 0.3s;
        }}
        
        .session-card:hover {{
            box-shadow: 0 10px 40px rgba(0,0,0,0.12);
            transform: translateY(-3px);
        }}
        
        .session-header {{
            background: linear-gradient(135deg, var(--primary) 0%, var(--secondary) 100%);
            color: white;
            padding: 25px 30px;
            display: flex;
            justify-content: space-between;
            align-items: center;
            flex-wrap: wrap;
            gap: 15px;
        }}
        
        .session-number {{
            background: rgba(255,255,255,0.2);
            width: 45px;
            height: 45px;
            border-radius: 50%;
            display: flex;
            align-items: center;
            justify-content: center;
            font-weight: 700;
            font-size: 1.2em;
        }}
        
        .session-info {{
            flex: 1;
            min-width: 200px;
        }}
        
        .session-title {{
            font-size: 1.4em;
            font-weight: 700;
            margin-bottom: 5px;
        }}
        
        .session-meta {{
            opacity: 0.9;
            font-size: 0.95em;
        }}
        
        .session-duration {{
            background: rgba(255,255,255,0.2);
            padding: 8px 16px;
            border-radius: 20px;
            font-weight: 600;
        }}
        
        .session-body {{
            padding: 25px 30px;
        }}
        
        .session-description {{
            color: var(--gray);
            margin-bottom: 20px;
            font-size: 1.05em;
        }}
        
        /* Skills List */
        .skills-grid {{
            display: grid;
            gap: 15px;
        }}
        
        .skill-item {{
            background: var(--light);
            border-radius: 12px;
            padding: 20px;
            border: 1px solid var(--border);
            transition: all 0.3s;
        }}
        
        .skill-item:hover {{
            background: white;
            box-shadow: 0 4px 15px rgba(0,0,0,0.08);
        }}
        
        .skill-header {{
            display: flex;
            justify-content: space-between;
            align-items: center;
            margin-bottom: 12px;
        }}
        
        .skill-name {{
            font-weight: 600;
            font-size: 1.1em;
            color: var(--dark);
        }}
        
        .skill-toggle {{
            background: var(--primary);
            color: white;
            border: none;
            padding: 6px 14px;
            border-radius: 6px;
            cursor: pointer;
            font-size: 0.85em;
            font-weight: 600;
            transition: all 0.3s;
        }}
        
        .skill-toggle:hover {{
            background: var(--primary-dark);
        }}
        
        .skill-resources {{
            display: none;
            margin-top: 15px;
            padding-top: 15px;
            border-top: 1px solid var(--border);
        }}
        
        .skill-resources.show {{
            display: block;
            animation: slideDown 0.3s ease;
        }}
        
        @keyframes slideDown {{
            from {{ opacity: 0; max-height: 0; }}
            to {{ opacity: 1; max-height: 500px; }}
        }}
        
        .resource-grid {{
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(220px, 1fr));
            gap: 12px;
        }}
        
        .resource-link {{
            display: flex;
            align-items: center;
            gap: 10px;
            padding: 12px 15px;
            background: white;
            border: 1px solid var(--border);
            border-radius: 8px;
            text-decoration: none;
            color: var(--dark);
            transition: all 0.3s;
        }}
        
        .resource-link:hover {{
            border-color: var(--primary);
            box-shadow: 0 4px 12px rgba(99, 102, 241, 0.15);
            transform: translateX(3px);
        }}
        
        .resource-icon {{
            font-size: 1.4em;
        }}
        
        .resource-info {{
            flex: 1;
            min-width: 0;
        }}
        
        .resource-title {{
            font-weight: 600;
            font-size: 0.9em;
            white-space: nowrap;
            overflow: hidden;
            text-overflow: ellipsis;
        }}
        
        .resource-provider {{
            font-size: 0.8em;
            color: var(--gray);
        }}
        
        .resource-arrow {{
            color: var(--primary);
            font-size: 1.1em;
        }}
        
        /* Quiz Section */
        .quiz-overview {{
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
            gap: 20px;
            margin-bottom: 35px;
        }}
        
        .quiz-stat-card {{
            background: linear-gradient(135deg, var(--light), white);
            border-radius: 16px;
            padding: 25px;
            border: 1px solid var(--border);
            text-align: center;
        }}
        
        .quiz-stat-card.primary {{
            background: linear-gradient(135deg, var(--primary), var(--secondary));
            color: white;
            border: none;
        }}
        
        .quiz-stat-card.success {{
            background: linear-gradient(135deg, var(--success), #059669);
            color: white;
            border: none;
        }}
        
        .quiz-stat-icon {{
            font-size: 2.5em;
            margin-bottom: 10px;
        }}
        
        .quiz-stat-value {{
            font-size: 2.8em;
            font-weight: 800;
            line-height: 1;
        }}
        
        .quiz-stat-label {{
            margin-top: 8px;
            font-weight: 500;
            opacity: 0.9;
        }}
        
        /* Progress Bar */
        .progress-container {{
            background: var(--border);
            border-radius: 10px;
            height: 20px;
            margin: 20px 0;
            overflow: hidden;
        }}
        
        .progress-bar {{
            height: 100%;
            background: linear-gradient(90deg, var(--success), #34d399);
            border-radius: 10px;
            transition: width 1s ease;
        }}
        
        /* Question Cards */
        .question-card {{
            background: white;
            border-radius: 12px;
            margin-bottom: 20px;
            border: 1px solid var(--border);
            overflow: hidden;
            transition: all 0.3s;
        }}
        
        .question-card:hover {{
            box-shadow: 0 5px 20px rgba(0,0,0,0.08);
        }}
        
        .question-card.correct {{
            border-left: 4px solid var(--success);
        }}
        
        .question-card.incorrect {{
            border-left: 4px solid var(--danger);
        }}
        
        .question-header {{
            padding: 20px 25px;
            display: flex;
            justify-content: space-between;
            align-items: center;
            background: var(--light);
            cursor: pointer;
        }}
        
        .question-number {{
            font-weight: 700;
            color: var(--primary);
        }}
        
        .question-meta {{
            display: flex;
            gap: 10px;
            align-items: center;
        }}
        
        .difficulty-badge {{
            padding: 4px 12px;
            border-radius: 15px;
            font-size: 0.8em;
            font-weight: 600;
        }}
        
        .difficulty-badge.easy {{
            background: #dcfce7;
            color: #166534;
        }}
        
        .difficulty-badge.medium {{
            background: #fef3c7;
            color: #92400e;
        }}
        
        .difficulty-badge.hard {{
            background: #fee2e2;
            color: #991b1b;
        }}
        
        .result-badge {{
            width: 28px;
            height: 28px;
            border-radius: 50%;
            display: flex;
            align-items: center;
            justify-content: center;
            font-weight: bold;
        }}
        
        .result-badge.correct {{
            background: var(--success);
            color: white;
        }}
        
        .result-badge.incorrect {{
            background: var(--danger);
            color: white;
        }}
        
        .question-body {{
            display: none;
            padding: 25px;
            border-top: 1px solid var(--border);
        }}
        
        .question-body.show {{
            display: block;
            animation: fadeIn 0.3s ease;
        }}
        
        .question-text {{
            font-size: 1.1em;
            font-weight: 500;
            margin-bottom: 20px;
            color: var(--dark);
        }}
        
        .options-list {{
            list-style: none;
        }}
        
        .option-item {{
            padding: 15px 20px;
            margin-bottom: 10px;
            border-radius: 10px;
            border: 2px solid var(--border);
            display: flex;
            align-items: center;
            gap: 12px;
            transition: all 0.3s;
        }}
        
        .option-item.correct-answer {{
            background: #dcfce7;
            border-color: var(--success);
        }}
        
        .option-item.user-wrong {{
            background: #fee2e2;
            border-color: var(--danger);
        }}
        
        .option-key {{
            width: 30px;
            height: 30px;
            border-radius: 50%;
            background: var(--light);
            display: flex;
            align-items: center;
            justify-content: center;
            font-weight: 600;
            font-size: 0.9em;
        }}
        
        .option-item.correct-answer .option-key {{
            background: var(--success);
            color: white;
        }}
        
        .option-item.user-wrong .option-key {{
            background: var(--danger);
            color: white;
        }}
        
        .explanation {{
            margin-top: 20px;
            padding: 15px 20px;
            background: #eff6ff;
            border-radius: 10px;
            border-left: 4px solid var(--info);
        }}
        
        .explanation-title {{
            font-weight: 600;
            color: var(--info);
            margin-bottom: 5px;
        }}
        
        /* Analysis Section */
        .analysis-grid {{
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
            gap: 25px;
        }}
        
        .analysis-card {{
            background: white;
            border-radius: 16px;
            padding: 25px;
            border: 1px solid var(--border);
        }}
        
        .analysis-card h3 {{
            font-size: 1.2em;
            margin-bottom: 15px;
            color: var(--dark);
            display: flex;
            align-items: center;
            gap: 8px;
        }}
        
        .strength-item, .weakness-item {{
            padding: 12px 15px;
            margin-bottom: 10px;
            border-radius: 8px;
            display: flex;
            justify-content: space-between;
            align-items: center;
        }}
        
        .strength-item {{
            background: #dcfce7;
        }}
        
        .weakness-item {{
            background: #fee2e2;
        }}
        
        .topic-name {{
            font-weight: 600;
        }}
        
        .topic-score {{
            font-weight: 700;
            padding: 4px 10px;
            border-radius: 6px;
            background: rgba(255,255,255,0.6);
        }}
        
        /* Difficulty Chart */
        .difficulty-chart {{
            display: flex;
            gap: 20px;
            margin-top: 15px;
        }}
        
        .difficulty-item {{
            flex: 1;
            text-align: center;
        }}
        
        .difficulty-bar {{
            height: 120px;
            background: var(--border);
            border-radius: 8px;
            position: relative;
            overflow: hidden;
            margin-bottom: 8px;
        }}
        
        .difficulty-fill {{
            position: absolute;
            bottom: 0;
            left: 0;
            right: 0;
            background: linear-gradient(to top, var(--primary), var(--primary-light));
            border-radius: 8px;
            transition: height 1s ease;
        }}
        
        .difficulty-label {{
            font-weight: 600;
            font-size: 0.9em;
        }}
        
        .difficulty-score {{
            font-size: 0.85em;
            color: var(--gray);
        }}
        
        /* Summary Section */
        .summary-grid {{
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
            gap: 20px;
        }}
        
        .summary-card {{
            background: var(--light);
            border-radius: 12px;
            padding: 25px;
            text-align: center;
        }}
        
        .summary-icon {{
            font-size: 2.5em;
            margin-bottom: 10px;
        }}
        
        .summary-value {{
            font-size: 1.4em;
            font-weight: 700;
            color: var(--dark);
        }}
        
        .summary-label {{
            color: var(--gray);
            font-size: 0.9em;
            margin-top: 5px;
        }}
        
        /* Footer */
        .footer {{
            background: var(--dark);
            color: white;
            padding: 30px;
            text-align: center;
        }}
        
        .footer-text {{
            opacity: 0.8;
            font-size: 0.95em;
        }}
        
        /* Responsive */
        @media (max-width: 768px) {{
            .header {{
                padding: 30px 20px;
            }}
            
            .header h1 {{
                font-size: 1.8em;
            }}
            
            .tab-content {{
                padding: 20px;
            }}
            
            .session-header {{
                padding: 20px;
            }}
            
            .resource-grid {{
                grid-template-columns: 1fr;
            }}
        }}
        
        /* Print Styles */
        @media print {{
            .nav-tabs, .skill-toggle {{
                display: none;
            }}
            
            .tab-content {{
                display: block !important;
            }}
            
            .skill-resources, .question-body {{
                display: block !important;
            }}
        }}
    </style>
</head>
<body>
    <div class="container">
        <div class="main-card">
            <!-- Header -->
            <div class="header">
                <div class="header-content">
                    <span class="badge">🎯 Full System Test Report</span>
                    <h1>Learning Path Analysis</h1>
                    <p class="subtitle">{final_summary.get('test_goal', 'Career Goal')}</p>
                    
                    <div class="occupation-match">
                        <span class="match-score">
                            🎯 {occupation.get('similarity_score', 0)*100:.1f}% Match
                        </span>
                        <span class="occupation-label">
                            📋 {occupation.get('label', 'N/A')}
                        </span>
                    </div>
                </div>
            </div>
            
            <!-- Stats Bar -->
            <div class="stats-bar">
                <div class="stat-item">
                    <div class="stat-icon">📚</div>
                    <div class="stat-value">{len(sessions)}</div>
                    <div class="stat-label">Sessions</div>
                </div>
                <div class="stat-item">
                    <div class="stat-icon">💡</div>
                    <div class="stat-value">{sum(len(s.get('skills', [])) for s in sessions)}</div>
                    <div class="stat-label">Skills</div>
                </div>
                <div class="stat-item">
                    <div class="stat-icon">❓</div>
                    <div class="stat-value">{len(questions)}</div>
                    <div class="stat-label">Quiz Questions</div>
                </div>
                <div class="stat-item">
                    <div class="stat-icon">🏆</div>
                    <div class="stat-value">{score_data.get('percentage', 0)}%</div>
                    <div class="stat-label">Quiz Score</div>
                </div>
                <div class="stat-item">
                    <div class="stat-icon">✅</div>
                    <div class="stat-value">{final_summary.get('success_rate', 0):.0f}%</div>
                    <div class="stat-label">Test Success</div>
                </div>
            </div>
            
            <!-- Navigation Tabs -->
            <div class="nav-tabs">
                <div class="nav-tab active" data-tab="learning-path">
                    <span class="tab-icon">📚</span> Learning Path
                </div>
                <div class="nav-tab" data-tab="quiz">
                    <span class="tab-icon">📝</span> Quiz & Analysis
                </div>
                <div class="nav-tab" data-tab="summary">
                    <span class="tab-icon">📊</span> Test Summary
                </div>
            </div>
            
            <!-- Learning Path Tab -->
            <div class="tab-content active" id="learning-path">
                <h2 class="section-title">
                    <span class="icon">🎓</span> Your Learning Journey
                </h2>
                
                {self._generate_sessions_html(sessions)}
            </div>
            
            <!-- Quiz Tab -->
            <div class="tab-content" id="quiz">
                {self._generate_quiz_html(questions, analysis, score_data)}
            </div>
            
            <!-- Summary Tab -->
            <div class="tab-content" id="summary">
                {self._generate_summary_html(final_summary)}
            </div>
            
            <!-- Footer -->
            <div class="footer">
                <p class="footer-text">
                    Generated by Hybrid GenMentor • Full System Integration Test • {datetime.now().strftime('%B %d, %Y at %I:%M %p')}
                </p>
            </div>
        </div>
    </div>
    
    <script>
        // Tab Navigation
        document.querySelectorAll('.nav-tab').forEach(tab => {{
            tab.addEventListener('click', () => {{
                // Remove active from all tabs and contents
                document.querySelectorAll('.nav-tab').forEach(t => t.classList.remove('active'));
                document.querySelectorAll('.tab-content').forEach(c => c.classList.remove('active'));
                
                // Add active to clicked tab and corresponding content
                tab.classList.add('active');
                const tabId = tab.getAttribute('data-tab');
                document.getElementById(tabId).classList.add('active');
            }});
        }});
        
        // Skill Resource Toggle
        document.querySelectorAll('.skill-toggle').forEach(btn => {{
            btn.addEventListener('click', () => {{
                const resources = btn.closest('.skill-item').querySelector('.skill-resources');
                resources.classList.toggle('show');
                btn.textContent = resources.classList.contains('show') ? 'Hide Resources' : 'View Resources';
            }});
        }});
        
        // Question Expand Toggle
        document.querySelectorAll('.question-header').forEach(header => {{
            header.addEventListener('click', () => {{
                const body = header.nextElementSibling;
                body.classList.toggle('show');
            }});
        }});
        
        // Animate progress bars on load
        document.addEventListener('DOMContentLoaded', () => {{
            document.querySelectorAll('.progress-bar').forEach(bar => {{
                const width = bar.style.width;
                bar.style.width = '0';
                setTimeout(() => {{ bar.style.width = width; }}, 100);
            }});
            
            document.querySelectorAll('.difficulty-fill').forEach(fill => {{
                const height = fill.style.height;
                fill.style.height = '0';
                setTimeout(() => {{ fill.style.height = height; }}, 100);
            }});
        }});
    </script>
</body>
</html>'''
        
        return html
    
    def _generate_sessions_html(self, sessions: List[Dict]) -> str:
        """Generate HTML for learning sessions."""
        html = ''
        
        for i, session in enumerate(sessions, 1):
            skills_html = self._generate_skills_html(session.get('skills', []))
            
            html += f'''
            <div class="session-card">
                <div class="session-header">
                    <div class="session-number">{i}</div>
                    <div class="session-info">
                        <div class="session-title">{session.get('title', f'Session {i}')}</div>
                        <div class="session-meta">{len(session.get('skills', []))} skills to master</div>
                    </div>
                    <div class="session-duration">⏱️ {session.get('duration', '2-3 hours')}</div>
                </div>
                <div class="session-body">
                    <p class="session-description">{session.get('description', '')}</p>
                    <div class="skills-grid">
                        {skills_html}
                    </div>
                </div>
            </div>
            '''
        
        return html
    
    def _generate_skills_html(self, skills: List[str]) -> str:
        """Generate HTML for skills with resource links."""
        html = ''
        
        for skill in skills:
            resources = self._get_skill_resources(skill)
            resources_html = ''
            
            for res in resources:
                if res.get('url'):
                    resources_html += f'''
                    <a href="{res.get('url', '#')}" target="_blank" class="resource-link">
                        <span class="resource-icon">{res.get('icon', '📖')}</span>
                        <div class="resource-info">
                            <div class="resource-title">{res.get('title', 'Resource')}</div>
                            <div class="resource-provider">{res.get('provider', '')} • {res.get('category', '')}</div>
                        </div>
                        <span class="resource-arrow">→</span>
                    </a>
                    '''
            
            html += f'''
            <div class="skill-item">
                <div class="skill-header">
                    <span class="skill-name">💡 {skill}</span>
                    <button class="skill-toggle">View Resources</button>
                </div>
                <div class="skill-resources">
                    <div class="resource-grid">
                        {resources_html}
                    </div>
                </div>
            </div>
            '''
        
        return html
    
    def _generate_quiz_html(self, questions: List[Dict], analysis: Dict, score_data: Dict) -> str:
        """Generate HTML for quiz and analysis section."""
        correct = score_data.get('correct', 0)
        total = score_data.get('total', 0)
        percentage = score_data.get('percentage', 0)
        grade = score_data.get('grade', 'N/A')
        
        difficulty_analysis = analysis.get('difficulty_analysis', {})
        easy = difficulty_analysis.get('easy', {})
        medium = difficulty_analysis.get('medium', {})
        hard = difficulty_analysis.get('hard', {})
        
        strengths = analysis.get('strengths', [])
        weaknesses = analysis.get('weaknesses', [])
        needs_improvement = analysis.get('needs_improvement', [])
        detailed_results = analysis.get('detailed_results', [])
        recommendations = analysis.get('recommendations', [])
        
        # Build results map
        results_map = {str(r.get('question_id', i)): r for i, r in enumerate(detailed_results)}
        
        html = f'''
        <h2 class="section-title">
            <span class="icon">📊</span> Quiz Performance Analysis
        </h2>
        
        <!-- Quiz Overview -->
        <div class="quiz-overview">
            <div class="quiz-stat-card primary">
                <div class="quiz-stat-icon">🎯</div>
                <div class="quiz-stat-value">{percentage}%</div>
                <div class="quiz-stat-label">Overall Score</div>
            </div>
            <div class="quiz-stat-card success">
                <div class="quiz-stat-icon">✅</div>
                <div class="quiz-stat-value">{correct}/{total}</div>
                <div class="quiz-stat-label">Correct Answers</div>
            </div>
            <div class="quiz-stat-card">
                <div class="quiz-stat-icon">🏅</div>
                <div class="quiz-stat-value">{grade}</div>
                <div class="quiz-stat-label">Grade</div>
            </div>
            <div class="quiz-stat-card">
                <div class="quiz-stat-icon">📈</div>
                <div class="quiz-stat-value">{analysis.get('performance_level', 'N/A')}</div>
                <div class="quiz-stat-label">Performance Level</div>
            </div>
        </div>
        
        <!-- Progress Bar -->
        <div style="margin-bottom: 40px;">
            <div style="display: flex; justify-content: space-between; margin-bottom: 10px;">
                <span style="font-weight: 600;">Progress</span>
                <span style="color: var(--success); font-weight: 700;">{correct} of {total} correct</span>
            </div>
            <div class="progress-container">
                <div class="progress-bar" style="width: {percentage}%;"></div>
            </div>
        </div>
        
        <!-- Analysis Grid -->
        <div class="analysis-grid">
            <!-- Difficulty Breakdown -->
            <div class="analysis-card">
                <h3>📊 Difficulty Breakdown</h3>
                <div class="difficulty-chart">
                    <div class="difficulty-item">
                        <div class="difficulty-bar">
                            <div class="difficulty-fill" style="height: {easy.get('percentage', 0)}%; background: linear-gradient(to top, #10b981, #34d399);"></div>
                        </div>
                        <div class="difficulty-label">Easy</div>
                        <div class="difficulty-score">{easy.get('correct', 0)}/{easy.get('total', 0)}</div>
                    </div>
                    <div class="difficulty-item">
                        <div class="difficulty-bar">
                            <div class="difficulty-fill" style="height: {medium.get('percentage', 0)}%; background: linear-gradient(to top, #f59e0b, #fbbf24);"></div>
                        </div>
                        <div class="difficulty-label">Medium</div>
                        <div class="difficulty-score">{medium.get('correct', 0)}/{medium.get('total', 0)}</div>
                    </div>
                    <div class="difficulty-item">
                        <div class="difficulty-bar">
                            <div class="difficulty-fill" style="height: {hard.get('percentage', 0)}%; background: linear-gradient(to top, #ef4444, #f87171);"></div>
                        </div>
                        <div class="difficulty-label">Hard</div>
                        <div class="difficulty-score">{hard.get('correct', 0)}/{hard.get('total', 0)}</div>
                    </div>
                </div>
            </div>
            
            <!-- Strengths -->
            <div class="analysis-card">
                <h3>💪 Strengths</h3>
                {"".join(f'<div class="strength-item"><span class="topic-name">{s.get("topic", "Topic")}</span><span class="topic-score">{s.get("accuracy", 0)}%</span></div>' for s in strengths) if strengths else '<p style="color: var(--gray);">Complete more questions to see your strengths.</p>'}
            </div>
            
            <!-- Areas to Improve -->
            <div class="analysis-card">
                <h3>📈 Areas to Improve</h3>
                {"".join(f'<div class="weakness-item"><span class="topic-name">{w.get("topic", "Topic")}</span><span class="topic-score">{w.get("accuracy", 0)}%</span></div>' for w in (needs_improvement + weaknesses)[:5]) if (needs_improvement or weaknesses) else '<p style="color: var(--gray);">Great job! No major weaknesses detected.</p>'}
            </div>
            
            <!-- Recommendations -->
            <div class="analysis-card">
                <h3>💡 Recommendations</h3>
                <ul style="padding-left: 20px; color: var(--gray);">
                    {"".join(f'<li style="margin-bottom: 8px;">{rec}</li>' for rec in recommendations[:5]) if recommendations else '<li>Keep practicing to improve your skills!</li>'}
                </ul>
            </div>
        </div>
        
        <!-- Questions Section -->
        <h3 class="section-title" style="margin-top: 40px;">
            <span class="icon">❓</span> Question Details
        </h3>
        <p style="color: var(--gray); margin-bottom: 20px;">Click on any question to expand and see the details.</p>
        '''
        
        # Add individual questions
        for i, q in enumerate(questions):
            if not isinstance(q, dict):
                continue
            
            result = results_map.get(str(i), {})
            is_correct = result.get('is_correct', False)
            user_answer = result.get('user_answer', '')
            correct_answer = q.get('correct_answer', '')
            difficulty = q.get('difficulty', 'medium')
            topic = q.get('topic', 'General')
            
            options = q.get('options', {})
            options_html = ''
            
            if isinstance(options, dict):
                for key, value in options.items():
                    option_class = ''
                    if key == correct_answer:
                        option_class = 'correct-answer'
                    elif key == user_answer and not is_correct:
                        option_class = 'user-wrong'
                    
                    options_html += f'''
                    <li class="option-item {option_class}">
                        <span class="option-key">{key}</span>
                        <span>{value}</span>
                    </li>
                    '''
            
            explanation = q.get('explanation', '')
            explanation_html = f'''
            <div class="explanation">
                <div class="explanation-title">💡 Explanation</div>
                <p>{explanation}</p>
            </div>
            ''' if explanation else ''
            
            html += f'''
            <div class="question-card {'correct' if is_correct else 'incorrect'}">
                <div class="question-header">
                    <span class="question-number">Question {i + 1}</span>
                    <div class="question-meta">
                        <span class="topic-badge" style="background: var(--light); padding: 4px 12px; border-radius: 15px; font-size: 0.85em;">{topic}</span>
                        <span class="difficulty-badge {difficulty}">{difficulty.capitalize()}</span>
                        <span class="result-badge {'correct' if is_correct else 'incorrect'}">{'✓' if is_correct else '✗'}</span>
                    </div>
                </div>
                <div class="question-body">
                    <div class="question-text">{q.get('question', '')}</div>
                    <ul class="options-list">
                        {options_html}
                    </ul>
                    {explanation_html}
                </div>
            </div>
            '''
        
        return html
    
    def _generate_summary_html(self, final_summary: Dict) -> str:
        """Generate HTML for test summary section."""
        results = final_summary.get('results', [])
        
        # Fix feedback statistics to show session votes, not database totals
        community_voting = self.data.get('community_voting') or []
        session_votes = len([v for v in community_voting if v.get('status') == 'success'])
        
        results_html = ''
        for r in results:
            # Fix the feedback statistics detail to show session votes
            feature = r.get('feature', '')
            detail = r.get('detail', '')
            
            if 'Feedback Statistics' in feature and 'total votes' in detail:
                # Replace misleading database totals with session votes
                detail = f"{session_votes} votes submitted (this session)"
            
            status_class = 'success' if r.get('status') == '✅' else 'warning' if r.get('status') == '⚠️' else 'danger'
            results_html += f'''
            <div class="summary-card" style="border-left: 4px solid var(--{status_class});">
                <div class="summary-icon">{r.get('status', '✅')}</div>
                <div class="summary-value">{feature}</div>
                <div class="summary-label">{detail}</div>
            </div>
            '''
        
        duration = final_summary.get('test_duration_seconds', 0)
        
        return f'''
        <h2 class="section-title">
            <span class="icon">📊</span> Test Execution Summary
        </h2>
        
        <!-- Summary Stats -->
        <div class="quiz-overview" style="margin-bottom: 40px;">
            <div class="quiz-stat-card primary">
                <div class="quiz-stat-icon">🎯</div>
                <div class="quiz-stat-value">{final_summary.get('success_rate', 0):.0f}%</div>
                <div class="quiz-stat-label">Success Rate</div>
            </div>
            <div class="quiz-stat-card success">
                <div class="quiz-stat-icon">✅</div>
                <div class="quiz-stat-value">{final_summary.get('features_passed', 0)}/{final_summary.get('features_tested', 0)}</div>
                <div class="quiz-stat-label">Features Passed</div>
            </div>
            <div class="quiz-stat-card">
                <div class="quiz-stat-icon">⏱️</div>
                <div class="quiz-stat-value">{duration:.1f}s</div>
                <div class="quiz-stat-label">Duration</div>
            </div>
            <div class="quiz-stat-card">
                <div class="quiz-stat-icon">👤</div>
                <div class="quiz-stat-value" style="font-size: 1.2em;">{final_summary.get('test_user', 'N/A')}</div>
                <div class="quiz-stat-label">Test User</div>
            </div>
        </div>
        
        <h3 class="section-title" style="font-size: 1.4em;">
            <span class="icon">🔍</span> Feature Test Results
        </h3>
        
        <div class="summary-grid">
            {results_html}
        </div>
        
        <div style="margin-top: 40px; padding: 25px; background: var(--light); border-radius: 12px;">
            <h4 style="margin-bottom: 15px; color: var(--dark);">📁 Output Files Generated</h4>
            <div style="display: flex; flex-wrap: wrap; gap: 10px;">
                {"".join(f'<span style="background: white; padding: 8px 15px; border-radius: 8px; font-size: 0.9em; border: 1px solid var(--border);">📄 {f}</span>' for f in final_summary.get('output_files', []))}
            </div>
        </div>
        '''
    
    def save_html(self, filename: str = 'test_report.html'):
        """Save the HTML report to a file."""
        html = self.generate_html()
        filepath = os.path.join(self.output_dir, filename)
        
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(html)
        
        print(f"✅ HTML report saved to: {filepath}")
        return filepath


def generate_test_report(output_dir: str) -> str:
    """Generate HTML report from test output directory."""
    generator = TestOutputHTMLGenerator(output_dir)
    return generator.save_html()


if __name__ == "__main__":
    import sys
    
    if len(sys.argv) > 1:
        output_dir = sys.argv[1]
    else:
        # Find the most recent test output directory
        import glob
        dirs = glob.glob("test_outputs_*")
        if dirs:
            output_dir = sorted(dirs)[-1]
        else:
            print("No test output directory found. Run full_system_test.py first.")
            sys.exit(1)
    
    print(f"\n{'='*60}")
    print(" GENERATING TEST OUTPUT HTML REPORT")
    print(f"{'='*60}")
    print(f"Source: {output_dir}")
    
    filepath = generate_test_report(output_dir)
    
    print(f"\n{'='*60}")
    print(f" Report generated: {filepath}")
    print(f"{'='*60}\n")
