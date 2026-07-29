import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from app.services.indexer import IndexerService
from app.models import Page


def test_indexer_service_collects_documents():
    page = Page(url='https://example.org', title='Example', content='Example content')
    service = IndexerService(db=None)  # type: ignore[arg-type]

    indexed = service.index_pages([page])

    assert len(indexed) == 1
    assert indexed[0]['url'] == 'https://example.org'
