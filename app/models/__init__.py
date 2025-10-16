"""
Data models for the Slide Generator API
"""
from .enums import SlideLayout
from .theme import ThemeConfig
from .slide import SlideContent
from .citation import Citation
from .request import GenerateRequest
from .response import GenerateResponse, ErrorResponse, HealthResponse

__all__ = [
    "SlideLayout",
    "ThemeConfig",
    "SlideContent",
    "Citation",
    "GenerateRequest",
    "GenerateResponse",
    "ErrorResponse",
    "HealthResponse",
]
