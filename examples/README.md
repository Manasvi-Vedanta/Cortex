# API Response Examples

This directory contains real JSON response examples from the GenMentor Enhanced Features API endpoints.

## Files Overview

### Community Feedback Endpoints
- `vote_response.json` - Response from POST /api/feedback/vote
- `suggest_response.json` - Response from POST /api/feedback/suggest
- `pending_suggestions_response.json` - Response from GET /api/feedback/suggestions/pending
- `vote_on_suggestion_response.json` - Response from POST /api/feedback/suggestions/:id/vote
- `trending_response.json` - Response from GET /api/feedback/trending
- `metrics_response.json` - Response from GET /api/feedback/metrics

### Visualization Endpoints
- `visualize_response.json` - Complete response from POST /api/path/visualize
- `gantt_sample.json` - Extracted gantt_data structure
- `dependency_graph_sample.json` - Extracted dependency_graph structure

### Resource Curation Endpoints
- `search_resources_response.json` - Response from GET /api/resources/search
- `add_resource_response.json` - Response from POST /api/resources/add
- `get_skill_resources_response.json` - Response from GET /api/resources/skill/:uri
- `rate_resource_response.json` - Response from POST /api/resources/rate
- `popular_resources_response.json` - Response from GET /api/resources/popular

### Integrated Endpoint
- `path_with_resources_response.json` - Complete response from POST /api/path/with-resources

## How These Were Generated

These examples were captured from actual API calls during testing. They represent the real data structures your application will work with.

## Usage

Use these files to:
- Understand the exact JSON structure returned by each endpoint
- Test frontend code without needing the backend running
- Document API contracts for other developers
- Create mock data for unit tests
