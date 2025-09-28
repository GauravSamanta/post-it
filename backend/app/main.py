from fastapi import FastAPI
from app.api.router import api_router
from app.lifespan import lifespan
from app.core import logging
from app.core.middleware import LoggingMiddleware  # Ensure logging is configured


app = FastAPI(title="Post It", lifespan=lifespan, logging=logging.logger)


app.include_router(api_router, prefix="/api/v1")

app.add_middleware(LoggingMiddleware)


@app.get("/")
async def root():
    return {"message": "FastAPI + asyncpg with lifespan running!"}
