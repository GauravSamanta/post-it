from typing import List, Optional
import secrets
import os
from dotenv import load_dotenv

load_dotenv()

class Settings:
    def __init__(self, **kwargs):
        self.PROJECT_NAME: str = os.getenv("PROJECT_NAME", "Post-It Notes API")
        self.VERSION: str = os.getenv("VERSION", "1.0.0")
        self.DESCRIPTION: str = os.getenv("DESCRIPTION", "A production-ready FastAPI application for post-it notes")
        self.API_STR: str = os.getenv("API_STR", "/api")
        self.ENVIRONMENT: str = os.getenv("ENVIRONMENT", "development")
        self.DEBUG: bool = os.getenv("DEBUG", "false").lower() == "true"
        
        self.SECRET_KEY: str = os.getenv("SECRET_KEY", secrets.token_urlsafe(32))
        self.ACCESS_TOKEN_EXPIRE_MINUTES: int = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES", "1440"))
        self.REFRESH_TOKEN_EXPIRE_MINUTES: int = int(os.getenv("REFRESH_TOKEN_EXPIRE_MINUTES", "10080"))
        self.ALGORITHM: str = os.getenv("ALGORITHM", "HS256")
        
        cors_origins = os.getenv("BACKEND_CORS_ORIGINS", "http://localhost:3000,http://localhost:3001,http://localhost:5173")
        self.BACKEND_CORS_ORIGINS: List[str] = [origin.strip() for origin in cors_origins.split(",")]
        
        allowed_hosts = os.getenv("ALLOWED_HOSTS", "localhost,127.0.0.1,*")
        self.ALLOWED_HOSTS: List[str] = [host.strip() for host in allowed_hosts.split(",")]
        

        # Database
        self.DATABASE_URL: str = os.getenv("DATABASE_URL", "postgresql+psycopg2://postgres:rishi@localhost:5432/app")
        
        # Redis
        self.REDIS_URL: str = os.getenv("REDIS_URL", "redis://localhost:6379")
        
        self.FIRST_SUPERUSER: str = os.getenv("FIRST_SUPERUSER", "admin@example.com")
        self.FIRST_SUPERUSER_PASSWORD: str = os.getenv("FIRST_SUPERUSER_PASSWORD", "changethis")
        
        self.LOG_LEVEL: str = os.getenv("LOG_LEVEL", "INFO")
        
        self.MAX_FILE_SIZE: int = int(os.getenv("MAX_FILE_SIZE", str(10 * 1024 * 1024)))
        self.UPLOAD_DIR: str = os.getenv("UPLOAD_DIR", "uploads")
        
        self.RATE_LIMIT_PER_MINUTE: int = int(os.getenv("RATE_LIMIT_PER_MINUTE", "60"))


settings = Settings()
