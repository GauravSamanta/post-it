from fastapi import APIRouter, Depends

from app.core.deps import get_current_user
from app.schemas.user import UserInDB, UserPublic

router = APIRouter()


@router.get('/me', response_model=UserPublic)
async def read_users_me(current_user: UserInDB = Depends(get_current_user)):
	"""
	Get current user details.
	"""
	return current_user
