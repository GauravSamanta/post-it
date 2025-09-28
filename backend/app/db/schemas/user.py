from datetime import datetime
from pydantic import BaseModel, EmailStr, field_validator, validator


class UserCreate(BaseModel):
    username: str
    email: str
    password: str


class UserLogin(BaseModel):
    email: EmailStr
    password: str
    @field_validator('password')
    def password_not_empty(cls, v):
        if not v or v.strip() == "":
            raise ValueError('Password must not be empty')
        return v

    


class UserRead(BaseModel):
    id: int
    username: str
    email: str
    created_at: datetime
    updated_at: datetime


class UserUpdate(BaseModel):
    email: str
    password: str
