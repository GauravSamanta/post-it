import asyncpg

from app.core.config import settings

# Global variable to hold the connection pool
pool: asyncpg.Pool = None


async def connect_to_db():
	global pool
	pool = await asyncpg.create_pool(dsn=settings.DATABASE_URL)
	print('Database connection pool created.')


async def close_db_connection():
	global pool
	if pool:
		await pool.close()
		print('Database connection pool closed.')


def get_pool():
	return pool


async def init_db():
	global pool
	if pool is None:
		raise Exception('Database pool is not initialized. Call connect_to_db first.')

	async with pool.acquire() as connection:
		with open('app/models/schema.sql', 'r') as f:
			schema_sql = f.read()
		await connection.execute(schema_sql)
		print('Database schema initialized.')
