from pydantic import BaseModel, EmailStr


class UserBase(BaseModel):
	email: EmailStr
	full_name: str | None = None


class UserCreate(UserBase):
	password: str


class UserInDB(UserBase):
	id: int
	hashed_password: str

	class Config:
		from_attributes = True


class UserPublic(UserBase):
	id: int
