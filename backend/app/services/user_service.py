from app.db.connection import get_db, pool
from app.db.queries.loader import load_queries
from app.db.schemas.user import UserRead, UserCreate
from app.db.schemas.user import UserLogin
from app.core.security import token_generator, verify_password
from app.db.models.user import User

queries = load_queries()


async def list_users() -> list[UserRead]:
    async with pool.acquire() as conn:
        rows = await conn.fetch(queries["users"]["get_all_users"])
        return [UserRead(**row) for row in rows]



async def create_user(user: UserCreate) -> UserRead:
    async with pool.acquire() as conn:
        row = await conn.fetchrow(
            queries["users"]["create_user"], user.name, user.email
        )
        return UserRead(**row)

async def login_user(user:UserLogin):
    # process
    async for conn in get_db():
        get_user_password = await conn.fetchrow(
            queries["users"]["get_password_hash_by_email"], user.email
        )
        if not get_user_password:
            raise ValueError("Invalid email or password")
        user_obj = User(**get_user_password)
        if not  verify_password(user_obj.password_hash, user.password):
            raise ValueError("Invalid email or password")
        token = token_generator(user_obj.email)

        return token

    # post process
    # return
    