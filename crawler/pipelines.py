import logging
from typing import Any, Dict, Iterable

from sqlalchemy.orm import Session

from backend.app.database import SessionLocal
from backend.app.models import Domain, Page

logger = logging.getLogger(__name__)


class Pipeline:
    """Store scraped items into PostgreSQL and, when possible, Elasticsearch."""

    def __init__(self, db: Session | None = None):
        self.db = db or SessionLocal()

    def process_item(self, item: Dict[str, Any]) -> Dict[str, Any]:
        domain_name = item.get("domain") or "example.org"
        domain = self.db.query(Domain).filter(Domain.domain_name == domain_name).first()
        if not domain:
            domain = Domain(domain_name=domain_name, is_allowed=True)
            self.db.add(domain)
            self.db.flush()

        page = Page(
            domain_id=domain.id,
            url=item.get("url") or f"https://{domain_name}/",
            title=item.get("title"),
            content=item.get("content"),
            meta_description=item.get("meta_description"),
            meta_keywords=item.get("meta_keywords"),
            content_type=item.get("content_type", "text/html"),
            status_code=item.get("status_code", 200),
            pagerank_score=float(item.get("pagerank_score") or 0.0),
            engagement_score=float(item.get("engagement_score") or 0.0),
            freshness_score=float(item.get("freshness_score") or 0.0),
            last_modified=item.get("last_modified"),
        )
        self.db.add(page)
        self.db.commit()

        try:
            from elasticsearch import Elasticsearch
            from backend.app.config import settings

            client = Elasticsearch([settings.ELASTICSEARCH_URL])
            client.index(index=settings.ELASTICSEARCH_INDEX, id=page.id, document=page.to_elasticsearch_doc())
        except Exception as exc:  # pragma: no cover - best effort
            logger.warning("Elasticsearch sync skipped: %s", exc)

        return page.to_elasticsearch_doc()
