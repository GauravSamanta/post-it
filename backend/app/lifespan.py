from contextlib import asynccontextmanager
from fastapi import FastAPI
from app.db.connection import init_db, close_db


@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup code
    await init_db()
    
    yield  # Control is passed to FastAPI here
    # Shutdown code
    await close_db()
