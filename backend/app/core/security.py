# app/core/security.py
import jwt

from app.core.config import settings


def create_jwt(data: dict) -> str:
    return jwt.encode(data, settings.JWT_SECRET, algorithm=settings.JWT_ALGORITHM)
