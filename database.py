from typing import AsyncGenerator

from sqlalchemy import URL
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncSession
from settings import settings

postgres_url = URL.create(
    'postgresql+asyncpg',
    username=settings.db_postgres.db_user,
    password=settings.db_postgres.db_password,
    host=settings.db_postgres.db_host,
    database=settings.db_postgres.database,
    port=settings.db_postgres.db_port
)

async_engine = create_async_engine(url=postgres_url, echo=True)
session_maker = async_sessionmaker(async_engine, expire_on_commit=False)


async def get_async_session() -> AsyncGenerator[AsyncSession, None]:
    async with session_maker() as session:
        yield session
# def get_session_local():
#     yield session_maker()
