from typing import AsyncGenerator

import asyncpg
from fastapi.security import OAuth2PasswordBearer

from app.core.config import settings
from app.core.database import get_pool

oauth2_scheme = OAuth2PasswordBearer(tokenUrl=f'{settings.API_V1_STR}/auth/login')


# @asynccontextmanager
async def get_db_connection() -> AsyncGenerator[asyncpg.Connection, None]:
	"""Dependency to get a database connection from the pool."""
	pool = get_pool()
	try:
		async with pool.acquire() as connection:
			yield connection
	finally:
		print('Releasing connection back to pool')
		await pool.release(connection)


# async def get_current_user(
# 	user_service: Annotated[UserService, Depends(UserService)],
# 	token: str = Depends(oauth2_scheme),
# ) -> UserInDB:
# 	credentials_exception = HTTPException(
# 		status_code=status.HTTP_401_UNAUTHORIZED,
# 		detail='Could not validate credentials',
# 		headers={'WWW-Authenticate': 'Bearer'},
# 	)
# 	try:
# 		payload = jwt.decode(token, settings.JWT_SECRET, algorithms=['HS256'])
# 		email: str = payload.get('sub')
# 		if email is None:
# 			raise credentials_exception
# 		token_data = TokenData(email=email)
# 	except ValidationError:
# 		raise credentials_exception

# 	user = await user_service.get_by_email(email=token_data.email)
# 	if user is None:
# 		raise credentials_exception
# 	return user
