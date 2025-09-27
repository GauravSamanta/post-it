from typing import List, Optional, Union
from pydantic import AnyHttpUrl, EmailStr
from pydantic_settings import BaseSettings
import secrets


class Settings(BaseSettings):
    # Project settings
    PROJECT_NAME: str = "FastAPI React Boilerplate"
    VERSION: str = "1.0.0"
    DESCRIPTION: str = "A scalable FastAPI + React boilerplate"
    API_V1_STR: str = "/api/v1"
    
    # Security
    SECRET_KEY: str = secrets.token_urlsafe(32)
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60 * 24 * 8  # 8 days
    REFRESH_TOKEN_EXPIRE_MINUTES: int = 60 * 24 * 30  # 30 days
    ALGORITHM: str = "HS256"
    
    # CORS
    BACKEND_CORS_ORIGINS: List[AnyHttpUrl] = [
        "http://localhost:3000",
        "http://localhost:3001",
        "http://localhost:5173",  # Vite default
    ]
    
    # Trusted hosts
    ALLOWED_HOSTS: List[str] = ["localhost", "127.0.0.1"]

    # @validator("BACKEND_CORS_ORIGINS", pre=True)
    # def assemble_cors_origins(cls, v: Union[str, List[str]]) -> Union[List[str], str]:
    #     if isinstance(v, str) and not v.startswith("["):
    #         return [i.strip() for i in v.split(",")]
    #     elif isinstance(v, (list, str)):
    #         return v
    #     raise ValueError(v)

    # Database
    DATABASE_URL: str = "sqlite:///./app.db"
    
    # For PostgreSQL (uncomment and configure as needed)
    # POSTGRES_SERVER: str = "localhost"
    # POSTGRES_USER: str = "postgres"
    # POSTGRES_PASSWORD: str = "password"
    # POSTGRES_DB: str = "app"
    # DATABASE_URL: str = f"postgresql://{POSTGRES_USER}:{POSTGRES_PASSWORD}@{POSTGRES_SERVER}/{POSTGRES_DB}"
    
    # Redis (for caching and sessions)
    REDIS_URL: str = "redis://localhost:6379"
    
    # Email settings
    SMTP_TLS: bool = True
    SMTP_PORT: Optional[int] = None
    SMTP_HOST: Optional[str] = None
    SMTP_USER: Optional[str] = None
    SMTP_PASSWORD: Optional[str] = None
    EMAILS_FROM_EMAIL: Optional[EmailStr] = None
    EMAILS_FROM_NAME: Optional[str] = None
    
    # Superuser
    FIRST_SUPERUSER: EmailStr = "admin@example.com"
    FIRST_SUPERUSER_PASSWORD: str = "changethis"
    
    # Logging
    LOG_LEVEL: str = "INFO"
    
    # File upload
    MAX_FILE_SIZE: int = 10 * 1024 * 1024  # 10MB
    UPLOAD_DIR: str = "uploads"
    
    # Rate limiting
    RATE_LIMIT_PER_MINUTE: int = 60
    
    model_config = {
        "env_file": ".env",
        "case_sensitive": True
    }


settings = Settings()
