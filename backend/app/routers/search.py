from fastapi import APIRouter, Query, Depends, HTTPException, BackgroundTasks
from typing import Optional, List
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
router = APIRouter()

@router.post("/search", response_model=SearchResponse)
async def search(
    request: SearchRequest,
    background_tasks: BackgroundTasks,
    db: Session = Depends(get_db)
):
    """
    Perform a search query and return ranked results.
    """
    query = request.query
    user_id = request.user_id
    page = request.page or 1
    page_size = request.page_size or 10
    
    logger.info(f"Search query: {query} (user: {user_id})")
    
    try:
        # Step 1: Query Elasticsearch for candidates
        es_results = await _query_elasticsearch(query, page, page_size)
        
        if not es_results:
            return SearchResponse(
                query=query,
                results=[],
                total_results=0,
                page=page,
                page_size=page_size
            )
        
        # Step 2: Rank candidates using the ML model
        async with httpx.AsyncClient() as client:
            ranking_response = await client.post(
                f"{settings.RANKING_SERVICE_URL}/rank",
                json={"query": query, "candidates": es_results}
            )
            ranking_response.raise_for_status()
            ranked_results = ranking_response.json()
        
        # Step 3: Log search history in background
        background_tasks.add_task(
            _log_search_history,
            query=query,
            user_id=user_id,
            num_results=len(ranked_results),
            db=db
        )
        
        return SearchResponse(
            query=query,
            results=ranked_results[:page_size],
            total_results=len(ranked_results),
            page=page,
            page_size=page_size
        )
        
    except Exception as e:
        logger.error(f"Search error: {str(e)}", exc_info=True)
        raise HTTPException(status_code=500, detail="Search service unavailable")

async def _query_elasticsearch(query: str, page: int, page_size: int) -> List[dict]:
    """
    Query Elasticsearch for candidate documents.
    """
    # Simplified: In production, use elasticsearch-py client
    # This is a mock/placeholder for demonstration
    from elasticsearch import Elasticsearch
    es = Elasticsearch([settings.ELASTICSEARCH_URL])
    
    body = {
        "from": (page - 1) * page_size,
        "size": page_size * 2,  # Fetch more for re-ranking
        "query": {
            "multi_match": {
                "query": query,
                "fields": ["title^3", "content", "meta_description^2", "meta_keywords"],
                "fuzziness": "AUTO"
            }
        }
    }
    
    response = es.search(index=settings.ELASTICSEARCH_INDEX, body=body)
    hits = response.get('hits', {}).get('hits', [])
    return [hit['_source'] for hit in hits]

def _log_search_history(query: str, user_id: int, num_results: int, db: Session):
    """Log search query to database as background task"""
    history = SearchHistory(
        query=query,
        user_id=user_id,
        num_results=num_results,
        created_at=datetime.utcnow()
    )
    db.add(history)
    db.commit()
