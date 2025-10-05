from pydantic import BaseModel, EmailStr


class UserBase(BaseModel):
	email: EmailStr
	full_name: str | None = None


class UserCreate(UserBase):
	password: str


class UserPasswordHash(UserBase):
	id: int
	hashed_password: str

	class Config:
		from_attributes = True


class UserPublic(UserBase):
	id: int


class User(UserPasswordHash):
	pass


class UserPasswordOnly(BaseModel):
	"""Minimal class for password verification - only contains hashed_password"""
	hashed_password: str
	
	class Config:
		from_attributes = True