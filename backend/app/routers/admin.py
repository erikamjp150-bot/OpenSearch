from fastapi import APIRouter, Depends, HTTPException, BackgroundTasks
from sqlalchemy.orm import Session
from ..database import get_db
from ..models import Page, Domain
from ..services.crawler import CrawlerService
import logging

logger = logging.getLogger(__name__)
router = APIRouter(prefix="/admin", tags=["administration"])

@router.post("/crawl/start")
async def start_crawl(
    domain: str,
    background_tasks: BackgroundTasks,
    db: Session = Depends(get_db)
):
    """
    Start a crawl for a specific domain.
    """
    # Check if domain exists in DB
    domain_record = db.query(Domain).filter(Domain.domain_name == domain).first()
    if not domain_record:
        raise HTTPException(status_code=404, detail="Domain not found")
    
    background_tasks.add_task(
        CrawlerService.start_crawl,
        domain=domain,
        domain_id=domain_record.id,
        db=db
    )
    
    return {"status": "started", "domain": domain}

@router.get("/stats")
def get_stats(db: Session = Depends(get_db)):
    """Get basic search engine statistics"""
    total_pages = db.query(Page).count()
    total_domains = db.query(Domain).count()
    active_domains = db.query(Domain).filter(Domain.is_allowed == True).count()
    
    return {
        "total_pages": total_pages,
        "total_domains": total_domains,
        "active_domains": active_domains,
        "last_crawl": db.query(Domain.last_crawled_at).order_by(Domain.last_crawled_at.desc()).first()
    }
