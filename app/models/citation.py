"""
Citation model
"""
from typing import Optional
from pydantic import BaseModel, Field


class Citation(BaseModel):
    """Citation information"""
    source: str = Field(description="Source name or URL")
    title: Optional[str] = Field(default=None, description="Source title")
    date: Optional[str] = Field(default=None, description="Publication date")
