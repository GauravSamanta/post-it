#!/usr/bin/env python3

import uvicorn

from app.core.config import settings
from app.main import app


def main() -> None:
    config = {
        "app": "app.main:app",
        "host": "0.0.0.0",
        "port": 8000,
        "workers": 1 if settings.ENVIRONMENT == "development" else 4,
        "reload": settings.ENVIRONMENT == "development",
        "log_level": settings.LOG_LEVEL.lower(),
        "access_log": True,
        "use_colors": settings.ENVIRONMENT == "development",
        "server_header": False,
        "date_header": False,
    }

    if settings.ENVIRONMENT == "production":
        config.update(
            {
                "reload": False,
                "debug": False,
                "log_config": None,
            }
        )

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
