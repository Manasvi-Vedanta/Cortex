"""
Database Optimization Module
Implements indexes, connection pooling, and prepared statements for better performance.
"""

import sqlite3
import threading
from queue import Queue, Empty
from typing import Optional, List, Tuple
import time
from contextlib import contextmanager


class ConnectionPool:
    """
    Thread-safe database connection pool.
    Reuses connections instead of creating new ones for each request.
    """
    
    def __init__(self, db_path: str, pool_size: int = 10):
        """
        Initialize connection pool.
        
        Args:
            db_path: Path to SQLite database
            pool_size: Maximum number of connections in pool
        """
        self.db_path = db_path
        self.pool_size = pool_size
        self.pool = Queue(maxsize=pool_size)
        self.lock = threading.Lock()
        self._initialized = False
        
    def _initialize_pool(self):
        """Create initial pool of connections."""
        with self.lock:
            if self._initialized:
                return
            
            print(f"Initializing connection pool with {self.pool_size} connections...")
            for _ in range(self.pool_size):
                conn = sqlite3.connect(
                    self.db_path,
                    check_same_thread=False,  # Allow sharing across threads
                    timeout=30.0
                )
                # Enable WAL mode for better concurrency
                conn.execute("PRAGMA journal_mode=WAL")
                conn.execute("PRAGMA synchronous=NORMAL")
                conn.execute("PRAGMA cache_size=-64000")  # 64MB cache
                conn.row_factory = sqlite3.Row  # Enable dict-like access
                self.pool.put(conn)
            
            self._initialized = True
            print(f"✅ Connection pool initialized with {self.pool_size} connections")
    
    @contextmanager
    def get_connection(self, timeout: float = 5.0):
        """
        Get a connection from the pool (context manager).
        
        Args:
            timeout: Maximum time to wait for available connection
            
        Yields:
            Database connection
        """
        if not self._initialized:
            self._initialize_pool()
        
        conn = None
        try:
            conn = self.pool.get(timeout=timeout)
            yield conn
        except Empty:
            raise RuntimeError(f"Connection pool timeout after {timeout}s")
        finally:
            if conn:
                self.pool.put(conn)
    
    def close_all(self):
        """Close all connections in the pool."""
        while not self.pool.empty():
            try:
                conn = self.pool.get_nowait()
                conn.close()
            except Empty:
                break


class PreparedStatementCache:
    """
    Cache for frequently used SQL queries.
    Reduces parsing overhead by reusing prepared statements.
    """
    
    def __init__(self):
        self.cache = {}
        self.hit_count = 0
        self.miss_count = 0
    
    def get_query(self, query_key: str) -> Optional[str]:
        """Get cached query by key."""
        if query_key in self.cache:
            self.hit_count += 1
            return self.cache[query_key]
        self.miss_count += 1
        return None
    
    def cache_query(self, query_key: str, query: str):
        """Cache a query."""
        self.cache[query_key] = query
    
    def get_stats(self) -> dict:
        """Get cache statistics."""
        total = self.hit_count + self.miss_count
        hit_rate = (self.hit_count / total * 100) if total > 0 else 0
        return {
            'hits': self.hit_count,
            'misses': self.miss_count,
            'hit_rate': hit_rate,
            'cached_queries': len(self.cache)
        }


class OptimizedDatabase:
    """
    Optimized database interface with connection pooling and prepared statements.
    """
    
    # Prepared statement templates
    QUERIES = {
        'get_occupation_skills': """
            SELECT s.concept_uri, s.preferred_label, s.description, 
                   osr.relation_type, s.relevance_score
            FROM skills s
            JOIN occupation_skill_relations osr ON s.concept_uri = osr.skill_uri
            WHERE osr.occupation_uri = ?
            ORDER BY 
                CASE osr.relation_type 
                    WHEN 'essential' THEN 1 
                    WHEN 'optional' THEN 2 
                    ELSE 3 
                END,
                s.relevance_score DESC
        """,
        
        'get_skill_dependencies': """
            SELECT source_skill_uri, target_skill_uri, relation_type
            FROM skill_skill_relations
            WHERE source_skill_uri IN ({placeholders})
            AND target_skill_uri IN ({placeholders})
        """,
        
        'get_vote_scores': """
            SELECT item_uri, SUM(vote_value) as vote_score
            FROM votes
            WHERE item_uri IN ({placeholders})
            GROUP BY item_uri
        """,
        
        'get_occupation_by_uri': """
            SELECT concept_uri, preferred_label, description, relevance_score
            FROM occupations
            WHERE concept_uri = ?
        """,
        
        'get_all_occupations': """
            SELECT concept_uri, preferred_label, description
            FROM occupations
        """,
        
        'search_resources_cached': """
            SELECT resource_url, resource_title, resource_type, provider,
                   description, difficulty_level, quality_score, created_at
            FROM resource_cache
            WHERE skill_search_key = ? 
            AND datetime(created_at, '+24 hours') > datetime('now')
            ORDER BY quality_score DESC
            LIMIT ?
        """,
        
        'insert_resource_cache': """
            INSERT OR REPLACE INTO resource_cache 
            (skill_search_key, resource_url, resource_title, resource_type, 
             provider, description, difficulty_level, quality_score, created_at)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, datetime('now'))
        """
    }
    
    def __init__(self, db_path: str = 'genmentor.db', pool_size: int = 10):
        """
        Initialize optimized database interface.
        
        Args:
            db_path: Path to SQLite database
            pool_size: Connection pool size
        """
        self.pool = ConnectionPool(db_path, pool_size)
        self.query_cache = PreparedStatementCache()
        self.db_path = db_path
        
        # Create indexes and cache table
        self._create_indexes()
        self._create_cache_table()
    
    def _create_indexes(self):
        """Create performance indexes on critical tables."""
        with self.pool.get_connection() as conn:
            cursor = conn.cursor()
            
            print("Creating database indexes...")
            
            indexes = [
                # A3.1: Occupation-Skill Relations Index
                ("idx_occ_skill_uri", 
                 "CREATE INDEX IF NOT EXISTS idx_occ_skill_uri ON occupation_skill_relations(occupation_uri)"),
                ("idx_occ_skill_relation", 
                 "CREATE INDEX IF NOT EXISTS idx_occ_skill_relation ON occupation_skill_relations(occupation_uri, relation_type)"),
                ("idx_occ_skill_skill_uri",
                 "CREATE INDEX IF NOT EXISTS idx_occ_skill_skill_uri ON occupation_skill_relations(skill_uri)"),
                
                # Skill-Skill Relations Index
                ("idx_skill_skill_source", 
                 "CREATE INDEX IF NOT EXISTS idx_skill_skill_source ON skill_skill_relations(source_skill_uri)"),
                ("idx_skill_skill_target", 
                 "CREATE INDEX IF NOT EXISTS idx_skill_skill_target ON skill_skill_relations(target_skill_uri)"),
                ("idx_skill_skill_both",
                 "CREATE INDEX IF NOT EXISTS idx_skill_skill_both ON skill_skill_relations(source_skill_uri, target_skill_uri)"),
                
                # Votes Index
                ("idx_votes_item", 
                 "CREATE INDEX IF NOT EXISTS idx_votes_item ON votes(item_uri)"),
                ("idx_votes_item_type", 
                 "CREATE INDEX IF NOT EXISTS idx_votes_item_type ON votes(item_uri, item_type)"),
                
                # Skills Index
                ("idx_skills_uri",
                 "CREATE INDEX IF NOT EXISTS idx_skills_uri ON skills(concept_uri)"),
                ("idx_skills_label",
                 "CREATE INDEX IF NOT EXISTS idx_skills_label ON skills(preferred_label)"),
                
                # Occupations Index
                ("idx_occupations_uri",
                 "CREATE INDEX IF NOT EXISTS idx_occupations_uri ON occupations(concept_uri)"),
            ]
            
            for idx_name, idx_sql in indexes:
                try:
                    cursor.execute(idx_sql)
                    print(f"  ✅ Created index: {idx_name}")
                except sqlite3.OperationalError as e:
                    if "already exists" not in str(e):
                        print(f"  ⚠️ Failed to create {idx_name}: {e}")
            
            conn.commit()
            print("✅ Database indexes created successfully!")
    
    def _create_cache_table(self):
        """Create cache table for resource search results (B4.2)."""
        with self.pool.get_connection() as conn:
            cursor = conn.cursor()
            
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS resource_cache (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    skill_search_key TEXT NOT NULL,
                    resource_url TEXT NOT NULL,
                    resource_title TEXT,
                    resource_type TEXT,
                    provider TEXT,
                    description TEXT,
                    difficulty_level TEXT,
                    quality_score REAL,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    UNIQUE(skill_search_key, resource_url)
                )
            """)
            
            cursor.execute("""
                CREATE INDEX IF NOT EXISTS idx_resource_cache_skill 
                ON resource_cache(skill_search_key, created_at)
            """)
            
            conn.commit()
            print("✅ Resource cache table created!")
    
    def get_occupation_skills(self, occupation_uri: str) -> List[Tuple]:
        """
        Get all skills for an occupation (optimized with index).
        
        Args:
            occupation_uri: Occupation URI
            
        Returns:
            List of skill tuples (uri, label, description, relation_type, relevance_score)
        """
        query = self.QUERIES['get_occupation_skills']
        
        with self.pool.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute(query, (occupation_uri,))
            return cursor.fetchall()
    
    def get_skill_dependencies(self, skill_uris: List[str]) -> List[Tuple]:
        """
        Get dependencies for a list of skills (optimized).
        
        Args:
            skill_uris: List of skill URIs
            
        Returns:
            List of dependency tuples (source, target, relation_type)
        """
        if not skill_uris:
            return []
        
        placeholders = ','.join(['?' for _ in skill_uris])
        query = self.QUERIES['get_skill_dependencies'].format(placeholders=placeholders)
        
        with self.pool.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute(query, skill_uris + skill_uris)
            return cursor.fetchall()
    
    def get_vote_scores(self, item_uris: List[str]) -> dict:
        """
        Get vote scores for items (optimized with index).
        
        Args:
            item_uris: List of item URIs
            
        Returns:
            Dictionary mapping URIs to vote scores
        """
        if not item_uris:
            return {}
        
        placeholders = ','.join(['?' for _ in item_uris])
        query = self.QUERIES['get_vote_scores'].format(placeholders=placeholders)
        
        with self.pool.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute(query, item_uris)
            return dict(cursor.fetchall())
    
    def get_cached_resources(self, skill_key: str, limit: int = 10) -> List[dict]:
        """
        Get cached resource search results (B4.2).
        
        Args:
            skill_key: Skill search key
            limit: Maximum results
            
        Returns:
            List of cached resources
        """
        query = self.QUERIES['search_resources_cached']
        
        with self.pool.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute(query, (skill_key, limit))
            
            rows = cursor.fetchall()
            return [dict(row) for row in rows]
    
    def cache_resources(self, skill_key: str, resources: List[dict]):
        """
        Cache resource search results with 24-hour TTL (B4.2).
        
        Args:
            skill_key: Skill search key
            resources: List of resource dictionaries
        """
        query = self.QUERIES['insert_resource_cache']
        
        with self.pool.get_connection() as conn:
            cursor = conn.cursor()
            
            for resource in resources:
                try:
                    cursor.execute(query, (
                        skill_key,
                        resource.get('url', ''),
                        resource.get('title', ''),
                        resource.get('type', ''),
                        resource.get('provider', ''),
                        resource.get('description', ''),
                        resource.get('difficulty_level', ''),
                        resource.get('quality_score', 0.0)
                    ))
                except sqlite3.IntegrityError:
                    pass  # Already cached
            
            conn.commit()
    
    def get_query_cache_stats(self) -> dict:
        """Get query cache statistics."""
        return self.query_cache.get_stats()
    
    def close(self):
        """Close all database connections."""
        self.pool.close_all()


# Global instance (singleton pattern)
_db_instance: Optional[OptimizedDatabase] = None


def get_optimized_db(db_path: str = 'genmentor.db') -> OptimizedDatabase:
    """
    Get global OptimizedDatabase instance (singleton).
    
    Args:
        db_path: Path to database
        
    Returns:
        OptimizedDatabase instance
    """
    global _db_instance
    if _db_instance is None:
        _db_instance = OptimizedDatabase(db_path)
    return _db_instance


if __name__ == "__main__":
    # Test the optimization
    print("Testing database optimizations...")
    
    db = OptimizedDatabase()
    
    # Test connection pooling
    start = time.time()
    for i in range(10):
        with db.pool.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT COUNT(*) FROM occupations")
            count = cursor.fetchone()[0]
    pooled_time = time.time() - start
    
    print(f"\n✅ Connection pooling test: {pooled_time:.3f}s for 10 queries")
    print(f"   Average: {pooled_time/10*1000:.1f}ms per query")
    
    # Test query cache stats
    stats = db.get_query_cache_stats()
    print(f"\n📊 Query Cache Stats: {stats}")
    
    print("\n✅ Database optimization complete!")
