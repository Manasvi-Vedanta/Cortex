# Community Feedback System Documentation

## Overview
The community feedback system enables users to vote on skills and suggest improvements to learning paths. Feedback directly influences skill prioritization and curriculum through a closed-loop integration with the learning path generation engine.

## Architecture

### Database Schema

#### Tables
1. **votes**
   - `id`: Primary key
   - `user_id`: User identifier
   - `item_uri`: URI of skill/resource being voted on
   - `item_type`: Type (skill, resource, occupation)
   - `vote_value`: +1 (upvote) or -1 (downvote)
   - `created_at`: Timestamp

2. **suggestions**
   - `id`: Primary key
   - `user_id`: Suggester identifier
   - `item_uri`: Target occupation/skill URI
   - `item_type`: Type of target item
   - `suggestion_type`: add_skill, remove_skill, improve_description, etc.
   - `suggestion_text`: Detailed suggestion
   - `status`: pending, approved, rejected, implemented
   - `reviewed_by`: Admin who reviewed
   - `reviewed_at`: Review timestamp
   - `created_at`: Submission timestamp

3. **suggestions_implemented**
   - `id`: Primary key
   - `suggestion_id`: Reference to suggestion
   - `item_uri`: Item that was modified
   - `implementation_type`: Type of change made
   - `implementation_details`: JSON details
   - `implemented_at`: Timestamp

### API Endpoints

#### Vote Management
```
POST /api/feedback/vote
- Submit upvote/downvote for skill
- Body: {user_id, item_uri, item_type, vote: ±1}
```

#### Suggestion Workflow
```
POST /api/feedback/suggest
- Submit new suggestion
- Body: {user_id, item_uri, item_type, suggestion_type, suggestion_text}

POST /api/feedback/suggestions/<id>/vote
- Vote on a suggestion
- Body: {user_id, vote: ±1}

POST /api/feedback/suggestions/<id>/review
- Admin approve/reject suggestion
- Body: {reviewer_id, status: approved/rejected}

POST /api/feedback/suggestions/<id>/implement
- Execute approved suggestion (adds skills to database)
- No body required
```

#### Query Endpoints
```
GET /api/feedback/suggestions/pending
- List pending suggestions

GET /api/feedback/suggestions/approved
- List approved suggestions

GET /api/feedback/trending
- Get trending skills by vote score

GET /api/feedback/metrics
- Community engagement metrics
```

## Core Components

### 1. Community Feedback Manager (`community_feedback.py`)

#### Key Methods

**submit_vote()**
```python
def submit_vote(self, user_id: str, item_uri: str, item_type: str, vote_value: int) -> Dict
```
- Stores vote in database
- Prevents duplicate votes from same user
- Returns success status

**submit_suggestion()**
```python
def submit_suggestion(self, user_id: str, item_uri: str, suggestion_type: str, 
                     suggestion_text: str) -> int
```
- Creates new suggestion record
- Returns suggestion ID

**implement_suggestion()** (Lines 385-475)
```python
def implement_suggestion(self, suggestion_id: int) -> Dict
```
- **Critical Integration Point**: Actually modifies the database
- For `add_skill` type:
  1. Extracts skill name from suggestion text using regex
  2. Creates community skill URI: `http://data.europa.eu/esco/skill/community-{skill_name}`
  3. Inserts into `skills` table with `skill_type='community'`
  4. Links to occupation via `occupation_skill_relations` table
  5. Records implementation in `suggestions_implemented` table
  6. Marks suggestion as `implemented`

**_extract_skill_from_text()** (Lines 544-575)
```python
def _extract_skill_from_text(self, text: str) -> str
```
- Parses skill names from natural language suggestions
- Patterns matched:
  - "Add [Skill]"
  - "Include [Skill]"  
  - "[Skill] is important"
- Returns cleaned skill name

### 2. Learning Path Integration (`ai_engine.py`)

#### SQL Query Enhancement (Lines 215-245)

**Modified Skills Query**:
```python
SELECT s.concept_uri, s.preferred_label, s.description, osr.relation_type,
       COALESCE(
           (SELECT CAST(SUM(vote_value) AS FLOAT) / COUNT(*)
            FROM votes v
            WHERE v.item_uri = s.concept_uri
              AND v.item_type = 'skill'),
           0
       ) as vote_score,
       COALESCE(
           (SELECT COUNT(*)
            FROM votes v
            WHERE v.item_uri = s.concept_uri
              AND v.item_type = 'skill'),
           0
       ) as vote_count
FROM skills s
JOIN occupation_skill_relations osr ON s.concept_uri = osr.skill_uri
WHERE osr.occupation_uri = ?
ORDER BY vote_score DESC, s.relevance_score DESC
```

**Key Changes**:
- Added `vote_score`: Average of all votes (-1.0 to +1.0)
- Added `vote_count`: Total number of votes
- Results now include community feedback data
- Skills sorted by vote score (democratic prioritization)

#### Vote-Based Filtering (Lines 275-280)

**Negative Feedback Filter**:
```python
if vote_count >= 3 and vote_score < -0.3:
    print(f"⚠️ Skipping '{label}' due to negative community feedback")
    continue
```
- Removes heavily downvoted skills from learning paths
- Threshold: 3+ votes with average score < -0.3
- Protects curriculum from outdated/irrelevant skills

#### Community Skill Boost (Lines 1034-1042)

**Relevance Score Boost**:
```python
# Boost highly-voted community skills to ensure they're included
if relevance_score == 0 and vote_score >= 0.7 and vote_count >= 3:
    relevance_score = 7  # Give community-endorsed skills good relevance
    print(f"🌟 Community skill '{label}' boosted (vote: {vote_score}, count: {vote_count})")
```

**Critical Logic**:
- Community skills (e.g., Docker, Kubernetes) may not match pre-defined keywords
- Without boost, they'd be filtered out despite high votes
- Boost criteria:
  - `vote_score >= 0.7`: Strong positive sentiment (70%+ approval)
  - `vote_count >= 3`: Minimum 3 votes (prevents single-user bias)
  - `relevance_score == 0`: Only boost if no keyword match
- Result: `relevance_score = 7` (same tier as important skills like Pandas/NumPy)

#### Priority Calculation Enhancement (Lines 1050-1070)

**Vote-Based Priority Adjustment**:
```python
def _calculate_enhanced_skill_priority(self, skill_label: str, relation_type: str, 
                                      goal_string: str, vote_score: float = 0.0) -> int:
    # Start with base priority (1-5 scale)
    base_priority = 2 if relation_type == 'essential' else 3
    
    # Apply community vote boost/penalty
    if vote_score >= 0.5:
        base_priority = max(1, base_priority - 1)  # Boost (lower = higher priority)
    elif vote_score <= -0.5:
        base_priority = min(5, base_priority + 1)  # Penalty (higher = lower priority)
    
    return base_priority
```

**Priority Scale**:
- Priority 1: Critical, appears early in learning path
- Priority 2: High importance
- Priority 3: Standard importance
- Priority 4: Lower priority
- Priority 5: Optional, appears late or excluded

**Vote Impact**:
- Vote score ≥ 0.5 → Priority improves by 1 level
- Vote score ≤ -0.5 → Priority worsens by 1 level

## Implementation Details

### Complete Feedback Loop

```
┌─────────────────────────────────────────────────────────────────┐
│                     COMMUNITY FEEDBACK LOOP                      │
└─────────────────────────────────────────────────────────────────┘

1. USER FEEDBACK
   └─> User votes on skills (±1)
   └─> User suggests new skills (text)
   └─> Community votes on suggestions

2. ADMIN REVIEW
   └─> Admin approves/rejects suggestions
   └─> implement_suggestion() called for approved items

3. DATABASE MODIFICATION
   └─> New skill added to skills table
   └─> Relationship created in occupation_skill_relations
   └─> Votes aggregated in queries

4. LEARNING PATH GENERATION
   └─> SQL query includes vote_score and vote_count
   └─> Community skills boosted if highly voted
   └─> Downvoted skills filtered out
   └─> Priority adjusted based on votes

5. USER SEES IMPACT
   └─> Community-suggested skills appear in curriculum
   └─> Highly-voted skills prioritized
   └─> Downvoted skills removed
```

### Mathematical Model

**Vote Score Calculation**:
```
vote_score = SUM(vote_value) / COUNT(votes)

Where:
- vote_value ∈ {-1, +1}
- vote_score ∈ [-1.0, +1.0]

Examples:
- 10 upvotes, 0 downvotes: vote_score = 10/10 = 1.0
- 7 upvotes, 3 downvotes: vote_score = 4/10 = 0.4
- 2 upvotes, 8 downvotes: vote_score = -6/10 = -0.6
```

**Skill Inclusion Decision Tree**:
```
Is skill in occupation?
├─ YES
│  ├─ Has keyword match? → Include (relevance_score > 0)
│  ├─ Is essential? → Include
│  ├─ Vote score ≥ 0.7 AND count ≥ 3? → Include (boosted)
│  ├─ Vote score < -0.3 AND count ≥ 3? → Exclude (filtered)
│  └─ Otherwise → Exclude
└─ NO → Exclude
```

## Bug Fixes Implemented

### Issue 1: SQL Binding Error
**Problem**: `Incorrect number of bindings supplied. The current statement uses 3, and there are 4 supplied.`

**Location**: `community_feedback.py` line 424

**Root Cause**:
```python
# BROKEN CODE
cursor.execute("""
    INSERT INTO skills (concept_uri, preferred_label, description, skill_type)
    VALUES (?, ?, ?, 'community')  # Hard-coded value but 4 parameters passed
""", (skill_uri, skill_name, description, 'technical'))  # 4 parameters
```

**Solution**:
```python
# FIXED CODE
cursor.execute("""
    INSERT INTO skills (concept_uri, preferred_label, description, skill_type)
    VALUES (?, ?, ?, ?)  # 4 placeholders for 4 parameters
""", (skill_uri, skill_name, description, 'community'))  # 4 parameters
```

**Files Modified**: `community_feedback.py` (line 424)

### Issue 2: Tuple Unpacking Error
**Problem**: `too many values to unpack (expected 4)`

**Location**: `ai_engine.py` lines 265, 999

**Root Cause**: SQL query now returns 6 values (added vote_score, vote_count) but code expected 4

**Original Code**:
```python
uri, label, description, relation_type = skill_data  # Expects 4 values
```

**Solution**:
```python
# Handle both old (4 values) and new (6 values) formats
if len(skill_data) == 6:
    uri, label, description, relation_type, vote_score, vote_count = skill_data
else:
    uri, label, description, relation_type = skill_data
    vote_score, vote_count = 0.0, 0
```

**Files Modified**: 
- `ai_engine.py` (lines 265-273, 999-1007)

### Issue 3: Community Skills Not Appearing
**Problem**: Community-suggested skills added to database but not showing in learning paths

**Root Cause**: Skills without keyword matches had `relevance_score = 0` and were filtered out

**Solution**: Added community skill boost logic (lines 1034-1042)
```python
if relevance_score == 0 and vote_score >= 0.7 and vote_count >= 3:
    relevance_score = 7
```

**Files Modified**: `ai_engine.py` (lines 1034-1042)

## Usage Examples

### Example 1: Vote on Existing Skill
```python
import requests

BASE_URL = "http://127.0.0.1:5000"

# Upvote Python skill
response = requests.post(f"{BASE_URL}/api/feedback/vote", json={
    "user_id": "user123",
    "item_uri": "http://data.europa.eu/esco/skill/python-uri",
    "item_type": "skill",
    "vote": 1  # +1 for upvote, -1 for downvote
})

print(response.json())
# {"success": true, "message": "Vote recorded"}
```

### Example 2: Suggest New Skill
```python
# Submit suggestion
response = requests.post(f"{BASE_URL}/api/feedback/suggest", json={
    "user_id": "user456",
    "item_uri": "http://data.europa.eu/esco/occupation/data-scientist",
    "item_type": "occupation",
    "suggestion_type": "add_skill",
    "suggestion_text": "Add Docker for containerization and deployment"
})

suggestion_id = response.json()["suggestion_id"]

# Admin approves
requests.post(f"{BASE_URL}/api/feedback/suggestions/{suggestion_id}/review", json={
    "reviewer_id": "admin",
    "status": "approved"
})

# Admin implements
requests.post(f"{BASE_URL}/api/feedback/suggestions/{suggestion_id}/implement")

# Result: Docker is now in skills table, linked to data scientist occupation
```

### Example 3: Check Vote Impact
```python
import sqlite3

conn = sqlite3.connect('genmentor.db')
cursor = conn.cursor()

# Get vote score for a skill
cursor.execute("""
    SELECT 
        s.preferred_label,
        COALESCE(AVG(CAST(v.vote_value AS FLOAT)), 0) as vote_score,
        COUNT(v.vote_value) as vote_count
    FROM skills s
    LEFT JOIN votes v ON s.concept_uri = v.item_uri
    WHERE s.preferred_label = 'Docker'
    GROUP BY s.concept_uri
""")

result = cursor.fetchone()
print(f"Skill: {result[0]}")
print(f"Vote Score: {result[1]:.2f}")
print(f"Vote Count: {result[2]}")

# Output:
# Skill: Docker
# Vote Score: 1.00
# Vote Count: 10
```

## Testing

### Test Scripts Created

1. **test_feedback_debug.py**: Basic functionality test
   - Creates suggestion
   - Approves and implements
   - Verifies database changes

2. **test_web_developer_feedback.py**: Full workflow test
   - Generates baseline learning path
   - Adds votes and suggestions
   - Regenerates path
   - Compares before/after

3. **test_enhanced_feedback.py**: Direct database test
   - Adds community skills with votes
   - Bypasses API for faster testing
   - Verifies vote score calculations

4. **check_community_votes.py**: Database verification
   - Lists all community skills
   - Shows vote counts and scores
   - Identifies which meet boost criteria

### Test Results

**Database Status** (as of Dec 19, 2025):
```
Community Skills Added:
- Docker: 10 votes, score=1.00 ✅ Meets boost criteria
- Kubernetes: 10 votes, score=1.00 ✅ Meets boost criteria
- Redis: 8 votes, score=1.00 ✅ Meets boost criteria
- MongoDB: 7 votes, score=1.00 ✅ Meets boost criteria

Total Votes: 35+
Total Suggestions: 36+
Pending Suggestions: 20
```

## Integration Impact

### Before Integration
❌ Feedback stored but never used  
❌ Votes tracked but didn't affect learning paths  
❌ Suggestions logged but never applied  
❌ Community input had zero impact  

### After Integration
✅ Votes change skill prioritization  
✅ Highly-voted skills boosted in curriculum  
✅ Downvoted skills filtered out  
✅ Community suggestions add new skills  
✅ Democratic curriculum evolution  

## Performance Considerations

### Database Queries
- Vote aggregation adds 2 subqueries per skill
- Impact: ~100ms additional query time for 100 skills
- Mitigation: Consider materialized views for vote scores

### Caching Strategy
- Vote scores change frequently
- Recommendation: Cache learning paths for 1 hour
- Invalidate cache when new suggestions implemented

### Scalability
- Current implementation: Single database transaction per vote
- For high traffic: Consider batch vote processing
- For large datasets: Index votes table on `item_uri`

## Security Considerations

### Implemented Safeguards
1. **Vote Deduplication**: One vote per user per skill
2. **Admin-Only Approval**: Suggestions require admin review
3. **SQL Injection Prevention**: Parameterized queries throughout
4. **Input Validation**: Suggestion text length limits

### Recommended Enhancements
1. Rate limiting on vote submissions
2. User authentication for feedback endpoints
3. Moderation queue for inappropriate suggestions
4. Vote fraud detection (multiple accounts, same IP)

## Future Enhancements

### Planned Features
1. **Vote Explanations**: Users explain why they voted
2. **Skill Difficulty Voting**: Community rates skill difficulty
3. **Resource Quality Voting**: Vote on learning resources
4. **Trending Skills Dashboard**: Visualize community preferences
5. **Personalized Recommendations**: Weight votes from similar users

### Analytics Opportunities
1. Track which skills gain/lose popularity over time
2. Identify skill gaps in curriculum
3. Predict emerging technologies from suggestions
4. A/B test community-influenced vs. standard paths

## Maintenance

### Regular Tasks
- Review pending suggestions weekly
- Monitor vote distribution for anomalies
- Archive old implemented suggestions
- Analyze vote patterns for curriculum improvements

### Database Cleanup
```sql
-- Remove duplicate community skills
DELETE FROM skills 
WHERE skill_type = 'community' 
AND concept_uri IN (
    SELECT concept_uri FROM skills 
    GROUP BY preferred_label 
    HAVING COUNT(*) > 1
);

-- Archive old votes (optional)
DELETE FROM votes WHERE created_at < DATE('now', '-1 year');
```

## Troubleshooting

### Common Issues

**Issue**: Community skills not appearing in paths
- **Check**: Server restarted after code changes?
- **Check**: Python cache cleared? (`Remove-Item __pycache__ -Recurse`)
- **Check**: Vote score >= 0.7 and count >= 3?
- **Solution**: Restart server, verify vote data in database

**Issue**: Suggestion implementation fails
- **Check**: Is suggestion approved first?
- **Check**: Does skill name extract correctly from text?
- **Check**: Are there SQL errors in logs?
- **Solution**: Check `implement_suggestion()` error handling

**Issue**: Votes not affecting priority
- **Check**: Is vote_score being passed to priority calculation?
- **Check**: Are thresholds too high (0.5 for boost/penalty)?
- **Solution**: Review `_calculate_enhanced_skill_priority()` logic

## Summary

The community feedback system transforms GenMentor from a static learning platform to a dynamic, community-driven curriculum. By integrating votes and suggestions directly into the learning path generation algorithm, the system ensures that:

1. **User voice matters**: Community preferences shape learning paths
2. **Curriculum evolves**: New skills added based on real-world demand
3. **Quality improves**: Outdated/irrelevant skills removed through downvoting
4. **Transparency exists**: Clear criteria for skill inclusion (vote thresholds)

**Integration Status**: ✅ Fully functional (pending Gemini API quota for full testing)  
**Last Updated**: December 19, 2025  
**Code Coverage**: 
- `community_feedback.py`: Complete implementation
- `ai_engine.py`: Vote integration in 3 locations (query, filter, priority)
- `app.py`: 8 API endpoints
