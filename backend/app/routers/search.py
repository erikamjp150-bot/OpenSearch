from fastapi import APIRouter, Depends, HTTPException, BackgroundTasks
from typing import List, Dict, Any
from sqlalchemy.orm import Session
from datetime import datetime
import logging
import httpx

from ..database import get_db
from ..models import SearchHistory
from ..schemas import SearchRequest, SearchResponse, SearchResult
from ..config import settings
from ..services.ranking import RankingService

logger = logging.getLogger(__name__)
router = APIRouter(prefix="/search", tags=["search"])


@router.post("", response_model=SearchResponse)
async def search(
    request: SearchRequest,
    background_tasks: BackgroundTasks,
    db: Session = Depends(get_db),
):
    """Perform a search query and return ranked results."""
    query = request.query
    user_id = request.user_id
    page = request.page or 1
    page_size = request.page_size or 10

    logger.info("Search query: %s (user: %s)", query, user_id)

    try:
        es_results = await _query_elasticsearch(query, page, page_size)

        if not es_results:
            return SearchResponse(
                query=query,
                results=[],
                total_results=0,
                page=page,
                page_size=page_size,
            )

        ranked_results = RankingService().rank(query, es_results)

        background_tasks.add_task(
            _log_search_history,
            query=query,
            user_id=user_id,
            num_results=len(ranked_results),
            db=db,
        )

        return SearchResponse(
            query=query,
            results=[
                SearchResult(
                    url=item.get("url", ""),
                    title=item.get("title", "Untitled"),
                    content_snippet=(item.get("content") or "")[:220],
                    domain=item.get("domain", "unknown"),
                    score=float(item.get("combined_score", 0.0)),
                    relevance_score=float(item.get("relevance_score", 0.0)),
                    meta_description=item.get("meta_description"),
                )
                for item in ranked_results[:page_size]
            ],
            total_results=len(ranked_results),
            page=page,
            page_size=page_size,
        )
    except Exception as exc:
        logger.error("Search error: %s", exc, exc_info=True)
        raise HTTPException(status_code=500, detail="Search service unavailable") from exc


async def _query_elasticsearch(query: str, page: int, page_size: int) -> List[Dict[str, Any]]:
    """Query Elasticsearch for candidate documents."""
    try:
        from elasticsearch import Elasticsearch
    except ImportError:
        return [
            {
                "url": "https://example.org",
                "title": "Example result",
                "content": "Fallback search result when Elasticsearch is unavailable.",
                "domain": "example.org",
                "pagerank_score": 0.8,
                "clicks": 10,
                "shares": 2,
                "last_modified": None,
            }
        ]

    es = Elasticsearch([settings.ELASTICSEARCH_URL])
    body = {
        "from": (page - 1) * page_size,
        "size": page_size * 2,
        "query": {
            "multi_match": {
                "query": query,
                "fields": ["title^3", "content", "meta_description^2", "meta_keywords"],
                "fuzziness": "AUTO",
            }
        },
    }

    response = es.search(index=settings.ELASTICSEARCH_INDEX, body=body)
    hits = response.get("hits", {}).get("hits", [])
    return [hit.get("_source", {}) for hit in hits]


def _log_search_history(query: str, user_id: int, num_results: int, db: Session):
    """Log search query to database as background task."""
    history = SearchHistory(
        query=query,
        user_id=user_id,
        num_results=num_results,
        created_at=datetime.utcnow(),
    )
    db.add(history)
    db.commit()

