from fastapi import FastAPI
from pydantic import BaseModel
from typing import List, Dict, Any

from ranking.model import SearchRankingModel

app = FastAPI(title="OpenSearch ranking service")


class RankRequest(BaseModel):
    query: str
    candidates: List[Dict[str, Any]]


@app.get("/health")
def health():
    return {"status": "ok"}


@app.post("/rank")
def rank(request: RankRequest):
    model = SearchRankingModel()
    ranked = []
    for candidate in request.candidates:
        content = str(candidate.get("content") or "")
        title = str(candidate.get("title") or "")
        score = 0.0
        if request.query.lower() in title.lower():
            score += 0.5
        if request.query.lower() in content.lower():
            score += 0.3
        score += float(candidate.get("pagerank_score") or 0.0) * 0.2
        scored = dict(candidate)
        scored["combined_score"] = round(score, 6)
        scored["relevance_score"] = round(score, 6)
        scored["score"] = round(score, 6)
        ranked.append(scored)

    ranked.sort(key=lambda item: item["combined_score"], reverse=True)
    return ranked
