"""
Application configuration
"""
import os
from functools import lru_cache
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    """Application settings"""

    # API Configuration
    app_name: str = "Slide Generator API"
    version: str = "1.0.0"
    environment: str = "development"

    # OpenAI Configuration
    openai_api_key: str = os.environ.get("OPENAI_API_KEY")

    # Slide Configuration
    max_slides: int = 20
    min_slides: int = 1
    default_slides: int = 5

    # File Storage
    output_dir: str = "./generated_presentations"

    # LLM Configuration
    llm_model: str = "gpt-3.5-turbo"
    llm_temperature: float = 0.7
    llm_max_tokens: int = 2000

    class Config:
        env_file = ".env"
        case_sensitive = False


@lru_cache()
def get_settings() -> Settings:
    """Get cached settings instance"""
    return Settings()
