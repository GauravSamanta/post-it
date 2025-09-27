#!/usr/bin/env python3
"""
Database initialization script.
Creates the initial database schema and superuser.
"""

import asyncio
from sqlalchemy.orm import Session

from app.core.config import settings
from app.core.database import SessionLocal, engine
from app.models import Base
from app.crud.user import user_crud
from app.schemas.user import UserCreate


def init_db(db: Session) -> None:
    """Initialize database with tables and superuser."""
    
    # Create all tables
    Base.metadata.create_all(bind=engine)
    
    # Create superuser if it doesn't exist
    user = user_crud.get_by_email(db, email=settings.FIRST_SUPERUSER)
    if not user:
        user_in = UserCreate(
            email=settings.FIRST_SUPERUSER,
            password=settings.FIRST_SUPERUSER_PASSWORD,
            is_superuser=True,
            full_name="System Administrator"
        )
        user = user_crud.create(db, obj_in=user_in)
        print(f"Created superuser: {user.email}")
    else:
        print(f"Superuser already exists: {user.email}")


def main() -> None:
    """Main function."""
    print("Initializing database...")
    
    db = SessionLocal()
    try:
        init_db(db)
        print("Database initialization completed successfully!")
    except Exception as e:
        print(f"Error initializing database: {e}")
        raise
    finally:
        db.close()


if __name__ == "__main__":
    main()

