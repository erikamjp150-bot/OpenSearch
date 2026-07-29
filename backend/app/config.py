import os
from typing import List


class Settings:
    PROJECT_NAME: str = "OpenSearch"
    DATABASE_URL: str = os.getenv("DATABASE_URL", "sqlite:///./opensearch.db")
    ELASTICSEARCH_URL: str = os.getenv("ELASTICSEARCH_URL", "http://localhost:9200")
    ELASTICSEARCH_INDEX: str = os.getenv("ELASTICSEARCH_INDEX", "pages")
    RANKING_SERVICE_URL: str = os.getenv("RANKING_SERVICE_URL", "http://localhost:8001")
    ALLOWED_ORIGINS: List[str] = [
        origin.strip()
        for origin in os.getenv("ALLOWED_ORIGINS", "http://localhost:3000,http://localhost:5173").split(",")
        if origin.strip()
    ]
    SECRET_KEY: str = os.getenv("SECRET_KEY", "dev-secret")
    ACCESS_TOKEN_EXPIRE_MINUTES: int = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES", "30"))
    ALGORITHM: str = "HS256"


settings = Settings()
