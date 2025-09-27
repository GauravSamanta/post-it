#!/usr/bin/env python3
"""
Database initialization script.
Creates the initial database schema and superuser.
"""

from sqlalchemy.orm import Session

from app.core.config import settings
from app.core.database import SessionLocal, engine
from app.core.logging import setup_logging, get_logger
from app.models import Base
from app.crud.user import user_crud
from app.schemas.user import UserCreate

# Setup logging
setup_logging()
logger = get_logger(__name__)


def init_db(db: Session) -> None:
    Base.metadata.create_all(bind=engine)
    
    user = user_crud.get_by_email(db, email=settings.FIRST_SUPERUSER)
    if not user:
        user_in = UserCreate(
            email=settings.FIRST_SUPERUSER,
            password=settings.FIRST_SUPERUSER_PASSWORD,
            is_superuser=True,
            full_name="System Administrator"
        )
        user_crud.create(db, obj_in=user_in)


def main() -> None:
    db = SessionLocal()
    try:
        init_db(db)
        db.commit()
    except Exception as e:
        logger.error("Database initialization failed", error=str(e))
        db.rollback()
        raise
    finally:
        db.close()


if __name__ == "__main__":
    main()

