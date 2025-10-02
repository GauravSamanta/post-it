import asyncpg

from app.core.config import settings

# Global variable to hold the connection pool
pool: asyncpg.Pool = None


async def connect_to_db():
	"""Connects to the database and initializes the connection pool."""
	global pool
	pool = await asyncpg.create_pool(dsn=settings.DATABASE_URL)
	print('Database connection pool created.')


async def close_db_connection():
	"""Closes the database connection pool."""
	global pool
	if pool:
		await pool.close()
		print('Database connection pool closed.')


def get_pool():
	"""A dependency-like function to get the pool."""
	return pool


async def init_db():
	"""Initializes the database schema."""
	global pool
	if pool is None:
		raise Exception('Database pool is not initialized. Call connect_to_db first.')

	async with pool.acquire() as connection:
		with open('app/models/schema.sql', 'r') as f:
			schema_sql = f.read()
		await connection.execute(schema_sql)
		print('Database schema initialized.')
