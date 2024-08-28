from sqlalchemy import URL
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker
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
async_session = async_sessionmaker(async_engine, expire_on_commit=False)
