import logging
from typing import Iterable, List, Dict, Any
from sqlalchemy.orm import Session

from ..models import Page
from ..config import settings

logger = logging.getLogger(__name__)


class IndexerService:
    """Persist pages into PostgreSQL and optionally mirror them to Elasticsearch."""

    def __init__(self, db: Session | None):
        self.db = db

    def index_pages(self, pages: Iterable[Page]) -> List[Dict[str, Any]]:
        indexed = []
        for page in pages:
            if self.db is not None:
                self.db.add(page)
                self.db.flush()
            doc = page.to_elasticsearch_doc()
            indexed.append(doc)
        if self.db is not None:
            self.db.commit()
        self._sync_to_elasticsearch(indexed)
        return indexed

    def _sync_to_elasticsearch(self, docs: List[Dict[str, Any]]) -> None:
        try:
            from elasticsearch import Elasticsearch

            client = Elasticsearch([settings.ELASTICSEARCH_URL], request_timeout=5)
            for doc in docs:
                client.index(index=settings.ELASTICSEARCH_INDEX, id=doc["id"], document=doc)
        except Exception as exc:  # pragma: no cover - best effort sync
            logger.warning("Elasticsearch sync skipped: %s", exc)
