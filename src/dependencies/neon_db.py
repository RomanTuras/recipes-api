from contextlib import asynccontextmanager
from typing import Any, AsyncGenerator

from sqlalchemy import NullPool
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncSession
from sqlalchemy.orm import declarative_base

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

# Base class for models
Base = declarative_base()

# Session factory
AsyncDBSession = async_sessionmaker(
    bind=async_engine,
    class_=AsyncSession,
    expire_on_commit=False,
)


async def create_db_and_tables():
    """Run migrations or create tables (use only for quick start / dev mode)."""
    async with async_engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)


@asynccontextmanager
async def lifespan(app):
    # await create_db_and_tables()
    yield


# Dependency for FastAPI
async def get_session() -> AsyncGenerator[AsyncSession | Any, Any]:
    async with AsyncDBSession() as session:
        try:
            yield session
        except SQLAlchemyError:
            await session.rollback()
            raise


# from contextlib import asynccontextmanager
#
# from sqlalchemy.exc import SQLAlchemyError
# from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker
# from sqlmodel import SQLModel
# from sqlmodel.ext.asyncio.session import AsyncSession
#
# from src.core.config import get_settings
#
# from src.core.app_logger import logger
#
#
# settings = get_settings()
# connection_string = str(settings.DATABASE_URL).replace("postgres", "postgresql+asyncpg")
#
# logger.info(
#     f"--> The App is Started in {'local' if settings.IS_LOCAL_MODE else 'production'} mode!"
# )
#
# if settings.IS_LOCAL_MODE is False:
#     connection_string = f"{connection_string}?ssl=require"
#
# async_engine = create_async_engine(connection_string, pool_recycle=300, echo=True)
#
# AsyncDBSession = async_sessionmaker(
#     async_engine, expire_on_commit=False, class_=AsyncSession
# )
#
#
# async def create_db_and_tables():
#     print("Creating tables...")
#     async with async_engine.begin() as conn:
#         await conn.run_sync(SQLModel.metadata.create_all)
#
#
# @asynccontextmanager
# async def lifespan(app):
#     # await create_db_and_tables()
#     yield
#
#
# async def get_session():
#     async with AsyncDBSession() as session:
#         yield session
