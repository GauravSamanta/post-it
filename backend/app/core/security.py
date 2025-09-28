from argon2 import PasswordHasher
import jwt
from datetime import datetime, timedelta
from typing import Optional
from app.core.config import settings  # for secret key and expiration

ph = PasswordHasher()


async def hash_password(password: str) -> str:
    return ph.hash(password)


def verify_password(hash: str, password: str) -> bool:
    try:
        ph.verify(hash, password)
        return True
    except:
        return False


def token_generator(email: str, expires_delta: Optional[timedelta] = None) -> str:
    """
    Generate a JWT token for the given email.
    """
    expire = datetime.now() + (
        expires_delta or timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    )

    payload = {"sub": email, "exp": expire}

    token = jwt.encode(
        payload, settings.JWT_SECRET_KEY, algorithm=settings.JWT_ALGORITHM
    )
    return token
