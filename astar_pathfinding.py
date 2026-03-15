"""
A* Pathfinding Algorithm for Optimal Learning Routes
Finds the most efficient path through skill dependencies considering multiple factors.
"""

import heapq
import networkx as nx
from typing import List, Dict, Tuple, Set, Optional
import numpy as np


class AStarLearningPath:
    """
    A* algorithm implementation for finding optimal learning paths.
    
    The algorithm considers:
    - Skill dependencies (prerequisites must come first)
    - Learning difficulty (estimated time/effort)
    - User's current skill level
    - Community feedback scores
    - Career relevance
    """
    
    def __init__(self, skill_graph: nx.DiGraph, community_votes: Dict[str, int] = None):
        """
        Initialize A* pathfinder with skill dependency graph.
        
        Args:
            skill_graph: NetworkX directed graph where nodes are skills
                        and edges represent dependencies
            community_votes: Dictionary mapping skill URIs to vote scores
        """
        self.graph = skill_graph
        self.community_votes = community_votes or {}
        
    def heuristic(self, skill_uri: str, goal_skills: Set[str], 
                  user_current_skills: Set[str]) -> float:
        """
        Heuristic function (h) estimating cost from current skill to goal.
        
        Uses multiple factors:
        1. Distance to goal (graph-based)
        2. Skill difficulty
        3. Community feedback
        4. Career relevance
        
        Lower score = better (closer to goal, easier, more valuable)
        """
        if skill_uri in goal_skills:
            return 0.0
        
        skill_data = self.graph.nodes.get(skill_uri, {})
        
        # Factor 1: Estimated learning time (difficulty)
        difficulty_hours = skill_data.get('estimated_hours', 6.0)
        
        # Factor 2: Community feedback (negative because higher votes = better)
        community_score = self.community_votes.get(skill_uri, 0)
        community_penalty = max(0, 5 - community_score)  # Penalize low-voted skills
        
        # Factor 3: Priority/relevance to career
        priority = skill_data.get('priority', 0.5)
        priority_bonus = (1.0 - priority) * 3  # Lower priority = higher cost
        
        # Factor 4: Number of remaining dependencies
        descendants = nx.descendants(self.graph, skill_uri) if skill_uri in self.graph else set()
        remaining_deps = len(descendants.intersection(goal_skills))
        
        # Combined heuristic (weighted sum)
        h_score = (
            difficulty_hours * 0.4 +          # Learning time weight
            community_penalty * 0.2 +          # Community feedback weight
            priority_bonus * 0.3 +             # Career relevance weight
            remaining_deps * 0.1               # Dependency chain weight
        )
        
        return h_score
    
    def cost(self, from_skill: str, to_skill: str) -> float:
        """
        Actual cost function (g) of moving from one skill to another.
        
        Represents real effort required to learn the skill.
        """
        to_skill_data = self.graph.nodes.get(to_skill, {})
        
        # Base cost: learning time
        base_cost = to_skill_data.get('estimated_hours', 6.0)
        
        # Relation type modifier
        edge_data = self.graph.get_edge_data(from_skill, to_skill, {})
        relation_type = edge_data.get('relation_type', 'optional')
        
        # Essential skills have lower cost (higher priority)
        if relation_type == 'essential':
            cost_modifier = 0.8
        elif relation_type == 'optional':
            cost_modifier = 1.2
        else:
            cost_modifier = 1.0
        
        return base_cost * cost_modifier
    
    def reconstruct_path(self, came_from: Dict[str, str], 
                        current: str) -> List[str]:
        """Reconstruct the path from start to goal."""
        path = [current]
        while current in came_from:
            current = came_from[current]
            path.append(current)
        path.reverse()
        return path
    
    def find_optimal_path(self, 
                         start_skills: List[str],
                         goal_skills: List[str],
                         user_current_skills: List[str] = None) -> Dict:
        """
        Find optimal learning path using A* algorithm.
        
        Args:
            start_skills: Skills to start from (prerequisites already learned)
            goal_skills: Target skills to achieve
            user_current_skills: Skills user already has
            
        Returns:
            Dictionary containing:
            - path: Ordered list of skills to learn
            - total_cost: Estimated total learning time
            - path_details: Detailed information about each step
        """
        if user_current_skills is None:
            user_current_skills = []
        
        goal_set = set(goal_skills)
        current_skill_set = set(user_current_skills)
        
        # Priority queue: (f_score, skill_uri)
        # f_score = g_score + h_score
        open_set = []
        
        # For each skill, track best path cost (g_score)
        g_score = {skill: float('inf') for skill in self.graph.nodes}
        
        # For each skill, track estimated total cost (f_score)
        f_score = {skill: float('inf') for skill in self.graph.nodes}
        
        # Track the path
        came_from = {}
        
        # Initialize with start skills
        virtual_start = "__START__"
        g_score[virtual_start] = 0
        f_score[virtual_start] = 0
        
        heapq.heappush(open_set, (0, virtual_start))
        
        # Track visited nodes to avoid cycles
        closed_set = set()
        
        # Track skills learned in order
        learning_sequence = []
        total_learning_cost = 0
        
        while open_set:
            current_f, current = heapq.heappop(open_set)
            
            # Skip if already processed
            if current in closed_set:
                continue
            
            closed_set.add(current)
            
            # Check if we've learned all goal skills
            if current != virtual_start:
                learning_sequence.append(current)
                if current in goal_set:
                    goal_set.remove(current)
                    
            if not goal_set:
                # All goals achieved!
                break
            
            # Get neighbors (next skills to learn)
            if current == virtual_start:
                neighbors = start_skills
            else:
                neighbors = list(self.graph.successors(current)) if current in self.graph else []
            
            for neighbor in neighbors:
                if neighbor in closed_set:
                    continue
                
                # Calculate tentative g_score
                if current == virtual_start:
                    tentative_g = 0
                else:
                    tentative_g = g_score[current] + self.cost(current, neighbor)
                
                # If this path is better than previous
                if tentative_g < g_score[neighbor]:
                    came_from[neighbor] = current
                    g_score[neighbor] = tentative_g
                    f_score[neighbor] = tentative_g + self.heuristic(
                        neighbor, goal_set, current_skill_set
                    )
                    
                    heapq.heappush(open_set, (f_score[neighbor], neighbor))
        
        # Build detailed path information
        path_details = []
        for i, skill_uri in enumerate(learning_sequence):
            skill_data = self.graph.nodes.get(skill_uri, {})
            detail = {
                'order': i + 1,
                'skill_uri': skill_uri,
                'skill_name': skill_data.get('label', skill_uri),
                'estimated_hours': skill_data.get('estimated_hours', 6.0),
                'priority': skill_data.get('priority', 0.5),
                'relation_type': skill_data.get('relation_type', 'optional'),
                'community_score': self.community_votes.get(skill_uri, 0),
                'g_score': g_score.get(skill_uri, 0),
                'reason': self._get_skill_reason(skill_uri, came_from)
            }
            path_details.append(detail)
            total_learning_cost += detail['estimated_hours']
        
        return {
            'path': learning_sequence,
            'total_cost': total_learning_cost,
            'path_details': path_details,
            'algorithm': 'A* Pathfinding',
            'skills_learned': len(learning_sequence),
            'estimated_weeks': round(total_learning_cost / 40, 1)  # Assuming 40 hours/week
        }
    
    def _get_skill_reason(self, skill_uri: str, came_from: Dict[str, str]) -> str:
        """Generate explanation for why this skill is in the path."""
        if skill_uri not in came_from:
            return "Starting skill"
        
        predecessor = came_from[skill_uri]
        if predecessor == "__START__":
            return "Foundation skill for learning path"
        
        skill_data = self.graph.nodes.get(skill_uri, {})
        relation = skill_data.get('relation_type', 'optional')
        
        if relation == 'essential':
            return f"Essential skill, prerequisite for advanced topics"
        elif relation == 'optional':
            return f"Recommended skill to enhance capabilities"
        else:
            return f"Skill in optimal learning sequence"
    
    def compare_with_topological(self, topological_path: List[str], 
                                 astar_path: List[str]) -> Dict:
        """
        Compare A* path with simple topological sorting.
        
        Shows benefits of A* optimization.
        """
        def calculate_path_metrics(path):
            total_time = 0
            total_priority = 0
            total_community = 0
            
            for skill in path:
                skill_data = self.graph.nodes.get(skill, {})
                total_time += skill_data.get('estimated_hours', 6.0)
                total_priority += skill_data.get('priority', 0.5)
                total_community += self.community_votes.get(skill, 0)
            
            return {
                'total_hours': total_time,
                'avg_priority': total_priority / len(path) if path else 0,
                'total_community_score': total_community,
                'num_skills': len(path)
            }
        
        topo_metrics = calculate_path_metrics(topological_path)
        astar_metrics = calculate_path_metrics(astar_path)
        
        improvement = {
            'time_saved_hours': topo_metrics['total_hours'] - astar_metrics['total_hours'],
            'time_saved_percent': (
                (topo_metrics['total_hours'] - astar_metrics['total_hours']) / 
                topo_metrics['total_hours'] * 100
            ) if topo_metrics['total_hours'] > 0 else 0,
            'priority_improvement': astar_metrics['avg_priority'] - topo_metrics['avg_priority'],
            'community_score_improvement': (
                astar_metrics['total_community_score'] - topo_metrics['total_community_score']
            )
        }
        
        return {
            'topological_sort': topo_metrics,
            'astar_algorithm': astar_metrics,
            'improvement': improvement,
            'recommendation': 'A* Algorithm' if improvement['time_saved_hours'] > 2 else 'Both Similar'
        }
