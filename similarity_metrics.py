"""
Multiple Similarity Metrics for Career Matching
Implements various similarity measures for comparing user goals with occupations.
"""

import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity, euclidean_distances, manhattan_distances
from typing import List, Dict, Tuple
import re


class SimilarityMetrics:
    """
    Comprehensive similarity metrics for text comparison.
    Implements multiple algorithms for robust career matching.
    """
    
    def __init__(self):
        self.tfidf_vectorizer = TfidfVectorizer(
            max_features=5000,
            ngram_range=(1, 2),
            stop_words='english',
            lowercase=True
        )
        self.corpus_fitted = False
        
    def fit_corpus(self, documents: List[str]):
        """Fit TF-IDF vectorizer on corpus of documents."""
        self.tfidf_vectorizer.fit(documents)
        self.corpus_fitted = True
        
    def cosine_similarity_score(self, vec1: np.ndarray, vec2: np.ndarray) -> float:
        """
        Cosine Similarity: Measures angle between vectors
        Formula: cos(θ) = (A·B) / (||A|| × ||B||)
        Range: [-1, 1], where 1 = identical, 0 = orthogonal, -1 = opposite
        """
        if vec1.ndim == 1:
            vec1 = vec1.reshape(1, -1)
        if vec2.ndim == 1:
            vec2 = vec2.reshape(1, -1)
        
        similarity = cosine_similarity(vec1, vec2)[0][0]
        return float(similarity)
    
    def euclidean_distance_similarity(self, vec1: np.ndarray, vec2: np.ndarray) -> float:
        """
        Euclidean Distance converted to similarity
        Formula: distance = sqrt(Σ(ai - bi)²)
        Converted to similarity: 1 / (1 + distance)
        Range: [0, 1], where 1 = identical, approaching 0 = very different
        """
        if vec1.ndim == 1:
            vec1 = vec1.reshape(1, -1)
        if vec2.ndim == 1:
            vec2 = vec2.reshape(1, -1)
            
        distance = euclidean_distances(vec1, vec2)[0][0]
        # Convert distance to similarity (normalized)
        similarity = 1.0 / (1.0 + distance)
        return float(similarity)
    
    def manhattan_distance_similarity(self, vec1: np.ndarray, vec2: np.ndarray) -> float:
        """
        Manhattan Distance (L1 norm) converted to similarity
        Formula: distance = Σ|ai - bi|
        Converted to similarity: 1 / (1 + distance)
        Range: [0, 1], where 1 = identical
        """
        if vec1.ndim == 1:
            vec1 = vec1.reshape(1, -1)
        if vec2.ndim == 1:
            vec2 = vec2.reshape(1, -1)
            
        distance = manhattan_distances(vec1, vec2)[0][0]
        similarity = 1.0 / (1.0 + distance)
        return float(similarity)
    
    def jaccard_similarity(self, text1: str, text2: str) -> float:
        """
        Jaccard Similarity: Intersection over Union of word sets
        Formula: J(A,B) = |A ∩ B| / |A ∪ B|
        Range: [0, 1], where 1 = identical sets
        """
        # Tokenize and clean
        words1 = set(re.findall(r'\w+', text1.lower()))
        words2 = set(re.findall(r'\w+', text2.lower()))
        
        if not words1 or not words2:
            return 0.0
        
        intersection = len(words1.intersection(words2))
        union = len(words1.union(words2))
        
        return float(intersection / union) if union > 0 else 0.0
    
    def tfidf_similarity(self, text1: str, text2: str) -> float:
        """
        TF-IDF Cosine Similarity
        TF = Term Frequency, IDF = Inverse Document Frequency
        Measures importance of terms in documents
        Range: [0, 1]
        """
        if not self.corpus_fitted:
            # Fit on both texts if corpus not fitted
            self.tfidf_vectorizer.fit([text1, text2])
        
        vectors = self.tfidf_vectorizer.transform([text1, text2])
        similarity = cosine_similarity(vectors[0:1], vectors[1:2])[0][0]
        return float(similarity)
    
    def dice_coefficient(self, text1: str, text2: str) -> float:
        """
        Dice Coefficient (Sørensen-Dice): Similar to Jaccard but weights intersection more
        Formula: DC = 2|A ∩ B| / (|A| + |B|)
        Range: [0, 1]
        """
        words1 = set(re.findall(r'\w+', text1.lower()))
        words2 = set(re.findall(r'\w+', text2.lower()))
        
        if not words1 or not words2:
            return 0.0
        
        intersection = len(words1.intersection(words2))
        return float(2.0 * intersection / (len(words1) + len(words2)))
    
    def overlap_coefficient(self, text1: str, text2: str) -> float:
        """
        Overlap Coefficient: Similarity based on smaller set
        Formula: overlap(A,B) = |A ∩ B| / min(|A|, |B|)
        Range: [0, 1]
        """
        words1 = set(re.findall(r'\w+', text1.lower()))
        words2 = set(re.findall(r'\w+', text2.lower()))
        
        if not words1 or not words2:
            return 0.0
        
        intersection = len(words1.intersection(words2))
        min_size = min(len(words1), len(words2))
        
        return float(intersection / min_size) if min_size > 0 else 0.0
    
    def comprehensive_similarity(self, 
                                 text1: str, 
                                 text2: str,
                                 embedding1: np.ndarray = None,
                                 embedding2: np.ndarray = None) -> Dict[str, float]:
        """
        Calculate all similarity metrics and return comprehensive comparison.
        
        Args:
            text1: First text for comparison
            text2: Second text for comparison
            embedding1: Optional pre-computed embedding for text1
            embedding2: Optional pre-computed embedding for text2
            
        Returns:
            Dictionary with all similarity scores and weighted average
        """
        scores = {}
        
        # Text-based metrics
        scores['jaccard'] = self.jaccard_similarity(text1, text2)
        scores['dice'] = self.dice_coefficient(text1, text2)
        scores['overlap'] = self.overlap_coefficient(text1, text2)
        scores['tfidf'] = self.tfidf_similarity(text1, text2)
        
        # Embedding-based metrics (if embeddings provided)
        if embedding1 is not None and embedding2 is not None:
            scores['cosine'] = self.cosine_similarity_score(embedding1, embedding2)
            scores['euclidean'] = self.euclidean_distance_similarity(embedding1, embedding2)
            scores['manhattan'] = self.manhattan_distance_similarity(embedding1, embedding2)
        
        # Calculate weighted average (semantic embeddings weighted higher)
        if embedding1 is not None and embedding2 is not None:
            scores['weighted_average'] = (
                scores['cosine'] * 0.35 +
                scores['euclidean'] * 0.15 +
                scores['manhattan'] * 0.10 +
                scores['tfidf'] * 0.20 +
                scores['jaccard'] * 0.10 +
                scores['dice'] * 0.05 +
                scores['overlap'] * 0.05
            )
        else:
            scores['weighted_average'] = (
                scores['tfidf'] * 0.50 +
                scores['jaccard'] * 0.25 +
                scores['dice'] * 0.15 +
                scores['overlap'] * 0.10
            )
        
        return scores
    
    def get_best_metric_for_task(self, task_type: str) -> str:
        """
        Recommend best similarity metric based on task type.
        
        Args:
            task_type: 'semantic', 'lexical', 'hybrid', or 'short_text'
            
        Returns:
            Recommended metric name
        """
        recommendations = {
            'semantic': 'cosine',  # Best for meaning-based comparison
            'lexical': 'jaccard',  # Best for word overlap
            'hybrid': 'weighted_average',  # Best overall
            'short_text': 'dice',  # Better for short texts
            'long_text': 'tfidf',  # Better for long documents
        }
        
        return recommendations.get(task_type, 'weighted_average')


def compare_metrics_performance(texts1: List[str], 
                               texts2: List[str],
                               embeddings1: List[np.ndarray] = None,
                               embeddings2: List[np.ndarray] = None) -> Dict:
    """
    Compare performance of different metrics across multiple text pairs.
    
    Returns detailed statistics and recommendations.
    """
    metrics = SimilarityMetrics()
    
    # Fit TF-IDF on combined corpus
    all_texts = texts1 + texts2
    metrics.fit_corpus(all_texts)
    
    results = {
        'individual_scores': [],
        'metric_statistics': {},
        'recommendations': {}
    }
    
    # Calculate scores for each pair
    for i in range(len(texts1)):
        emb1 = embeddings1[i] if embeddings1 else None
        emb2 = embeddings2[i] if embeddings2 else None
        
        scores = metrics.comprehensive_similarity(
            texts1[i], texts2[i], emb1, emb2
        )
        results['individual_scores'].append(scores)
    
    # Calculate statistics for each metric
    metric_names = results['individual_scores'][0].keys()
    for metric in metric_names:
        scores = [s[metric] for s in results['individual_scores']]
        results['metric_statistics'][metric] = {
            'mean': np.mean(scores),
            'std': np.std(scores),
            'min': np.min(scores),
            'max': np.max(scores),
            'median': np.median(scores)
        }
    
    return results
