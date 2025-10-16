"""
Presentation management endpoints
"""
import os
import time
import uuid
import logging
from fastapi import APIRouter, HTTPException, Request, status
from fastapi.responses import FileResponse
from slowapi import Limiter
from slowapi.util import get_remote_address

from app.models import GenerateRequest, GenerateResponse
from app.config import get_settings
from app.services.content_generator import ContentGenerator
from app.services.presentation_generator import PresentationGenerator
from app.storage import StorageFactory

logger = logging.getLogger(__name__)
settings = get_settings()

# Initialize rate limiter
limiter = Limiter(key_func=get_remote_address)

# Initialize storage
storage = StorageFactory.create()  # Uses default 'file_storage' backend

router = APIRouter(prefix="/api/v1", tags=["Presentations"])


@router.post(
    "/generate",
    response_model=GenerateResponse,
    status_code=status.HTTP_201_CREATED
)
@limiter.limit(settings.api_rate_limit)
async def generate_presentation(request: Request, generate_req: GenerateRequest):
    """
    Generate a PowerPoint presentation

    Args:
        generate_req: Request containing topic and configuration

    Returns:
        GenerateResponse with presentation details and file path
    """
    start_time = time.time()

    try:
        logger.info(f"Generating presentation for topic: {generate_req.topic}")

        # Use custom content if provided, otherwise generate with AI
        if generate_req.custom_content:
            slides = generate_req.custom_content
            citations = None
            logger.info("Using custom content")
        else:
            # Generate content using LLM
            content_gen = ContentGenerator()
            slides, citations = await content_gen.generate_slides(
                topic=generate_req.topic,
                num_slides=generate_req.num_slides,
                include_citations=generate_req.include_citations
            )
            logger.info(f"Generated {len(slides)} slides with AI")

        # Create PowerPoint presentation
        ppt_gen = PresentationGenerator(theme=generate_req.theme)
        ppt_gen.create_presentation(
            slides=slides,
            citations=citations,
            aspect_ratio=generate_req.aspect_ratio
        )

        # Save presentation
        presentation_id = str(uuid.uuid4())
        filename = f"{presentation_id}.pptx"
        temp_file_path = os.path.join(settings.output_dir, filename)

        ppt_gen.save_presentation(temp_file_path)
        logger.info(f"Presentation created at {temp_file_path}")

        # Store using storage factory
        file_path = storage.save(temp_file_path, presentation_id)
        logger.info(f"Presentation stored via storage backend at {file_path}")

        # Calculate generation time
        generation_time = time.time() - start_time

        return GenerateResponse(
            presentation_id=presentation_id,
            topic=generate_req.topic,
            num_slides=len(slides),
            slides=slides,
            citations=citations,
            file_path=file_path,
            generation_time_seconds=round(generation_time, 2)
        )

    except Exception as e:
        logger.error(f"Error generating presentation: {str(e)}", exc_info=True)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to generate presentation: {str(e)}"
        )


@router.get("/download/{presentation_id}")
@limiter.limit("20/minute")
async def get_download_link(request: Request, presentation_id: str):
    """
    Get download link for a generated presentation

    Args:
        presentation_id: UUID of the presentation

    Returns:
        JSON with download link
    """
    try:
        # Check if file exists in storage
        if not storage.exists(presentation_id):
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Presentation not found"
            )

        # Build download URL
        base_url = str(request.base_url).rstrip('/')
        download_url = f"{base_url}/api/v1/presentations/{presentation_id}/file"

        logger.info(f"Generated download link for presentation: {presentation_id}")

        return {
            "presentation_id": presentation_id,
            "download_url": download_url,
            "message": "Use the download_url to get the presentation file"
        }

    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error generating download link: {str(e)}", exc_info=True)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to generate download link: {str(e)}"
        )


@router.get("/presentations/{presentation_id}/file")
@limiter.limit("20/minute")
async def download_presentation_file(request: Request, presentation_id: str):
    """
    Download the actual presentation file

    Args:
        presentation_id: UUID of the presentation

    Returns:
        PowerPoint file
    """
    try:
        # Get file path from storage
        file_path = storage.get(presentation_id)

        if not file_path:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Presentation not found"
            )

        logger.info(f"Serving presentation file from: {file_path}")

        return FileResponse(
            path=file_path,
            media_type="application/vnd.openxmlformats-officedocument.presentationml.presentation",
            filename=f"presentation_{presentation_id}.pptx"
        )

    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error downloading presentation: {str(e)}", exc_info=True)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to download presentation: {str(e)}"
        )


@router.delete("/presentations/{presentation_id}")
@limiter.limit("30/minute")
async def delete_presentation(request: Request, presentation_id: str):
    """
    Delete a generated presentation

    Args:
        presentation_id: UUID of the presentation

    Returns:
        Success message
    """
    try:
        # Check if presentation exists
        if not storage.exists(presentation_id):
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Presentation not found"
            )

        # Delete from storage
        success = storage.delete(presentation_id)

        if not success:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Failed to delete presentation"
            )

        logger.info(f"Deleted presentation: {presentation_id}")
        return {"message": "Presentation deleted successfully", "presentation_id": presentation_id}

    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error deleting presentation: {str(e)}", exc_info=True)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to delete presentation: {str(e)}"
        )
