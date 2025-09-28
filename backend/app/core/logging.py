import logging
import os
import coloredlogs

LOG_LEVEL = os.getenv("LOG_LEVEL", "INFO").upper()

# Create a logger
logger = logging.getLogger("fastapi-app")
logger.setLevel(LOG_LEVEL)

# Install coloredlogs for console output
coloredlogs.install(
    level=LOG_LEVEL,
    logger=logger,
    fmt="%(asctime)s | %(levelname)s | %(name)s | %(message)s",
)

# Optional file logging
file_handler = logging.FileHandler("app.log")
file_handler.setLevel(LOG_LEVEL)
file_handler.setFormatter(
    logging.Formatter("%(asctime)s | %(levelname)s | %(name)s | %(message)s")
)
logger.addHandler(file_handler)

# Replace FastAPI/Starlette loggers
logging.getLogger("uvicorn").handlers = logger.handlers
logging.getLogger("uvicorn.error").handlers = logger.handlers
logging.getLogger("uvicorn.access").handlers = logger.handlers
logging.getLogger("fastapi").handlers = logger.handlers
