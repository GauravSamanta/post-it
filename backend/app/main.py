from contextlib import asynccontextmanager
from typing import Dict, Any
from fastapi import FastAPI, Request, status
from fastapi.middleware.cors import CORSMiddleware
from fastapi.middleware.trustedhost import TrustedHostMiddleware
from fastapi.middleware.gzip import GZipMiddleware
from fastapi.responses import JSONResponse
from fastapi.exceptions import RequestValidationError, HTTPException
import uvicorn
import structlog

from app.core.config import settings
from app.core.database import engine, get_db_health
from app.core.logging import setup_logging, get_logger
from app.core.middleware import RequestLoggingMiddleware, SecurityHeadersMiddleware
from app.models import Base
from app.api.v1.router import api_router
from app.core.exceptions import CustomException

# Setup structured logging
setup_logging()
logger = get_logger(__name__)


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Application lifespan events."""
    # Startup
    logger.info(
        "Starting up application",
        version=settings.VERSION,
        environment=settings.ENVIRONMENT,
    )
    
    # Create database tables
    try:
        Base.metadata.create_all(bind=engine)
        logger.info("Database tables created/verified")
    except Exception as e:
        logger.error("Failed to create database tables", error=str(e))
        raise
    
    yield
    
    # Shutdown
    logger.info("Shutting down application")


def create_application() -> FastAPI:
    """Create FastAPI application with all configurations."""
    
    # Configure docs based on environment
    docs_url = "/docs" if settings.ENVIRONMENT != "production" else None
    redoc_url = "/redoc" if settings.ENVIRONMENT != "production" else None
    
    app = FastAPI(
        title=settings.PROJECT_NAME,
        version=settings.VERSION,
        description=settings.DESCRIPTION,
        openapi_url=f"{settings.API_V1_STR}/openapi.json" if settings.ENVIRONMENT != "production" else None,
        docs_url=docs_url,
        redoc_url=redoc_url,
        lifespan=lifespan,
    )

    # Add middleware in reverse order (last added = first executed)
    
    # Security headers middleware
    # app.add_middleware(SecurityHeadersMiddleware)
    
    # Request logging middleware
    app.add_middleware(RequestLoggingMiddleware)
    
    # GZip compression
    app.add_middleware(GZipMiddleware, minimum_size=1000)
    
    # CORS middleware
    if settings.BACKEND_CORS_ORIGINS:
        app.add_middleware(
            CORSMiddleware,
            allow_origins=[str(origin) for origin in settings.BACKEND_CORS_ORIGINS],
            allow_credentials=True,
            allow_methods=["GET", "POST", "PUT", "DELETE", "OPTIONS"],
            allow_headers=["*"],
        )

    # Trusted host middleware
    app.add_middleware(
        TrustedHostMiddleware,
        allowed_hosts=settings.ALLOWED_HOSTS
    )

    # Include API router
    app.include_router(api_router, prefix=settings.API_V1_STR)

    # Exception handlers
    @app.exception_handler(CustomException)
    async def custom_exception_handler(request: Request, exc: CustomException):
        logger.error(
            "Custom exception occurred",
            request_id=getattr(request.state, "request_id", None),
            status_code=exc.status_code,
            detail=exc.detail,
        )
        return JSONResponse(
            status_code=exc.status_code,
            content={
                "error": {
                    "type": "CustomException",
                    "message": exc.detail,
                    "request_id": getattr(request.state, "request_id", None),
                }
            }
        )

    @app.exception_handler(RequestValidationError)
    async def validation_exception_handler(request: Request, exc: RequestValidationError):
        logger.warning(
            "Validation error",
            request_id=getattr(request.state, "request_id", None),
            errors=exc.errors(),
        )
        return JSONResponse(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            content={
                "error": {
                    "type": "ValidationError",
                    "message": "Request validation failed",
                    "details": exc.errors(),
                    "request_id": getattr(request.state, "request_id", None),
                }
            }
        )

    @app.exception_handler(HTTPException)
    async def http_exception_handler(request: Request, exc: HTTPException):
        logger.warning(
            "HTTP exception",
            request_id=getattr(request.state, "request_id", None),
            status_code=exc.status_code,
            detail=exc.detail,
        )
        return JSONResponse(
            status_code=exc.status_code,
            content={
                "error": {
                    "type": "HTTPException",
                    "message": exc.detail,
                    "request_id": getattr(request.state, "request_id", None),
                }
            }
        )

    @app.exception_handler(500)
    async def internal_server_error_handler(request: Request, exc: Exception):
        logger.error(
            "Internal server error",
            request_id=getattr(request.state, "request_id", None),
            error=str(exc),
            exc_info=True,
        )
        return JSONResponse(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            content={
                "error": {
                    "type": "InternalServerError",
                    "message": "Internal server error occurred",
                    "request_id": getattr(request.state, "request_id", None),
                }
            }
        )

    # Health check endpoints
    @app.get("/health")
    async def health_check() -> Dict[str, Any]:
        """Basic health check."""
        return {
            "status": "healthy",
            "version": settings.VERSION,
            "environment": settings.ENVIRONMENT,
        }

    @app.get("/health/detailed")
    async def detailed_health_check() -> Dict[str, Any]:
        """Detailed health check including database."""
        db_healthy = get_db_health()
        
        health_status = {
            "status": "healthy" if db_healthy else "unhealthy",
            "version": settings.VERSION,
            "environment": settings.ENVIRONMENT,
            "checks": {
                "database": "healthy" if db_healthy else "unhealthy",
            }
        }
        
        # Return 503 if any check fails
        status_code = status.HTTP_200_OK if db_healthy else status.HTTP_503_SERVICE_UNAVAILABLE
        return JSONResponse(status_code=status_code, content=health_status)

    return app


app = create_application()


if __name__ == "__main__":
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=8000,
        reload=True,
        log_level="info"
    )

