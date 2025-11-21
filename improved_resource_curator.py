"""
Improved Resource Curator with High-Quality Curated Resources
Provides actual educational content (not just search results) similar to roadmap.sh
"""

import asyncio
import aiohttp
from typing import List, Dict, Optional
import time
from datetime import datetime, timedelta
import hashlib
import json


class ImprovedResourceCurator:
    """
    Enhanced resource curator with curated, high-quality learning resources.
    Focuses on credible sources like official docs, structured courses, and verified channels.
    """
    
    def __init__(self, cache_backend='sqlite'):
        """Initialize improved resource curator."""
        self.cache_backend = cache_backend
        self.memory_cache = {}
        
        if cache_backend == 'sqlite':
            from database_optimizer import get_optimized_db
            self.db = get_optimized_db()
        
        # Curated learning resource database (similar to roadmap.sh approach)
        self.curated_resources = self._load_curated_resources()
        
        print(f"✅ Improved Resource Curator initialized with {len(self.curated_resources)} curated mappings")
    
    def _load_curated_resources(self) -> Dict[str, Dict]:
        """
        Load curated, high-quality resources for common skills.
        Structure similar to roadmap.sh's approach.
        """
        return {
            'python': {
                'official_docs': [
                    {
                        'title': 'Official Python Tutorial',
                        'url': 'https://docs.python.org/3/tutorial/',
                        'type': 'documentation',
                        'provider': 'Python.org',
                        'description': 'Official Python documentation and tutorial',
                        'is_free': True,
                        'quality_score': 1.0
                    }
                ],
                'courses': [
                    {
                        'title': 'Python for Everybody Specialization',
                        'url': 'https://www.coursera.org/specializations/python',
                        'type': 'course',
                        'provider': 'Coursera',
                        'description': 'University of Michigan\'s comprehensive Python course',
                        'is_free': True,
                        'quality_score': 0.95
                    },
                    {
                        'title': 'Complete Python Bootcamp',
                        'url': 'https://www.udemy.com/course/complete-python-bootcamp/',
                        'type': 'course',
                        'provider': 'Udemy',
                        'description': 'From zero to hero in Python',
                        'is_free': False,
                        'quality_score': 0.9
                    }
                ],
                'videos': [
                    {
                        'title': 'Python Tutorial for Beginners',
                        'url': 'https://www.youtube.com/watch?v=_uQrJ0TkZlc',
                        'type': 'video',
                        'provider': 'YouTube',
                        'channel': 'Programming with Mosh',
                        'description': 'Complete Python tutorial (6+ hours)',
                        'is_free': True,
                        'quality_score': 0.95
                    },
                    {
                        'title': 'Python Full Course - freeCodeCamp',
                        'url': 'https://www.youtube.com/watch?v=rfscVS0vtbw',
                        'type': 'video',
                        'provider': 'YouTube',
                        'channel': 'freeCodeCamp.org',
                        'description': 'Complete Python course for beginners (4.5 hours)',
                        'is_free': True,
                        'quality_score': 0.98
                    }
                ],
                'practice': [
                    {
                        'title': 'Python Exercises - W3Schools',
                        'url': 'https://www.w3schools.com/python/python_exercises.asp',
                        'type': 'practice',
                        'provider': 'W3Schools',
                        'description': 'Interactive Python exercises',
                        'is_free': True,
                        'quality_score': 0.85
                    }
                ]
            },
            'javascript': {
                'official_docs': [
                    {
                        'title': 'MDN JavaScript Guide',
                        'url': 'https://developer.mozilla.org/en-US/docs/Web/JavaScript/Guide',
                        'type': 'documentation',
                        'provider': 'MDN',
                        'description': 'Comprehensive JavaScript documentation by Mozilla',
                        'is_free': True,
                        'quality_score': 1.0
                    }
                ],
                'courses': [
                    {
                        'title': 'JavaScript Algorithms and Data Structures',
                        'url': 'https://www.freecodecamp.org/learn/javascript-algorithms-and-data-structures/',
                        'type': 'course',
                        'provider': 'freeCodeCamp',
                        'description': 'Complete JavaScript course with certification',
                        'is_free': True,
                        'quality_score': 0.95
                    }
                ],
                'videos': [
                    {
                        'title': 'JavaScript Tutorial for Beginners',
                        'url': 'https://www.youtube.com/watch?v=W6NZfCO5SIk',
                        'type': 'video',
                        'provider': 'YouTube',
                        'channel': 'Programming with Mosh',
                        'description': 'Complete JavaScript tutorial (1 hour)',
                        'is_free': True,
                        'quality_score': 0.95
                    }
                ]
            },
            'react': {
                'official_docs': [
                    {
                        'title': 'React Official Documentation',
                        'url': 'https://react.dev/learn',
                        'type': 'documentation',
                        'provider': 'React.dev',
                        'description': 'Official React documentation and tutorial',
                        'is_free': True,
                        'quality_score': 1.0
                    }
                ],
                'courses': [
                    {
                        'title': 'React - The Complete Guide',
                        'url': 'https://www.udemy.com/course/react-the-complete-guide-incl-redux/',
                        'type': 'course',
                        'provider': 'Udemy',
                        'description': 'Comprehensive React course by Maximilian Schwarzmüller',
                        'is_free': False,
                        'quality_score': 0.95
                    }
                ],
                'videos': [
                    {
                        'title': 'React Course - Beginner\'s Tutorial for React',
                        'url': 'https://www.youtube.com/watch?v=bMknfKXIFA8',
                        'type': 'video',
                        'provider': 'YouTube',
                        'channel': 'freeCodeCamp.org',
                        'description': 'Complete React tutorial (12 hours)',
                        'is_free': True,
                        'quality_score': 0.98
                    }
                ]
            },
            'html': {
                'official_docs': [
                    {
                        'title': 'MDN HTML Guide',
                        'url': 'https://developer.mozilla.org/en-US/docs/Web/HTML',
                        'type': 'documentation',
                        'provider': 'MDN',
                        'description': 'Complete HTML documentation and guides',
                        'is_free': True,
                        'quality_score': 1.0
                    }
                ],
                'courses': [
                    {
                        'title': 'Responsive Web Design',
                        'url': 'https://www.freecodecamp.org/learn/2022/responsive-web-design/',
                        'type': 'course',
                        'provider': 'freeCodeCamp',
                        'description': 'Complete HTML/CSS course with certification',
                        'is_free': True,
                        'quality_score': 0.95
                    }
                ],
                'videos': [
                    {
                        'title': 'HTML Full Course - Build a Website Tutorial',
                        'url': 'https://www.youtube.com/watch?v=pQN-pnXPaVg',
                        'type': 'video',
                        'provider': 'YouTube',
                        'channel': 'freeCodeCamp.org',
                        'description': 'Complete HTML tutorial (2 hours)',
                        'is_free': True,
                        'quality_score': 0.95
                    }
                ]
            },
            'css': {
                'official_docs': [
                    {
                        'title': 'MDN CSS Guide',
                        'url': 'https://developer.mozilla.org/en-US/docs/Web/CSS',
                        'type': 'documentation',
                        'provider': 'MDN',
                        'description': 'Complete CSS documentation and guides',
                        'is_free': True,
                        'quality_score': 1.0
                    }
                ],
                'videos': [
                    {
                        'title': 'CSS Tutorial - Zero to Hero',
                        'url': 'https://www.youtube.com/watch?v=1Rs2ND1ryYc',
                        'type': 'video',
                        'provider': 'YouTube',
                        'channel': 'freeCodeCamp.org',
                        'description': 'Complete CSS course (11 hours)',
                        'is_free': True,
                        'quality_score': 0.95
                    }
                ]
            },
            'sql': {
                'official_docs': [
                    {
                        'title': 'PostgreSQL Documentation',
                        'url': 'https://www.postgresql.org/docs/',
                        'type': 'documentation',
                        'provider': 'PostgreSQL',
                        'description': 'Official PostgreSQL documentation',
                        'is_free': True,
                        'quality_score': 1.0
                    }
                ],
                'courses': [
                    {
                        'title': 'Complete SQL Course',
                        'url': 'https://roadmap.sh/courses/sql',
                        'type': 'course',
                        'provider': 'roadmap.sh',
                        'description': 'Comprehensive SQL course from beginner to advanced',
                        'is_free': False,
                        'quality_score': 0.95
                    }
                ],
                'videos': [
                    {
                        'title': 'SQL Tutorial - Full Database Course for Beginners',
                        'url': 'https://www.youtube.com/watch?v=HXV3zeQKqGY',
                        'type': 'video',
                        'provider': 'YouTube',
                        'channel': 'freeCodeCamp.org',
                        'description': 'Complete SQL course (4 hours)',
                        'is_free': True,
                        'quality_score': 0.98
                    }
                ],
                'practice': [
                    {
                        'title': 'SQLBolt',
                        'url': 'https://sqlbolt.com/',
                        'type': 'practice',
                        'provider': 'SQLBolt',
                        'description': 'Interactive SQL exercises',
                        'is_free': True,
                        'quality_score': 0.9
                    }
                ]
            },
            'machine learning': {
                'courses': [
                    {
                        'title': 'Machine Learning by Andrew Ng',
                        'url': 'https://www.coursera.org/specializations/machine-learning-introduction',
                        'type': 'course',
                        'provider': 'Coursera',
                        'description': 'Stanford\'s legendary ML course',
                        'is_free': True,
                        'quality_score': 1.0
                    },
                    {
                        'title': 'Practical Deep Learning for Coders',
                        'url': 'https://course.fast.ai/',
                        'type': 'course',
                        'provider': 'Fast.ai',
                        'description': 'Hands-on deep learning course',
                        'is_free': True,
                        'quality_score': 0.95
                    }
                ],
                'videos': [
                    {
                        'title': 'Machine Learning Course - freeCodeCamp',
                        'url': 'https://www.youtube.com/watch?v=NWONeJKn6kc',
                        'type': 'video',
                        'provider': 'YouTube',
                        'channel': 'freeCodeCamp.org',
                        'description': 'Complete ML tutorial with Python (10 hours)',
                        'is_free': True,
                        'quality_score': 0.95
                    }
                ]
            },
            'git': {
                'official_docs': [
                    {
                        'title': 'Pro Git Book',
                        'url': 'https://git-scm.com/book/en/v2',
                        'type': 'documentation',
                        'provider': 'Git',
                        'description': 'Official Git documentation and book',
                        'is_free': True,
                        'quality_score': 1.0
                    }
                ],
                'courses': [
                    {
                        'title': 'Git and GitHub Course',
                        'url': 'https://roadmap.sh/git-github',
                        'type': 'course',
                        'provider': 'roadmap.sh',
                        'description': 'Complete Git and GitHub guide',
                        'is_free': True,
                        'quality_score': 0.95
                    }
                ],
                'videos': [
                    {
                        'title': 'Git and GitHub for Beginners',
                        'url': 'https://www.youtube.com/watch?v=RGOj5yH7evk',
                        'type': 'video',
                        'provider': 'YouTube',
                        'channel': 'freeCodeCamp.org',
                        'description': 'Complete Git tutorial (1 hour)',
                        'is_free': True,
                        'quality_score': 0.95
                    }
                ]
            },
            'docker': {
                'official_docs': [
                    {
                        'title': 'Docker Documentation',
                        'url': 'https://docs.docker.com/',
                        'type': 'documentation',
                        'provider': 'Docker',
                        'description': 'Official Docker documentation',
                        'is_free': True,
                        'quality_score': 1.0
                    }
                ],
                'courses': [
                    {
                        'title': 'Docker Roadmap',
                        'url': 'https://roadmap.sh/docker',
                        'type': 'course',
                        'provider': 'roadmap.sh',
                        'description': 'Complete Docker learning path',
                        'is_free': True,
                        'quality_score': 0.95
                    }
                ],
                'videos': [
                    {
                        'title': 'Docker Tutorial for Beginners',
                        'url': 'https://www.youtube.com/watch?v=fqMOX6JJhGo',
                        'type': 'video',
                        'provider': 'YouTube',
                        'channel': 'freeCodeCamp.org',
                        'description': 'Complete Docker course (3 hours)',
                        'is_free': True,
                        'quality_score': 0.95
                    }
                ]
            },
            'java': {
                'official_docs': [
                    {'title': 'Java Documentation', 'url': 'https://docs.oracle.com/en/java/', 'type': 'documentation', 'provider': 'Oracle', 'is_free': True, 'quality_score': 1.0}
                ],
                'courses': [
                    {'title': 'Java Programming Masterclass', 'url': 'https://www.udemy.com/course/java-the-complete-java-developer-course/', 'type': 'course', 'provider': 'Udemy', 'is_free': False, 'quality_score': 0.92}
                ],
                'videos': [
                    {'title': 'Java Tutorial for Beginners', 'url': 'https://www.youtube.com/watch?v=eIrMbAQSU34', 'type': 'video', 'provider': 'YouTube', 'is_free': True, 'quality_score': 0.90}
                ]
            },
            'typescript': {
                'official_docs': [
                    {'title': 'TypeScript Handbook', 'url': 'https://www.typescriptlang.org/docs/', 'type': 'documentation', 'provider': 'TypeScript', 'is_free': True, 'quality_score': 1.0}
                ],
                'videos': [
                    {'title': 'TypeScript Course for Beginners', 'url': 'https://www.youtube.com/watch?v=BwuLxPH8IDs', 'type': 'video', 'provider': 'YouTube', 'is_free': True, 'quality_score': 0.92}
                ]
            },
            'nodejs': {
                'official_docs': [
                    {'title': 'Node.js Documentation', 'url': 'https://nodejs.org/docs/latest/api/', 'type': 'documentation', 'provider': 'Node.js', 'is_free': True, 'quality_score': 1.0}
                ],
                'courses': [
                    {'title': 'The Complete Node.js Course', 'url': 'https://www.udemy.com/course/the-complete-nodejs-developer-course-2/', 'type': 'course', 'provider': 'Udemy', 'is_free': False, 'quality_score': 0.94}
                ],
                'videos': [
                    {'title': 'Node.js Tutorial for Beginners', 'url': 'https://www.youtube.com/watch?v=TlB_eWDSMt4', 'type': 'video', 'provider': 'YouTube', 'is_free': True, 'quality_score': 0.91}
                ]
            },
            'data_science': {
                'courses': [
                    {'title': 'Data Science Specialization', 'url': 'https://www.coursera.org/specializations/jhu-data-science', 'type': 'course', 'provider': 'Coursera', 'is_free': True, 'quality_score': 0.96}
                ],
                'videos': [
                    {'title': 'Data Science Full Course', 'url': 'https://www.youtube.com/watch?v=ua-CiDNNj30', 'type': 'video', 'provider': 'YouTube', 'is_free': True, 'quality_score': 0.89}
                ]
            },
            'pandas': {
                'official_docs': [
                    {'title': 'Pandas Documentation', 'url': 'https://pandas.pydata.org/docs/', 'type': 'documentation', 'provider': 'Pandas', 'is_free': True, 'quality_score': 1.0}
                ],
                'videos': [
                    {'title': 'Pandas Tutorial', 'url': 'https://www.youtube.com/watch?v=vmEHCJofslg', 'type': 'video', 'provider': 'YouTube', 'is_free': True, 'quality_score': 0.90}
                ]
            },
            'numpy': {
                'official_docs': [
                    {'title': 'NumPy Documentation', 'url': 'https://numpy.org/doc/', 'type': 'documentation', 'provider': 'NumPy', 'is_free': True, 'quality_score': 1.0}
                ],
                'videos': [
                    {'title': 'NumPy Tutorial', 'url': 'https://www.youtube.com/watch?v=QUT1VHiLmmI', 'type': 'video', 'provider': 'YouTube', 'is_free': True, 'quality_score': 0.88}
                ]
            },
            'aws': {
                'official_docs': [
                    {'title': 'AWS Documentation', 'url': 'https://docs.aws.amazon.com/', 'type': 'documentation', 'provider': 'AWS', 'is_free': True, 'quality_score': 1.0}
                ],
                'courses': [
                    {'title': 'AWS Certified Solutions Architect', 'url': 'https://www.udemy.com/course/aws-certified-solutions-architect-associate-saa-c03/', 'type': 'course', 'provider': 'Udemy', 'is_free': False, 'quality_score': 0.95}
                ],
                'videos': [
                    {'title': 'AWS Tutorial for Beginners', 'url': 'https://www.youtube.com/watch?v=ulprqHHWlng', 'type': 'video', 'provider': 'YouTube', 'is_free': True, 'quality_score': 0.92}
                ]
            },
            'azure': {
                'official_docs': [
                    {'title': 'Azure Documentation', 'url': 'https://learn.microsoft.com/en-us/azure/', 'type': 'documentation', 'provider': 'Microsoft', 'is_free': True, 'quality_score': 1.0}
                ],
                'videos': [
                    {'title': 'Azure Full Course', 'url': 'https://www.youtube.com/watch?v=10PbGbTUSAg', 'type': 'video', 'provider': 'YouTube', 'is_free': True, 'quality_score': 0.89}
                ]
            },
            'kubernetes': {
                'official_docs': [
                    {'title': 'Kubernetes Documentation', 'url': 'https://kubernetes.io/docs/', 'type': 'documentation', 'provider': 'Kubernetes', 'is_free': True, 'quality_score': 1.0}
                ],
                'videos': [
                    {'title': 'Kubernetes Tutorial for Beginners', 'url': 'https://www.youtube.com/watch?v=X48VuDVv0do', 'type': 'video', 'provider': 'YouTube', 'is_free': True, 'quality_score': 0.93}
                ]
            },
            'testing': {
                'videos': [
                    {'title': 'Software Testing Tutorial', 'url': 'https://www.youtube.com/watch?v=sB_5fqiysi4', 'type': 'video', 'provider': 'YouTube', 'is_free': True, 'quality_score': 0.85}
                ]
            },
            'api': {
                'videos': [
                    {'title': 'APIs for Beginners', 'url': 'https://www.youtube.com/watch?v=GZvSYJDk-us', 'type': 'video', 'provider': 'YouTube', 'is_free': True, 'quality_score': 0.91}
                ],
                'practice': [
                    {'title': 'Postman Learning Center', 'url': 'https://learning.postman.com/', 'type': 'practice', 'provider': 'Postman', 'is_free': True, 'quality_score': 0.88}
                ]
            },
            'database': {
                'courses': [
                    {'title': 'Database Design', 'url': 'https://www.coursera.org/learn/database-design', 'type': 'course', 'provider': 'Coursera', 'is_free': True, 'quality_score': 0.90}
                ],
                'videos': [
                    {'title': 'Database Design Course', 'url': 'https://www.youtube.com/watch?v=ztHopE5Wnpc', 'type': 'video', 'provider': 'YouTube', 'is_free': True, 'quality_score': 0.87}
                ]
            },
            'algorithms': {
                'courses': [
                    {'title': 'Algorithms Specialization', 'url': 'https://www.coursera.org/specializations/algorithms', 'type': 'course', 'provider': 'Coursera', 'is_free': True, 'quality_score': 0.97}
                ],
                'videos': [
                    {'title': 'Algorithms Course', 'url': 'https://www.youtube.com/watch?v=8hly31xKli0', 'type': 'video', 'provider': 'YouTube', 'is_free': True, 'quality_score': 0.90}
                ],
                'practice': [
                    {'title': 'LeetCode', 'url': 'https://leetcode.com/', 'type': 'practice', 'provider': 'LeetCode', 'is_free': True, 'quality_score': 0.95}
                ]
            },
            'data_structures': {
                'videos': [
                    {'title': 'Data Structures Full Course', 'url': 'https://www.youtube.com/watch?v=RBSGKlAvoiM', 'type': 'video', 'provider': 'YouTube', 'is_free': True, 'quality_score': 0.91}
                ],
                'practice': [
                    {'title': 'HackerRank Data Structures', 'url': 'https://www.hackerrank.com/domains/data-structures', 'type': 'practice', 'provider': 'HackerRank', 'is_free': True, 'quality_score': 0.88}
                ]
            },
            'linux': {
                'videos': [
                    {'title': 'Linux for Beginners', 'url': 'https://www.youtube.com/watch?v=ROjZy1WbCIA', 'type': 'video', 'provider': 'YouTube', 'is_free': True, 'quality_score': 0.89}
                ],
                'practice': [
                    {'title': 'Linux Journey', 'url': 'https://linuxjourney.com/', 'type': 'practice', 'provider': 'Linux Journey', 'is_free': True, 'quality_score': 0.92}
                ]
            },
            'security': {
                'courses': [
                    {'title': 'Cybersecurity Specialization', 'url': 'https://www.coursera.org/specializations/cyber-security', 'type': 'course', 'provider': 'Coursera', 'is_free': True, 'quality_score': 0.93}
                ],
                'videos': [
                    {'title': 'Cybersecurity Full Course', 'url': 'https://www.youtube.com/watch?v=U_P23SqJaDc', 'type': 'video', 'provider': 'YouTube', 'is_free': True, 'quality_score': 0.86}
                ]
            },
            'networking': {
                'videos': [
                    {'title': 'Computer Networking Course', 'url': 'https://www.youtube.com/watch?v=qiQR5rTSshw', 'type': 'video', 'provider': 'YouTube', 'is_free': True, 'quality_score': 0.90}
                ]
            },
            'devops': {
                'courses': [
                    {'title': 'DevOps Specialization', 'url': 'https://www.coursera.org/specializations/devops', 'type': 'course', 'provider': 'Coursera', 'is_free': True, 'quality_score': 0.91}
                ],
                'videos': [
                    {'title': 'DevOps Tutorial', 'url': 'https://www.youtube.com/watch?v=Xrgk023l4lI', 'type': 'video', 'provider': 'YouTube', 'is_free': True, 'quality_score': 0.88}
                ]
            },
            'mobile': {
                'videos': [
                    {'title': 'Mobile App Development', 'url': 'https://www.youtube.com/watch?v=fis26HvvDII', 'type': 'video', 'provider': 'YouTube', 'is_free': True, 'quality_score': 0.85}
                ]
            },
            'agile': {
                'courses': [
                    {'title': 'Agile Development Specialization', 'url': 'https://www.coursera.org/specializations/agile-development', 'type': 'course', 'provider': 'Coursera', 'is_free': True, 'quality_score': 0.89}
                ]
            },
            # Frontend Frameworks
            'angular': {
                'official_docs': [
                    {'title': 'Angular Official Documentation', 'url': 'https://angular.io/docs', 'type': 'documentation', 'provider': 'Angular', 'is_free': True, 'quality_score': 0.98}
                ],
                'videos': [
                    {'title': 'Angular Full Course', 'url': 'https://www.youtube.com/watch?v=3qBXWUpoPHo', 'type': 'video', 'provider': 'YouTube', 'is_free': True, 'quality_score': 0.89}
                ]
            },
            'vue': {
                'official_docs': [
                    {'title': 'Vue.js Official Documentation', 'url': 'https://vuejs.org/guide/', 'type': 'documentation', 'provider': 'Vue.js', 'is_free': True, 'quality_score': 0.98}
                ],
                'videos': [
                    {'title': 'Vue.js Course', 'url': 'https://www.youtube.com/watch?v=FXpIoQ_rT_c', 'type': 'video', 'provider': 'YouTube', 'is_free': True, 'quality_score': 0.90}
                ]
            },
            'svelte': {
                'official_docs': [
                    {'title': 'Svelte Official Tutorial', 'url': 'https://svelte.dev/tutorial', 'type': 'documentation', 'provider': 'Svelte', 'is_free': True, 'quality_score': 0.97}
                ]
            },
            # Backend Frameworks
            'django': {
                'official_docs': [
                    {'title': 'Django Official Documentation', 'url': 'https://docs.djangoproject.com/', 'type': 'documentation', 'provider': 'Django', 'is_free': True, 'quality_score': 0.98}
                ],
                'videos': [
                    {'title': 'Django Tutorial', 'url': 'https://www.youtube.com/watch?v=F5mRW0jo-U4', 'type': 'video', 'provider': 'YouTube', 'is_free': True, 'quality_score': 0.91}
                ]
            },
            'flask': {
                'official_docs': [
                    {'title': 'Flask Official Documentation', 'url': 'https://flask.palletsprojects.com/', 'type': 'documentation', 'provider': 'Flask', 'is_free': True, 'quality_score': 0.97}
                ],
                'videos': [
                    {'title': 'Flask Tutorial', 'url': 'https://www.youtube.com/watch?v=Z1RJmh_OqeA', 'type': 'video', 'provider': 'YouTube', 'is_free': True, 'quality_score': 0.88}
                ]
            },
            'fastapi': {
                'official_docs': [
                    {'title': 'FastAPI Official Documentation', 'url': 'https://fastapi.tiangolo.com/', 'type': 'documentation', 'provider': 'FastAPI', 'is_free': True, 'quality_score': 0.98}
                ]
            },
            'express': {
                'official_docs': [
                    {'title': 'Express.js Documentation', 'url': 'https://expressjs.com/', 'type': 'documentation', 'provider': 'Express', 'is_free': True, 'quality_score': 0.96}
                ]
            },
            'spring': {
                'official_docs': [
                    {'title': 'Spring Framework Documentation', 'url': 'https://spring.io/guides', 'type': 'documentation', 'provider': 'Spring', 'is_free': True, 'quality_score': 0.97}
                ],
                'videos': [
                    {'title': 'Spring Boot Tutorial', 'url': 'https://www.youtube.com/watch?v=vtPkZShrvXQ', 'type': 'video', 'provider': 'YouTube', 'is_free': True, 'quality_score': 0.89}
                ]
            },
            # Mobile Development
            'react_native': {
                'official_docs': [
                    {'title': 'React Native Documentation', 'url': 'https://reactnative.dev/docs/getting-started', 'type': 'documentation', 'provider': 'React Native', 'is_free': True, 'quality_score': 0.97}
                ],
                'videos': [
                    {'title': 'React Native Tutorial', 'url': 'https://www.youtube.com/watch?v=0-S5a0eXPoc', 'type': 'video', 'provider': 'YouTube', 'is_free': True, 'quality_score': 0.91}
                ]
            },
            'flutter': {
                'official_docs': [
                    {'title': 'Flutter Official Documentation', 'url': 'https://docs.flutter.dev/', 'type': 'documentation', 'provider': 'Flutter', 'is_free': True, 'quality_score': 0.98}
                ],
                'videos': [
                    {'title': 'Flutter Course', 'url': 'https://www.youtube.com/watch?v=VPvVD8t02U8', 'type': 'video', 'provider': 'YouTube', 'is_free': True, 'quality_score': 0.92}
                ]
            },
            'swift': {
                'official_docs': [
                    {'title': 'Swift Official Documentation', 'url': 'https://swift.org/documentation/', 'type': 'documentation', 'provider': 'Swift', 'is_free': True, 'quality_score': 0.97}
                ],
                'videos': [
                    {'title': 'Swift Programming Tutorial', 'url': 'https://www.youtube.com/watch?v=8Xg7E9shq0U', 'type': 'video', 'provider': 'YouTube', 'is_free': True, 'quality_score': 0.90}
                ]
            },
            'kotlin': {
                'official_docs': [
                    {'title': 'Kotlin Official Documentation', 'url': 'https://kotlinlang.org/docs/home.html', 'type': 'documentation', 'provider': 'Kotlin', 'is_free': True, 'quality_score': 0.97}
                ],
                'videos': [
                    {'title': 'Kotlin Course', 'url': 'https://www.youtube.com/watch?v=F9UC9DY-vIU', 'type': 'video', 'provider': 'YouTube', 'is_free': True, 'quality_score': 0.88}
                ]
            },
            # Databases
            'mongodb': {
                'official_docs': [
                    {'title': 'MongoDB University', 'url': 'https://university.mongodb.com/', 'type': 'course', 'provider': 'MongoDB', 'is_free': True, 'quality_score': 0.96}
                ],
                'videos': [
                    {'title': 'MongoDB Crash Course', 'url': 'https://www.youtube.com/watch?v=-56x56UppqQ', 'type': 'video', 'provider': 'YouTube', 'is_free': True, 'quality_score': 0.90}
                ]
            },
            'postgresql': {
                'official_docs': [
                    {'title': 'PostgreSQL Tutorial', 'url': 'https://www.postgresql.org/docs/current/tutorial.html', 'type': 'documentation', 'provider': 'PostgreSQL', 'is_free': True, 'quality_score': 0.97}
                ],
                'videos': [
                    {'title': 'PostgreSQL Tutorial', 'url': 'https://www.youtube.com/watch?v=qw--VYLpxG4', 'type': 'video', 'provider': 'YouTube', 'is_free': True, 'quality_score': 0.89}
                ]
            },
            'mysql': {
                'official_docs': [
                    {'title': 'MySQL Documentation', 'url': 'https://dev.mysql.com/doc/', 'type': 'documentation', 'provider': 'MySQL', 'is_free': True, 'quality_score': 0.96}
                ],
                'videos': [
                    {'title': 'MySQL Tutorial', 'url': 'https://www.youtube.com/watch?v=7S_tz1z_5bA', 'type': 'video', 'provider': 'YouTube', 'is_free': True, 'quality_score': 0.88}
                ]
            },
            'redis': {
                'official_docs': [
                    {'title': 'Redis University', 'url': 'https://university.redis.com/', 'type': 'course', 'provider': 'Redis', 'is_free': True, 'quality_score': 0.95}
                ]
            },
            # Testing
            'jest': {
                'official_docs': [
                    {'title': 'Jest Documentation', 'url': 'https://jestjs.io/docs/getting-started', 'type': 'documentation', 'provider': 'Jest', 'is_free': True, 'quality_score': 0.96}
                ]
            },
            'pytest': {
                'official_docs': [
                    {'title': 'Pytest Documentation', 'url': 'https://docs.pytest.org/', 'type': 'documentation', 'provider': 'Pytest', 'is_free': True, 'quality_score': 0.97}
                ]
            },
            'selenium': {
                'official_docs': [
                    {'title': 'Selenium Documentation', 'url': 'https://www.selenium.dev/documentation/', 'type': 'documentation', 'provider': 'Selenium', 'is_free': True, 'quality_score': 0.95}
                ],
                'videos': [
                    {'title': 'Selenium Tutorial', 'url': 'https://www.youtube.com/watch?v=j7VZsCCnptM', 'type': 'video', 'provider': 'YouTube', 'is_free': True, 'quality_score': 0.87}
                ]
            },
            'cypress': {
                'official_docs': [
                    {'title': 'Cypress Documentation', 'url': 'https://docs.cypress.io/', 'type': 'documentation', 'provider': 'Cypress', 'is_free': True, 'quality_score': 0.97}
                ]
            },
            # DevOps & CI/CD
            'jenkins': {
                'official_docs': [
                    {'title': 'Jenkins Documentation', 'url': 'https://www.jenkins.io/doc/', 'type': 'documentation', 'provider': 'Jenkins', 'is_free': True, 'quality_score': 0.95}
                ]
            },
            'gitlab_ci': {
                'official_docs': [
                    {'title': 'GitLab CI/CD Documentation', 'url': 'https://docs.gitlab.com/ee/ci/', 'type': 'documentation', 'provider': 'GitLab', 'is_free': True, 'quality_score': 0.96}
                ]
            },
            'github_actions': {
                'official_docs': [
                    {'title': 'GitHub Actions Documentation', 'url': 'https://docs.github.com/en/actions', 'type': 'documentation', 'provider': 'GitHub', 'is_free': True, 'quality_score': 0.97}
                ]
            },
            'terraform': {
                'official_docs': [
                    {'title': 'Terraform Documentation', 'url': 'https://developer.hashicorp.com/terraform/docs', 'type': 'documentation', 'provider': 'HashiCorp', 'is_free': True, 'quality_score': 0.97}
                ],
                'videos': [
                    {'title': 'Terraform Course', 'url': 'https://www.youtube.com/watch?v=SLB_c_ayRMo', 'type': 'video', 'provider': 'YouTube', 'is_free': True, 'quality_score': 0.91}
                ]
            },
            'ansible': {
                'official_docs': [
                    {'title': 'Ansible Documentation', 'url': 'https://docs.ansible.com/', 'type': 'documentation', 'provider': 'Ansible', 'is_free': True, 'quality_score': 0.96}
                ]
            },
            # Cloud Platforms
            'aws_lambda': {
                'official_docs': [
                    {'title': 'AWS Lambda Documentation', 'url': 'https://docs.aws.amazon.com/lambda/', 'type': 'documentation', 'provider': 'AWS', 'is_free': True, 'quality_score': 0.97}
                ]
            },
            'aws_ec2': {
                'official_docs': [
                    {'title': 'AWS EC2 Documentation', 'url': 'https://docs.aws.amazon.com/ec2/', 'type': 'documentation', 'provider': 'AWS', 'is_free': True, 'quality_score': 0.97}
                ]
            },
            'aws_s3': {
                'official_docs': [
                    {'title': 'AWS S3 Documentation', 'url': 'https://docs.aws.amazon.com/s3/', 'type': 'documentation', 'provider': 'AWS', 'is_free': True, 'quality_score': 0.97}
                ]
            },
            'gcp': {
                'official_docs': [
                    {'title': 'Google Cloud Documentation', 'url': 'https://cloud.google.com/docs', 'type': 'documentation', 'provider': 'Google Cloud', 'is_free': True, 'quality_score': 0.97}
                ]
            },
            # Version Control & Collaboration
            'github': {
                'official_docs': [
                    {'title': 'GitHub Skills', 'url': 'https://skills.github.com/', 'type': 'practice', 'provider': 'GitHub', 'is_free': True, 'quality_score': 0.96}
                ]
            },
            'gitlab': {
                'official_docs': [
                    {'title': 'GitLab Documentation', 'url': 'https://docs.gitlab.com/', 'type': 'documentation', 'provider': 'GitLab', 'is_free': True, 'quality_score': 0.95}
                ]
            },
            # Data Science & ML Libraries
            'tensorflow': {
                'official_docs': [
                    {'title': 'TensorFlow Tutorials', 'url': 'https://www.tensorflow.org/tutorials', 'type': 'documentation', 'provider': 'TensorFlow', 'is_free': True, 'quality_score': 0.98}
                ],
                'videos': [
                    {'title': 'TensorFlow Course', 'url': 'https://www.youtube.com/watch?v=tPYj3fFJGjk', 'type': 'video', 'provider': 'YouTube', 'is_free': True, 'quality_score': 0.92}
                ]
            },
            'pytorch': {
                'official_docs': [
                    {'title': 'PyTorch Tutorials', 'url': 'https://pytorch.org/tutorials/', 'type': 'documentation', 'provider': 'PyTorch', 'is_free': True, 'quality_score': 0.98}
                ],
                'videos': [
                    {'title': 'PyTorch Tutorial', 'url': 'https://www.youtube.com/watch?v=c36lUUr864M', 'type': 'video', 'provider': 'YouTube', 'is_free': True, 'quality_score': 0.91}
                ]
            },
            'scikit_learn': {
                'official_docs': [
                    {'title': 'Scikit-learn Documentation', 'url': 'https://scikit-learn.org/stable/tutorial/index.html', 'type': 'documentation', 'provider': 'Scikit-learn', 'is_free': True, 'quality_score': 0.97}
                ]
            },
            'matplotlib': {
                'official_docs': [
                    {'title': 'Matplotlib Tutorials', 'url': 'https://matplotlib.org/stable/tutorials/index.html', 'type': 'documentation', 'provider': 'Matplotlib', 'is_free': True, 'quality_score': 0.95}
                ]
            },
            'seaborn': {
                'official_docs': [
                    {'title': 'Seaborn Tutorial', 'url': 'https://seaborn.pydata.org/tutorial.html', 'type': 'documentation', 'provider': 'Seaborn', 'is_free': True, 'quality_score': 0.94}
                ]
            },
            # Web Technologies
            'graphql': {
                'official_docs': [
                    {'title': 'GraphQL Documentation', 'url': 'https://graphql.org/learn/', 'type': 'documentation', 'provider': 'GraphQL', 'is_free': True, 'quality_score': 0.96}
                ]
            },
            'websocket': {
                'official_docs': [
                    {'title': 'WebSocket API', 'url': 'https://developer.mozilla.org/en-US/docs/Web/API/WebSockets_API', 'type': 'documentation', 'provider': 'MDN', 'is_free': True, 'quality_score': 0.95}
                ]
            },
            'oauth': {
                'official_docs': [
                    {'title': 'OAuth 2.0 Simplified', 'url': 'https://www.oauth.com/', 'type': 'documentation', 'provider': 'OAuth', 'is_free': True, 'quality_score': 0.94}
                ]
            },
            'jwt': {
                'official_docs': [
                    {'title': 'JWT Introduction', 'url': 'https://jwt.io/introduction', 'type': 'documentation', 'provider': 'JWT', 'is_free': True, 'quality_score': 0.93}
                ]
            }
        }
    
    def _get_cache_key(self, skill: str, difficulty: str = None) -> str:
        """Generate cache key for skill search."""
        key_str = f"{skill.lower()}:{difficulty or 'any'}"
        return hashlib.md5(key_str.encode()).hexdigest()
    
    def _check_cache(self, cache_key: str) -> Optional[List[dict]]:
        """Check if results are cached and not expired."""
        # Check memory cache first
        if cache_key in self.memory_cache:
            cached_data, timestamp = self.memory_cache[cache_key]
            if datetime.now() - timestamp < timedelta(hours=24):
                return cached_data
            else:
                del self.memory_cache[cache_key]
        
        # Check SQLite cache
        if self.cache_backend == 'sqlite':
            results = self.db.get_cached_resources(cache_key, limit=100)
            if results:
                self.memory_cache[cache_key] = (results, datetime.now())
                return results
        
        return None
    
    def _store_cache(self, cache_key: str, resources: List[dict]):
        """Store results in cache."""
        self.memory_cache[cache_key] = (resources, datetime.now())
        
        if self.cache_backend == 'sqlite' and resources:
            self.db.cache_resources(cache_key, resources)
    
    def _match_curated_resource(self, skill: str) -> List[dict]:
        """
        Match skill to curated resources using fuzzy matching.
        Returns high-quality, verified resources.
        """
        skill_lower = skill.lower()
        matched_resources = []
        
        # Skip ONLY pure soft skills (very specific list)
        pure_soft_skills = [
            'critical thinking', 'analytical thinking', 'creative thinking',
            'communication skills', 'collaboration skills', 'teamwork',
            'leadership', 'time management', 'organizational skills'
        ]
        
        if any(skill_lower == soft or skill_lower.startswith(soft + ' ') for soft in pure_soft_skills):
            return []  # Skip pure soft skills
        
        # Enhanced matching with skill mappings
        skill_mappings = {
            # Programming Languages
            'programming': 'python',
            'computer programming': 'python',
            'scripting': 'python',
            'python': 'python',
            'java': 'java',
            'object-oriented programming': 'java',
            'software development': 'python',
            'code': 'python',
            
            # Web Development
            'web programming': 'javascript',
            'web development': 'javascript',
            'javascript': 'javascript',
            'typescript': 'typescript',
            'node': 'nodejs',
            'nodejs': 'nodejs',
            'html': 'html',
            'css': 'css',
            'front-end': 'react',
            'frontend': 'react',
            'react': 'react',
            'web design': 'html',
            'responsive design': 'css',
            'user interface': 'html',
            'world wide web consortium': 'html',
            'web services': 'api',
            'web based': 'javascript',
            'rest': 'api',
            'restful': 'api',
            
            # Database
            'database': 'database',
            'sql': 'sql',
            'query': 'sql',
            'data storage': 'database',
            'relational database': 'sql',
            'mysql': 'sql',
            'postgresql': 'sql',
            
            # Data Science & Analytics
            'data science': 'data_science',
            'data analysis': 'pandas',
            'data visualization': 'pandas',
            'pandas': 'pandas',
            'numpy': 'numpy',
            'statistical': 'data_science',
            'analytical': 'data_science',
            'information extraction': 'data_science',
            
            # DevOps & Cloud
            'version control': 'git',
            'git': 'git',
            'github': 'git',
            'source control': 'git',
            'configuration management': 'git',
            'software configuration management': 'git',
            'jenkins': 'devops',
            'containerization': 'docker',
            'docker': 'docker',
            'kubernetes': 'kubernetes',
            'container': 'docker',
            'cloud': 'aws',
            'aws': 'aws',
            'amazon web services': 'aws',
            'azure': 'azure',
            'microsoft azure': 'azure',
            'devops': 'devops',
            'continuous integration': 'devops',
            'ci/cd': 'devops',
            
            # AI & ML
            'artificial intelligence': 'machine_learning',
            'machine learning': 'machine_learning',
            'deep learning': 'machine_learning',
            'neural network': 'machine_learning',
            'artificial neural': 'machine_learning',
            
            # Algorithms & Data Structures
            'algorithm': 'algorithms',
            'data structure': 'data_structures',
            'algorithmisation': 'algorithms',
            
            # Systems & Infrastructure
            'linux': 'linux',
            'unix': 'linux',
            'operating system': 'linux',
            
            # Frontend Frameworks
            'angular': 'angular',
            'vue': 'vue',
            'vue.js': 'vue',
            'svelte': 'svelte',
            'single page application': 'react',
            
            # Backend Frameworks
            'django': 'django',
            'flask': 'flask',
            'fastapi': 'fastapi',
            'express': 'express',
            'express.js': 'express',
            'spring': 'spring',
            'spring boot': 'spring',
            
            # Mobile Development
            'react native': 'react_native',
            'flutter': 'flutter',
            'swift': 'swift',
            'ios': 'swift',
            'kotlin': 'kotlin',
            'android': 'kotlin',
            'mobile development': 'mobile',
            'mobile app': 'mobile',
            
            # Databases (specific)
            'mongodb': 'mongodb',
            'postgres': 'postgresql',
            'postgresql': 'postgresql',
            'mysql': 'mysql',
            'redis': 'redis',
            'nosql': 'mongodb',
            
            # Testing
            'jest': 'jest',
            'pytest': 'pytest',
            'unit test': 'testing',
            'testing': 'testing',
            'test automation': 'selenium',
            'selenium': 'selenium',
            'cypress': 'cypress',
            'end-to-end': 'cypress',
            
            # CI/CD & DevOps Tools
            'jenkins': 'jenkins',
            'gitlab ci': 'gitlab_ci',
            'github actions': 'github_actions',
            'terraform': 'terraform',
            'ansible': 'ansible',
            'infrastructure as code': 'terraform',
            
            # Cloud Services
            'lambda': 'aws_lambda',
            'aws lambda': 'aws_lambda',
            'ec2': 'aws_ec2',
            'aws ec2': 'aws_ec2',
            's3': 'aws_s3',
            'aws s3': 'aws_s3',
            'google cloud': 'gcp',
            'gcp': 'gcp',
            
            # Version Control Platforms
            'github': 'github',
            'gitlab': 'gitlab',
            
            # ML/AI Frameworks
            'tensorflow': 'tensorflow',
            'pytorch': 'pytorch',
            'scikit-learn': 'scikit_learn',
            'scikit learn': 'scikit_learn',
            'sklearn': 'scikit_learn',
            'matplotlib': 'matplotlib',
            'seaborn': 'seaborn',
            'data visualization library': 'matplotlib',
            
            # Web Technologies
            'graphql': 'graphql',
            'websocket': 'websocket',
            'oauth': 'oauth',
            'jwt': 'jwt',
            'authentication': 'oauth',
            'json web token': 'jwt',
            
            # General Software Development
            'ide': 'python',  # Generic IDE usage maps to basic programming
            'integrated development environment': 'python',
            'debugging': 'python',
            'code review': 'git',
            'refactoring': 'python',
            'design pattern': 'python',
            'software architecture': 'python',
            'framework': 'react',  # Generic framework usage
            'library': 'python',  # Generic library usage
            'api': 'api',
            'rest api': 'api',
            'graphql api': 'graphql',
            'microservices': 'docker',
            'service-oriented': 'api',
            'networking': 'networking',
            'network': 'networking',
            'security': 'security',
            'cybersecurity': 'security',
            'information security': 'security',
            
            # Mobile Development
            'mobile': 'mobile',
            'android': 'mobile',
            'ios': 'mobile',
            'mobile app': 'mobile',
            
            # Software Engineering Practices
            'testing': 'testing',
            'test': 'testing',
            'quality assurance': 'testing',
            'debugging': 'testing',
            'agile': 'agile',
            'scrum': 'agile',
            
            # General Tech Skills
            'integrated development environment': 'python',
            'ide': 'python',
            'application-specific interface': 'api',
            'api': 'api'
        }
        
        # Check skill mappings first
        for pattern, target in skill_mappings.items():
            if pattern in skill_lower:
                if target in self.curated_resources:
                    for category, resources in self.curated_resources[target].items():
                        matched_resources.extend(resources)
                    if matched_resources:
                        break
        
        # Direct match or keyword match
        if not matched_resources:
            for key, resources in self.curated_resources.items():
                if key in skill_lower or skill_lower in key:
                    # Flatten all resource categories
                    for category, resource_list in resources.items():
                        matched_resources.extend(resource_list)
        
        # If no exact match, try partial matching with common keywords
        if not matched_resources:
            keywords = skill_lower.split()
            for keyword in keywords:
                if len(keyword) > 3:  # Skip very short words
                    for key, resources in self.curated_resources.items():
                        if keyword in key or key in keyword:
                            for category, resource_list in resources.items():
                                matched_resources.extend(resource_list)
                            break
        
        # Sort by quality score
        matched_resources.sort(key=lambda x: x.get('quality_score', 0), reverse=True)
        
        return matched_resources[:10]  # Return top 10
    
    async def search_github_quality(self, session: aiohttp.ClientSession, skill: str) -> List[dict]:
        """
        Search GitHub for high-quality educational repositories.
        Only for technical skills - skips generic/soft skills.
        """
        # Skip GitHub search for non-technical skills
        skip_keywords = [
            'domain', 'dns', 'service', 'management', 'process', 'communication',
            'leadership', 'teamwork', 'planning', 'strategy', 'business',
            'migration', 'documentation', 'literature', 'empirical', 'draft',
            'categorisation', 'architecture', 'modelling', 'design thinking',
            'w3c', 'consortium', 'standards', 'online analytical', 'information extraction'
        ]
        
        skill_lower = skill.lower()
        if any(keyword in skill_lower for keyword in skip_keywords):
            return []
        
        try:
            search_url = f"https://api.github.com/search/repositories?q={skill}+stars:>5000&sort=stars&order=desc&per_page=3"
            headers = {'Accept': 'application/vnd.github.v3+json'}
            timeout = aiohttp.ClientTimeout(total=10)
            
            async with session.get(search_url, headers=headers, timeout=timeout) as response:
                if response.status == 200:
                    data = await response.json()
                    resources = []
                    
                    for repo in data.get('items', [])[:3]:
                        # Only include if description seems educational
                        description = repo.get('description', '').lower()
                        if any(word in description for word in ['learn', 'tutorial', 'course', 'guide', 'example', 'practice', 'book', 'documentation', 'resource']):
                            resources.append({
                                'title': f"{repo['name']} ({repo['stargazers_count']:,} stars)",
                                'url': repo['html_url'],
                                'type': 'repository',
                                'provider': 'GitHub',
                                'description': repo.get('description', 'No description'),
                                'is_free': True,
                                'quality_score': min(1.0, repo.get('stargazers_count', 0) / 50000),
                                'stars': repo.get('stargazers_count', 0)
                            })
                    
                    return resources
        except Exception as e:
            print(f"  ⚠️ GitHub search error: {e}")
        
        return []
    
    async def search_all_sources(self, skill: str, difficulty: str = None) -> List[dict]:
        """
        Search all sources with emphasis on curated resources.
        """
        # Check cache first
        cache_key = self._get_cache_key(skill, difficulty)
        cached_results = self._check_cache(cache_key)
        
        if cached_results:
            print(f"  ✅ Cache hit for: {skill}")
            return cached_results
        
        print(f"  🔍 Searching curated sources for: {skill}")
        start_time = time.time()
        
        # First, try curated resources (instant, high-quality)
        curated = self._match_curated_resource(skill)
        
        # Then, augment with GitHub if needed
        github_resources = []
        if len(curated) < 8:
            async with aiohttp.ClientSession() as session:
                github_resources = await self.search_github_quality(session, skill)
        
        # Combine: curated first, then GitHub
        all_resources = curated + github_resources
        
        # Remove duplicates by URL
        seen_urls = set()
        unique_resources = []
        for resource in all_resources:
            if resource['url'] not in seen_urls:
                seen_urls.add(resource['url'])
                unique_resources.append(resource)
        
        # Sort by quality score
        unique_resources.sort(key=lambda x: x.get('quality_score', 0), reverse=True)
        
        # Store in cache
        self._store_cache(cache_key, unique_resources[:15])
        
        elapsed = time.time() - start_time
        print(f"  ✅ Found {len(unique_resources)} quality resources in {elapsed:.2f}s")
        
        return unique_resources[:15]
    
    def search_resources(self, skill: str, difficulty: str = None, limit: int = 10) -> List[dict]:
        """Synchronous wrapper for async search."""
        try:
            loop = asyncio.get_event_loop()
            if loop.is_running():
                # If loop is already running, create task
                import nest_asyncio
                nest_asyncio.apply()
            return loop.run_until_complete(self.search_all_sources(skill, difficulty))
        except Exception as e:
            print(f"  ⚠️ Error in search_resources: {e}")
            return []
    
    async def batch_search_resources(self, skills: List[str]) -> Dict[str, List[dict]]:
        """
        Batch search for multiple skills in parallel.
        """
        print(f"📚 Batch searching {len(skills)} skills...")
        
        tasks = [self.search_all_sources(skill) for skill in skills]
        results = await asyncio.gather(*tasks, return_exceptions=True)
        
        resources_by_skill = {}
        for skill, result in zip(skills, results):
            if isinstance(result, list):
                resources_by_skill[skill] = result
            else:
                print(f"  ⚠️ Error for {skill}: {result}")
                resources_by_skill[skill] = []
        
        total_resources = sum(len(res) for res in resources_by_skill.values())
        print(f"✅ Batch search complete: {total_resources} total resources")
        
        return resources_by_skill
    
    # Alias for backward compatibility
    async def batch_search(self, skills: List[str]) -> Dict[str, List[dict]]:
        """Alias for batch_search_resources for backward compatibility."""
        return await self.batch_search_resources(skills)
