# app/core/config.py
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
	model_config = SettingsConfigDict(env_file='.env', env_file_encoding='utf-8')
	DATABASE_URL: str
	JWT_SECRET: str
	JWT_ALGORITHM: str = 'HS256'
	PROJECT_NAME: str = 'My Awesome Project'
	API_V1_STR: str = '/api/v1'
	PORT: int


settings = Settings()
