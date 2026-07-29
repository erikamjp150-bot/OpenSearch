from sqlalchemy import Column, Integer, String, DateTime, Text, Boolean, Float, ForeignKey, JSON, BigInteger
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from datetime import datetime
import pytz

Base = declarative_base()

def utc_now():
    return datetime.now(pytz.UTC)

class Domain(Base):
    """Represents a domain in the search index"""
    __tablename__ = "domains"
    
    id = Column(Integer, primary_key=True, index=True)
    domain_name = Column(String(255), unique=True, index=True, nullable=False)
    robots_txt_url = Column(String(500))
    crawl_delay = Column(Integer, default=1)
    is_allowed = Column(Boolean, default=True)
    last_crawled_at = Column(DateTime(timezone=True))
    created_at = Column(DateTime(timezone=True), default=utc_now)
    updated_at = Column(DateTime(timezone=True), default=utc_now, onupdate=utc_now)
    
    pages = relationship("Page", back_populates="domain")

class Page(Base):
    """Represents a single web page/document in the index"""
    __tablename__ = "pages"
    
    id = Column(Integer, primary_key=True, index=True)
    domain_id = Column(Integer, ForeignKey("domains.id"), nullable=False)
    url = Column(String(1000), unique=True, index=True, nullable=False)
    title = Column(Text)
    content = Column(Text)
    meta_description = Column(Text)
    meta_keywords = Column(Text)
    content_type = Column(String(100))
    content_length = Column(BigInteger)
    status_code = Column(Integer)
    
    # Rankings
    pagerank_score = Column(Float, default=0.0)
    engagement_score = Column(Float, default=0.0)
    freshness_score = Column(Float, default=0.0)
    
    # Metadata
    crawled_at = Column(DateTime(timezone=True), default=utc_now)
    indexed_at = Column(DateTime(timezone=True))
    last_modified = Column(DateTime(timezone=True))
    is_active = Column(Boolean, default=True)
    
    # Relationships
    domain = relationship("Domain", back_populates="pages")
    
    def to_elasticsearch_doc(self):
        """Convert page to Elasticsearch document"""
        return {
            "id": self.id,
            "domain": self.domain.domain_name,
            "url": self.url,
            "title": self.title,
            "content": self.content,
            "meta_description": self.meta_description,
            "meta_keywords": self.meta_keywords,
            "content_type": self.content_type,
            "pagerank_score": self.pagerank_score,
            "engagement_score": self.engagement_score,
            "freshness_score": self.freshness_score,
            "last_modified": self.last_modified.isoformat() if self.last_modified else None,
            "crawled_at": self.crawled_at.isoformat()
        }

class SearchHistory(Base):
    """Track user search queries"""
    __tablename__ = "search_history"
    
    id = Column(Integer, primary_key=True, index=True)
    query = Column(Text, nullable=False)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=True)
    num_results = Column(Integer)
    clicked_url = Column(String(1000))
    search_time_ms = Column(Float)
    created_at = Column(DateTime(timezone=True), default=utc_now)
    
class User(Base):
    __tablename__ = "users"
    
    id = Column(Integer, primary_key=True, index=True)
    username = Column(String(50), unique=True, index=True, nullable=False)
    email = Column(String(255), unique=True, index=True, nullable=False)
    hashed_password = Column(String(255), nullable=False)
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime(timezone=True), default=utc_now)
