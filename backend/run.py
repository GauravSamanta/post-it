#!/usr/bin/env python3
"""Production-ready FastAPI application runner."""

import uvicorn
from app.main import app
from app.core.config import settings


def main() -> None:
    """Run the FastAPI application."""
    
    # Production configuration
    config = {
        "app": "app.main:app",
        "host": "0.0.0.0",
        "port": 8000,
        "workers": 1 if settings.ENVIRONMENT == "development" else 4,
        "reload": settings.ENVIRONMENT == "development",
        "log_level": settings.LOG_LEVEL.lower(),
        "access_log": True,
        "use_colors": settings.ENVIRONMENT == "development",
        "server_header": False,  # Security: hide server header
        "date_header": False,    # Security: hide date header
    }
    
    # Additional production settings
    if settings.ENVIRONMENT == "production":
        config.update({
            "reload": False,
            "debug": False,
            "log_config": None,  # Use our custom logging
        })
    
    print(f"Starting {settings.PROJECT_NAME} v{settings.VERSION}")
    print(f"Environment: {settings.ENVIRONMENT}")
    print(f"Debug mode: {settings.DEBUG}")
    print(f"Docs available: {settings.ENVIRONMENT != 'production'}")
    print(f"Workers: {config['workers']}")
    print(f"Host: {config['host']}:{config['port']}")
    print("-" * 50)
    
    uvicorn.run(**config)


if __name__ == "__main__":
    main()
