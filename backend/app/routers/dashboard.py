from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from ..database import get_db
from ..models import Page, Domain

router = APIRouter(prefix="/dashboard", tags=["dashboard"])


@router.get("/flags")
def get_flagged_content(db: Session = Depends(get_db)):
    pages = db.query(Page).filter(Page.is_active.is_(True)).limit(20).all()
    return [
        {
            "id": page.id,
            "url": page.url,
            "title": page.title,
            "domain": page.domain.domain_name if page.domain else None,
            "content": page.content,
            "flagged": False,
        }
        for page in pages
    ]
