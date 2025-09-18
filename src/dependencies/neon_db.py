from contextlib import asynccontextmanager
from typing import Any, AsyncGenerator

from sqlalchemy import NullPool
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncSession

from src.core.config import get_settings
from src.core.app_logger import logger


settings = get_settings()
connection_string = str(settings.DATABASE_URL).replace("postgres", "postgresql+asyncpg")

logger.info(
    f"--> The App is Started in {'local' if settings.IS_LOCAL_MODE else 'production'} mode!"
)

if settings.IS_LOCAL_MODE is False:
    connection_string = f"{connection_string}?ssl=require"

# Create async engine
async_engine = create_async_engine(
    connection_string,
    echo=True,
    poolclass=NullPool,
)

# Session factory
AsyncDBSession = async_sessionmaker(
    bind=async_engine,
    class_=AsyncSession,
    expire_on_commit=False,
)


@asynccontextmanager
async def lifespan(app):
    # Lifecycle Scaffold:
    # Do something before starting the app (!once)
    yield
    # Do something before the app will shut down (!once)


# Dependency for FastAPI
async def get_session() -> AsyncGenerator[AsyncSession | Any, Any]:
    async with AsyncDBSession() as session:
        try:
            yield session
        except SQLAlchemyError:
            await session.rollback()
            raise
