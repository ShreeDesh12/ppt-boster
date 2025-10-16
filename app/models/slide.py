"""
Slide content model
"""
from typing import List, Optional
from pydantic import BaseModel, Field, validator
from .enums import SlideLayout


class SlideContent(BaseModel):
    """Content for a single slide"""
    layout: SlideLayout = Field(description="Layout type for this slide")
    title: str = Field(description="Slide title", min_length=1, max_length=200)
    content: Optional[str] = Field(
        default=None,
        description="Main content text"
    )
    bullet_points: Optional[List[str]] = Field(
        default=None,
        description="List of bullet points (3-5 items for bullet_points layout)"
    )
    left_column: Optional[str] = Field(
        default=None,
        description="Left column content for two_column layout"
    )
    right_column: Optional[str] = Field(
        default=None,
        description="Right column content for two_column layout"
    )
    image_url: Optional[str] = Field(
        default=None,
        description="URL or placeholder for image"
    )
    image_description: Optional[str] = Field(
        default=None,
        description="Description of suggested image"
    )
    notes: Optional[str] = Field(
        default=None,
        description="Speaker notes"
    )

    @validator('bullet_points')
    def validate_bullet_points(cls, v, values):
        if values.get('layout') == SlideLayout.BULLET_POINTS:
            if not v or len(v) < 3 or len(v) > 5:
                raise ValueError('Bullet points layout requires 3-5 bullet points')
        return v
