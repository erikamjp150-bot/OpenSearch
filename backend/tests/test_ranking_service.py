import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from app.services.ranking import RankingService


def test_rank_returns_sorted_candidates():
    service = RankingService(model_path=None)
    candidates = [
        {"content": "python programming", "pagerank_score": 0.1, "clicks": 10, "shares": 2},
        {"content": "fastapi backend", "pagerank_score": 0.9, "clicks": 100, "shares": 10},
    ]

    ranked = service.rank("fastapi", candidates)

    assert ranked[0]["url"] == "https://example.org/fastapi"
