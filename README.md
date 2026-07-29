OpenSearch
An Open-Source, Transparent Google Search Alternative

https://github.com/erikamjp150-bot/OpenSearch/actions/workflows/ci.yml/badge.svg
https://img.shields.io/badge/License-MIT-yellow.svg
https://img.shields.io/badge/python-3.11+-blue.svg

📖 Overview
OpenSearch is a fully open-source, privacy-respecting search engine alternative to Google Search. Built with transparency and user agency at its core, the platform provides:

Complete Visibility: Every component—from crawling to ranking—is auditable and open.

Privacy-First: No behavioral tracking, data minimization by design, and full user control over personal data.

Community-Governed: Decisions about ranking, moderation, and features are made transparently by the community.

Open Architecture: Modular and extensible components that can be deployed independently.

🎯 Mission
To create a search engine that serves users first—not advertisers. We prioritize relevant, quality results over engagement metrics and provide a public alternative to opaque, corporate-controlled search systems.

🧰 Tech Stack
Component	Technology	Purpose
Frontend	React + TypeScript	User interface for search and administration
Backend API	FastAPI (Python)	REST API for search, authentication, and admin
Search Index	Elasticsearch / Meilisearch	Full-text search and inverted index
Ranking Engine	PyTorch + Transformers	Neural re-ranking of search results
Database	PostgreSQL	User data, search history, metadata
Cache	KeyDB / Redis	Query caching and session storage
Storage	MinIO (S3-compatible)	Stored webpage content
Crawler	Scrapy + Airflow	Distributed web crawling and extraction
Messaging	Kafka	Event streaming for real-time updates
Infrastructure	Docker, Kubernetes, Terraform	Containerization and orchestration
✨ Key Features
Transparent Ranking: Our ranking model is open-source and not optimized for ad revenue or engagement metrics.

Privacy Protection: No tracking pixels, no personal data sales, and full GDPR/CCPA compliance.

Audit Trail: All search queries and ranking decisions are logged for research and oversight.

Human-in-the-Loop Moderation: Community-reviewed content moderation and result correction.

Personalization Controls: Users can opt-in to personalization with full visibility into how their data is used.

📁 Project Structure
text
OpenSearch/
├── backend/                 # FastAPI backend service
│   ├── app/
│   │   ├── main.py         # Application entry point
│   │   ├── models.py       # SQLAlchemy ORM models
│   │   ├── schemas.py      # Pydantic schemas
│   │   ├── config.py       # Configuration settings
│   │   ├── routers/        # API route handlers
│   │   │   ├── search.py   # Search endpoint
│   │   │   ├── auth.py     # Authentication
│   │   │   └── admin.py    # Admin controls
│   │   ├── services/       # Business logic
│   │   └── database.py     # Database connection
│   ├── requirements.txt
│   └── Dockerfile
├── crawler/                 # Scrapy-based web crawler
│   ├── spiders/
│   │   └── domain_spider.py
│   └── items.py
├── frontend/                # React UI
│   ├── public/
│   └── src/
│       ├── App.js
│       ├── components/
│       └── pages/
├── indexer/                 # Elasticsearch indexing
│   ├── mappings.json        # Index schema
│   └── indexer.py
├── ranking/                 # ML ranking model
│   ├── model.py             # PyTorch model definition
│   ├── train.py             # Training script
│   └── inference.py         # Inference service
├── infrastructure/          # Deployment configs
│   ├── kubernetes/          # K8s manifests
│   └── terraform/           # Infrastructure as code
├── scripts/                 # Utility scripts
├── docs/                    # Documentation
├── docker-compose.yml       # Local development stack
├── .env.example             # Environment variables template
├── LICENSE
└── README.md
🚀 Quick Start
Prerequisites
Docker and Docker Compose

Python 3.11+

Node.js 18+

Make (optional)

Development Setup
Clone the repository

bash
git clone https://github.com/erikamjp150-bot/OpenSearch.git
cd OpenSearch
Configure environment

bash
cp .env.example .env
# Edit .env with your settings (database, JWT secret, etc.)
Start infrastructure services

bash
docker-compose up -d postgres elasticsearch redis minio
Set up the backend

bash
cd backend
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements.txt
alembic upgrade head      # Run database migrations
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
Set up the frontend

bash
cd frontend
npm install
npm start
Run the ranking service (optional, for development)

bash
cd ranking
pip install -r requirements.txt
python inference.py
Start the crawler (optional)

bash
cd crawler
scrapy crawl domain_spider -a domain=example.com -a start_urls=https://example.com
Using Docker Compose (Full Stack)
bash
# Build and start all services
docker-compose up -d --build

# View logs
docker-compose logs -f

# Stop all services
docker-compose down
🗺️ Architecture Overview
OpenSearch follows a modular, microservices-based architecture:

flowchart LR
    User[User] --> Frontend[Frontend<br>React/TS]
    Frontend --> Backend[Backend API<br>FastAPI]
    Backend --> Cache[Cache<br>KeyDB/Redis]
    Backend --> Index[Search Index<br>Elasticsearch]
    Backend --> Ranking[Ranking Service<br>PyTorch]
    Backend --> DB[(PostgreSQL)]
    
    Crawler[Web Crawler<br>Scrapy] --> Indexer[Indexer]
    Indexer --> Index
    
    Moderation[HITL Moderation] --> Backend
    Admin[Admin Dashboard] --> Backend
    
    style Backend fill:#4CAF50,color:white
    style Ranking fill:#FF9800,color:white
    style Index fill:#2196F3,color:white

The flow works as follows:

Crawling: Scrapy spiders crawl the web, extracting page content, links, and metadata.

Indexing: Pages are indexed in Elasticsearch with n-gram and full-text search capabilities.

Search: User queries hit the FastAPI backend, which queries Elasticsearch and passes candidates to the ranking service.

Ranking: The PyTorch model re-ranks results based on relevance, freshness, and quality signals.

Delivery: Ranked results are returned to the frontend and cached for performance.

🧪 Testing
bash
# Backend tests
cd backend
pytest tests/ -v --cov=./

# Frontend tests
cd frontend
npm test

# E2E tests
npm run test:e2e
🤝 Contributing
We welcome contributions! Please see our Contributing Guidelines for details.

Quick Contribution Guide:

Fork the repository

Create a feature branch (git checkout -b feat/amazing-feature)

Commit your changes (git commit -m 'Add amazing feature')

Push to the branch (git push origin feat/amazing-feature)

Open a Pull Request

Please ensure your PR passes all CI checks and includes appropriate tests.

📜 License
This project is licensed under the MIT License - see the LICENSE file for details.

📊 Transparency & Governance
OpenSearch is committed to transparency and community governance:

All ranking logic and training data are open-source.

All moderation decisions are logged and auditable.

The project is governed by a community-elected board.

Regular transparency reports are published.

🙏 Acknowledgements
Built with FastAPI, Elasticsearch, PyTorch, and Scrapy

Inspired by open-source search projects and the need for transparent, user-centric search engines

Thanks to all contributors and the open-source community

⚡ Stay Connected
GitHub Issues: Report bugs or request features

Discussions: Join the community conversation

Security Issues: Please report responsibly via our Security Policy



