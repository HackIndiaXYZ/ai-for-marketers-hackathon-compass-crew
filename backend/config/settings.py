"""
PainToAd AI - Backend System Configuration
==========================================
Production-ready configuration management powered by Pydantic BaseSettings.
Loads environment variables seamlessly from system environment or .env file.
"""

import os
from typing import List, Union
from pydantic import Field, validator
try:
    from pydantic_settings import BaseSettings
except ImportError:
    from pydantic import BaseSettings  # Fallback for Pydantic v1


class Settings(BaseSettings):
    """
    Central Application Settings for PainToAd AI Backend service.
    """

    # --- General App Settings ---
    APP_NAME: str = Field(default="PainToAd AI", description="Name of the application")
    APP_VERSION: str = Field(default="1.0.0", description="API version tag")
    ENVIRONMENT: str = Field(default="production", description="Environment mode: development, staging, production")
    DEBUG: bool = Field(default=False, description="Debug mode flag")
    API_V1_STR: str = Field(default="/api/v1", description="Global API Route Prefix")
    HOST: str = Field(default="0.0.0.0", description="Binding host address")
    PORT: int = Field(default=8000, description="Binding port number")

    # --- Security & Auth Settings ---
    SECRET_KEY: str = Field(
        default="pain_to_ad_ai_super_secret_jwt_key_hackathon_2026_production_secure",
        description="JWT secret key for signing tokens"
    )
    ALGORITHM: str = Field(default="HS256", description="JWT encryption algorithm")
    ACCESS_TOKEN_EXPIRE_MINUTES: int = Field(
        default=60 * 24 * 7, description="Access token expiration time (7 days)"
    )

    # --- CORS Security ---
    BACKEND_CORS_ORIGINS: List[str] = Field(
        default=[
            "http://localhost:3000",
            "http://localhost:8000",
            "https://pain-to-ad-ai.vercel.app",
            "https://praintoad-ai.onrender.com",
            "*"
        ],
        description="Allowed CORS origin domains"
    )

    @validator("BACKEND_CORS_ORIGINS", pre=True)
    def assemble_cors_origins(cls, v: Union[str, List[str]]) -> List[str]:
        if isinstance(v, str) and not v.startswith("["):
            return [i.strip() for i in v.split(",")]
        elif isinstance(v, (list, str)):
            return v
        raise ValueError(v)

    # --- Database Settings (MongoDB Atlas) ---
    MONGODB_URL: str = Field(
        default="mongodb+srv://admin:password@cluster.mongodb.net/?retryWrites=true&w=majority",
        description="MongoDB connection string URI"
    )
    DATABASE_NAME: str = Field(default="pain_to_ad_ai_db", description="Database name")
    MONGODB_MIN_POOL_SIZE: int = Field(default=10, description="Minimum connection pool size")
    MONGODB_MAX_POOL_SIZE: int = Field(default=100, description="Maximum connection pool size")

    # --- AI & LLM Model Settings ---
    GEMINI_API_KEY: str = Field(
        default="YOUR_GEMINI_API_KEY_HERE",
        description="Google Gemini API key"
    )
    GEMINI_MODEL: str = Field(
        default="gemini-1.5-pro",
        description="Google Gemini model identifier for campaign generation"
    )
    EMBEDDING_MODEL: str = Field(
        default="sentence-transformers/all-MiniLM-L6-v2",
        description="Sentence Transformer model for semantic embedding vector space"
    )
    LLM_TEMPERATURE: float = Field(default=0.7, description="Temperature parameter for LLM generation")
    LLM_MAX_TOKENS: int = Field(default=2048, description="Maximum token generation limit")

    # --- Data Scraper & Crawler Settings ---
    MAX_SCRAPE_RESULTS: int = Field(default=100, description="Maximum posts fetched per scraping session")
    SCRAPER_USER_AGENT: str = Field(
        default="PainToAd-Bot/1.0 (+https://pain-to-ad-ai.com)",
        description="User agent string for social data collection"
    )

    # --- Redis / Cache Settings (Optional/Future Scaling) ---
    REDIS_URL: str = Field(default="redis://localhost:6379/0", description="Redis connection URL for caching")
    ENABLE_CACHE: bool = Field(default=True, description="Enable caching for repeated intelligence queries")

    class Config:
        case_sensitive = True
        env_file = ".env"
        env_file_encoding = "utf-8"


# Singleton instance of configuration settings
settings = Settings()
