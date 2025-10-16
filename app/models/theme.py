"""
Theme configuration model
"""
from typing import Optional
from pydantic import BaseModel, Field, validator


class ThemeConfig(BaseModel):
    """Theme configuration for presentation styling"""
    primary_color: Optional[str] = Field(
        default="#1F4788",
        description="Primary color in hex format"
    )
    secondary_color: Optional[str] = Field(
        default="#FFFFFF",
        description="Secondary color in hex format"
    )
    font_name: Optional[str] = Field(
        default="Calibri",
        description="Font family name"
    )
    font_size_title: Optional[int] = Field(
        default=44,
        ge=20,
        le=72,
        description="Font size for titles"
    )
    font_size_body: Optional[int] = Field(
        default=18,
        ge=10,
        le=36,
        description="Font size for body text"
    )

    @validator('primary_color', 'secondary_color')
    def validate_hex_color(cls, v):
        if v and not v.startswith('#'):
            raise ValueError('Color must be in hex format (e.g., #1F4788)')
        if v and len(v) != 7:
            raise ValueError('Color must be 7 characters including # (e.g., #1F4788)')
        return v
