"""Runtime configuration for the NovaShield API."""

from __future__ import annotations

from functools import lru_cache
from typing import List

from pydantic import BaseSettings, Field


class Settings(BaseSettings):
    app_name: str = "NovaShield API"
    api_prefix: str = "/api"
    cors_origins: List[str] = Field(default_factory=lambda: ["*"])
    history_size: int = 10

    class Config:
        env_prefix = "NOVASHIELD_"


@lru_cache()
def get_settings() -> Settings:
    """Provide a singleton-style accessor for application settings."""

    return Settings()
