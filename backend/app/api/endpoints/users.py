from typing import Any, List

from fastapi import APIRouter, Depends, HTTPException

from app.api import dependencies
from app.core.database import Database
from app.crud.user import user_crud
from app.models.user import User
from app.schemas.user import User as UserSchema, UserCreate, UserUpdate

router = APIRouter()


@router.get("/", response_model=List[UserSchema])
async def read_users(
    db: Database = Depends(dependencies.get_db),
    skip: int = 0,
    limit: int = 100,
    current_user: User = Depends(dependencies.get_current_active_superuser),
) -> Any:
    users = await user_crud.get_multi(db, skip=skip, limit=limit)
    return users


@router.post("/", response_model=UserSchema)
async def create_user(
    *,
    db: Database = Depends(dependencies.get_db),
    user_in: UserCreate,
    current_user: User = Depends(dependencies.get_current_active_superuser),
) -> Any:
    user = await user_crud.get_by_email(db, email=user_in.email)
    if user:
        raise HTTPException(
            status_code=400,
            detail="The user with this username already exists in the system.",
        )
    user = await user_crud.create(db, obj_in=user_in)
    return user


@router.put("/me", response_model=UserSchema)
async def update_user_me(
    *,
    db: Database = Depends(dependencies.get_db),
    password: str = None,
    full_name: str = None,
    email: str = None,
    current_user: User = Depends(dependencies.get_current_active_user),
) -> Any:
    update_data = {}
    if password is not None:
        update_data["password"] = password
    if full_name is not None:
        update_data["full_name"] = full_name
    if email is not None:
        update_data["email"] = email
    
    if not update_data:
        return current_user
    
    user = await user_crud.update(db, user_id=current_user.id, obj_in=update_data)
    return user


@router.get("/{user_id}", response_model=UserSchema)
async def read_user_by_id(
    user_id: int,
    current_user: User = Depends(dependencies.get_current_active_user),
    db: Database = Depends(dependencies.get_db),
) -> Any:
    user = await user_crud.get(db, id=user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    
    if user.id == current_user.id:
        return user
    if not user_crud.is_superuser(current_user):
        raise HTTPException(
            status_code=400, detail="The user doesn't have enough privileges"
        )
    return user


@router.put("/{user_id}", response_model=UserSchema)
async def update_user(
    *,
    db: Database = Depends(dependencies.get_db),
    user_id: int,
    user_in: UserUpdate,
    current_user: User = Depends(dependencies.get_current_active_superuser),
) -> Any:
    user = await user_crud.get(db, id=user_id)
    if not user:
        raise HTTPException(
            status_code=404,
            detail="The user with this username does not exist in the system",
        )
    user = await user_crud.update(db, user_id=user_id, obj_in=user_in)
    return user

