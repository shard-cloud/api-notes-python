"""
Configuration settings
"""

from pydantic_settings import BaseSettings
from typing import Optional


class Settings(BaseSettings):
    """Application settings"""
    
    # Database - REQUIRED
    database: str
    
    # Server - REQUIRED
    port: int
    host: str = "0.0.0.0"
    
    # Security - REQUIRED
    secret_key: str
    algorithm: str = "HS256"
    access_token_expire_minutes: int = 1440  # 24 hours
    
    # Environment - REQUIRED
    environment: str
    debug: bool = True
    
    class Config:
        env_file = ".env"
        case_sensitive = False


# Global settings instance
settings = Settings()
