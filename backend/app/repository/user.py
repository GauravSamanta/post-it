import asyncpg
from typing import Annotated
from fastapi import Depends

from app.schemas.user import UserCreate, UserInDB
from app.core.deps import get_db_connection


class UserRepository:
	def __init__(self, conn: Annotated[asyncpg.Connection, Depends(get_db_connection)]):
		self.conn = conn

	async def get_by_email(self, *, email: str) -> UserInDB | None:
		query = 'SELECT id, email, full_name, hashed_password FROM users WHERE email = $1'
		row = await self.conn.fetchrow(query, email)
		return UserInDB(**row) if row else None

	async def create_user(self, *, user_in: UserCreate, hashed_password: str) -> UserInDB:
		query = """
            INSERT INTO users (email, full_name, hashed_password)
            VALUES ($1, $2, $3)
            RETURNING id, email, full_name, hashed_password
        """
		row = await self.conn.fetchrow(query, user_in.email, user_in.full_name, hashed_password)
		return UserInDB(**row)
