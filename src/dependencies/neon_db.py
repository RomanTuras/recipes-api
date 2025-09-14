from contextlib import asynccontextmanager

from sqlalchemy.ext.asyncio import create_async_engine
from sqlmodel import SQLModel
from sqlmodel.ext.asyncio.session import AsyncSession

from src.core.config import get_settings


settings = get_settings()
connection_string = str(settings.DATABASE_URL).replace("postgres", "postgresql+asyncpg")


async_engine = create_async_engine(connection_string, pool_recycle=300)


async def create_db_and_tables():
    print("Creating tables...")
    async with async_engine.begin() as conn:
        await conn.run_sync(SQLModel.metadata.create_all)


@asynccontextmanager
async def lifespan(app):
    # await create_db_and_tables()
    yield


async def get_session():
    async with AsyncSession(async_engine) as session:
        yield session
