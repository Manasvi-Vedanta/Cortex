"""
Retrieval-Augmented Generation (RAG) System for Skill Learning
Combines vector database retrieval with LLM generation for enhanced content quality.
"""

import numpy as np
from typing import List, Dict, Optional, Tuple
import pickle
import os
from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity
import json


class SkillKnowledgeBase:
    """
    Vector database for skill-specific knowledge.
    Stores and retrieves relevant information for content generation.
    """
    
    def __init__(self, model_name: str = 'all-mpnet-base-v2', 
                 knowledge_path: str = 'skill_knowledge_base.pkl'):
        """
        Initialize RAG knowledge base.
        
        Args:
            model_name: Sentence transformer model for embeddings
            knowledge_path: Path to stored knowledge base
        """
        self.model = SentenceTransformer(model_name)
        self.knowledge_path = knowledge_path
        self.knowledge_base = {
            'documents': [],
            'embeddings': [],
            'metadata': []
        }
        
        self._load_or_initialize()
        
    def _load_or_initialize(self):
        """Load existing knowledge base or initialize new one."""
        if os.path.exists(self.knowledge_path):
            print(f"Loading knowledge base from {self.knowledge_path}...")
            with open(self.knowledge_path, 'rb') as f:
                self.knowledge_base = pickle.load(f)
            print(f"Loaded {len(self.knowledge_base['documents'])} knowledge documents")
        else:
            print("Initializing new knowledge base...")
            self._initialize_default_knowledge()
    
    def _initialize_default_knowledge(self):
        """Initialize with default skill knowledge."""
        default_knowledge = [
            {
                'skill_category': 'programming',
                'content': """
                Programming fundamentals include understanding variables, data types, control structures (if/else, loops),
                functions, and basic algorithms. Key concepts: syntax, debugging, problem-solving approach, code organization.
                Best practices: write readable code, use meaningful variable names, comment your code, test thoroughly.
                Common learning path: syntax → data structures → algorithms → design patterns → system design.
                """,
                'tags': ['programming', 'coding', 'software development', 'python', 'javascript']
            },
            {
                'skill_category': 'data_science',
                'content': """
                Data science combines statistics, programming, and domain knowledge to extract insights from data.
                Core skills: Python/R programming, statistics, machine learning, data visualization, SQL databases.
                Typical workflow: data collection → cleaning → exploratory analysis → modeling → visualization → communication.
                Key tools: Pandas, NumPy, Scikit-learn, Matplotlib, Jupyter notebooks, SQL databases.
                """,
                'tags': ['data science', 'machine learning', 'statistics', 'python', 'analytics']
            },
            {
                'skill_category': 'machine_learning',
                'content': """
                Machine learning enables computers to learn from data without explicit programming.
                Main types: supervised learning (labeled data), unsupervised learning (patterns), reinforcement learning (rewards).
                Common algorithms: linear regression, decision trees, random forests, neural networks, clustering.
                Prerequisites: Python programming, statistics, linear algebra, calculus basics.
                Learning approach: theory → implementation → practice with real datasets → model tuning → deployment.
                """,
                'tags': ['machine learning', 'AI', 'neural networks', 'deep learning', 'algorithms']
            },
            {
                'skill_category': 'database',
                'content': """
                Databases store and organize data for efficient retrieval and manipulation.
                SQL databases: structured data with tables, relationships, ACID properties (MySQL, PostgreSQL, SQL Server).
                NoSQL databases: flexible schemas for unstructured data (MongoDB, Cassandra, Redis).
                Key concepts: queries, indexes, joins, normalization, transactions, optimization.
                Essential SQL: SELECT, INSERT, UPDATE, DELETE, JOINs, WHERE, GROUP BY, aggregate functions.
                """,
                'tags': ['database', 'SQL', 'MySQL', 'PostgreSQL', 'data management']
            },
            {
                'skill_category': 'statistics',
                'content': """
                Statistics provides methods for collecting, analyzing, and interpreting data.
                Descriptive statistics: mean, median, mode, variance, standard deviation, distributions.
                Inferential statistics: hypothesis testing, confidence intervals, p-values, significance levels.
                Key concepts: sampling, probability, correlation vs causation, regression analysis.
                Applications: A/B testing, experimentation, data-driven decision making, quality control.
                """,
                'tags': ['statistics', 'data analysis', 'probability', 'hypothesis testing']
            },
            {
                'skill_category': 'web_development',
                'content': """
                Web development involves creating websites and web applications.
                Frontend: HTML (structure), CSS (styling), JavaScript (interactivity), frameworks (React, Vue, Angular).
                Backend: Server-side logic, databases, APIs, authentication (Node.js, Python/Django, Java/Spring).
                Full-stack: combines frontend and backend development skills.
                Modern practices: responsive design, RESTful APIs, version control (Git), deployment, security.
                """,
                'tags': ['web development', 'HTML', 'CSS', 'JavaScript', 'React', 'Node.js']
            },
            {
                'skill_category': 'cloud_computing',
                'content': """
                Cloud computing delivers computing services over the internet.
                Major providers: AWS (Amazon), Azure (Microsoft), GCP (Google Cloud Platform).
                Core services: compute (VMs, containers), storage (S3, blob storage), databases, networking.
                Key concepts: scalability, elasticity, pay-as-you-go, high availability, disaster recovery.
                Common patterns: IaaS, PaaS, SaaS, serverless, microservices architecture.
                """,
                'tags': ['cloud computing', 'AWS', 'Azure', 'DevOps', 'infrastructure']
            },
            {
                'skill_category': 'project_management',
                'content': """
                Project management involves planning, organizing, and executing projects successfully.
                Methodologies: Agile (iterative), Scrum (sprints), Kanban (flow), Waterfall (sequential).
                Key skills: planning, scheduling, budgeting, risk management, stakeholder communication.
                Tools: Jira, Trello, Asana, Microsoft Project, Gantt charts.
                Best practices: clear goals, regular communication, adaptability, continuous improvement.
                """,
                'tags': ['project management', 'Agile', 'Scrum', 'leadership', 'planning']
            }
        ]
        
        for knowledge in default_knowledge:
            self.add_knowledge(
                content=knowledge['content'],
                metadata={
                    'category': knowledge['skill_category'],
                    'tags': knowledge['tags'],
                    'source': 'default_initialization'
                }
            )
        
        self.save()
    
    def add_knowledge(self, content: str, metadata: Dict):
        """Add new knowledge to the base."""
        embedding = self.model.encode(content)
        
        self.knowledge_base['documents'].append(content)
        self.knowledge_base['embeddings'].append(embedding)
        self.knowledge_base['metadata'].append(metadata)
    
    def retrieve(self, query: str, top_k: int = 3, min_similarity: float = 0.3) -> List[Dict]:
        """
        Retrieve most relevant knowledge for a query.
        
        Args:
            query: Search query (skill name, learning goal, etc.)
            top_k: Number of top results to return
            min_similarity: Minimum similarity threshold
            
        Returns:
            List of relevant knowledge documents with metadata
        """
        if not self.knowledge_base['documents']:
            return []
        
        # Encode query
        query_embedding = self.model.encode(query).reshape(1, -1)
        
        # Calculate similarities
        embeddings_array = np.array(self.knowledge_base['embeddings'])
        similarities = cosine_similarity(query_embedding, embeddings_array)[0]
        
        # Get top-k indices above threshold
        top_indices = np.argsort(similarities)[::-1]
        
        results = []
        for idx in top_indices[:top_k]:
            if similarities[idx] >= min_similarity:
                results.append({
                    'content': self.knowledge_base['documents'][idx],
                    'similarity': float(similarities[idx]),
                    'metadata': self.knowledge_base['metadata'][idx]
                })
        
        return results
    
    def save(self):
        """Save knowledge base to disk."""
        with open(self.knowledge_path, 'wb') as f:
            pickle.dump(self.knowledge_base, f)
        print(f"Knowledge base saved to {self.knowledge_path}")
    
    def get_stats(self) -> Dict:
        """Get statistics about the knowledge base."""
        return {
            'total_documents': len(self.knowledge_base['documents']),
            'embedding_dimension': len(self.knowledge_base['embeddings'][0]) if self.knowledge_base['embeddings'] else 0,
            'categories': list(set(m.get('category', 'unknown') for m in self.knowledge_base['metadata']))
        }


class RAGContentGenerator:
    """
    RAG-enhanced content generator using retrieved knowledge + LLM.
    """
    
    def __init__(self, knowledge_base: SkillKnowledgeBase, llm_model):
        """
        Initialize RAG generator.
        
        Args:
            knowledge_base: SkillKnowledgeBase instance
            llm_model: LLM model for generation (e.g., Gemini)
        """
        self.kb = knowledge_base
        self.llm = llm_model
    
    def generate_enhanced_content(self, 
                                  skill_name: str,
                                  user_level: str = 'beginner',
                                  user_goal: str = '',
                                  max_length: int = 1000) -> Dict:
        """
        Generate enhanced learning content using RAG.
        
        Process:
        1. Retrieve relevant knowledge from vector database
        2. Construct enhanced prompt with retrieved context
        3. Generate personalized content with LLM
        4. Return content with sources and confidence
        """
        # Step 1: Retrieve relevant knowledge
        query = f"{skill_name} {user_level} {user_goal}"
        retrieved_docs = self.kb.retrieve(query, top_k=3)
        
        if not retrieved_docs:
            retrieved_context = "No specific knowledge base context available."
            confidence = "low"
        else:
            retrieved_context = "\n\n".join([
                f"Reference {i+1} (relevance: {doc['similarity']:.2%}):\n{doc['content']}"
                for i, doc in enumerate(retrieved_docs)
            ])
            avg_similarity = sum(d['similarity'] for d in retrieved_docs) / len(retrieved_docs)
            confidence = "high" if avg_similarity > 0.7 else "medium" if avg_similarity > 0.5 else "low"
        
        # Step 2: Construct RAG-enhanced prompt
        enhanced_prompt = f"""
You are an expert educator creating personalized learning content.

SKILL TO TEACH: {skill_name}
USER LEVEL: {user_level}
USER GOAL: {user_goal}

RELEVANT KNOWLEDGE BASE CONTEXT:
{retrieved_context}

TASK: Create comprehensive, personalized learning content for "{skill_name}" suitable for a {user_level} learner.

STRUCTURE YOUR RESPONSE:
1. **Overview & Relevance** (2-3 sentences)
   - What is this skill and why is it important?
   - How does it relate to the user's goal: "{user_goal}"?

2. **Key Concepts** (3-5 main concepts)
   - Core ideas that form the foundation
   - Simple explanations for each

3. **Learning Path** (Step-by-step)
   - Concrete steps to learn this skill
   - Ordered from basics to advanced
   - Time estimates for each step

4. **Practical Applications**
   - Real-world examples
   - How to apply this skill

5. **Resources & Next Steps**
   - Recommended learning resources
   - Practice exercises
   - What to learn after mastering this

Keep language clear and encouraging. Use the knowledge base context to ensure accuracy.
Max length: {max_length} words.
"""
        
        # Step 3: Generate with LLM
        try:
            if self.llm:
                response = self.llm.generate_content(enhanced_prompt)
                generated_content = response.text
            else:
                generated_content = self._fallback_template(skill_name, user_level, retrieved_docs)
        except Exception as e:
            print(f"Error generating content: {e}")
            generated_content = self._fallback_template(skill_name, user_level, retrieved_docs)
        
        # Step 4: Return with metadata
        return {
            'content': generated_content,
            'skill': skill_name,
            'user_level': user_level,
            'rag_confidence': confidence,
            'sources_used': len(retrieved_docs),
            'retrieved_similarities': [d['similarity'] for d in retrieved_docs],
            'generation_method': 'RAG-enhanced' if retrieved_docs else 'LLM-only',
            'content_length': len(generated_content.split())
        }
    
    def _fallback_template(self, skill_name: str, user_level: str, 
                          retrieved_docs: List[Dict]) -> str:
        """Fallback template-based generation if LLM fails."""
        context = retrieved_docs[0]['content'] if retrieved_docs else ""
        
        return f"""
# Learning Guide: {skill_name}

## Overview
This guide will help you learn {skill_name} at the {user_level} level.

## Foundation Knowledge
{context[:300] if context else 'Start with the fundamentals and build systematically.'}

## Learning Steps
1. Understand the basics and core concepts
2. Practice with simple examples
3. Build small projects to apply knowledge
4. Learn advanced techniques
5. Master through real-world application

## Resources
- Search for "{skill_name} tutorial for {user_level}"
- Practice on coding platforms
- Join online communities
- Work on hands-on projects

## Next Steps
Continue learning related skills and applying knowledge to real projects.
"""
    
    def batch_generate(self, skills: List[str], user_level: str, 
                      user_goal: str) -> Dict[str, Dict]:
        """Generate content for multiple skills efficiently."""
        results = {}
        for skill in skills:
            results[skill] = self.generate_enhanced_content(
                skill, user_level, user_goal
            )
        return results
