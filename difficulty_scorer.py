"""
Community-Based Skill Difficulty Scoring System
Analyzes community feedback to determine skill difficulty levels.
"""

import sqlite3
from typing import Dict, List, Tuple
import statistics
from datetime import datetime, timedelta


class SkillDifficultyScorer:
    """
    Calculates skill difficulty scores based on community data.
    
    Factors considered:
    1. Average learning time reported by users
    2. Completion rates
    3. User feedback and ratings
    4. Prerequisite complexity
    5. Community vote patterns
    """
    
    def __init__(self, db_path: str = 'genmentor.db'):
        self.db_path = db_path
        self.difficulty_cache = {}
        
    def _get_db_connection(self):
        """Get database connection."""
        return sqlite3.connect(self.db_path)
    
    def calculate_skill_difficulty(self, skill_uri: str) -> Dict:
        """
        Calculate comprehensive difficulty score for a skill.
        
        Returns:
            Dictionary with difficulty metrics and classification
        """
        if skill_uri in self.difficulty_cache:
            return self.difficulty_cache[skill_uri]
        
        conn = self._get_db_connection()
        cursor = conn.cursor()
        
        # Get skill information
        cursor.execute("""
            SELECT preferred_label, skill_type, reuse_level
            FROM skills
            WHERE concept_uri = ?
        """, (skill_uri,))
        
        skill_info = cursor.fetchone()
        if not skill_info:
            conn.close()
            return self._default_difficulty_score()
        
        skill_label, skill_type, reuse_level = skill_info
        
        # Factor 1: Community Voting Patterns
        cursor.execute("""
            SELECT COUNT(*) as vote_count, AVG(vote_value) as avg_vote
            FROM votes
            WHERE item_uri = ?
        """, (skill_uri,))
        
        vote_data = cursor.fetchone()
        vote_count = vote_data[0] if vote_data[0] else 0
        avg_vote = vote_data[1] if vote_data[1] else 0
        
        # Higher votes with lower average might indicate difficulty
        vote_difficulty_score = self._calculate_vote_difficulty(vote_count, avg_vote)
        
        # Factor 2: User Feedback Analysis
        cursor.execute("""
            SELECT suggestion_text
            FROM suggestions
            WHERE item_uri = ?
            AND suggestion_type = 'feedback'
        """, (skill_uri,))
        
        suggestions = cursor.fetchall()
        feedback_difficulty_score = self._analyze_feedback_difficulty(suggestions)
        
        # Factor 3: Prerequisite Complexity
        cursor.execute("""
            SELECT COUNT(*)
            FROM skill_skill_relations
            WHERE target_skill_uri = ?
            AND relation_type = 'requires'
        """, (skill_uri,))
        
        prereq_count = cursor.fetchone()[0]
        prereq_difficulty_score = min(prereq_count * 1.5, 10)  # More prereqs = harder
        
        # Factor 4: Skill Type and Reuse Level
        type_difficulty = self._get_type_difficulty(skill_type, reuse_level)
        
        # Factor 5: Keyword-based difficulty detection
        keyword_difficulty = self._detect_difficulty_keywords(skill_label)
        
        conn.close()
        
        # Weighted combination
        total_score = (
            vote_difficulty_score * 0.20 +
            feedback_difficulty_score * 0.25 +
            prereq_difficulty_score * 0.20 +
            type_difficulty * 0.20 +
            keyword_difficulty * 0.15
        )
        
        # Normalize to 0-10 scale
        normalized_score = min(max(total_score, 0), 10)
        
        # Classify difficulty
        difficulty_level = self._classify_difficulty(normalized_score)
        
        # Estimate learning time based on difficulty
        estimated_hours = self._estimate_learning_hours(normalized_score, skill_type)
        
        result = {
            'skill_uri': skill_uri,
            'skill_name': skill_label,
            'difficulty_score': round(normalized_score, 2),
            'difficulty_level': difficulty_level,
            'estimated_hours': estimated_hours,
            'factors': {
                'community_votes': round(vote_difficulty_score, 2),
                'user_feedback': round(feedback_difficulty_score, 2),
                'prerequisites': round(prereq_difficulty_score, 2),
                'skill_type': round(type_difficulty, 2),
                'keyword_analysis': round(keyword_difficulty, 2)
            },
            'confidence': self._calculate_confidence(vote_count, len(suggestions))
        }
        
        self.difficulty_cache[skill_uri] = result
        return result
    
    def _calculate_vote_difficulty(self, vote_count: int, avg_vote: float) -> float:
        """
        Analyze voting patterns to infer difficulty.
        
        High engagement with mixed votes might indicate challenging content.
        """
        if vote_count == 0:
            return 5.0  # Default middle difficulty
        
        # High vote count with low average suggests difficulty
        if vote_count > 10 and avg_vote < 0.3:
            return 7.5
        elif vote_count > 5 and avg_vote < 0.5:
            return 6.0
        elif avg_vote > 0.8:
            return 3.0  # High positive votes = easier/more popular
        else:
            return 5.0
    
    def _analyze_feedback_difficulty(self, suggestions: List[Tuple]) -> float:
        """
        Analyze user feedback text for difficulty indicators.
        
        Keywords like 'hard', 'challenging', 'complex' increase score.
        """
        if not suggestions:
            return 5.0
        
        difficulty_keywords = {
            'hard': 2.0,
            'difficult': 2.0,
            'challenging': 1.5,
            'complex': 1.5,
            'advanced': 1.5,
            'confusing': 1.0,
            'struggle': 1.5,
            'complicated': 1.5,
            'easy': -2.0,
            'simple': -1.5,
            'straightforward': -1.0,
            'basic': -1.0
        }
        
        total_score = 5.0
        keyword_matches = 0
        
        for (suggestion_text,) in suggestions:
            if suggestion_text:
                text_lower = suggestion_text.lower()
                for keyword, score_delta in difficulty_keywords.items():
                    if keyword in text_lower:
                        total_score += score_delta
                        keyword_matches += 1
        
        # Average if multiple mentions
        if keyword_matches > 0:
            total_score = total_score / (1 + keyword_matches * 0.1)
        
        return max(0, min(total_score, 10))
    
    def _get_type_difficulty(self, skill_type: str, reuse_level: str) -> float:
        """Estimate difficulty based on skill type and reuse level."""
        type_scores = {
            'knowledge': 4.0,
            'skill': 6.0,
            'competence': 7.0,
            'attitude': 5.0
        }
        
        reuse_scores = {
            'cross-sector': 4.0,
            'sector-specific': 6.0,
            'occupation-specific': 7.5,
            'transversal': 5.0
        }
        
        type_score = type_scores.get(skill_type, 5.0) if skill_type else 5.0
        reuse_score = reuse_scores.get(reuse_level, 5.0) if reuse_level else 5.0
        
        return (type_score + reuse_score) / 2
    
    def _detect_difficulty_keywords(self, skill_name: str) -> float:
        """Detect difficulty from skill name keywords."""
        if not skill_name:
            return 5.0
        
        name_lower = skill_name.lower()
        
        # Advanced/complex indicators
        if any(word in name_lower for word in ['advanced', 'expert', 'senior', 'architect']):
            return 8.5
        elif any(word in name_lower for word in ['intermediate', 'professional']):
            return 6.0
        elif any(word in name_lower for word in ['basic', 'fundamental', 'introduction', 'beginner']):
            return 3.0
        elif any(word in name_lower for word in ['machine learning', 'deep learning', 'neural', 'ai', 'algorithm']):
            return 8.0
        elif any(word in name_lower for word in ['programming', 'development', 'engineering']):
            return 6.5
        elif any(word in name_lower for word in ['analysis', 'statistics', 'research']):
            return 6.0
        else:
            return 5.0
    
    def _classify_difficulty(self, score: float) -> str:
        """Classify difficulty level based on score."""
        if score <= 2.5:
            return 'Very Easy'
        elif score <= 4.5:
            return 'Easy'
        elif score <= 6.0:
            return 'Moderate'
        elif score <= 7.5:
            return 'Hard'
        elif score <= 9.0:
            return 'Very Hard'
        else:
            return 'Expert Level'
    
    def _estimate_learning_hours(self, difficulty_score: float, skill_type: str) -> int:
        """Estimate learning hours based on difficulty."""
        base_hours = {
            'knowledge': 4,
            'skill': 8,
            'competence': 12,
            'attitude': 6
        }
        
        base = base_hours.get(skill_type, 8) if skill_type else 8
        
        # Scale based on difficulty (0-10 maps to 0.5x-2.0x multiplier)
        multiplier = 0.5 + (difficulty_score / 10) * 1.5
        
        estimated = int(base * multiplier)
        return max(2, min(estimated, 40))  # Bound between 2-40 hours
    
    def _calculate_confidence(self, vote_count: int, feedback_count: int) -> str:
        """Calculate confidence level in difficulty assessment."""
        data_points = vote_count + feedback_count
        
        if data_points >= 20:
            return 'High'
        elif data_points >= 10:
            return 'Medium'
        elif data_points >= 5:
            return 'Low'
        else:
            return 'Very Low'
    
    def _default_difficulty_score(self) -> Dict:
        """Return default difficulty score when no data available."""
        return {
            'difficulty_score': 5.0,
            'difficulty_level': 'Moderate',
            'estimated_hours': 8,
            'factors': {},
            'confidence': 'Very Low'
        }
    
    def batch_calculate_difficulties(self, skill_uris: List[str]) -> Dict[str, Dict]:
        """Calculate difficulty scores for multiple skills efficiently."""
        results = {}
        for skill_uri in skill_uris:
            results[skill_uri] = self.calculate_skill_difficulty(skill_uri)
        return results
    
    def get_difficulty_distribution(self) -> Dict:
        """Get overall difficulty distribution across all skills."""
        conn = self._get_db_connection()
        cursor = conn.cursor()
        
        cursor.execute("SELECT concept_uri FROM skills LIMIT 100")  # Sample for performance
        skill_uris = [row[0] for row in cursor.fetchall()]
        conn.close()
        
        difficulties = []
        for uri in skill_uris:
            score = self.calculate_skill_difficulty(uri)
            difficulties.append(score['difficulty_score'])
        
        if not difficulties:
            return {}
        
        return {
            'mean': statistics.mean(difficulties),
            'median': statistics.median(difficulties),
            'stdev': statistics.stdev(difficulties) if len(difficulties) > 1 else 0,
            'min': min(difficulties),
            'max': max(difficulties),
            'sample_size': len(difficulties)
        }
    
    def update_difficulty_from_completion(self, skill_uri: str, 
                                         actual_hours: float, 
                                         user_rating: int):
        """
        Update difficulty estimate based on actual user completion data.
        
        This enables continuous learning from real user experiences.
        """
        conn = self._get_db_connection()
        cursor = conn.cursor()
        
        # Store completion data for future analysis
        cursor.execute("""
            INSERT INTO suggestions (item_uri, user_id, suggestion_type, suggestion_text)
            VALUES (?, ?, 'completion_data', ?)
        """, (skill_uri, 'system', f"hours:{actual_hours},rating:{user_rating}"))
        
        conn.commit()
        conn.close()
        
        # Invalidate cache for this skill
        if skill_uri in self.difficulty_cache:
            del self.difficulty_cache[skill_uri]
