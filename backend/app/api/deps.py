import jwt
from app.db.connection import get_db
from app.core.config import settings
from app.db.schemas.user import UserRead

from app.db.connection import pool


async def get_db_pool():
    if pool is None:
        raise RuntimeError("Database pool is not initialized")
    return pool


async def get_current_user(credentials, queries, pool):
    """
    Dependency function for protected routes
    """
    from fastapi import HTTPException, status

    token = credentials.credentials
    try:
        payload = jwt.decode(
            token, settings.JWT_SECRET_KEY, algorithms=[settings.JWT_ALGORITHM]
        )
        email = payload.get("sub")
        if email is None:
            raise HTTPException(status_code=401, detail="Invalid token")

        async with pool.acquire() as conn:
            row = await conn.fetchrow(queries["users"]["get_user_by_email"], email)
            if not row:
                raise HTTPException(status_code=401, detail="User not found")
            return UserRead(**row)  # or convert to schema if needed
    except jwt.ExpiredSignatureError:
        raise HTTPException(status_code=401, detail="Token expired")
    except jwt.InvalidTokenError:
        raise HTTPException(status_code=401, detail="Invalid token")
