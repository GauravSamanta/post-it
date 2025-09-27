from typing import Any, List

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.api import dependencies
from app.crud.user import user_crud
from app.models.user import User
from app.schemas.user import User as UserSchema, UserCreate, UserUpdate

router = APIRouter()


@router.get("/", response_model=List[UserSchema])
def read_users(
    db: Session = Depends(dependencies.get_db),
    skip: int = 0,
    limit: int = 100,
    current_user: User = Depends(dependencies.get_current_active_superuser),
) -> Any:
    """
    Retrieve users.
    """
    users = user_crud.get_multi(db, skip=skip, limit=limit)
    return users


@router.post("/", response_model=UserSchema)
def create_user(
    *,
    db: Session = Depends(dependencies.get_db),
    user_in: UserCreate,
    current_user: User = Depends(dependencies.get_current_active_superuser),
) -> Any:
    """
    Create new user.
    """
    user = user_crud.get_by_email(db, email=user_in.email)
    if user:
        raise HTTPException(
            status_code=400,
            detail="The user with this username already exists in the system.",
        )
    user = user_crud.create(db, obj_in=user_in)
    return user


@router.put("/me", response_model=UserSchema)
def update_user_me(
    *,
    db: Session = Depends(dependencies.get_db),
    password: str = None,
    full_name: str = None,
    email: str = None,
    current_user: User = Depends(dependencies.get_current_active_user),
) -> Any:
    """
    Update own user.
    """
    current_user_data = UserUpdate(**current_user.__dict__)
    if password is not None:
        current_user_data.password = password
    if full_name is not None:
        current_user_data.full_name = full_name
    if email is not None:
        current_user_data.email = email
    user = user_crud.update(db, db_obj=current_user, obj_in=current_user_data)
    return user


@router.get("/{user_id}", response_model=UserSchema)
def read_user_by_id(
    user_id: int,
    current_user: User = Depends(dependencies.get_current_active_user),
    db: Session = Depends(dependencies.get_db),
) -> Any:
    """
    Get a specific user by id.
    """
    user = user_crud.get(db, id=user_id)
    if user == current_user:
        return user
    if not user_crud.is_superuser(current_user):
        raise HTTPException(
            status_code=400, detail="The user doesn't have enough privileges"
        )
    return user


@router.put("/{user_id}", response_model=UserSchema)
def update_user(
    *,
    db: Session = Depends(dependencies.get_db),
    user_id: int,
    user_in: UserUpdate,
    current_user: User = Depends(dependencies.get_current_active_superuser),
) -> Any:
    """
    Update a user.
    """
    user = user_crud.get(db, id=user_id)
    if not user:
        raise HTTPException(
            status_code=404,
            detail="The user with this username does not exist in the system",
        )
    user = user_crud.update(db, db_obj=user, obj_in=user_in)
    return user

