# API reference

## Backend endpoints

### Health

- GET /health
- Returns a simple health check payload.

### Search

- POST /search
- Accepts a JSON body with:
  - query: string
  - user_id: optional integer
  - page: optional integer
  - page_size: optional integer
- Returns ranked results in the SearchResponse schema.

### Ranking

- POST /rank
- Accepts a query and a list of candidate documents.
- Returns the candidates sorted by combined relevance score.

### Dashboard

- GET /dashboard/flags
- Returns a list of reviewable content items for the HITL dashboard.
