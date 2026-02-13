# Cortex – Adaptive Learning Platform
## Project Report Submitted in Partial Fulfilment of the Requirements for the Degree of Bachelor of Technology in Computer Science and Engineering

**Submitted by:** Manasvi Vedanta (Roll No. 2210110385)  
**Under the Supervision of:** Dr. Sonia Khetarpaul  
**Department:** Computer Science and Engineering  
**Date:** November 28, 2025

---

## Abstract

This final report describes the Cortex system (also referred to as Hybrid-GenMentor) — an AI-driven career guidance platform that maps user goals and existing skills to occupation recommendations and personalized learning paths. The system uses semantic embeddings, FAISS for approximate nearest neighbor search, dependency-based scheduling of skills, and LLM-powered content generation (Gemini 2.0 Flash). Key achievements include a fully validated system with a 100% test success rate across 25 scenarios, achieving 83.7% average similarity in occupation matching and 95/100 in skill relevance scoring. The system features advanced optimizations like FAISS vector search and asynchronous resource curation, reducing processing time to ~18 seconds.

The project source code and documentation are available at:  
[https://github.com/Manasvi-Vedanta/Hybrid-GenMentor](https://github.com/Manasvi-Vedanta/Hybrid-GenMentor)

---

## Chapter 1 — Introduction

### 1.1 Problem Statement
Many learners and job-transitioners struggle to identify which concrete skills to learn and in what order to reach a target occupation. Traditional systems often rely on static keyword matching, failing to understand the semantic nuance of user goals. Cortex aims to automate career matching and curriculum generation at scale using semantic matching of goals to occupations, skill-gap analysis, and dependency-aware learning plans.

### 1.2 Objectives
*   **Map user career goals** to relevant occupations (3,039+ occupations indexed) using semantic understanding.
*   **Generate personalized, ordered learning paths** from the skill repository (≈13,939 skills) based on skill gaps.
*   **Provide explainable matching** using cosine similarity and dependency graphs.
*   **Expose a REST API and LLM session integration** for interactive guidance and real-time content generation.
*   **Optimize system performance** for low-latency responses using FAISS and asynchronous processing.

---

## Chapter 2 — Literature Survey

This project draws primarily from two research works:
1.  **Wang et al., 'LLM-powered Multi-agent Framework for Goal-oriented Learning in Intelligent Tutoring System' (GenMentor, WWW '25).**
    *   GenMentor provides an LLM multi-agent framework for goal-oriented ITS, fine-tuning LLMs on goal-to-skill mappings, learner-profiling, and evolvable path scheduling.
2.  **Tavakoli et al., 'Hybrid Human-AI Curriculum Development for Personalised Informal Learning Environments' (LAK22).**
    *   Hybrid Human-AI presents AI + crowdsourcing for curriculum authoring and community feedback loops.

The Cortex system synthesizes elements from both works: goal-to-skill / CoT fine-tuning and a community-driven curriculum update mechanism.

---

## Chapter 3 — Datasets and Methodology

### 3.1 Datasets present in the repository
The repository includes the following primary data artifacts sourced from the **ESCO (European Skills, Competences, Qualifications and Occupations)** database:
*   `occupations_en.csv` — occupations list (3,039 records).
*   `skills_en.csv`, `skillsHierarchy_en.csv` — skill lists (13,939 records) and hierarchy.
*   `occupationSkillRelations_en.csv`, `skillSkillRelations_en.csv` — mappings and relations between occupations and skills (129,004 relations) and between skills (35,847 relations).
*   Precomputed embeddings files: `occupation_embeddings_all-mpnet-base-v2.pkl`.
*   `genmentor.db` — SQLite database integrating all the above data.

### 3.2 Database Schema Details
The system uses a SQLite database (`genmentor.db`) with the following schema:

#### 3.2.1 `skills` Table (13,939 rows)
```sql
CREATE TABLE skills (
 concept_uri TEXT PRIMARY KEY, -- Unique identifier
 skill_type TEXT, -- 'skill' or 'knowledge'
 preferred_label TEXT, -- Human-readable name
 alt_labels TEXT, -- Alternative names (JSON)
 description TEXT, -- Detailed description
 scope_note TEXT -- Usage context
);
```

#### 3.2.2 `occupations` Table (3,039 rows)
```sql
CREATE TABLE occupations (
 concept_uri TEXT PRIMARY KEY, -- Unique identifier
 preferred_label TEXT, -- Job title
 alt_labels TEXT, -- Alternative titles
 description TEXT, -- Role description
 isco_group TEXT -- ISCO classification code
);
```

#### 3.2.3 `occupation_skill_relations` Table (129,004 rows)
```sql
CREATE TABLE occupation_skill_relations (
 occupation_uri TEXT, -- Foreign key to occupations
 skill_uri TEXT, -- Foreign key to skills
 relation_type TEXT, -- 'essential' or 'optional'
 PRIMARY KEY (occupation_uri, skill_uri)
);
```

#### 3.2.4 `skill_skill_relations` Table (35,847 rows)
```sql
CREATE TABLE skill_skill_relations (
 source_skill_uri TEXT, -- Parent skill
 target_skill_uri TEXT, -- Prerequisite skill
 relation_type TEXT, -- 'requires', 'related'
 PRIMARY KEY (source_skill_uri, target_skill_uri)
);
```

---

## Chapter 4 — Implementation

### 4.1 System Architecture
The following diagram illustrates the complete data flow and component interaction within the Cortex system:

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                                 USER INPUT                                  │
│                       (Career Goal + Current Skills)                        │
└─────────────────────────────────────────────────────────────────────────────┘
                                       │
                                       ▼
┌─────────────────────────────────────────────────────────────────────────────┐
│                           PHASE 1: INITIALIZATION                           │
│ ┌──────────────────┐   ┌──────────────────┐   ┌──────────────────┐          │
│ │   Load ESCO DB   │   │ Load Embeddings  │   │ Initialize FAISS │          │
│ │ (13,939 skills)  │   │(3,039 occupations│   │   (ANN Index)    │          │
│ └──────────────────┘   └──────────────────┘   └──────────────────┘          │
│ ┌──────────────────┐   ┌──────────────────┐   ┌──────────────────┐          │
│ │ Connection Pool  │   │    Gemini API    │   │ Resource Curator │          │
│ │ (20 connections) │   │   (2.0 Flash)    │   │ (69 categories)  │          │
│ └──────────────────┘   └──────────────────┘   └──────────────────┘          │
└─────────────────────────────────────────────────────────────────────────────┘
                                       │
                                       ▼
┌─────────────────────────────────────────────────────────────────────────────┐
│                        PHASE 2: OCCUPATION MATCHING                         │
│                                                                             │
│ User Goal ──────► Sentence Transformer ──────► 768-dim Embedding            │
│                   (all-mpnet-base-v2)                                       │
│                           │                                                 │
│ Embedding ──────►    FAISS Index       ──────► Top 50 Candidates            │
│                   (IVF100,Flat)                (Approximate NN)             │
│                           │                                                 │
│ Candidates ──────► Cosine Similarity   ──────► Best Match + Score           │
│                   (Precise ranking)            (0.0 - 1.0)                  │
└─────────────────────────────────────────────────────────────────────────────┘
                                       │
                                       ▼
┌─────────────────────────────────────────────────────────────────────────────┐
│                         PHASE 3: SKILL GAP ANALYSIS                         │
│                                                                             │
│ Matched Occupation ──────► Query ESCO DB ──────► Required Skills            │
│                          (129,004 relations)     (Essential + Optional)     │
│                                   │                                         │
│ Required Skills    ──────► Filter User Skills ──────► Skill Gap             │
│                          (What they know)             (What they need)      │
│                                   │                                         │
│ Skill Gap          ──────► Soft Skill Filter  ──────► Technical Skills Only │
│                          (Remove vague/conceptual)                          │
│                                   │                                         │
│ Skills             ──────► Beginner Filter    ──────► Appropriate Difficulty│
│                          (If few current skills)                            │
└─────────────────────────────────────────────────────────────────────────────┘
                                       │
                                       ▼
┌─────────────────────────────────────────────────────────────────────────────┐
│                   PHASE 4: DEPENDENCY GRAPH CONSTRUCTION                    │
│                                                                             │
│ Skills        ──────► Query Skill Relations ──────► Prerequisites           │
│                       (skill_skill_relations)       (What to learn first)   │
│                                   │                                         │
│ Prerequisites ──────►   NetworkX DiGraph    ──────► Dependency Graph        │
│                       (Directed edges)              (Learning order)        │
│                                   │                                         │
│ Graph         ──────►   Topological Sort    ──────► Ordered Learning Seq    │
│                       (Cycle detection)             (Foundations first)     │
│                                   │                                         │
│ Sequence      ──────►   Category Grouping   ──────► Logical Batches         │
│                       (programming, ML, etc)        (Related skills together)│
└─────────────────────────────────────────────────────────────────────────────┘
                                       │
                                       ▼
┌─────────────────────────────────────────────────────────────────────────────┐
│                    PHASE 5: LEARNING SESSION GENERATION                     │
│                                                                             │
│ ┌─────────────────────────────────────────────────────────────────────┐     │
│ │                        GEMINI 2.0 FLASH (LLM)                       │     │
│ │                                                                     │     │
│ │ Input:                                                              │     │
│ │ - Ordered skill list (from Phase 4)                                 │     │
│ │ - Target occupation                                                 │     │
│ │ - Study hours per week                                              │     │
│ │ - Strict instruction: USE ONLY PROVIDED SKILLS                      │     │
│ │                                                                     │     │
│ │ Output (JSON):                                                      │     │
│ │ - 7-10 learning sessions                                            │     │
│ │ - Each session: title, skills, duration, objectives, difficulty     │     │
│ │ - Prerequisites between sessions                                    │     │
│ │ - Logical progression from beginner to advanced                     │     │
│ └─────────────────────────────────────────────────────────────────────┘     │
│                                   │                                         │
│ Sessions      ──────►   Database Filter     ──────► Only Valid Skills       │
│                       (Remove any LLM additions)                            │
│                                   │                                         │
│ Sessions      ──────►   Soft Skill Filter   ──────► Technical Sessions Only │
│                       (Remove non-actionable)                               │
└─────────────────────────────────────────────────────────────────────────────┘
                                       │
                                       ▼
┌─────────────────────────────────────────────────────────────────────────────┐
│                         PHASE 6: RESOURCE CURATION                          │
│                                                                             │
│ ┌─────────────────────────────────────────────────────────────────────┐     │
│ │                      IMPROVED RESOURCE CURATOR                      │     │
│ │                                                                     │     │
│ │ For each skill in learning path:                                    │     │
│ │                                                                     │     │
│ │ Step 1: Check Curated Database (69 skill categories)                │     │
│ │         - Pre-verified high-quality resources                       │     │
│ │         - YouTube tutorials, Coursera courses, docs                 │     │
│ │         - Instant lookup (0.001s)                                   │     │
│ │                                                                     │     │
│ │ Step 2: Skill Mapping (80+ mappings)                                │     │
│ │         - "programming" → Python resources                          │     │
│ │         - "web development" → JavaScript resources                  │     │
│ │                                                                     │     │
│ │ Step 3: Fallback to External APIs (if not curated)                  │     │
│ │         - GitHub API (educational repos, 5000+ stars)               │     │
│ │         - DuckDuckGo search (for specific topics)                   │     │
│ │                                                                     │     │
│ │ Step 4: Quality Filtering                                           │     │
│ │         - Remove broken links                                       │     │
│ │         - Verify URLs start with http                               │     │
│ └─────────────────────────────────────────────────────────────────────┘     │
│                                   │                                         │
│ Resources     ──────► Async Batch Processing ──────► Parallel Fetching      │
│                       (aiohttp, asyncio)             (76% faster)           │
│                                   │                                         │
│ Resources     ──────►    Cache Storage       ──────► SQLite Cache DB        │
│                       (24-hour TTL)                  (Instant future lookups)│
└─────────────────────────────────────────────────────────────────────────────┘
                                       │
                                       ▼
┌─────────────────────────────────────────────────────────────────────────────┐
│                         PHASE 7: OUTPUT GENERATION                          │
│                                                                             │
│ Complete Learning Path:                                                     │
│ ┌─────────────────────────────────────────────────────────────────────┐     │
│ │ {                                                                   │     │
│ │   "occupation": { "title": "...", "similarity": 0.89 },             │     │
│ │   "skill_gap": [ { "uri": "...", "label": "..." }, ... ],           │     │
│ │   "learning_path": {                                                │     │
│ │     "sessions": [                                                   │     │
│ │       {                                                             │     │
│ │         "session_id": 1,                                            │     │
│ │         "title": "Python Fundamentals",                             │     │
│ │         "skills": ["python", "programming basics"],                 │     │
│ │         "duration_hours": 8,                                        │     │
│ │         "difficulty": "beginner",                                   │     │
│ │         "objectives": ["...", "..."],                               │     │
│ │         "prerequisites": []                                         │     │
│ │       },                                                            │     │
│ │       ...                                                           │     │
│ │     ],                                                              │     │
│ │     "total_hours": 52,                                              │     │
│ │     "estimated_weeks": 6                                            │     │
│ │   },                                                                │     │
│ │   "resources": {                                                    │     │
│ │     "python": [                                                     │     │
│ │       { "title": "...", "url": "...", "type": "course" },           │     │
│ │       ...                                                           │     │
│ │     ]                                                               │     │
│ │   }                                                                 │     │
│ │ }                                                                   │     │
│ └─────────────────────────────────────────────────────────────────────┘     │
│                                   │                                         │
│ JSON          ──────►    HTML Visualizer     ──────► Interactive Webpage    │
│                       (Professional styling)         (Clickable resources)  │
└─────────────────────────────────────────────────────────────────────────────┘
```

### 4.2 Component 2: Sentence Transformers
**Model**: `all-mpnet-base-v2`
**Architecture**:
The system uses a BERT-based transformer model to convert text into 768-dimensional vectors.
1.  **Tokenizer**: Converts text into subwords (30,522 vocab).
2.  **MPNet Encoder**: 12 transformer layers, 12 attention heads, 768 hidden dimensions.
3.  **Mean Pooling**: Averages all token embeddings.
4.  **Normalization**: Produces a unit vector.

**Semantic Similarity**:
$$ Similarity(A, B) = \frac{A \cdot B}{\|A\| \|B\|} $$
This allows the system to understand that "Data Scientist" and "Machine Learning Engineer" are semantically close (Similarity ~0.82), while "Data Scientist" and "Pizza Chef" are distant (Similarity ~0.15).

### 4.3 Component 3: FAISS Indexing
**Library**: Facebook AI Similarity Search (FAISS)
**Index Type**: `IVF100,Flat`
*   **IVF100**: Divides the vector space into 100 Voronoi cells (clusters) using K-Means clustering.
*   **Flat**: Performs exact distance computation within the identified cells.

**Search Process**:
1.  **Coarse Quantizer**: Finds the nearest 10 centroids (`nprobe=10`) to the query vector.
2.  **Fine Search**: Searches only within those 10 clusters (approx. 300 items) instead of the full 3,039 dataset.
3.  **Result**: Returns top 50 candidates ~10x faster than linear search.

### 4.4 Component 4: Google Gemini 2.0 Flash
**API**: `google-generativeai`
**Model**: `gemini-2.0-flash`
**Purpose**: Generates structured learning sessions from the ordered skill list.

**Prompt Structure**:
The system enforces strict constraints to ensure the LLM only uses skills present in the database:
```text
You are a career learning path expert.
Create a structured learning path for someone wanting to become a {occupation}.
IMPORTANT: Use ONLY the following skills from our database:
{skill_list}
Create 7-10 learning sessions...
```

**Safety Settings**:
Configured to `BLOCK_NONE` for Harassment, Hate Speech, Sexually Explicit, and Dangerous Content to prevent false positives on technical terms.

### 4.5 Component 5: RAG (Retrieval-Augmented Generation)
The system uses RAG to generate detailed learning content for individual skills.
1.  **Retrieval**: Fetches skill info, related skills, occupations, and curated resources from the SQLite database.
2.  **Augmentation**: Builds a comprehensive prompt containing all retrieved context.
3.  **Generation**: Gemini 2.0 Flash generates contextualized learning objectives, topics, exercises, and assessment criteria.

### 4.6 Component 6 & 7: Resource Curation (Improved & Async)
**Improved Resource Curator**:
*   **Direct Lookup**: Checks a dictionary of 69 curated skill categories (O(1) access).
*   **Skill Mapping**: Maps 80+ variations (e.g., "web programming" -> "javascript").
*   **Fallbacks**: Uses GitHub API (min 5000 stars) and DuckDuckGo if no curated resource is found.

**Async Resource Curator**:
Uses `aiohttp` and `asyncio` to fetch resources for multiple skills in parallel.
*   **Sequential**: Total Time = Sum of all fetch times (~9s for 3 skills).
*   **Parallel**: Total Time = Max of fetch times (~3s for 3 skills).
*   **Speedup**: 76% faster.

### 4.7 Component 8: Connection Pooling
Implemented using `queue.Queue` and `threading.Lock`.
*   **Pool Size**: 20 connections.
*   **Mechanism**: Pre-creates connections and reuses them, avoiding the ~50ms overhead of opening/closing connections for every query.
*   **Result**: Database queries are ~10x faster for repeated operations.

### 4.8 Component 9: Skill Filtering
The system applies multiple filters to ensure quality:
1.  **Soft Skill Filter**: Removes non-actionable skills like "critical thinking" or "communication" using a predefined set and partial matching.
2.  **Beginner Filter**: Removes advanced topics (e.g., "microservices orchestration") if the user has fewer than 3 current skills.
3.  **Database-Only Filter**: Removes any hallucinations from the LLM output that don't match the ESCO database.

### 4.9 Component 10: Dependency Graph
**Library**: `networkx`
**Construction**:
1.  **Nodes**: All required skills.
2.  **Edges**: Directed edges based on `skill_skill_relations` (prerequisites).
3.  **Ordering**: Performs a **Topological Sort** to ensure prerequisites are scheduled before dependent skills.
4.  **Cycle Handling**: Falls back to category-based priority (Programming -> Database -> Tools) if cycles are detected.

### 4.10 Component 11: Community Feedback System
Allows the curriculum to evolve based on user input.
*   **Votes Table**: Tracks upvotes/downvotes on skills and resources.
*   **Suggestions Table**: Stores user-suggested resources.
*   **API**: Endpoints for submitting votes and retrieving trending items.

---

## Chapter 5 — Results and Performance Analysis

### 5.1 Performance Benchmarks
The following table summarizes the performance improvements achieved through the implemented optimizations:

| Component | Before Optimization | After Optimization | Improvement |
|-----------|--------------------|--------------------|-------------|
| Occupation Matching | 5.2s (linear) | 0.86s (FAISS) | **6x faster** |
| Database Queries | 2.5s | 0.85s (pooled) | **66% faster** |
| Resource Fetching | 12s (sequential) | 3s (async) | **76% faster** |
| Overall System | 45s | 18s | **60% faster** |

### 5.2 Quality Metrics & Calculation Methodology
The system's performance was evaluated using four key metrics. The calculation methodology for each is detailed below:

#### 5.2.1 Similarity Score (Target: >80%, Achieved: 83.7%)
**Definition**: Measures the semantic closeness between the user's natural language goal and the matched occupation.
**Formula**:
$$ S_{final} = \min(1.0, S_{cosine} \times B_{domain} \times B_{keyword}) $$
Where:
*   $S_{cosine} = \frac{A \cdot B}{\|A\| \|B\|}$ (Cosine Similarity between 768-dim embeddings)
*   $B_{domain}$: Domain-specific boost factor (1.0 - 1.5x) for exact role matches (e.g., "Data Scientist").
*   $B_{keyword}$: Keyword density boost based on term overlap.

#### 5.2.2 Skill Relevance Score (Target: >85/100, Achieved: 95/100)
**Definition**: Quantifies how appropriate the recommended skills are for the target occupation.
**Calculation**:
Each skill is assigned a relevance score ($R_s$) based on a tiered priority system:
*   **Tier 1 (Critical)**: 10 points (e.g., Python for Data Science).
*   **Tier 2 (Important)**: 8 points (e.g., Visualization).
*   **Tier 3 (Standard)**: 5 points (General tools).
*   **Essential Flag**: +2 points if marked 'essential' in ESCO database.

$$ \text{Average Relevance} = \frac{\sum R_s}{\text{Total Skills}} \times 10 $$
(Normalized to a 0-100 scale).

#### 5.2.3 Resource Coverage (Target: >70%, Achieved: 80%)
**Definition**: The percentage of recommended skills for which high-quality learning resources were successfully curated.
**Formula**:
$$ \text{Coverage} = \left( \frac{\text{Count}(Skills_{with\_resources})}{\text{Count}(Skills_{total})} \right) \times 100 $$
*   *Skills_with_resources*: Skills returning valid URLs from Curated DB, GitHub API, or DuckDuckGo.

#### 5.2.4 Test Pass Rate (Target: 100%, Achieved: 100%)
**Definition**: The success rate of the system across the comprehensive test suite of 25 scenarios.
**Criteria for Pass**:
1.  **Keyword Match**: Matched occupation contains expected keywords.
2.  **Skill Sufficiency**: Identified skill gap > Minimum threshold (5-8 skills).
3.  **Path Validity**: Generated learning path has valid sessions, durations, and no hallucinations.

**Formula**:
$$ \text{Pass Rate} = \left( \frac{\text{Tests}_{passed}}{\text{Tests}_{total}} \right) \times 100 $$

### 5.3 Complete System Flow Analysis
The following breakdown illustrates the timing and logic of a typical user request ("I want to become a data scientist"):

1.  **Encode Goal (0.1s)**: Sentence Transformer converts text to 768-dim embedding.
2.  **Match Occupation (0.8s)**: FAISS retrieves top 50; Cosine Similarity identifies "Data Scientist" (89% match).
3.  **Identify Skill Gap (2.5s)**:
    *   Query ESCO DB -> 45 required skills.
    *   Filter user skills -> 43 needed.
    *   Filter soft skills -> 28 technical skills.
    *   Filter for beginners -> 22 appropriate skills.
4.  **Build Dependency Graph (0.5s)**: NetworkX builds DAG; Topological sort determines order.
5.  **Generate Sessions (8s)**: Gemini 2.0 Flash groups skills into 10 sessions; Filters ensure validity.
6.  **Curate Resources (3s)**: Async fetch for 22 skills; Check curated DB -> Map skills -> Fallback to API -> Cache results.
7.  **Generate Output (0.2s)**: Combine into JSON and render HTML.

**Total Time**: ~15-18 seconds (down from 45s).

---

## Chapter 6 — Timeline & Plan (Updated)

### 6.1 Completed milestones (to date)
*   ✅ Data ingestion and embedding pipeline implemented.
*   ✅ Core similarity & scheduling algorithms developed.
*   ✅ REST API and local DB prepared.
*   ✅ **Optimization Layer:** FAISS and Async curation integrated.
*   ✅ **Community Feedback:** Voting and suggestion system implemented.
*   ✅ **Visualizations:** Interactive HTML output generation completed.
*   ✅ **Final Validation:** 100% success rate on comprehensive test suite.

### 6.2 Plan & deadlines — Final completion target: 30 November 2025
*   **Project is effectively complete.**
*   Remaining tasks involve final code cleanup, documentation refinement, and preparing presentation materials for the final defense.

---

## Chapter 7 — Limitations & Risks

### 7.1 Known limitations
*   **LLM Dependency:** The system relies on the Google Gemini API, which requires an internet connection and API key.
*   **Resource Availability:** While coverage is high (80%), some niche skills may still lack high-quality curated resources.
*   **Cold Start:** The community feedback system requires an active user base to become effective.

### 7.2 Mitigation strategies
*   **Caching:** Extensive caching (SQLite, Pickle) is used to minimize API calls and latency.
*   **Fallbacks:** The system has robust fallbacks (e.g., using DuckDuckGo if curated resources are missing, using Numpy if FAISS is unavailable).
*   **Pre-seeding:** The database is pre-seeded with 69 categories of high-quality resources to mitigate the cold start problem.

---

## References
[1] Wang et al., “LLM-powered Multi-agent Framework for Goal-oriented Learning in Intelligent Tutoring System.” WWW '25.
[2] Tavakoli et al., “Hybrid Human-AI Curriculum Development for Personalised Informal Learning Environments.” LAK22.
[3] Manasvi Vedanta, Cortex – Adaptive Learning Platform, GitHub Repository, 2025. [https://github.com/Manasvi-Vedanta/Hybrid-GenMentor](https://github.com/Manasvi-Vedanta/Hybrid-GenMentor)

---

## Declaration
I declare that this written submission represents my ideas in my own words and where others' ideas or words have been included, I have adequately cited and referenced the original sources. I also declare that I have adhered to all principles of academic honesty and integrity.

**Name of the Student:** Manasvi Vedanta  
**Signature and Date:** ____________________

**Faculty Advisor:** Dr. Sonia Khetarpaul  
**Signature and Date:** ____________________
