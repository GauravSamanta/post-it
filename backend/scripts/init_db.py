#!/usr/bin/env python3

import asyncio

from app.core.config import settings
from app.core.database import database, USERS_TABLE_SQL
from app.core.logging import setup_logging, get_logger
from app.crud.user import user_crud
from app.schemas.user import UserCreate

setup_logging()
logger = get_logger(__name__)


async def init_db() -> None:
    await database.connect()
    
    try:
        await database.execute(USERS_TABLE_SQL)
        
        user = await user_crud.get_by_email(database, email=settings.FIRST_SUPERUSER)
        if not user:
            user_in = UserCreate(
                email=settings.FIRST_SUPERUSER,
                password=settings.FIRST_SUPERUSER_PASSWORD,
                is_superuser=True,
                full_name="System Administrator"
            )
            await user_crud.create(database, obj_in=user_in)
    except Exception as e:
        logger.error("Database initialization failed", error=str(e))
        raise
    finally:
        await database.disconnect()


async def main() -> None:
    await init_db()


if __name__ == "__main__":
    asyncio.run(main())

