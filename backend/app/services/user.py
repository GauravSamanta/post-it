import asyncpg
from argon2 import PasswordHasher

from app.core.exceptions import DuplicateUserException, UserNotFoundException
from app.repository.user import UserRepository
from app.schemas.user import UserCreate


class UserService:
	def __init__(self, conn: asyncpg.Connection):
		self.repo = UserRepository(conn)
		self.ph = PasswordHasher()

	async def create(self, *, user_in: UserCreate):
		existing_user = await self.repo.get_by_email(email=user_in.email)
		if existing_user:
			# Raise the custom exception instead of HTTPException
			raise DuplicateUserException()

		hashed_password = self.ph.hash(user_in.password)
		return await self.repo.create_user(user_in=user_in, hashed_password=hashed_password)

	async def get_by_email(self, *, email: str):
		"""Get user by email."""
		return await self.repo.get_by_email(email=email)

	async def authenticate(self, *, email: str, password: str):
		user = await self.repo.get_by_email(email=email)
		if not user:
			# You can also raise it here for authentication failures
			raise UserNotFoundException('Incorrect email or password.')
		if not self.ph.verify(user.hashed_password, password):
			raise UserNotFoundException('Incorrect email or password.')
		return user
