"""
Configuration settings for EduInsight-AI.

This module manages application configuration using environment variables.
"""

from functools import lru_cache
from typing import Optional

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """Application settings."""

    # Application
    app_name: str = "EduInsight-AI"
    app_version: str = "0.1.0"
    debug: bool = False

    # Server
    host: str = "0.0.0.0"
    port: int = 8000

    # LLM Configuration
    llm_provider: str = "mock"  # mock, openai, azure
    openai_api_key: Optional[str] = None
    openai_model: str = "gpt-3.5-turbo"
    azure_api_key: Optional[str] = None
    azure_endpoint: Optional[str] = None
    azure_model: str = "gpt-35-turbo"
    azure_api_version: str = "2024-02-15-preview"

    # CORS
    cors_origins: list = ["*"]

    # Logging
    log_level: str = "INFO"

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=False,
        extra="ignore",
    )

    @property
    def is_production(self) -> bool:
        """Check if running in production mode."""
        return not self.debug


@lru_cache()
def get_settings() -> Settings:
    """Get cached settings instance."""
    return Settings()


# Example .env file content:
"""
# EduInsight-AI Configuration

# Application
APP_NAME=EduInsight-AI
DEBUG=false

# Server
HOST=0.0.0.0
PORT=8000

# LLM Provider (mock, openai, azure)
LLM_PROVIDER=mock

# OpenAI Configuration (if using OpenAI)
OPENAI_API_KEY=your-openai-api-key-here
OPENAI_MODEL=gpt-3.5-turbo

# Azure OpenAI Configuration (if using Azure)
AZURE_API_KEY=your-azure-api-key-here
AZURE_ENDPOINT=https://your-resource.openai.azure.com/
AZURE_MODEL=gpt-35-turbo
AZURE_API_VERSION=2024-02-15-preview

# Logging
LOG_LEVEL=INFO
"""
