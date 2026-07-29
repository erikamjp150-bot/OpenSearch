import httpx
from typing import List, Dict, Any
from ..config import settings
import logging

logger = logging.getLogger(__name__)

class RankingService:
    """Client for interacting with the external ranking service"""
    
    @staticmethod
    async def rank_results(query: str, candidates: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """
        Call the ranking service to re-rank candidates.
        """
        try:
            async with httpx.AsyncClient(timeout=10.0) as client:
                response = await client.post(
                    f"{settings.RANKING_SERVICE_URL}/rank",
                    json={"query": query, "candidates": candidates}
                )
                response.raise_for_status()
                return response.json()
        except Exception as e:
            logger.error(f"Ranking service error: {e}")
            # Fallback: return candidates with default scores
            for idx, doc in enumerate(candidates):
                doc['combined_score'] = 1.0 / (idx + 1)  # Simple decaying score
            return candidates
