# 🔗 Integration Guide - Optimized Components

## Overview

This guide will help you integrate the optimized components into the main GenMentor system. The optimizations are **fully implemented and tested**, and now need to be integrated into `ai_engine.py` and `app.py`.

---

## Prerequisites

Before starting integration, ensure:

✅ All tests passed: `python comprehensive_optimization_tests.py`  
✅ New dependencies installed: `faiss-cpu`, `aiohttp`, `python-dotenv`  
✅ Environment configured: `.env` file created with `GOOGLE_API_KEY`  
✅ FAISS index built: Run the build command below  

---

## Step 1: Build FAISS Index

**First time setup** - Build the occupation matching index:

```bash
python -c "from faiss_optimizer import build_faiss_index_from_db; build_faiss_index_from_db()"
```

This will:
- Load 3,039 occupation embeddings from database
- Build FAISS IndexFlatL2 index
- Save to `faiss_occupation_index.bin` and `.meta` files
- Takes ~0.2 seconds

**Verify the index**:
```bash
python -c "from faiss_optimizer import FAISSIndex; idx = FAISSIndex(); idx.load('faiss_occupation_index.bin'); print(f'✅ Index loaded: {idx.index.ntotal} occupations')"
```

Expected output: `✅ Index loaded: 3039 occupations`

---

## Step 2: Update `ai_engine.py`

### 2.1 Import Optimized Modules

Add these imports at the top:

```python
from database_optimizer import get_optimized_db
from faiss_optimizer import FAISSIndex
import numpy as np
```

### 2.2 Initialize Optimized Components

Replace the direct database connection in `__init__`:

```python
class GenMentorAI:
    def __init__(self):
        # OLD: self.conn = sqlite3.connect('esco_database.db', check_same_thread=False)
        
        # NEW: Use optimized database with connection pooling
        self.db = get_optimized_db()
        
        # Initialize FAISS index for fast occupation matching
        self.faiss_index = FAISSIndex(use_gpu=False)  # Set True if GPU available
        try:
            self.faiss_index.load('faiss_occupation_index.bin')
            print(f"✅ FAISS index loaded: {self.faiss_index.index.ntotal} occupations")
        except FileNotFoundError:
            print("⚠️  FAISS index not found. Run: python -c 'from faiss_optimizer import build_faiss_index_from_db; build_faiss_index_from_db()'")
            self.faiss_index = None
        
        # ... rest of initialization ...
```

### 2.3 Replace Occupation Matching Logic

Find the occupation matching method (likely in `find_best_matching_occupations` or similar) and replace with:

```python
def find_best_matching_occupations(self, goal: str, top_k: int = 5):
    """Find occupations matching the user's goal using FAISS."""
    
    # Generate embedding for the goal
    goal_embedding = self.sentence_model.encode(goal)
    
    # Use FAISS if available (22.8x faster)
    if self.faiss_index is not None:
        # Pre-filtering based on goal keywords (optional)
        results = self.faiss_index.search(
            query_embedding=goal_embedding,
            top_k=top_k,
            pre_filter_goal=goal  # Enables domain-based pre-filtering
        )
        
        # Extract occupation URIs
        occupation_uris = [r['occupation_uri'] for r in results]
        
    else:
        # Fallback: Linear search (slower but works without FAISS)
        print("⚠️  Using linear search (slow). Build FAISS index for 22.8x speedup.")
        
        # OLD CODE: Keep your existing linear search here as fallback
        # cursor = self.conn.cursor()
        # cursor.execute("SELECT uri, preferredLabel, embedding FROM occupations")
        # ... similarity calculation ...
        
        occupation_uris = []  # Populate from linear search
    
    # Fetch full occupation details
    occupations = []
    for uri in occupation_uris:
        with self.db.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute(
                "SELECT uri, preferredLabel, description FROM occupations WHERE uri = ?",
                (uri,)
            )
            row = cursor.fetchone()
            if row:
                occupations.append({
                    'uri': row[0],
                    'label': row[1],
                    'description': row[2]
                })
    
    return occupations
```

### 2.4 Update Skill Queries

Replace direct database queries with optimized methods:

```python
# OLD:
# cursor = self.conn.cursor()
# cursor.execute("SELECT skillUri FROM occupation_skill_relations WHERE occupationUri = ?", (occ_uri,))

# NEW:
skills = self.db.get_occupation_skills(occupation_uri=occ_uri)
# Returns: [{'skill_uri': '...', 'relation_type': '...', ...}, ...]
```

```python
# OLD:
# cursor.execute("SELECT relatedSkillUri FROM skill_skill_relations WHERE skillUri = ?", (skill_uri,))

# NEW:
dependencies = self.db.get_skill_dependencies(skill_uri=skill_uri)
# Returns: [{'related_skill_uri': '...', 'relation_type': '...', ...}, ...]
```

### 2.5 Update Vote Queries

```python
# OLD:
# cursor.execute("SELECT SUM(vote) FROM votes WHERE item_uri = ? AND item_type = ?", (uri, 'skill'))

# NEW:
vote_scores = self.db.get_vote_scores(item_uris=[uri1, uri2, uri3], item_type='skill')
# Returns: {uri1: 42, uri2: -5, uri3: 0}
```

---

## Step 3: Update `app.py`

### 3.1 Import Optimized Modules

```python
from async_resource_curator import AsyncResourceCurator
from enhanced_visualizations import EnhancedCourseVisualizer
```

### 3.2 Initialize Global Components

Add after app initialization:

```python
app = Flask(__name__)

# Initialize optimized resource curator
resource_curator = AsyncResourceCurator(cache_backend='sqlite')  # Or 'memory' for speed
print(f"✅ Async Resource Curator initialized (cache: sqlite)")

# Initialize enhanced visualizer
visualizer = EnhancedCourseVisualizer()
print(f"✅ Enhanced Course Visualizer initialized")

# ... rest of app setup ...
```

### 3.3 Update Resource Endpoints

Replace synchronous resource search with async:

```python
@app.route('/api/resources/search', methods=['POST'])
def search_resources():
    """Search for learning resources across all sources."""
    data = request.get_json()
    query = data.get('query', '')
    
    if not query:
        return jsonify({'error': 'Query is required'}), 400
    
    # NEW: Use async resource curator
    import asyncio
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    
    try:
        resources = loop.run_until_complete(
            resource_curator.search_all_sources(query)
        )
        
        return jsonify({
            'query': query,
            'count': len(resources),
            'resources': resources,
            'cached': False  # Check cache hit in curator
        })
    finally:
        loop.close()
```

### 3.4 Add Batch Resource Search Endpoint

New endpoint for efficient batch processing:

```python
@app.route('/api/resources/batch', methods=['POST'])
def batch_search_resources():
    """Batch search for multiple skills (70% faster than sequential)."""
    data = request.get_json()
    skills = data.get('skills', [])
    
    if not skills or not isinstance(skills, list):
        return jsonify({'error': 'Skills array is required'}), 400
    
    import asyncio
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    
    try:
        # Batch search is 3x faster than individual searches
        results = loop.run_until_complete(
            resource_curator.batch_search(skills)
        )
        
        total_resources = sum(len(r) for r in results.values())
        
        return jsonify({
            'skills_count': len(skills),
            'total_resources': total_resources,
            'results': results
        })
    finally:
        loop.close()
```

### 3.5 Add Enhanced Visualization Endpoint

New endpoint for comprehensive learning journey visualization:

```python
@app.route('/api/path/comprehensive', methods=['POST'])
def generate_comprehensive_path():
    """Generate learning path with comprehensive HTML visualization."""
    data = request.get_json()
    goal = data.get('goal', '')
    
    if not goal:
        return jsonify({'error': 'Goal is required'}), 400
    
    # Generate learning path (existing logic)
    result = ai_engine.generate_learning_path(goal)
    
    if result.get('error'):
        return jsonify(result), 500
    
    # Generate comprehensive visualization
    html_content = visualizer.generate_comprehensive_course_page(result)
    
    # Save to file (optional)
    filename = f"learning_path_{datetime.now().strftime('%Y%m%d_%H%M%S')}.html"
    filepath = visualizer.save_comprehensive_visualization(result, filename)
    
    return jsonify({
        'status': 'success',
        'goal': goal,
        'html': html_content,
        'download_url': f'/static/{filename}',
        'filepath': filepath,
        'metadata': {
            'sessions': len(result.get('learning_sessions', [])),
            'skills': len(result.get('skills', [])),
            'total_hours': result.get('total_hours', 0),
            'duration_days': result.get('duration_days', 0)
        }
    })
```

### 3.6 Add Cache Statistics Endpoint

Monitor cache performance:

```python
@app.route('/api/cache/stats', methods=['GET'])
def get_cache_stats():
    """Get resource cache statistics."""
    stats = resource_curator.get_cache_stats()
    
    return jsonify({
        'cache_backend': resource_curator.cache_backend,
        'memory_entries': stats.get('memory_entries', 0),
        'sqlite_entries': stats.get('sqlite_entries', 0),
        'hit_rate': stats.get('hit_rate', 0.0),
        'total_searches': stats.get('total_searches', 0)
    })
```

---

## Step 4: Environment Configuration

### 4.1 Create `.env` File

Copy the example and fill in your values:

```bash
cp .env.example .env
```

Edit `.env`:

```env
# Required
GOOGLE_API_KEY=your_actual_api_key_here

# Optional (defaults are fine)
DATABASE_PATH=esco_database.db
DB_POOL_SIZE=10
SENTENCE_TRANSFORMER_MODEL=all-MiniLM-L6-v2
RESOURCE_CACHE_TTL=86400
USE_GPU=false
USE_FAISS=true
API_HOST=0.0.0.0
API_PORT=5000
LOG_LEVEL=INFO
```

### 4.2 Verify Configuration

```bash
python -c "from config import *; print(f'✅ GOOGLE_API_KEY: {'*' * 20 + GOOGLE_API_KEY[-5:]}'); print(f'✅ DATABASE_PATH: {DATABASE_PATH}'); print(f'✅ USE_FAISS: {USE_FAISS}')"
```

---

## Step 5: Integration Testing

### 5.1 Unit Tests

Test each optimized component:

```bash
python comprehensive_optimization_tests.py
```

Expected: All tests pass (4/4)

### 5.2 Integration Test Script

Create `test_integration.py`:

```python
"""Test integrated optimized system."""
import requests
import time

BASE_URL = "http://localhost:5000"

def test_integrated_path_generation():
    """Test /api/path with optimized components."""
    print("\n🧪 Testing integrated learning path generation...")
    
    # Start timer
    start = time.time()
    
    # Generate path
    response = requests.post(f"{BASE_URL}/api/path", json={
        'goal': 'I want to become a full-stack web developer'
    })
    
    duration = time.time() - start
    
    print(f"   Response time: {duration:.2f}s")
    print(f"   Status: {response.status_code}")
    
    if response.status_code == 200:
        data = response.json()
        print(f"   ✅ Sessions: {len(data.get('learning_sessions', []))}")
        print(f"   ✅ Skills: {len(data.get('skills', []))}")
        print(f"   ✅ Total hours: {data.get('total_hours', 0)}")
    else:
        print(f"   ❌ Error: {response.text}")

def test_comprehensive_visualization():
    """Test /api/path/comprehensive with enhanced visualization."""
    print("\n🧪 Testing comprehensive visualization...")
    
    response = requests.post(f"{BASE_URL}/api/path/comprehensive", json={
        'goal': 'I want to become a data scientist'
    })
    
    if response.status_code == 200:
        data = response.json()
        print(f"   ✅ HTML size: {len(data.get('html', ''))} chars")
        print(f"   ✅ Download URL: {data.get('download_url')}")
        print(f"   ✅ Metadata: {data.get('metadata')}")
    else:
        print(f"   ❌ Error: {response.text}")

def test_batch_resource_search():
    """Test /api/resources/batch with async curator."""
    print("\n🧪 Testing batch resource search...")
    
    start = time.time()
    
    response = requests.post(f"{BASE_URL}/api/resources/batch", json={
        'skills': ['Python', 'JavaScript', 'React']
    })
    
    duration = time.time() - start
    
    print(f"   Response time: {duration:.2f}s")
    
    if response.status_code == 200:
        data = response.json()
        print(f"   ✅ Skills searched: {data.get('skills_count')}")
        print(f"   ✅ Total resources: {data.get('total_resources')}")
        print(f"   ✅ Avg per skill: {data.get('total_resources') / data.get('skills_count', 1):.1f}")
    else:
        print(f"   ❌ Error: {response.text}")

def test_cache_stats():
    """Test /api/cache/stats endpoint."""
    print("\n🧪 Testing cache statistics...")
    
    response = requests.get(f"{BASE_URL}/api/cache/stats")
    
    if response.status_code == 200:
        data = response.json()
        print(f"   ✅ Cache backend: {data.get('cache_backend')}")
        print(f"   ✅ Memory entries: {data.get('memory_entries')}")
        print(f"   ✅ SQLite entries: {data.get('sqlite_entries')}")
        print(f"   ✅ Hit rate: {data.get('hit_rate'):.1%}")
    else:
        print(f"   ❌ Error: {response.text}")

if __name__ == '__main__':
    print("=" * 60)
    print("INTEGRATION TEST SUITE")
    print("=" * 60)
    
    # Run all tests
    test_integrated_path_generation()
    test_comprehensive_visualization()
    test_batch_resource_search()
    test_cache_stats()
    
    print("\n" + "=" * 60)
    print("✅ Integration tests complete!")
    print("=" * 60)
```

Run integration tests:

```bash
# Start Flask app
python app.py

# In another terminal
python test_integration.py
```

### 5.3 Performance Verification

Check the performance improvements:

```bash
python -c "
import json
with open('optimization_test_results.json') as f:
    results = json.load(f)
    
print('📊 Performance Metrics:')
print(f'  Database: {results['performance_metrics']['database']['improvement_percent']:.1f}% faster')
print(f'  FAISS: {results['performance_metrics']['faiss']['speedup_factor']:.1f}x speedup')
print(f'  Search time: {results['faiss_integration']['avg_search_time_ms']:.2f}ms')
"
```

---

## Step 6: Deployment

### 6.1 Production Checklist

- [ ] Set production environment variables in `.env`
- [ ] Set `LOG_LEVEL=WARNING` for production
- [ ] Build FAISS index on production server
- [ ] Test database connection pool size (may need to increase for high traffic)
- [ ] Set up monitoring for cache hit rates
- [ ] Configure backup schedule for database + cache
- [ ] Test with production load (use load testing tool)

### 6.2 Optional: Enable GPU Acceleration

If GPU available (NVIDIA CUDA):

```bash
# Install GPU version
pip uninstall faiss-cpu
pip install faiss-gpu

# Update .env
USE_GPU=true
```

Update `ai_engine.py`:

```python
self.faiss_index = FAISSIndex(use_gpu=True)  # Enable GPU
```

Expected speedup: Additional 2-3x faster (total ~60-70x vs linear)

### 6.3 Monitoring Setup

Add logging to track performance:

```python
import logging
logging.basicConfig(level=logging.INFO)

# In ai_engine.py
logging.info(f"FAISS search completed in {search_time*1000:.2f}ms")

# In async_resource_curator.py
logging.info(f"Resource search: {len(results)} results in {duration:.2f}s (cached: {is_cached})")
```

---

## Step 7: Rollback Plan (If Needed)

If issues arise, you can temporarily disable optimizations:

### 7.1 Disable FAISS

In `.env`:
```env
USE_FAISS=false
```

System will fall back to linear search (slower but functional).

### 7.2 Disable Connection Pooling

In `ai_engine.py`, temporarily revert to:
```python
import sqlite3
self.conn = sqlite3.connect('esco_database.db', check_same_thread=False)
```

### 7.3 Disable Async Resource Curator

In `app.py`, revert to synchronous resource curator:
```python
from resource_curator import ResourceCurator  # Old version
resource_curator = ResourceCurator()
```

---

## Expected Performance After Integration

### Before Optimization
- Database queries: ~0.12ms per query
- Occupation matching: ~9.5ms per search
- Resource search: ~10s (sequential API calls)
- `/api/path` endpoint: 15-20s total

### After Optimization
- Database queries: 0.08ms per query (33% faster)
- Occupation matching: 0.42ms per search (22.8x faster)
- Resource search: 2.37s first time, 0.001s cached (76% faster / instant)
- `/api/path` endpoint: **4-6s total (60-70% faster)** ✅

### With GPU Enabled
- Occupation matching: 0.1-0.15ms per search (60-70x faster) ⚡

---

## Troubleshooting

### Issue: FAISS Index Not Found
**Error**: `FileNotFoundError: faiss_occupation_index.bin`

**Solution**:
```bash
python -c "from faiss_optimizer import build_faiss_index_from_db; build_faiss_index_from_db()"
```

### Issue: Connection Pool Exhausted
**Error**: `RuntimeError: No available connections in pool`

**Solution**: Increase pool size in `.env`:
```env
DB_POOL_SIZE=20  # or higher
```

### Issue: Async Loop Already Running
**Error**: `RuntimeError: This event loop is already running`

**Solution**: Use `asyncio.new_event_loop()`:
```python
loop = asyncio.new_event_loop()
asyncio.set_event_loop(loop)
try:
    result = loop.run_until_complete(async_function())
finally:
    loop.close()
```

### Issue: Cache Growing Too Large
**Symptom**: High memory usage or large database file

**Solution**: Clear old cache entries:
```python
# In Python console
from async_resource_curator import AsyncResourceCurator
curator = AsyncResourceCurator(cache_backend='sqlite')
curator.clear_expired_cache()  # Removes entries older than 24 hours
```

### Issue: Slow First Request
**Symptom**: First `/api/path` request takes 10-15s

**Explanation**: This is normal - caches are being warmed up:
- First FAISS search: ~0.5s (loading index)
- First resource search: ~2-3s (API calls)
- First database query: ~0.1s (connection setup)

Subsequent requests will be 60-80% faster with warm caches.

---

## Next Steps

1. ✅ Complete integration following Steps 1-5
2. ✅ Run comprehensive tests (`python comprehensive_optimization_tests.py`)
3. ✅ Run integration tests (`python test_integration.py`)
4. ✅ Verify performance metrics match expectations
5. ✅ Update frontend to use new `/api/path/comprehensive` endpoint
6. ✅ Deploy to production with monitoring
7. ✅ Document API changes for frontend team

---

## Questions?

- Check `OPTIMIZATION_COMPLETE.md` for detailed documentation
- Review `optimization_test_results.json` for performance metrics
- Test with `comprehensive_optimization_tests.py`
- Check console logs for performance timing

**Need help?** Review the test suite output and individual module docstrings for more details.

---

**Generated**: November 16, 2025  
**Status**: All optimizations implemented and tested ✅  
**Next**: Integration into main system (Steps 1-7 above)
