"""
Response models
"""
from typing import List, Optional, Dict, Any
from pydantic import BaseModel, Field
from .slide import SlideContent
from .citation import Citation


class GenerateResponse(BaseModel):
    """Response model for presentation generation"""
    presentation_id: str = Field(description="Unique identifier for the presentation")
    topic: str = Field(description="Presentation topic")
    num_slides: int = Field(description="Number of slides generated")
    slides: List[SlideContent] = Field(description="Generated slide content")
    citations: Optional[List[Citation]] = Field(
        default=None,
        description="Source citations"
    )
    file_path: str = Field(description="Path to generated .pptx file")
    generation_time_seconds: float = Field(
        description="Time taken to generate the presentation"
    )


class ErrorResponse(BaseModel):
    """Error response model"""
    error: str = Field(description="Error type")
    message: str = Field(description="Error message")
    details: Optional[Dict[str, Any]] = Field(
        default=None,
        description="Additional error details"
    )


class HealthResponse(BaseModel):
    """Health check response"""
    status: str = Field(description="Service status")
    version: str = Field(description="API version")
    timestamp: str = Field(description="Current timestamp")
