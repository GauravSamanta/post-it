from datetime import datetime, timedelta, timezone
from hashlib import sha256
from typing import Any, Optional, Union

import structlog
from jose import JWTError, jwt

from app.core.config import settings

logger = structlog.get_logger(__name__)


def create_access_token(
    subject: Union[str, Any], expires_delta: timedelta = None
) -> str:
    now = datetime.now(timezone.utc)

    if expires_delta:
        expire = now + expires_delta
    else:
        expire = now + timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)

    to_encode = {"exp": expire, "sub": str(subject), "type": "access", "iat": now}

    try:
        encoded_jwt = jwt.encode(
            to_encode, settings.SECRET_KEY, algorithm=settings.ALGORITHM
        )
        return encoded_jwt
    except Exception as e:
        logger.error("Failed to create access token", error=str(e))
        raise


def create_refresh_token(
    subject: Union[str, Any], expires_delta: timedelta = None
) -> str:
    now = datetime.now(timezone.utc)

    if expires_delta:
        expire = now + expires_delta
    else:
        expire = now + timedelta(minutes=settings.REFRESH_TOKEN_EXPIRE_MINUTES)

    to_encode = {"exp": expire, "sub": str(subject), "type": "refresh", "iat": now}

    try:
        encoded_jwt = jwt.encode(
            to_encode, settings.SECRET_KEY, algorithm=settings.ALGORITHM
        )
        return encoded_jwt
    except Exception as e:
        logger.error("Failed to create refresh token", error=str(e))
        raise


def verify_token(token: str, token_type: str = "access") -> Optional[str]:
    try:
        payload = jwt.decode(
            token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM]
        )

        user_id: str = payload.get("sub")
        token_type_payload: str = payload.get("type")

        if user_id is None or token_type_payload != token_type:
            return None

        return user_id

    except JWTError:
        return None


def get_password_hash(password: str) -> str:
    try:

        hashed = sha256(password.strip().encode()).hexdigest()
        return hashed

    except Exception as e:
        logger.error("Failed to hash password", error=str(e))
        raise


def verify_password(plain_password: str, hashed_password: str) -> bool:
    try:

        hashed = sha256(plain_password.strip().encode()).hexdigest()
        is_valid = hashed == hashed_password
        logger.info("Password verification completed", is_valid=is_valid)
        return is_valid

    except Exception as e:
        logger.error("Password verification failed", error=str(e))
        return False
