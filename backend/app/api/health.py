"""
Health check and utility endpoints
"""
from fastapi import APIRouter, Depends
from sqlalchemy import text
from sqlalchemy.orm import Session

from ..db.session import get_db
from ..core.config import settings

router = APIRouter(tags=["Health"])


@router.get("/health")
def health_check(db: Session = Depends(get_db)):
    """
    Health check endpoint
    """
    # Check database
    db_status = "ok"
    try:
        db.execute(text("SELECT 1"))
    except Exception as e:
        db_status = f"error: {str(e)}"
    
    # Check Redis (optional)
    redis_status = "not configured"
    try:
        from redis import Redis
        redis_client = Redis.from_url(settings.REDIS_URL, socket_timeout=1)
        redis_client.ping()
        redis_status = "ok"
    except Exception as e:
        redis_status = f"error: {str(e)}"
    
    return {
        "status": "healthy" if db_status == "ok" else "degraded",
        "database": db_status,
        "redis": redis_status,
        "app": settings.APP_NAME,
        "version": "0.1.0"
    }


@router.get("/")
def root():
    """
    Root endpoint
    """
    return {
        "name": settings.APP_NAME,
        "version": "0.1.0",
        "docs": "/docs",
        "health": "/health"
    }
