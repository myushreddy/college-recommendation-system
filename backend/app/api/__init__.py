"""
API package initialization.
"""
from app.api.colleges import router as colleges_router

__all__ = ["colleges_router"]
