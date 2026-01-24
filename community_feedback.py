"""
Community Feedback Loop System
Crowdsourced curriculum updates, voting, and suggestion review integrated with DB.
"""

import sqlite3
import json
from datetime import datetime, timedelta
from typing import Dict, List, Tuple, Optional
import statistics

class CommunityFeedbackSystem:
    """Enhanced community feedback system with voting, suggestions, and review mechanisms."""
    
    def __init__(self, db_path: str = 'genmentor.db'):
        self.db_path = db_path
        self._ensure_feedback_tables()
        self._ensure_implementation_table()
    
    def _get_db_connection(self):
        """Get database connection."""
        return sqlite3.connect(self.db_path)
    
    def _ensure_feedback_tables(self):
        """Ensure all feedback tables exist with proper schema."""
        conn = self._get_db_connection()
        cursor = conn.cursor()
        
        # Enhanced votes table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS votes (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                item_uri TEXT NOT NULL,
                item_type TEXT NOT NULL,  -- 'skill', 'occupation', 'session', 'resource'
                user_id TEXT NOT NULL,
                vote_value INTEGER NOT NULL,  -- -1 (downvote), 0 (neutral), 1 (upvote)
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                UNIQUE(item_uri, user_id, item_type)
            )
        """)
        
        # Enhanced suggestions table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS suggestions (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                item_uri TEXT NOT NULL,
                item_type TEXT NOT NULL,  -- 'skill', 'occupation', 'session', 'general'
                user_id TEXT NOT NULL,
                suggestion_type TEXT NOT NULL,  -- 'add_skill', 'remove_skill', 'reorder', 'add_resource', 'general'
                suggestion_text TEXT NOT NULL,
                status TEXT DEFAULT 'pending',  -- 'pending', 'approved', 'rejected', 'implemented'
                votes_for INTEGER DEFAULT 0,
                votes_against INTEGER DEFAULT 0,
                reviewed_by TEXT,
                reviewed_at TIMESTAMP,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """)
        
        # Suggestion votes (for voting on suggestions themselves)
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS suggestion_votes (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                suggestion_id INTEGER NOT NULL,
                user_id TEXT NOT NULL,
                vote INTEGER NOT NULL,  -- 1 (support), -1 (oppose)
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (suggestion_id) REFERENCES suggestions(id),
                UNIQUE(suggestion_id, user_id)
            )
        """)
        
        # Community curriculum updates
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS curriculum_updates (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                occupation_uri TEXT NOT NULL,
                update_type TEXT NOT NULL,  -- 'add_skill', 'remove_skill', 'update_order', 'update_duration'
                skill_uri TEXT,
                old_value TEXT,
                new_value TEXT,
                reason TEXT,
                proposed_by TEXT NOT NULL,
                status TEXT DEFAULT 'pending',  -- 'pending', 'approved', 'rejected'
                community_score INTEGER DEFAULT 0,
                reviewed_by TEXT,
                reviewed_at TIMESTAMP,
                implemented_at TIMESTAMP,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """)
        
        # Resource quality ratings
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS resource_ratings (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                resource_url TEXT NOT NULL,
                skill_uri TEXT NOT NULL,
                user_id TEXT NOT NULL,
                rating INTEGER NOT NULL,  -- 1-5 stars
                quality_score INTEGER,  -- accuracy, relevance, clarity (1-10)
                review_text TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                UNIQUE(resource_url, user_id)
            )
        """)
        
        conn.commit()
        conn.close()
        print("✅ Community feedback tables initialized")
    
    # ==================== VOTING SYSTEM ====================
    
    def add_vote(self, item_uri: str, item_type: str, user_id: str, vote_value: int) -> Dict:
        """
        Add or update a vote for an item.
        
        Args:
            item_uri: URI of the item being voted on
            item_type: Type of item ('skill', 'occupation', 'session', 'resource')
            user_id: User identifier
            vote_value: -1 (downvote), 0 (neutral), 1 (upvote)
        
        Returns:
            Dict with vote statistics
        """
        if vote_value not in [-1, 0, 1]:
            raise ValueError("Vote value must be -1, 0, or 1")
        
        conn = self._get_db_connection()
        cursor = conn.cursor()
        
        # Insert or replace vote
        cursor.execute("""
            INSERT OR REPLACE INTO votes (item_uri, item_type, user_id, vote_value, created_at)
            VALUES (?, ?, ?, ?, CURRENT_TIMESTAMP)
        """, (item_uri, item_type, user_id, vote_value))
        
        conn.commit()
        
        # Get updated statistics
        stats = self.get_vote_statistics(item_uri, item_type)
        conn.close()
        
        return stats
    
    def get_vote_statistics(self, item_uri: str, item_type: str) -> Dict:
        """Get voting statistics for an item."""
        conn = self._get_db_connection()
        cursor = conn.cursor()
        
        cursor.execute("""
            SELECT 
                COUNT(*) as total_votes,
                SUM(CASE WHEN vote_value = 1 THEN 1 ELSE 0 END) as upvotes,
                SUM(CASE WHEN vote_value = -1 THEN 1 ELSE 0 END) as downvotes,
                SUM(vote_value) as net_score,
                AVG(vote_value) as average_score
            FROM votes
            WHERE item_uri = ? AND item_type = ?
        """, (item_uri, item_type))
        
        result = cursor.fetchone()
        conn.close()
        
        return {
            'total_votes': result[0] or 0,
            'upvotes': result[1] or 0,
            'downvotes': result[2] or 0,
            'net_score': result[3] or 0,
            'average_score': result[4] or 0.0,
            'approval_rate': (result[1] / result[0] * 100) if result[0] > 0 else 0.0
        }
    
    def get_trending_items(self, item_type: str, days: int = 7, limit: int = 10) -> List[Dict]:
        """Get trending items based on recent votes."""
        conn = self._get_db_connection()
        cursor = conn.cursor()
        
        cutoff_date = datetime.now() - timedelta(days=days)
        
        cursor.execute("""
            SELECT 
                v.item_uri,
                COUNT(*) as vote_count,
                SUM(v.vote_value) as net_score,
                AVG(v.vote_value) as avg_score
            FROM votes v
            WHERE v.item_type = ? 
                AND v.created_at >= ?
            GROUP BY v.item_uri
            ORDER BY net_score DESC, vote_count DESC
            LIMIT ?
        """, (item_type, cutoff_date, limit))
        
        results = []
        for row in cursor.fetchall():
            results.append({
                'item_uri': row[0],
                'vote_count': row[1],
                'net_score': row[2],
                'average_score': row[3]
            })
        
        conn.close()
        return results
    
    # ==================== SUGGESTION SYSTEM ====================
    
    def add_suggestion(self, item_uri: str, item_type: str, user_id: str, 
                      suggestion_type: str, suggestion_text: str) -> int:
        """
        Add a new suggestion.
        
        Args:
            item_uri: URI of the item
            item_type: Type of item
            user_id: User identifier
            suggestion_type: Type of suggestion
            suggestion_text: Detailed suggestion text
        
        Returns:
            suggestion_id
        """
        conn = self._get_db_connection()
        cursor = conn.cursor()
        
        cursor.execute("""
            INSERT INTO suggestions 
            (item_uri, item_type, user_id, suggestion_type, suggestion_text, created_at)
            VALUES (?, ?, ?, ?, ?, CURRENT_TIMESTAMP)
        """, (item_uri, item_type, user_id, suggestion_type, suggestion_text))
        
        suggestion_id = cursor.lastrowid
        conn.commit()
        conn.close()
        
        print(f"✅ Suggestion #{suggestion_id} added by {user_id}")
        return suggestion_id
    
    def vote_on_suggestion(self, suggestion_id: int, user_id: str, vote: int) -> Dict:
        """Vote on a suggestion (1 for support, -1 for oppose)."""
        if vote not in [-1, 1]:
            raise ValueError("Vote must be 1 or -1")
        
        conn = self._get_db_connection()
        cursor = conn.cursor()
        
        # Add suggestion vote
        cursor.execute("""
            INSERT OR REPLACE INTO suggestion_votes 
            (suggestion_id, user_id, vote, created_at)
            VALUES (?, ?, ?, CURRENT_TIMESTAMP)
        """, (suggestion_id, user_id, vote))
        
        # Update suggestion vote counts
        cursor.execute("""
            UPDATE suggestions
            SET votes_for = (SELECT COUNT(*) FROM suggestion_votes WHERE suggestion_id = ? AND vote = 1),
                votes_against = (SELECT COUNT(*) FROM suggestion_votes WHERE suggestion_id = ? AND vote = -1)
            WHERE id = ?
        """, (suggestion_id, suggestion_id, suggestion_id))
        
        conn.commit()
        
        # Get updated stats
        cursor.execute("""
            SELECT votes_for, votes_against, status
            FROM suggestions
            WHERE id = ?
        """, (suggestion_id,))
        
        result = cursor.fetchone()
        conn.close()
        
        return {
            'suggestion_id': suggestion_id,
            'votes_for': result[0],
            'votes_against': result[1],
            'status': result[2],
            'net_votes': result[0] - result[1]
        }
    
    def get_pending_suggestions(self, min_community_score: int = 5) -> List[Dict]:
        """Get suggestions pending review with sufficient community support."""
        conn = self._get_db_connection()
        cursor = conn.cursor()
        
        cursor.execute("""
            SELECT 
                id, item_uri, item_type, user_id, suggestion_type, 
                suggestion_text, votes_for, votes_against, created_at
            FROM suggestions
            WHERE status = 'pending' 
                AND (votes_for - votes_against) >= ?
            ORDER BY (votes_for - votes_against) DESC, created_at ASC
        """, (min_community_score,))
        
        suggestions = []
        for row in cursor.fetchall():
            suggestions.append({
                'id': row[0],
                'item_uri': row[1],
                'item_type': row[2],
                'user_id': row[3],
                'suggestion_type': row[4],
                'suggestion_text': row[5],
                'votes_for': row[6],
                'votes_against': row[7],
                'net_votes': row[6] - row[7],
                'created_at': row[8]
            })
        
        conn.close()
        return suggestions
    
    def review_suggestion(self, suggestion_id: int, reviewer_id: str, 
                         status: str, reason: str = None) -> bool:
        """
        Review and approve/reject a suggestion.
        
        Args:
            suggestion_id: ID of the suggestion
            reviewer_id: ID of the reviewer
            status: 'approved' or 'rejected'
            reason: Optional reason for the decision
        """
        if status not in ['approved', 'rejected']:
            raise ValueError("Status must be 'approved' or 'rejected'")
        
        conn = self._get_db_connection()
        cursor = conn.cursor()
        
        cursor.execute("""
            UPDATE suggestions
            SET status = ?,
                reviewed_by = ?,
                reviewed_at = CURRENT_TIMESTAMP
            WHERE id = ?
        """, (status, reviewer_id, suggestion_id))
        
        conn.commit()
        affected = cursor.rowcount
        conn.close()
        
        if affected > 0:
            print(f"✅ Suggestion #{suggestion_id} {status} by {reviewer_id}")
            return True
        return False
    
    def get_suggestion_details(self, suggestion_id: int) -> Optional[Dict]:
        """Get detailed information about a suggestion."""
        conn = self._get_db_connection()
        cursor = conn.cursor()
        
        cursor.execute("""
            SELECT id, item_uri, item_type, user_id, suggestion_type, 
                   suggestion_text, status, votes_for, votes_against,
                   reviewed_by, reviewed_at, created_at
            FROM suggestions
            WHERE id = ?
        """, (suggestion_id,))
        
        row = cursor.fetchone()
        conn.close()
        
        if not row:
            return None
        
        return {
            'id': row[0],
            'item_uri': row[1],
            'item_type': row[2],
            'user_id': row[3],
            'suggestion_type': row[4],
            'suggestion_text': row[5],
            'status': row[6],
            'votes_for': row[7],
            'votes_against': row[8],
            'reviewed_by': row[9],
            'reviewed_at': row[10],
            'created_at': row[11]
        }
    
    def implement_suggestion(self, suggestion_id: int) -> Dict:
        """
        Implement an approved suggestion by updating the database.
        
        This method applies the changes suggested by the community:
        - add_skill: Adds a new skill relationship
        - remove_skill: Removes a skill relationship
        - add_resource: Adds the suggestion as a note/resource
        - modify: Updates the description or details
        
        Returns:
            Dictionary with implementation status and details
        """
        suggestion = self.get_suggestion_details(suggestion_id)
        
        if not suggestion:
            return {'success': False, 'error': 'Suggestion not found'}
        
        if suggestion['status'] != 'approved':
            return {'success': False, 'error': 'Suggestion must be approved first'}
        
        suggestion_type = suggestion['suggestion_type']
        item_uri = suggestion['item_uri']
        suggestion_text = suggestion['suggestion_text']
        
        conn = self._get_db_connection()
        cursor = conn.cursor()
        
        try:
            if suggestion_type == 'add_skill':
                # Extract skill name from suggestion text
                skill_name = self._extract_skill_from_text(suggestion_text)
                
                # Create or get community skill URI
                skill_uri = f"http://data.europa.eu/esco/skill/community-{skill_name.lower().replace(' ', '-')}"
                
                # Add skill to skills table if it doesn't exist
                cursor.execute("""
                    INSERT OR IGNORE INTO skills (concept_uri, preferred_label, description, skill_type)
                    VALUES (?, ?, ?, ?)
                """, (skill_uri, skill_name, f"Community-suggested skill: {suggestion_text}", 'community'))
                
                # Add skill relationship to occupation
                cursor.execute("""
                    INSERT OR IGNORE INTO occupation_skill_relations 
                    (occupation_uri, skill_uri, relation_type)
                    VALUES (?, ?, 'optional')
                """, (item_uri, skill_uri))
                
                # Record implementation
                cursor.execute("""
                    INSERT OR IGNORE INTO suggestions_implemented
                    (suggestion_id, item_uri, implementation_type, implementation_details, implemented_at)
                    VALUES (?, ?, 'skill_suggested', ?, CURRENT_TIMESTAMP)
                """, (suggestion_id, item_uri, suggestion_text))
                
                # Mark suggestion as implemented
                cursor.execute("""
                    UPDATE suggestions
                    SET status = 'implemented'
                    WHERE id = ?
                """, (suggestion_id,))
                
                result = {
                    'success': True,
                    'action': 'skill_added',
                    'message': f'Skill "{skill_name}" added to {item_uri}',
                    'details': suggestion_text,
                    'skill_uri': skill_uri
                }
            
            elif suggestion_type == 'add_resource':
                # Store resource suggestion
                cursor.execute("""
                    INSERT OR IGNORE INTO suggestions_implemented
                    (suggestion_id, item_uri, implementation_type, implementation_details, implemented_at)
                    VALUES (?, ?, 'resource_added', ?, CURRENT_TIMESTAMP)
                """, (suggestion_id, item_uri, suggestion_text))
                
                cursor.execute("""
                    UPDATE suggestions
                    SET status = 'implemented'
                    WHERE id = ?
                """, (suggestion_id,))
                
                result = {
                    'success': True,
                    'action': 'resource_added',
                    'message': f'Resource suggestion added for {item_uri}',
                    'details': suggestion_text
                }
            
            elif suggestion_type in ['modify', 'improve_description', 'reorder']:
                # Store improvement suggestion for manual review
                cursor.execute("""
                    INSERT OR IGNORE INTO suggestions_implemented
                    (suggestion_id, item_uri, implementation_type, implementation_details, implemented_at)
                    VALUES (?, ?, ?, ?, CURRENT_TIMESTAMP)
                """, (suggestion_id, item_uri, suggestion_type, suggestion_text))
                
                cursor.execute("""
                    UPDATE suggestions
                    SET status = 'implemented'
                    WHERE id = ?
                """, (suggestion_id,))
                
                result = {
                    'success': True,
                    'action': suggestion_type,
                    'message': f'Suggestion recorded for manual implementation',
                    'details': suggestion_text
                }
            
            else:
                # General suggestion - just mark as noted
                cursor.execute("""
                    UPDATE suggestions
                    SET status = 'implemented'
                    WHERE id = ?
                """, (suggestion_id,))
                
                result = {
                    'success': True,
                    'action': 'noted',
                    'message': 'Suggestion acknowledged',
                    'details': suggestion_text
                }
            
            conn.commit()
            conn.close()
            
            print(f"✅ Implemented suggestion #{suggestion_id}: {suggestion_type}")
            return result
            
        except Exception as e:
            conn.rollback()
            conn.close()
            return {'success': False, 'error': str(e)}
    
    def _ensure_implementation_table(self):
        """Ensure the suggestions_implemented table exists."""
        conn = self._get_db_connection()
        cursor = conn.cursor()
        
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS suggestions_implemented (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                suggestion_id INTEGER NOT NULL,
                item_uri TEXT NOT NULL,
                implementation_type TEXT NOT NULL,
                implementation_details TEXT,
                implemented_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (suggestion_id) REFERENCES suggestions(id)
            )
        """)
        
        conn.commit()
        conn.close()
    
    def _extract_skill_from_text(self, text: str) -> str:
        """Extract skill name from suggestion text."""
        import re
        
        # Common patterns: "Add X", "Include X", "Should add X", "X is important"
        patterns = [
            r'(?:add|include|suggest|need)\s+([A-Z][a-zA-Z\s\.]+?)(?:\s+(?:skill|for|to|as)|\s*$)',
            r'([A-Z][a-zA-Z\s\.]+?)\s+(?:is|should be|must be)',
            r'(?:skill|technology):\s*([A-Z][a-zA-Z\s\.]+)',
        ]
        
        for pattern in patterns:
            match = re.search(pattern, text, re.IGNORECASE)
            if match:
                skill = match.group(1).strip()
                # Clean up common words
                skill = re.sub(r'\s+(skill|technology|tool|framework)s?\s*$', '', skill, flags=re.IGNORECASE)
                return skill.title()
        
        # Fallback: look for capitalized words
        words = text.split()
        for i, word in enumerate(words):
            if word[0].isupper() and len(word) > 2:
                # Take up to 3 consecutive capitalized/technical words
                skill_parts = [word]
                for j in range(i+1, min(i+3, len(words))):
                    if words[j][0].isupper() or words[j].lower() in ['and', 'for', 'with']:
                        skill_parts.append(words[j])
                    else:
                        break
                return ' '.join(skill_parts)
        
        # Ultimate fallback
        return "Community Suggested Skill"
    
    def get_community_skills_for_occupation(self, occupation_uri: str) -> List[Dict]:
        """Get community-added skills for an occupation."""
        conn = self._get_db_connection()
        cursor = conn.cursor()
        
        cursor.execute("""
            SELECT DISTINCT s.concept_uri, s.preferred_label, s.description
            FROM skills s
            JOIN occupation_skill_relations osr ON s.concept_uri = osr.skill_uri
            WHERE osr.occupation_uri = ?
              AND s.skill_type = 'community'
        """, (occupation_uri,))
        
        skills = []
        for row in cursor.fetchall():
            skills.append({
                'uri': row[0],
                'label': row[1],
                'description': row[2],
                'source': 'community'
            })
        
        conn.close()
        return skills

    
    # ==================== CURRICULUM UPDATE SYSTEM ====================
    
    def propose_curriculum_update(self, occupation_uri: str, update_type: str,
                                  proposed_by: str, skill_uri: str = None,
                                  old_value: str = None, new_value: str = None,
                                  reason: str = None) -> int:
        """Propose a curriculum update for community review."""
        conn = self._get_db_connection()
        cursor = conn.cursor()
        
        cursor.execute("""
            INSERT INTO curriculum_updates
            (occupation_uri, update_type, skill_uri, old_value, new_value, 
             reason, proposed_by, created_at)
            VALUES (?, ?, ?, ?, ?, ?, ?, CURRENT_TIMESTAMP)
        """, (occupation_uri, update_type, skill_uri, old_value, new_value, 
              reason, proposed_by))
        
        update_id = cursor.lastrowid
        conn.commit()
        conn.close()
        
        print(f"✅ Curriculum update #{update_id} proposed")
        return update_id
    
    def vote_on_curriculum_update(self, update_id: int, vote: int):
        """Vote on a curriculum update proposal."""
        conn = self._get_db_connection()
        cursor = conn.cursor()
        
        cursor.execute("""
            UPDATE curriculum_updates
            SET community_score = community_score + ?
            WHERE id = ?
        """, (vote, update_id))
        
        conn.commit()
        conn.close()
    
    def get_approved_curriculum_updates(self, min_score: int = 10) -> List[Dict]:
        """Get curriculum updates approved by the community."""
        conn = self._get_db_connection()
        cursor = conn.cursor()
        
        cursor.execute("""
            SELECT id, occupation_uri, update_type, skill_uri, 
                   old_value, new_value, reason, community_score
            FROM curriculum_updates
            WHERE status = 'approved' 
                AND community_score >= ?
                AND implemented_at IS NULL
            ORDER BY community_score DESC
        """, (min_score,))
        
        updates = []
        for row in cursor.fetchall():
            updates.append({
                'id': row[0],
                'occupation_uri': row[1],
                'update_type': row[2],
                'skill_uri': row[3],
                'old_value': row[4],
                'new_value': row[5],
                'reason': row[6],
                'community_score': row[7]
            })
        
        conn.close()
        return updates
    
    def implement_curriculum_update(self, update_id: int) -> bool:
        """Mark a curriculum update as implemented."""
        conn = self._get_db_connection()
        cursor = conn.cursor()
        
        cursor.execute("""
            UPDATE curriculum_updates
            SET implemented_at = CURRENT_TIMESTAMP,
                status = 'implemented'
            WHERE id = ?
        """, (update_id,))
        
        conn.commit()
        affected = cursor.rowcount
        conn.close()
        
        return affected > 0
    
    # ==================== RESOURCE RATING SYSTEM ====================
    
    def rate_resource(self, resource_url: str, skill_uri: str, user_id: str,
                     rating: int, quality_score: int = None, 
                     review_text: str = None) -> Dict:
        """Rate a learning resource."""
        if not (1 <= rating <= 5):
            raise ValueError("Rating must be between 1 and 5")
        
        if quality_score and not (1 <= quality_score <= 10):
            raise ValueError("Quality score must be between 1 and 10")
        
        conn = self._get_db_connection()
        cursor = conn.cursor()
        
        cursor.execute("""
            INSERT OR REPLACE INTO resource_ratings
            (resource_url, skill_uri, user_id, rating, quality_score, 
             review_text, created_at)
            VALUES (?, ?, ?, ?, ?, ?, CURRENT_TIMESTAMP)
        """, (resource_url, skill_uri, user_id, rating, quality_score, review_text))
        
        conn.commit()
        
        # Get average rating for this resource
        stats = self.get_resource_statistics(resource_url, skill_uri)
        conn.close()
        
        return stats
    
    def get_resource_statistics(self, resource_url: str, skill_uri: str) -> Dict:
        """Get statistics for a specific resource."""
        conn = self._get_db_connection()
        cursor = conn.cursor()
        
        cursor.execute("""
            SELECT 
                COUNT(*) as total_ratings,
                AVG(rating) as avg_rating,
                AVG(quality_score) as avg_quality,
                MIN(rating) as min_rating,
                MAX(rating) as max_rating
            FROM resource_ratings
            WHERE resource_url = ? AND skill_uri = ?
        """, (resource_url, skill_uri))
        
        result = cursor.fetchone()
        conn.close()
        
        return {
            'resource_url': resource_url,
            'skill_uri': skill_uri,
            'total_ratings': result[0] or 0,
            'average_rating': round(result[1], 2) if result[1] else 0.0,
            'average_quality': round(result[2], 2) if result[2] else 0.0,
            'min_rating': result[3] or 0,
            'max_rating': result[4] or 0
        }
    
    def get_top_rated_resources(self, skill_uri: str, min_ratings: int = 3, 
                               limit: int = 10) -> List[Dict]:
        """Get top-rated resources for a skill."""
        conn = self._get_db_connection()
        cursor = conn.cursor()
        
        cursor.execute("""
            SELECT 
                resource_url,
                COUNT(*) as rating_count,
                AVG(rating) as avg_rating,
                AVG(quality_score) as avg_quality
            FROM resource_ratings
            WHERE skill_uri = ?
            GROUP BY resource_url
            HAVING COUNT(*) >= ?
            ORDER BY AVG(rating) DESC, COUNT(*) DESC
            LIMIT ?
        """, (skill_uri, min_ratings, limit))
        
        resources = []
        for row in cursor.fetchall():
            resources.append({
                'resource_url': row[0],
                'rating_count': row[1],
                'average_rating': round(row[2], 2),
                'average_quality': round(row[3], 2) if row[3] else None
            })
        
        conn.close()
        return resources
    
    # ==================== ANALYTICS ====================
    
    def get_community_metrics(self) -> Dict:
        """Get overall community engagement metrics."""
        conn = self._get_db_connection()
        cursor = conn.cursor()
        
        # Total votes
        cursor.execute("SELECT COUNT(*) FROM votes")
        total_votes = cursor.fetchone()[0]
        
        # Total suggestions
        cursor.execute("SELECT COUNT(*) FROM suggestions")
        total_suggestions = cursor.fetchone()[0]
        
        # Pending suggestions
        cursor.execute("SELECT COUNT(*) FROM suggestions WHERE status = 'pending'")
        pending_suggestions = cursor.fetchone()[0]
        
        # Approved suggestions
        cursor.execute("SELECT COUNT(*) FROM suggestions WHERE status = 'approved'")
        approved_suggestions = cursor.fetchone()[0]
        
        # Implemented suggestions
        cursor.execute("SELECT COUNT(*) FROM suggestions WHERE status = 'implemented'")
        implemented_suggestions = cursor.fetchone()[0]
        
        # Active users (last 30 days)
        cursor.execute("""
            SELECT COUNT(DISTINCT user_id) 
            FROM votes 
            WHERE created_at >= datetime('now', '-30 days')
        """)
        active_users = cursor.fetchone()[0]
        
        # Resource ratings
        cursor.execute("SELECT COUNT(*), AVG(rating) FROM resource_ratings")
        rating_data = cursor.fetchone()
        
        conn.close()
        
        return {
            'total_votes': total_votes,
            'total_suggestions': total_suggestions,
            'pending_suggestions': pending_suggestions,
            'approved_suggestions': approved_suggestions,
            'implemented_suggestions': implemented_suggestions,
            'active_users_30d': active_users,
            'total_resource_ratings': rating_data[0] or 0,
            'average_resource_rating': round(rating_data[1], 2) if rating_data[1] else 0.0
        }

if __name__ == "__main__":
    # Example usage
    feedback = CommunityFeedbackSystem()
    
    # Test voting
    stats = feedback.add_vote(
        "http://data.europa.eu/esco/skill/example",
        "skill",
        "user123",
        1
    )
    print(f"Vote stats: {stats}")
    
    # Test suggestion
    suggestion_id = feedback.add_suggestion(
        "http://data.europa.eu/esco/occupation/data-scientist",
        "occupation",
        "user123",
        "add_skill",
        "Should add TensorFlow as a required skill"
    )
    print(f"Created suggestion: {suggestion_id}")
    
    # Get metrics
    metrics = feedback.get_community_metrics()
    print(f"Community metrics: {metrics}")
