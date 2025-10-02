import traceback
from contextlib import asynccontextmanager

from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse

from app.api import router as api_router
from app.core.config import settings
from app.core.database import close_db_connection, connect_to_db, init_db
from app.core.exceptions import CustomException
from app.core.logging import log, setup_logging


@asynccontextmanager
async def lifespan(app: FastAPI):
	# On startup
	setup_logging()  # Set up logging
	log.info('Application startup...')
	await connect_to_db()
	await init_db()  # Ensure DB schema is initialized
	yield
	# On shutdown
	log.info('Application shutdown...')
	await close_db_connection()

	log.info('Database connection closed.')


app = FastAPI(title=settings.PROJECT_NAME, lifespan=lifespan)
# ...


@app.exception_handler(Exception)
async def generic_exception_handler(request: Request, exc: Exception):
	# Log the full traceback for unexpected errors
	log.error(f'Unhandled exception: {exc}\n{traceback.format_exc()}')
	return JSONResponse(
		status_code=500,
		content={'detail': 'An internal server error occurred.'},
	)


# Custom Exception Handler
@app.exception_handler(CustomException)
async def custom_exception_handler(request: Request, exc: CustomException):
	return JSONResponse(
		status_code=exc.status_code,
		content={'detail': exc.detail},
	)


app.include_router(api_router.router, prefix=settings.API_V1_STR)
