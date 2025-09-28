import asyncio
import asyncpg
from pathlib import Path
from app.core.config import settings
from app.core.logging import logger

MIGRATIONS_DIR = Path(__file__).parent.parent / "app" / "db" / "migrations"

async def apply_migrations():
    conn = await asyncpg.connect(dsn=settings.DATABASE_URL)

    # ensure migrations table exists
    await conn.execute("""
        CREATE TABLE IF NOT EXISTS schema_migrations (
            id SERIAL PRIMARY KEY,
            filename TEXT UNIQUE NOT NULL,
            applied_at TIMESTAMP DEFAULT NOW()
        );
    """)

    applied = await conn.fetch("SELECT filename FROM schema_migrations;")
    applied_files = {row["filename"] for row in applied}

    for file in sorted(MIGRATIONS_DIR.glob("*.sql")):
        if file.name not in applied_files:
            logger.info(f"📂 Applying migration: {file.name}")
            sql = file.read_text()
            async with conn.transaction():
                await conn.execute(sql)
                await conn.execute(
                    "INSERT INTO schema_migrations (filename) VALUES ($1);",
                    file.name
                )
            logger.info(f"✅ Migration {file.name} applied")

    await conn.close()
    logger.info("🎉 All migrations complete")


if __name__ == "__main__":
    asyncio.run(apply_migrations())
