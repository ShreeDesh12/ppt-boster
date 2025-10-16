"""
Request models
"""
from typing import List, Optional
from pydantic import BaseModel, Field, validator
from .slide import SlideContent
from .theme import ThemeConfig


class GenerateRequest(BaseModel):
    """Request model for generating a presentation"""
    topic: str = Field(
        description="Topic or subject for the presentation",
        min_length=3,
        max_length=500
    )
    num_slides: int = Field(
        default=5,
        ge=1,
        le=20,
        description="Number of slides to generate (1-20)"
    )
    custom_content: Optional[List[SlideContent]] = Field(
        default=None,
        description="Custom slide content (overrides AI generation)"
    )
    theme: Optional[ThemeConfig] = Field(
        default=None,
        description="Custom theme configuration"
    )
    include_citations: bool = Field(
        default=True,
        description="Include source citations in slides"
    )
    aspect_ratio: Optional[str] = Field(
        default="16:9",
        description="Presentation aspect ratio (16:9 or 4:3)"
    )

    @validator('aspect_ratio')
    def validate_aspect_ratio(cls, v):
        if v not in ["16:9", "4:3"]:
            raise ValueError('Aspect ratio must be either "16:9" or "4:3"')
        return v
