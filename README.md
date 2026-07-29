# OpenSearch

OpenSearch is a lightweight, open-source search engine prototype built to demonstrate a full-stack pipeline for crawling, indexing, ranking, and reviewing content.

It combines a FastAPI backend, a React dashboard, and supporting crawler/indexer/ranking components so the project can be run locally or with Docker.

## What is included

- FastAPI backend with search, auth, admin, ranking, and dashboard routes
- Lightweight ranking service for reordering candidate results
- Scrapy-based crawler scaffold for collecting page content
- Indexer module that prepares documents for downstream search systems
- React dashboard for reviewing content in a human-in-the-loop workflow
- Docker and Docker Compose support for local development

## Project structure

```text
OpenSearch/
├── backend/
│   ├── app/
│   │   ├── main.py
│   │   ├── models.py
│   │   ├── schemas.py
│   │   ├── config.py
│   │   ├── routers/
│   │   └── services/
│   ├── requirements.txt
│   └── Dockerfile
├── crawler/
│   └── spiders/
├── frontend/
│   ├── src/
│   ├── package.json
│   └── Dockerfile
├── indexer/
│   └── mappings.json
├── ranking/
│   └── model.py
├── docker-compose.yml
└── README.md
```

## Quick start

### Option 1: Docker Compose

From the repository root:

```bash
docker compose up --build
```

Then open:

- Frontend: http://localhost:5173
- Backend API docs: http://localhost:8000/docs

### Option 2: Local development

#### Backend

```bash
cd backend
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

#### Frontend

```bash
cd frontend
npm install
npm run dev
```

## Running tests

```bash
cd backend
PYTHONPATH=. pytest tests -q
```

## Notes

- The current repository is a functional prototype rather than a production-ready search engine.
- Elasticsearch integration is implemented as a best-effort sync layer, so it can be used when the dependency is available.
- The React dashboard is designed to display reviewable content and can be extended for moderation workflows.

## Contributing

Contributions are welcome. Fork the repository, create a branch, make your changes, and open a pull request.

## License

This project is licensed under the MIT License. See the LICENSE file for details.


