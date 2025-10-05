from typing import Annotated

from argon2 import PasswordHasher
from argon2.exceptions import VerifyMismatchError
from fastapi import Depends, status

from app.core.exceptions import DuplicateUserException, CustomException
from app.repository.user import UserRepository
from app.schemas.user import UserCreate


class UserService:
	def __init__(self, repo: Annotated[UserRepository, Depends(UserRepository)]):
		self.repo = repo
		self.ph = PasswordHasher()

	async def create(self, *, user_in: UserCreate):
		# TODO: check if we can add a bloom filterr here to avoid hitting the DB every time a new User is created
		existing_user = await self.repo.get_by_email(email=user_in.email)
		if existing_user:
			raise DuplicateUserException()

		hashed_password = self.ph.hash(user_in.password)
		return await self.repo.create_user(user_in=user_in, hashed_password=hashed_password)

	async def authenticate(self, *, email: str, password: str):
		user = await self.repo.get_by_email(email=email)
		if not user:
			raise CustomException(status.HTTP_404_NOT_FOUND, "Email doesn't exist.")
		
		try:
			if not self.ph.verify(user.hashed_password, password):
				raise CustomException(status.HTTP_401_UNAUTHORIZED, "Incorrect email or password.")
		except VerifyMismatchError:
			raise CustomException(status.HTTP_401_UNAUTHORIZED, "Incorrect password.")
		
		return user
