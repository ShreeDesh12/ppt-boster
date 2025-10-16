"""
API Resources module
"""
from .health import router as health_router
from .presentations import router as presentations_router

__all__ = [
    "health_router",
    "presentations_router",
]
