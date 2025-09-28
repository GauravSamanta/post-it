from typing import Optional

from pydantic import BaseModel


class Token(BaseModel):
    accessToken: str
    refreshToken: str
    tokenType: str


class TokenPayload(BaseModel):
    sub: Optional[int] = None
