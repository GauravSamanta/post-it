from asyncpg import Connection
import asyncpg
from app.core.config import settings
from app.core.logging import logger

pool: asyncpg.Pool | None = None


async def init_db():
    global pool
    logger.info("📦 Initializing database connection pool...")
    pool = await asyncpg.create_pool(dsn=settings.DATABASE_URL,min_size=1, max_size=10)
    logger.info("✅ Database pool created")


async def close_db():
    global pool
    if pool:
        await pool.close()
        logger.info("🛑 Database pool closed")



async def get_db():
    if pool is None:
        raise RuntimeError("Database pool is not initialized")
    async with pool.acquire() as connection:
        yield connection
