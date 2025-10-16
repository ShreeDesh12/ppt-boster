"""
Enum definitions for the Slide Generator API
"""
from enum import Enum


class SlideLayout(str, Enum):
    """Supported slide layout types"""
    TITLE = "title"
    BULLET_POINTS = "bullet_points"
    TWO_COLUMN = "two_column"
    CONTENT_WITH_IMAGE = "content_with_image"
