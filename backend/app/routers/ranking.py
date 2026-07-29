from fastapi import APIRouter
from pydantic import BaseModel
from typing import List, Dict, Any

from ..services.ranker import RankerService

router = APIRouter()


class RankRequest(BaseModel):
    query: str
    candidates: List[Dict[str, Any]]


@router.post("/rank")
def rank(request: RankRequest):
    service = RankerService()
    return service.rank(request.query, request.candidates)
