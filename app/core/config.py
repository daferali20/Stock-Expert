# backend/app/core/config.py
from pydantic_settings import BaseSettings
from typing import Optional, List
from enum import Enum

class Environment(str, Enum):
    DEVELOPMENT = "development"
    STAGING = "staging"
    PRODUCTION = "production"

class Settings(BaseSettings):
    # ============================================
    # Application
    # ============================================
    APP_NAME: str = "ByToBy AI"
    VERSION: str = "1.0.0"
    ENVIRONMENT: Environment = Environment.DEVELOPMENT
    DEBUG: bool = True
    API_PREFIX: str = "/api/v1"
    
    # ============================================
    # Database
    # ============================================
    DATABASE_URL: str = "postgresql://user:password@localhost:5432/bytoby_db"
    DATABASE_POOL_SIZE: int = 20
    DATABASE_MAX_OVERFLOW: int = 40
    DATABASE_POOL_TIMEOUT: int = 30
    DATABASE_ECHO: bool = False
    
    # ============================================
    # Redis (for caching & workers)
    # ============================================
    REDIS_URL: str = "redis://localhost:6379/0"
    REDIS_CACHE_TTL: int = 3600  # 1 hour
    
    # ============================================
    # Security
    # ============================================
    SECRET_KEY: str = "your-super-secret-key-change-in-production"
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
    REFRESH_TOKEN_EXPIRE_DAYS: int = 7
    PASSWORD_MIN_LENGTH: int = 8
    BCRYPT_ROUNDS: int = 12
    
    # ============================================
    # CORS
    # ============================================
    CORS_ORIGINS: List[str] = [
        "http://localhost:3000",
        "http://localhost:8501",
        "https://bytoby.ai",
        "https://*.streamlit.app"
    ]
    
    # ============================================
    # External APIs
    # ============================================
    # Polygon.io (US Stocks)
    POLYGON_API_KEY: Optional[str] = None
    POLYGON_BASE_URL: str = "https://api.polygon.io"
    POLYGON_WS_URL: str = "wss://ws.polygon.io"
    
    # Finnhub (Global Stocks & News)
    FINNHUB_API_KEY: Optional[str] = None
    FINNHUB_BASE_URL: str = "https://finnhub.io/api/v1"
    
    # Alpha Vantage
    ALPHA_VANTAGE_KEY: Optional[str] = None
    ALPHA_VANTAGE_BASE_URL: str = "https://www.alphavantage.co/query"
    
    # OpenAI
    OPENAI_API_KEY: Optional[str] = None
    OPENAI_MODEL: str = "gpt-4-turbo-preview"
    OPENAI_MAX_TOKENS: int = 2000
    
    # News API
    NEWS_API_KEY: Optional[str] = None
    
    # ============================================
    # Email
    # ============================================
    SMTP_HOST: str = "smtp.gmail.com"
    SMTP_PORT: int = 587
    SMTP_USER: Optional[str] = None
    SMTP_PASSWORD: Optional[str] = None
    EMAIL_FROM: str = "noreply@bytoby.ai"
    
    # ============================================
    # Celery (Workers)
    # ============================================
    CELERY_BROKER_URL: str = "redis://localhost:6379/1"
    CELERY_RESULT_BACKEND: str = "redis://localhost:6379/2"
    CELERY_TASK_TRACK_STARTED: bool = True
    CELERY_TASK_TIME_LIMIT: int = 300  # 5 minutes
    
    # ============================================
    # WebSocket
    # ============================================
    WS_MAX_CONNECTIONS: int = 1000
    WS_PING_INTERVAL: int = 20
    WS_PING_TIMEOUT: int = 20
    
    # ============================================
    # Rate Limiting
    # ============================================
    RATE_LIMIT_PER_MINUTE: int = 60
    RATE_LIMIT_PER_DAY: int = 1000
    
    # ============================================
    # Subscription Plans
    # ============================================
    FREE_PLAN_LIMITS: dict = {
        "stocks_per_watchlist": 5,
        "max_watchlists": 3,
        "ai_analysis_per_day": 5,
        "alerts_per_day": 10,
        "historical_data_days": 30,
    }
    
    PREMIUM_PLAN_LIMITS: dict = {
        "stocks_per_watchlist": 50,
        "max_watchlists": 20,
        "ai_analysis_per_day": 100,
        "alerts_per_day": 100,
        "historical_data_days": 365,
        "real_time_data": True,
        "advanced_indicators": True,
    }
    
    PRO_PLAN_LIMITS: dict = {
        "stocks_per_watchlist": 200,
        "max_watchlists": 50,
        "ai_analysis_per_day": 500,
        "alerts_per_day": 500,
        "historical_data_days": 730,
        "real_time_data": True,
        "advanced_indicators": True,
        "custom_strategies": True,
        "api_access": True,
    }
    
    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"
        case_sensitive = True

settings = Settings()
