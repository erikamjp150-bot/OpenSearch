from typing import List, Dict, Any


class RankerService:
    """Small local ranking implementation for the FastAPI ranking endpoint."""

    def rank(self, query: str, candidates: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        if not candidates:
            return []

        normalized_query = (query or "").strip().lower()
        query_terms = [term for term in normalized_query.split() if term]
        ranked: List[Dict[str, Any]] = []

        for candidate in candidates:
            content = str(candidate.get("content") or "").lower()
            title = str(candidate.get("title") or "").lower()
            query_matches = sum(1 for term in query_terms if term in content or term in title)
            title_bonus = 1.0 if any(term in title for term in query_terms) else 0.0
            pagerank = float(candidate.get("pagerank_score") or 0.0)
            engagement = min(1.0, (int(candidate.get("clicks") or 0) / 100.0))
            freshness = 0.9 if candidate.get("last_modified") else 0.5
            score = 0.4 * min(1.0, query_matches / max(1, len(query_terms))) + 0.25 * pagerank + 0.2 * engagement + 0.15 * freshness + 0.1 * title_bonus
            scored = dict(candidate)
            scored["score"] = round(score, 6)
            scored["relevance_score"] = round(score, 6)
            scored["combined_score"] = round(score, 6)
            ranked.append(scored)

        ranked.sort(key=lambda item: item["combined_score"], reverse=True)
        return ranked
