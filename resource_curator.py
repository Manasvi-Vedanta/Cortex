"""
Resource Curation System
Curate and attach accurate study sources for each learning item using RAG + validated resources.
"""

import sqlite3
import json
import requests
from typing import Dict, List, Tuple, Optional
from bs4 import BeautifulSoup
import re
from datetime import datetime
from urllib.parse import urlparse, quote_plus

class ResourceCurator:
    """Curate and validate learning resources for skills using RAG and external sources."""
    
    def __init__(self, db_path: str = 'genmentor.db'):
        self.db_path = db_path
        self._ensure_resource_tables()
        
        # Trusted resource domains
        self.trusted_domains = [
            'coursera.org', 'udemy.com', 'edx.org', 'khanacademy.org',
            'youtube.com', 'medium.com', 'dev.to', 'stackoverflow.com',
            'github.com', 'docs.python.org', 'w3schools.com', 'mdn.mozilla.org',
            'freecodecamp.org', 'pluralsight.com', 'linkedin.com/learning'
        ]
    
    def _get_db_connection(self):
        """Get database connection."""
        return sqlite3.connect(self.db_path)
    
    def _ensure_resource_tables(self):
        """Ensure resource tables exist."""
        conn = self._get_db_connection()
        cursor = conn.cursor()
        
        # Learning resources table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS learning_resources (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                skill_uri TEXT NOT NULL,
                resource_url TEXT NOT NULL,
                resource_title TEXT NOT NULL,
                resource_type TEXT NOT NULL,  -- 'course', 'tutorial', 'documentation', 'video', 'article', 'book'
                provider TEXT,  -- 'Coursera', 'YouTube', 'Medium', etc.
                description TEXT,
                difficulty_level TEXT,  -- 'beginner', 'intermediate', 'advanced'
                estimated_duration TEXT,
                is_free BOOLEAN DEFAULT 1,
                language TEXT DEFAULT 'en',
                quality_score REAL DEFAULT 0.0,  -- 0-10, based on community ratings
                relevance_score REAL DEFAULT 0.0,  -- 0-1, based on content matching
                validation_status TEXT DEFAULT 'pending',  -- 'pending', 'validated', 'rejected'
                validated_by TEXT,
                validated_at TIMESTAMP,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                UNIQUE(skill_uri, resource_url)
            )
        """)
        
        # Resource tags (for better categorization)
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS resource_tags (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                resource_id INTEGER NOT NULL,
                tag TEXT NOT NULL,
                FOREIGN KEY (resource_id) REFERENCES learning_resources(id),
                UNIQUE(resource_id, tag)
            )
        """)
        
        # Resource access stats
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS resource_access_stats (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                resource_id INTEGER NOT NULL,
                user_id TEXT NOT NULL,
                accessed_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                completed BOOLEAN DEFAULT 0,
                completion_time_hours INTEGER,
                FOREIGN KEY (resource_id) REFERENCES learning_resources(id)
            )
        """)
        
        conn.commit()
        conn.close()
        print("✅ Resource curation tables initialized")
    
    # ==================== RESOURCE DISCOVERY ====================
    
    def search_resources(self, skill_name: str, limit: int = 10) -> List[Dict]:
        """
        Search for learning resources using multiple sources.
        
        Args:
            skill_name: Name of the skill to find resources for
            limit: Maximum number of resources to return
        
        Returns:
            List of discovered resources
        """
        resources = []
        
        # Try multiple search strategies
        resources.extend(self._search_youtube(skill_name, limit=3))
        resources.extend(self._search_github(skill_name, limit=2))
        resources.extend(self._search_medium(skill_name, limit=2))
        resources.extend(self._search_documentation(skill_name, limit=3))
        
        # Remove duplicates and limit
        seen_urls = set()
        unique_resources = []
        for resource in resources:
            if resource['url'] not in seen_urls:
                seen_urls.add(resource['url'])
                unique_resources.append(resource)
                if len(unique_resources) >= limit:
                    break
        
        return unique_resources
    
    def _search_youtube(self, skill_name: str, limit: int = 3) -> List[Dict]:
        """Search YouTube for tutorials (simulated - would need YouTube API)."""
        # In production, you would use YouTube Data API
        # For now, construct search URLs
        query = quote_plus(f"{skill_name} tutorial")
        search_url = f"https://www.youtube.com/results?search_query={query}"
        
        return [{
            'url': search_url,
            'title': f"{skill_name} Tutorial - YouTube",
            'type': 'video',
            'provider': 'YouTube',
            'description': f'Video tutorials for {skill_name}',
            'is_free': True,
            'relevance_score': 0.8
        }]
    
    def _search_github(self, skill_name: str, limit: int = 2) -> List[Dict]:
        """Search GitHub for repositories and examples."""
        try:
            query = skill_name.replace(' ', '+')
            search_url = f"https://api.github.com/search/repositories?q={query}&sort=stars&order=desc&per_page={limit}"
            
            response = requests.get(search_url, timeout=5)
            if response.status_code == 200:
                data = response.json()
                resources = []
                
                for repo in data.get('items', [])[:limit]:
                    resources.append({
                        'url': repo['html_url'],
                        'title': repo['name'],
                        'type': 'repository',
                        'provider': 'GitHub',
                        'description': repo.get('description', ''),
                        'is_free': True,
                        'relevance_score': 0.7
                    })
                
                return resources
        except Exception as e:
            print(f"GitHub search error: {e}")
        
        return []
    
    def _search_medium(self, skill_name: str, limit: int = 2) -> List[Dict]:
        """Search Medium for articles (simulated)."""
        query = quote_plus(skill_name)
        search_url = f"https://medium.com/search?q={query}"
        
        return [{
            'url': search_url,
            'title': f"{skill_name} Articles - Medium",
            'type': 'article',
            'provider': 'Medium',
            'description': f'Articles and guides about {skill_name}',
            'is_free': True,
            'relevance_score': 0.6
        }]
    
    def _search_documentation(self, skill_name: str, limit: int = 3) -> List[Dict]:
        """Search for official documentation."""
        resources = []
        
        # Common documentation patterns
        doc_patterns = [
            f"https://docs.{skill_name.lower().replace(' ', '')}.org",
            f"https://{skill_name.lower().replace(' ', '')}.org/docs",
            f"https://www.{skill_name.lower().replace(' ', '')}.com/docs"
        ]
        
        for url in doc_patterns[:limit]:
            resources.append({
                'url': url,
                'title': f"{skill_name} Official Documentation",
                'type': 'documentation',
                'provider': 'Official',
                'description': f'Official documentation for {skill_name}',
                'is_free': True,
                'relevance_score': 0.9
            })
        
        return resources
    
    # ==================== RESOURCE MANAGEMENT ====================
    
    def add_resource(self, skill_uri: str, resource_url: str, resource_title: str,
                    resource_type: str, provider: str = None, description: str = None,
                    difficulty_level: str = 'intermediate', is_free: bool = True,
                    estimated_duration: str = None) -> int:
        """
        Add a learning resource to the database.
        
        Returns:
            resource_id
        """
        conn = self._get_db_connection()
        cursor = conn.cursor()
        
        # Calculate relevance score based on URL domain
        relevance_score = self._calculate_url_relevance(resource_url)
        
        try:
            cursor.execute("""
                INSERT INTO learning_resources
                (skill_uri, resource_url, resource_title, resource_type, provider,
                 description, difficulty_level, is_free, estimated_duration, relevance_score)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """, (skill_uri, resource_url, resource_title, resource_type, provider,
                  description, difficulty_level, is_free, estimated_duration, relevance_score))
            
            resource_id = cursor.lastrowid
            conn.commit()
            print(f"✅ Added resource: {resource_title}")
            return resource_id
        
        except sqlite3.IntegrityError:
            # Resource already exists
            cursor.execute("""
                SELECT id FROM learning_resources
                WHERE skill_uri = ? AND resource_url = ?
            """, (skill_uri, resource_url))
            result = cursor.fetchone()
            return result[0] if result else None
        
        finally:
            conn.close()
    
    def _calculate_url_relevance(self, url: str) -> float:
        """Calculate relevance score based on URL domain."""
        domain = urlparse(url).netloc.lower()
        
        for trusted in self.trusted_domains:
            if trusted in domain:
                return 0.9
        
        return 0.5  # Default score for unknown domains
    
    def validate_resource(self, resource_id: int, validator_id: str, 
                         status: str = 'validated') -> bool:
        """Validate or reject a resource."""
        if status not in ['validated', 'rejected']:
            raise ValueError("Status must be 'validated' or 'rejected'")
        
        conn = self._get_db_connection()
        cursor = conn.cursor()
        
        cursor.execute("""
            UPDATE learning_resources
            SET validation_status = ?,
                validated_by = ?,
                validated_at = CURRENT_TIMESTAMP
            WHERE id = ?
        """, (status, validator_id, resource_id))
        
        conn.commit()
        success = cursor.rowcount > 0
        conn.close()
        
        return success
    
    def get_resources_for_skill(self, skill_uri: str, 
                               difficulty_level: str = None,
                               min_quality: float = 0.0,
                               only_validated: bool = False) -> List[Dict]:
        """
        Get curated resources for a specific skill.
        
        Args:
            skill_uri: URI of the skill
            difficulty_level: Filter by difficulty ('beginner', 'intermediate', 'advanced')
            min_quality: Minimum quality score (0-10)
            only_validated: Only return validated resources
        
        Returns:
            List of resources
        """
        conn = self._get_db_connection()
        cursor = conn.cursor()
        
        query = """
            SELECT id, resource_url, resource_title, resource_type, provider,
                   description, difficulty_level, estimated_duration, is_free,
                   quality_score, relevance_score, validation_status
            FROM learning_resources
            WHERE skill_uri = ?
                AND quality_score >= ?
        """
        params = [skill_uri, min_quality]
        
        if difficulty_level:
            query += " AND difficulty_level = ?"
            params.append(difficulty_level)
        
        if only_validated:
            query += " AND validation_status = 'validated'"
        
        query += " ORDER BY quality_score DESC, relevance_score DESC"
        
        cursor.execute(query, params)
        
        resources = []
        for row in cursor.fetchall():
            resources.append({
                'id': row[0],
                'url': row[1],
                'title': row[2],
                'type': row[3],
                'provider': row[4],
                'description': row[5],
                'difficulty_level': row[6],
                'estimated_duration': row[7],
                'is_free': bool(row[8]),
                'quality_score': row[9],
                'relevance_score': row[10],
                'validation_status': row[11]
            })
        
        conn.close()
        return resources
    
    def curate_resources_for_learning_path(self, learning_path: List[Dict]) -> List[Dict]:
        """
        Automatically curate resources for an entire learning path.
        
        Args:
            learning_path: List of learning sessions with skills
        
        Returns:
            Enhanced learning path with curated resources
        """
        enhanced_path = []
        
        for session in learning_path:
            enhanced_session = session.copy()
            session_resources = []
            
            for skill in session.get('skills', []):
                skill_name = skill if isinstance(skill, str) else skill.get('name', '')
                
                # Get existing resources from DB
                # Note: We need skill URI, so we'll search by name for now
                conn = self._get_db_connection()
                cursor = conn.cursor()
                
                cursor.execute("""
                    SELECT s.concept_uri
                    FROM skills s
                    WHERE s.preferred_label LIKE ?
                    LIMIT 1
                """, (f"%{skill_name}%",))
                
                result = cursor.fetchone()
                skill_uri = result[0] if result else None
                conn.close()
                
                if skill_uri:
                    # Get existing resources
                    existing = self.get_resources_for_skill(
                        skill_uri,
                        difficulty_level=session.get('difficulty_level'),
                        min_quality=5.0,
                        only_validated=True
                    )
                    
                    if existing:
                        session_resources.extend(existing[:2])  # Top 2 per skill
                    else:
                        # Search for new resources
                        discovered = self.search_resources(skill_name, limit=2)
                        for resource in discovered:
                            # Add to database
                            resource_id = self.add_resource(
                                skill_uri=skill_uri,
                                resource_url=resource['url'],
                                resource_title=resource['title'],
                                resource_type=resource['type'],
                                provider=resource.get('provider'),
                                description=resource.get('description'),
                                difficulty_level=session.get('difficulty_level', 'intermediate'),
                                is_free=resource.get('is_free', True)
                            )
                            
                            if resource_id:
                                resource['id'] = resource_id
                                session_resources.append(resource)
            
            # Remove duplicates
            unique_resources = []
            seen_urls = set()
            for res in session_resources:
                if res['url'] not in seen_urls:
                    seen_urls.add(res['url'])
                    unique_resources.append(res)
            
            enhanced_session['curated_resources'] = unique_resources
            enhanced_path.append(enhanced_session)
        
        return enhanced_path
    
    # ==================== RESOURCE ANALYTICS ====================
    
    def get_resource_statistics(self, resource_id: int) -> Dict:
        """Get statistics for a specific resource."""
        conn = self._get_db_connection()
        cursor = conn.cursor()
        
        # Get basic resource info
        cursor.execute("""
            SELECT resource_title, resource_type, provider, quality_score,
                   relevance_score, validation_status
            FROM learning_resources
            WHERE id = ?
        """, (resource_id,))
        
        resource_info = cursor.fetchone()
        if not resource_info:
            return None
        
        # Get access stats
        cursor.execute("""
            SELECT 
                COUNT(*) as total_accesses,
                COUNT(DISTINCT user_id) as unique_users,
                SUM(CASE WHEN completed = 1 THEN 1 ELSE 0 END) as completions,
                AVG(completion_time_hours) as avg_completion_time
            FROM resource_access_stats
            WHERE resource_id = ?
        """, (resource_id,))
        
        access_stats = cursor.fetchone()
        
        conn.close()
        
        return {
            'resource_id': resource_id,
            'title': resource_info[0],
            'type': resource_info[1],
            'provider': resource_info[2],
            'quality_score': resource_info[3],
            'relevance_score': resource_info[4],
            'validation_status': resource_info[5],
            'total_accesses': access_stats[0] or 0,
            'unique_users': access_stats[1] or 0,
            'completions': access_stats[2] or 0,
            'completion_rate': (access_stats[2] / access_stats[0] * 100) if access_stats[0] > 0 else 0,
            'avg_completion_time': access_stats[3] or 0
        }
    
    def track_resource_access(self, resource_id: int, user_id: str, 
                             completed: bool = False, 
                             completion_time_hours: int = None):
        """Track when a user accesses a resource."""
        conn = self._get_db_connection()
        cursor = conn.cursor()
        
        cursor.execute("""
            INSERT INTO resource_access_stats
            (resource_id, user_id, completed, completion_time_hours)
            VALUES (?, ?, ?, ?)
        """, (resource_id, user_id, completed, completion_time_hours))
        
        conn.commit()
        conn.close()
    
    def get_popular_resources(self, days: int = 30, limit: int = 10) -> List[Dict]:
        """Get most popular resources in the last N days."""
        conn = self._get_db_connection()
        cursor = conn.cursor()
        
        cursor.execute("""
            SELECT 
                lr.id, lr.resource_title, lr.resource_type, lr.provider,
                COUNT(ras.id) as access_count,
                lr.quality_score
            FROM learning_resources lr
            JOIN resource_access_stats ras ON lr.id = ras.resource_id
            WHERE ras.accessed_at >= datetime('now', '-' || ? || ' days')
            GROUP BY lr.id
            ORDER BY access_count DESC, lr.quality_score DESC
            LIMIT ?
        """, (days, limit))
        
        resources = []
        for row in cursor.fetchall():
            resources.append({
                'id': row[0],
                'title': row[1],
                'type': row[2],
                'provider': row[3],
                'access_count': row[4],
                'quality_score': row[5]
            })
        
        conn.close()
        return resources

if __name__ == "__main__":
    # Example usage
    curator = ResourceCurator()
    
    # Search for resources
    resources = curator.search_resources("Python programming", limit=5)
    print(f"Found {len(resources)} resources")
    
    # Add a resource
    resource_id = curator.add_resource(
        skill_uri="http://data.europa.eu/esco/skill/python",
        resource_url="https://docs.python.org/3/tutorial/",
        resource_title="Python Tutorial - Official Documentation",
        resource_type="documentation",
        provider="Python.org",
        description="Official Python tutorial for beginners",
        difficulty_level="beginner",
        is_free=True
    )
    print(f"Added resource ID: {resource_id}")
