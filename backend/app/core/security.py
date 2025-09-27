from datetime import datetime, timedelta, timezone
from typing import Any, Union, Optional
from jose import jwt, JWTError
from passlib.context import CryptContext
import structlog

from app.core.config import settings

logger = structlog.get_logger(__name__)

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def create_access_token(
    subject: Union[str, Any], expires_delta: timedelta = None
) -> str:
    """Create access token."""
    now = datetime.now(timezone.utc)
    
    if expires_delta:
        expire = now + expires_delta
    else:
        expire = now + timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    
    to_encode = {
        "exp": expire,
        "sub": str(subject),
        "type": "access",
        "iat": now
    }
    
    try:
        encoded_jwt = jwt.encode(to_encode, settings.SECRET_KEY, algorithm=settings.ALGORITHM)
        logger.info("Access token created", subject=subject, expires_at=expire.isoformat())
        return encoded_jwt
    except Exception as e:
        logger.error("Failed to create access token", error=str(e), subject=subject)
        raise


def create_refresh_token(
    subject: Union[str, Any], expires_delta: timedelta = None
) -> str:
    """Create refresh token."""
    now = datetime.now(timezone.utc)
    
    if expires_delta:
        expire = now + expires_delta
    else:
        expire = now + timedelta(minutes=settings.REFRESH_TOKEN_EXPIRE_MINUTES)
    
    to_encode = {
        "exp": expire,
        "sub": str(subject),
        "type": "refresh",
        "iat": now
    }
    
    try:
        encoded_jwt = jwt.encode(to_encode, settings.SECRET_KEY, algorithm=settings.ALGORITHM)
        logger.info("Refresh token created", subject=subject, expires_at=expire.isoformat())
        return encoded_jwt
    except Exception as e:
        logger.error("Failed to create refresh token", error=str(e), subject=subject)
        raise




def verify_token(token: str, token_type: str = "access") -> Optional[str]:
    """Verify JWT token."""
    try:
        payload = jwt.decode(
            token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM]
        )
        
        user_id: str = payload.get("sub")
        token_type_payload: str = payload.get("type")
        
        if user_id is None:
            logger.warning("Token verification failed: missing subject")
            return None
            
        if token_type_payload != token_type:
            logger.warning(
                "Token verification failed: invalid token type",
                expected=token_type,
                actual=token_type_payload
            )
            return None
            
        logger.info("Token verified successfully", user_id=user_id, token_type=token_type)
        return user_id
        
    except JWTError as e:
        logger.warning("Token verification failed", error=str(e), token_type=token_type)
        return None


def get_password_hash(password: str) -> str:
    """Hash password."""
    try:
        hashed = pwd_context.hash(password)
        logger.info("Password hashed successfully")
        return hashed
    except Exception as e:
        logger.error("Failed to hash password", error=str(e))
        raise


def verify_password(plain_password: str, hashed_password: str) -> bool:
    """Verify password."""
    try:
        is_valid = pwd_context.verify(plain_password, hashed_password)
        logger.info("Password verification completed", is_valid=is_valid)
        return is_valid
    except Exception as e:
        logger.error("Password verification failed", error=str(e))
        return False
