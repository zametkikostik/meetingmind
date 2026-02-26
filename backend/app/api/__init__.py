"""API module"""
from .auth import router as auth_router
from .meetings import router as meetings_router
from .health import router as health_router
from .extras import router as extras_router

__all__ = ["auth_router", "meetings_router", "health_router", "extras_router"]
