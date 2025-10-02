from fastapi import APIRouter, Depends

from app.schemas.user import UserInDB, UserPublic

router = APIRouter()


@router.get('/me', response_model=UserPublic)
async def read_users_me():
	"""
	Get current user details.
	"""
	return 'ok'
