from datetime import datetime
from typing import Optional

from pydantic import BaseModel, EmailStr


class User(BaseModel):
    id: Optional[int] = None
    email: str
    hashed_password: str
    full_name: Optional[str] = None
    is_active: bool = True
    is_superuser: bool = False
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None

    class Config:
        from_attributes = True

    @classmethod
    def from_record(cls, record):
        if not record:
            return None
        return cls(
            id=record["id"],
            email=record["email"],
            hashed_password=record["hashed_password"],
            full_name=record["full_name"],
            is_active=record["is_active"],
            is_superuser=record["is_superuser"],
            created_at=record["created_at"],
            updated_at=record["updated_at"],
        )
