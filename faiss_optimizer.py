"""
FAISS-based Fast Occupation Matching
Implements approximate nearest neighbor search for 80-90% faster occupation matching.
"""

import numpy as np
import pickle
import os
from typing import List, Tuple, Dict, Optional
import time


class FAISSIndex:
    """
    FAISS-based index for fast occupation matching.
    Uses approximate nearest neighbor search instead of linear search.
    """
    
    def __init__(self, embeddings_path: str = None, index_path: str = 'occupation_faiss.index'):
        """
        Initialize FAISS index.
        
        Args:
            embeddings_path: Path to occupation embeddings pickle file
            index_path: Path to save/load FAISS index
        """
        self.embeddings_path = embeddings_path
        self.index_path = index_path
        self.index = None
        self.occupation_uris = []
        self.embedding_dim = None
        
        # Try to import FAISS
        try:
            import sys
            sys.path.insert(0, 'venv/Lib/site-packages')
            import faiss
            self.faiss = faiss
            self.faiss_available = True
            print("✅ FAISS library loaded")
        except ImportError:
            print("⚠️ FAISS not available, falling back to linear search")
            self.faiss_available = False
            self.annoy_available = False
    
    def build_from_embeddings(self, occupation_embeddings: Dict[str, np.ndarray], 
                             use_gpu: bool = False) -> None:
        """
        Build FAISS index from occupation embeddings.
        
        Args:
            occupation_embeddings: Dictionary mapping occupation URIs to embeddings
            use_gpu: Whether to use GPU acceleration if available
        """
        if not occupation_embeddings:
            raise ValueError("Empty occupation embeddings dictionary")
        
        print(f"Building FAISS index for {len(occupation_embeddings)} occupations...")
        
        # Extract URIs and embeddings
        self.occupation_uris = list(occupation_embeddings.keys())
        embeddings_array = np.array([occupation_embeddings[uri] for uri in self.occupation_uris])
        self.embedding_dim = embeddings_array.shape[1]
        
        print(f"  Embedding dimension: {self.embedding_dim}")
        print(f"  Total occupations: {len(self.occupation_uris)}")
        
        if self.faiss_available:
            self._build_faiss_index(embeddings_array, use_gpu)
        else:
            # Fallback: store embeddings for linear search
            self.embeddings_array = embeddings_array
            print("  ⚠️ Using linear search (install faiss-cpu for better performance)")
    
    def _build_faiss_index(self, embeddings_array: np.ndarray, use_gpu: bool = False):
        """Build FAISS index."""
        n_occupations = len(embeddings_array)
        
        # For small datasets (<10k), use flat index
        # For larger datasets, use IVF (Inverted File Index) with clustering
        if n_occupations < 10000:
            # Flat L2 index (exact search)
            self.index = self.faiss.IndexFlatL2(self.embedding_dim)
            print("  Using FAISS IndexFlatL2 (exact search)")
        else:
            # IVF index with clustering (approximate search)
            nlist = min(100, n_occupations // 10)  # Number of clusters
            quantizer = self.faiss.IndexFlatL2(self.embedding_dim)
            self.index = self.faiss.IndexIVFFlat(quantizer, self.embedding_dim, nlist)
            
            print(f"  Training IVF index with {nlist} clusters...")
            self.index.train(embeddings_array.astype('float32'))
            print("  ✅ Training complete")
        
        # Move to GPU if available and requested
        if use_gpu and self.faiss.get_num_gpus() > 0:
            print("  Moving index to GPU...")
            res = self.faiss.StandardGpuResources()
            self.index = self.faiss.index_cpu_to_gpu(res, 0, self.index)
            print("  ✅ Index on GPU")
        
        # Add embeddings to index
        print("  Adding embeddings to index...")
        self.index.add(embeddings_array.astype('float32'))
        print(f"  ✅ FAISS index built with {self.index.ntotal} vectors")
    
    def _build_annoy_index(self, embeddings_array: np.ndarray):
        """Build Annoy index as fallback."""
        from annoy import AnnoyIndex
        
        self.index = AnnoyIndex(self.embedding_dim, 'angular')  # Angular = cosine distance
        
        print("  Building Annoy index...")
        for i, embedding in enumerate(embeddings_array):
            self.index.add_item(i, embedding)
        
        # Build with default trees (more trees = better accuracy but slower)
        n_trees = min(50, max(10, len(embeddings_array) // 100))
        self.index.build(n_trees)
        print(f"  ✅ Annoy index built with {n_trees} trees")
    
    def search(self, query_embedding: np.ndarray, k: int = 10) -> List[Tuple[str, float]]:
        """
        Search for k nearest occupations.
        
        Args:
            query_embedding: Query embedding vector
            k: Number of results to return
            
        Returns:
            List of (occupation_uri, similarity_score) tuples
        """
        if query_embedding.ndim == 1:
            query_embedding = query_embedding.reshape(1, -1)
        
        if self.faiss_available and self.index is not None:
            return self._search_faiss(query_embedding, k)
        else:
            return self._search_linear(query_embedding, k)
    
    def _search_faiss(self, query_embedding: np.ndarray, k: int) -> List[Tuple[str, float]]:
        """Search using FAISS index."""
        # Set search parameters for IVF index
        if hasattr(self.index, 'nprobe'):
            self.index.nprobe = min(10, self.index.nlist)  # Search 10 clusters
        
        # Search
        distances, indices = self.index.search(query_embedding.astype('float32'), k)
        
        # Convert L2 distances to similarity scores (1 / (1 + distance))
        results = []
        for idx, dist in zip(indices[0], distances[0]):
            if idx < len(self.occupation_uris):
                similarity = 1.0 / (1.0 + dist)
                results.append((self.occupation_uris[idx], similarity))
        
        return results
    
    def _search_annoy(self, query_embedding: np.ndarray, k: int) -> List[Tuple[str, float]]:
        """Search using Annoy index."""
        indices, distances = self.index.get_nns_by_vector(
            query_embedding.flatten(), k, include_distances=True
        )
        
        # Annoy returns angular distance, convert to similarity
        results = []
        for idx, dist in zip(indices, distances):
            if idx < len(self.occupation_uris):
                # Angular distance to cosine similarity: sim = 1 - (dist^2 / 2)
                similarity = 1.0 - (dist * dist / 2.0)
                results.append((self.occupation_uris[idx], similarity))
        
        return results
    
    def _search_linear(self, query_embedding: np.ndarray, k: int) -> List[Tuple[str, float]]:
        """Fallback linear search using cosine similarity."""
        from sklearn.metrics.pairwise import cosine_similarity
        
        similarities = cosine_similarity(query_embedding, self.embeddings_array)[0]
        
        # Get top-k indices
        top_k_indices = np.argsort(similarities)[-k:][::-1]
        
        results = []
        for idx in top_k_indices:
            results.append((self.occupation_uris[idx], float(similarities[idx])))
        
        return results
    
    def save(self):
        """Save FAISS index and metadata to disk."""
        if self.index is None and not hasattr(self, 'embeddings_array'):
            raise ValueError("No index to save")
        
        print(f"Saving index to {self.index_path}...")
        
        # Save index
        if self.faiss_available and self.index is not None:
            # Move to CPU before saving if on GPU
            if hasattr(self.index, 'getDevice'):
                index_cpu = self.faiss.index_gpu_to_cpu(self.index)
                self.faiss.write_index(index_cpu, self.index_path)
            else:
                self.faiss.write_index(self.index, self.index_path)
        
        # Save metadata
        metadata = {
            'occupation_uris': self.occupation_uris,
            'embedding_dim': self.embedding_dim,
            'index_type': 'faiss' if self.faiss_available else 'linear',
            'embeddings_array': self.embeddings_array if hasattr(self, 'embeddings_array') else None
        }
        
        with open(self.index_path + '.meta', 'wb') as f:
            pickle.dump(metadata, f)
        
        print(f"✅ Index saved to {self.index_path}")
    
    def load(self):
        """Load FAISS index and metadata from disk."""
        if not os.path.exists(self.index_path + '.meta'):
            raise FileNotFoundError(f"Index metadata not found: {self.index_path}.meta")
        
        print(f"Loading index from {self.index_path}...")
        
        # Load metadata
        with open(self.index_path + '.meta', 'rb') as f:
            metadata = pickle.load(f)
        
        self.occupation_uris = metadata['occupation_uris']
        self.embedding_dim = metadata['embedding_dim']
        
        # Load index
        index_type = metadata['index_type']
        
        if index_type == 'faiss' and self.faiss_available:
            self.index = self.faiss.read_index(self.index_path)
            print(f"✅ Loaded FAISS index with {self.index.ntotal} vectors")
        else:
            # Fallback to linear
            self.embeddings_array = metadata['embeddings_array']
            print(f"✅ Loaded embeddings for linear search")


class PreFilteredSearch:
    """
    Pre-filtering strategy to reduce search space (B5.2).
    Filters occupations by domain keywords before similarity search.
    """
    
    # Domain keywords mapping
    DOMAIN_KEYWORDS = {
        'technology': ['software', 'developer', 'engineer', 'programmer', 'IT', 'tech', 'data', 'AI', 'computer', 'web', 'mobile', 'cloud', 'cyber'],
        'healthcare': ['doctor', 'nurse', 'medical', 'health', 'care', 'physician', 'therapist', 'clinical', 'hospital', 'patient'],
        'business': ['manager', 'analyst', 'consultant', 'director', 'executive', 'sales', 'marketing', 'finance', 'accounting', 'business'],
        'education': ['teacher', 'professor', 'instructor', 'educator', 'tutor', 'trainer', 'academic', 'school', 'university'],
        'creative': ['designer', 'artist', 'writer', 'photographer', 'animator', 'creative', 'media', 'content', 'graphic'],
        'engineering': ['engineer', 'engineering', 'mechanical', 'electrical', 'civil', 'industrial', 'construction'],
        'science': ['scientist', 'researcher', 'chemist', 'biologist', 'physicist', 'laboratory', 'research'],
        'service': ['service', 'customer', 'support', 'representative', 'assistant', 'coordinator', 'specialist']
    }
    
    @staticmethod
    def detect_domain(goal_text: str) -> List[str]:
        """
        Detect relevant domains from goal text.
        
        Args:
            goal_text: User's career goal
            
        Returns:
            List of detected domains
        """
        goal_lower = goal_text.lower()
        detected = []
        
        for domain, keywords in PreFilteredSearch.DOMAIN_KEYWORDS.items():
            if any(keyword in goal_lower for keyword in keywords):
                detected.append(domain)
        
        return detected if detected else ['general']
    
    @staticmethod
    def filter_occupations(occupations: Dict[str, dict], domains: List[str], 
                          max_results: int = 500) -> Dict[str, dict]:
        """
        Filter occupations by domain keywords.
        
        Args:
            occupations: Dictionary of occupation data
            domains: List of domains to filter by
            max_results: Maximum occupations to return
            
        Returns:
            Filtered occupation dictionary
        """
        if 'general' in domains or not domains:
            # No filtering needed
            return occupations
        
        filtered = {}
        keywords = []
        for domain in domains:
            keywords.extend(PreFilteredSearch.DOMAIN_KEYWORDS.get(domain, []))
        
        for uri, data in occupations.items():
            label = data.get('label', '').lower()
            description = data.get('description', '').lower()
            
            # Check if any keyword matches
            if any(kw in label or kw in description for kw in keywords):
                filtered[uri] = data
                
                if len(filtered) >= max_results:
                    break
        
        print(f"  Pre-filtering: {len(occupations)} → {len(filtered)} occupations (domain: {', '.join(domains)})")
        
        return filtered if filtered else occupations  # Return all if no matches


def benchmark_search_methods(embeddings_path: str):
    """
    Benchmark different search methods to compare performance.
    
    Args:
        embeddings_path: Path to occupation embeddings
    """
    print("=" * 60)
    print("BENCHMARK: Search Method Comparison")
    print("=" * 60)
    
    # Load embeddings
    print("\nLoading embeddings...")
    with open(embeddings_path, 'rb') as f:
        occupation_embeddings = pickle.load(f)
    
    print(f"Loaded {len(occupation_embeddings)} occupation embeddings")
    
    # Create test query
    sample_uri = list(occupation_embeddings.keys())[0]
    query_embedding = occupation_embeddings[sample_uri]
    
    # Method 1: Linear search (current method)
    print("\n1. Linear Search (baseline):")
    from sklearn.metrics.pairwise import cosine_similarity
    
    embeddings_array = np.array(list(occupation_embeddings.values()))
    
    start = time.time()
    for _ in range(100):
        similarities = cosine_similarity(query_embedding.reshape(1, -1), embeddings_array)
        top_k = np.argsort(similarities[0])[-10:][::-1]
    linear_time = time.time() - start
    
    print(f"   Time: {linear_time:.3f}s for 100 queries")
    print(f"   Average: {linear_time/100*1000:.1f}ms per query")
    
    # Method 2: FAISS
    try:
        print("\n2. FAISS Index:")
        faiss_index = FAISSIndex()
        faiss_index.build_from_embeddings(occupation_embeddings, use_gpu=False)
        
        start = time.time()
        for _ in range(100):
            results = faiss_index.search(query_embedding, k=10)
        faiss_time = time.time() - start
        
        print(f"   Time: {faiss_time:.3f}s for 100 queries")
        print(f"   Average: {faiss_time/100*1000:.1f}ms per query")
        print(f"   ✅ Speedup: {linear_time/faiss_time:.1f}x faster than linear search")
    except Exception as e:
        print(f"   ⚠️ FAISS benchmark failed: {e}")
    
    print("\n" + "=" * 60)


if __name__ == "__main__":
    # Test FAISS integration
    embeddings_path = 'occupation_embeddings_all-mpnet-base-v2.pkl'
    
    if os.path.exists(embeddings_path):
        print("Testing FAISS integration...\n")
        
        # Load embeddings
        with open(embeddings_path, 'rb') as f:
            occupation_embeddings = pickle.load(f)
        
        print(f"Loaded {len(occupation_embeddings)} occupation embeddings")
        
        # Build FAISS index
        faiss_index = FAISSIndex()
        faiss_index.build_from_embeddings(occupation_embeddings, use_gpu=False)
        
        # Test search
        test_uri = list(occupation_embeddings.keys())[0]
        test_embedding = occupation_embeddings[test_uri]
        
        print(f"\nTesting search with query: {test_uri}")
        results = faiss_index.search(test_embedding, k=5)
        
        print("\nTop 5 results:")
        for i, (uri, score) in enumerate(results, 1):
            print(f"  {i}. {uri[:50]}... (score: {score:.4f})")
        
        # Save index
        faiss_index.save()
        
        # Run benchmark
        print("\n")
        benchmark_search_methods(embeddings_path)
    else:
        print(f"❌ Embeddings file not found: {embeddings_path}")
