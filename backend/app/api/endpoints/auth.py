from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm

from app.core.security import create_jwt
from app.schemas.token import Token
from app.schemas.user import UserCreate
from app.services.user import UserService

router = APIRouter()


@router.post('/login', response_model=Token)
async def login_for_access_token(
	form_data: OAuth2PasswordRequestForm = Depends(),
	user_service: Annotated[UserService, Depends(UserService)] = None,
):
	user = await user_service.authenticate(email=form_data.username, password=form_data.password)

	access_token = create_jwt(data={'sub': user.email})
	return {'access_token': access_token, 'token_type': 'bearer'}


@router.post('/register', status_code=status.HTTP_201_CREATED)
async def register_user(
	form_data: UserCreate,
	user_service: Annotated[UserService, Depends(UserService)] = None,
):
	try:
		await user_service.create(user_in=form_data)
	except Exception as e:
		raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))
	return {'msg': 'User created successfully'}
