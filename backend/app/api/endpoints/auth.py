from fastapi import APIRouter, Depends, HTTPException, logger
from argon2 import PasswordHasher
from app.api.deps import get_db  # must yield a single asyncpg connection
from app.core.security import token_generator
from app.db.queries.loader import load_queries
from app.db.schemas.user import UserLogin, UserRead, UserCreate
from app.core.security import verify_password, hash_password
from app.core.logging import logger
from app.db.models.user import User
from app.services.user_service import login_user

router = APIRouter()
queries = load_queries()


@router.post("/login")
async def login(user: UserLogin):

    token=await login_user(user)

    return {"access_token": token, "token_type": "bearer"}



@router.post("/register", response_model=UserRead)
async def register(user: UserCreate, conn=Depends(get_db)):
    # Check if email already exists
    existing = await conn.fetchrow(queries["users"]["get_user_by_email"], user.email)
    if existing:
        raise HTTPException(status_code=400, detail="Email already registered")

    # Hash password
    hashed_pw = await hash_password(user.password)

    # Insert new user
    row = await conn.fetchrow(
        queries["users"]["create_user"], user.username, user.email, hashed_pw
    )
    return UserRead(**row)


@router.post("/logout")
async def logout():
    return {"message": "Logout endpoint"}
