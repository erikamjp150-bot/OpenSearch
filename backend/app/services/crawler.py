import asyncio
import logging
from typing import Optional
from sqlalchemy.orm import Session

from ..models import Domain, Page
from ..database import SessionLocal

logger = logging.getLogger(__name__)


class CrawlerService:
    """Simple crawler wrapper used by the admin API and background tasks."""

    @staticmethod
    def start_crawl(domain: str, domain_id: int, db: Optional[Session] = None):
        if db is None:
            db = SessionLocal()

        domain_record = db.query(Domain).filter(Domain.id == domain_id).first()
        if not domain_record:
            raise ValueError(f"Domain {domain_id} not found")

        page = Page(
            domain_id=domain_id,
            url=f"https://{domain}/",
            title=f"Sample crawl for {domain}",
            content=f"Indexed placeholder content for {domain}",
            meta_description=f"Crawled from {domain}",
            meta_keywords="crawler, sample",
            content_type="text/html",
            content_length=150,
            status_code=200,
            pagerank_score=0.25,
            freshness_score=1.0,
            engagement_score=0.1,
            is_active=True,
        )
        db.add(page)
        domain_record.last_crawled_at = page.crawled_at
        db.commit()
        logger.info("Crawler completed for %s", domain)
        return page
