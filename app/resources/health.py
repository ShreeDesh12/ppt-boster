"""
Health check endpoints
"""
import logging
from datetime import datetime
from fastapi import APIRouter
from app.models import HealthResponse
from app.config import get_settings

logger = logging.getLogger(__name__)
settings = get_settings()

router = APIRouter(tags=["Health"])


@router.get("/", response_model=HealthResponse)
async def root():
    """Root endpoint - health check"""
    print(f"{datetime.utcnow()} - app.resources.health - INFO - Root endpoint accessed", flush=True)
    logger.info("Root endpoint accessed")
    logger.debug("Root endpoint returning health status")
    return HealthResponse(
        status="healthy",
        version=settings.version,
        timestamp=datetime.utcnow().isoformat()
    )


@router.get("/health", response_model=HealthResponse)
async def health_check():
    """Health check endpoint"""
    print(f"{datetime.utcnow()} - app.resources.health - INFO - Health check requested", flush=True)
    print(f"{datetime.utcnow()} - app.resources.health - DEBUG - Health check endpoint is operational", flush=True)
    logger.info("Health check requested")
    logger.debug("Health check endpoint is operational")
    return HealthResponse(
        status="healthy",
        version=settings.version,
        timestamp=datetime.utcnow().isoformat()
    )
