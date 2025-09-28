from datetime import timedelta
from typing import Any

from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm

from app.api import dependencies
from app.core import security
from app.core.config import settings
from app.core.database import Database
from app.crud.user import user_crud
from app.schemas.token import Token
from app.schemas.user import User

router = APIRouter()


@router.post("/login", response_model=Token)
async def login_access_token(
    db: Database = Depends(dependencies.get_db),
    form_data: OAuth2PasswordRequestForm = Depends()
) -> Any:
    """
    OAuth2 compatible token login, get an access token for future requests
    """
    user = await user_crud.authenticate(
        db, email=form_data.username, password=form_data.password
    )
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password"
        )
    elif not user_crud.is_active(user):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Inactive user"
        )
    access_token_expires = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    refresh_token_expires = timedelta(minutes=settings.REFRESH_TOKEN_EXPIRE_MINUTES)
    
    return {
        "accessToken": security.create_access_token(
            user.id, expires_delta=access_token_expires
        ),
        "refreshToken": security.create_refresh_token(
            user.id, expires_delta=refresh_token_expires
        ),
        "tokenType": "bearer",
    }


@router.post("/refresh", response_model=Token)
async def refresh_token(
    current_user: User = Depends(dependencies.get_current_user)
) -> Any:
    access_token_expires = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    refresh_token_expires = timedelta(minutes=settings.REFRESH_TOKEN_EXPIRE_MINUTES)
    
    return {
        "accessToken": security.create_access_token(
            current_user.id, expires_delta=access_token_expires
        ),
        "refreshToken": security.create_refresh_token(
            current_user.id, expires_delta=refresh_token_expires
        ),
        "tokenType": "bearer",
    }


@router.get("/me", response_model=User)
async def read_users_me(
    current_user: User = Depends(dependencies.get_current_active_user),
) -> Any:
    return current_user
