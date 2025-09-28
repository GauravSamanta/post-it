from typing import Any, Dict, List, Optional, Union

from app.core.database import Database
from app.core.security import get_password_hash, verify_password
from app.models.user import User
from app.schemas.user import UserCreate, UserUpdate


class CRUDUser:
    def __init__(self):
        pass

    async def get_by_email(self, db: Database, *, email: str) -> Optional[User]:
        query = "SELECT * FROM users WHERE email = $1"
        record = await db.fetchrow(query, email)
        return User.from_record(record)

    async def get(self, db: Database, *, id: int) -> Optional[User]:
        query = "SELECT * FROM users WHERE id = $1"
        record = await db.fetchrow(query, id)
        return User.from_record(record)

    async def get_multi(
        self, db: Database, *, skip: int = 0, limit: int = 100
    ) -> List[User]:
        query = "SELECT * FROM users OFFSET $1 LIMIT $2"
        records = await db.fetch(query, skip, limit)
        return [User.from_record(record) for record in records]

    async def create(self, db: Database, *, obj_in: UserCreate) -> User:
        hashed_password = get_password_hash(obj_in.password)
        query = """
            INSERT INTO users (email, hashed_password, full_name, is_superuser, is_active)
            VALUES ($1, $2, $3, $4, $5)
            RETURNING *
        """
        record = await db.fetchrow(
            query,
            obj_in.email,
            hashed_password,
            obj_in.full_name,
            obj_in.is_superuser,
            True,
        )
        return User.from_record(record)

    async def update(
        self, db: Database, *, user_id: int, obj_in: Union[UserUpdate, Dict[str, Any]]
    ) -> Optional[User]:
        if isinstance(obj_in, dict):
            update_data = obj_in
        else:
            update_data = obj_in.dict(exclude_unset=True)

        if update_data.get("password"):
            update_data["hashed_password"] = get_password_hash(update_data["password"])
            del update_data["password"]

        set_clauses = []
        values = []
        param_count = 1

        for field, value in update_data.items():
            if field in [
                "email",
                "hashed_password",
                "full_name",
                "is_active",
                "is_superuser",
            ]:
                set_clauses.append(f"{field} = ${param_count}")
                values.append(value)
                param_count += 1

        if not set_clauses:
            return await self.get(db, id=user_id)

        set_clauses.append(f"updated_at = NOW()")
        query = f"""
            UPDATE users 
            SET {', '.join(set_clauses)}
            WHERE id = ${param_count}
            RETURNING *
        """
        values.append(user_id)

        record = await db.fetchrow(query, *values)
        return User.from_record(record)

    async def delete(self, db: Database, *, id: int) -> Optional[User]:
        query = "DELETE FROM users WHERE id = $1 RETURNING *"
        record = await db.fetchrow(query, id)
        return User.from_record(record)

    async def authenticate(
        self, db: Database, *, email: str, password: str
    ) -> Optional[User]:
        user = await self.get_by_email(db, email=email)
        if not user:
            return None
        if not verify_password(password, user.hashed_password):
            return None
        return user

    def is_active(self, user: User) -> bool:
        return user.is_active

    def is_superuser(self, user: User) -> bool:
        return user.is_superuser


user_crud = CRUDUser()
