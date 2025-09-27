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
    """Initialize database with tables and superuser."""
    
    # Create all tables
    logger.info("Creating database tables...")
    Base.metadata.create_all(bind=engine)
    logger.info("Database tables created successfully")
    
    # Create superuser if it doesn't exist
    logger.info("Checking for superuser...")
    user = user_crud.get_by_email(db, email=settings.FIRST_SUPERUSER)
    if not user:
        logger.info("Creating superuser...", email=settings.FIRST_SUPERUSER)
        user_in = UserCreate(
            email=settings.FIRST_SUPERUSER,
            password=settings.FIRST_SUPERUSER_PASSWORD,
            is_superuser=True,
            full_name="System Administrator"
        )
        user = user_crud.create(db, obj_in=user_in)
        logger.info("Superuser created successfully", email=user.email, user_id=user.id)
    else:
        logger.info("Superuser already exists", email=user.email, user_id=user.id)


def main() -> None:
    """Main function."""
    logger.info("Starting database initialization...")
    
    db = SessionLocal()
    try:
        init_db(db)
        db.commit()
        logger.info("Database initialization completed successfully!")
    except Exception as e:
        logger.error("Database initialization failed", error=str(e))
        db.rollback()
        raise
    finally:
        db.close()


if __name__ == "__main__":
    main()

