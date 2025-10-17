"""
Application configuration settings
"""
import os
from functools import lru_cache
from pydantic import BaseSettings


class Settings(BaseSettings):
    """Application settings"""

    # API Configuration
    app_name: str = "Slide Generator API"
    version: str = "1.0.0"
    environment: str = "development"

    # OpenAI Configuration
    openai_api_key: str = os.getenv("OPENAI_API_KEY", "")

    # Redis Configuration (for caching)
    redis_host: str = "localhost"
    redis_port: int = 6379
    redis_db: int = 0
    cache_enabled: bool = False  # Set to True if Redis is available

    # Rate Limiting
    api_rate_limit: str = "10/minute"

    # Slide Configuration
    max_slides: int = 20
    min_slides: int = 1
    default_slides: int = 5

    # File Storage
    output_dir: str = "./generated_presentations"

    # LLM Configuration
    llm_model: str = "gpt-4.1-mini"
    llm_temperature: float = 0.7
    llm_max_tokens: int = 2000


@lru_cache()
def get_settings() -> Settings:
    """Get cached settings instance"""
    return Settings()
