from contextlib import asynccontextmanager

from pygments.styles.dracula import yellow
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker
from sqlmodel import SQLModel
from sqlmodel.ext.asyncio.session import AsyncSession

from src.core.config import get_settings

from src.core.app_logger import logger


settings = get_settings()
connection_string = str(settings.DATABASE_URL).replace("postgres", "postgresql+asyncpg")

logger.info(
    f"--> The App is Started in {'local' if settings.IS_LOCAL_MODE else 'production'} mode!"
)

if settings.IS_LOCAL_MODE is False:
    connection_string = f"{connection_string}?ssl=require"

async_engine = create_async_engine(
    connection_string,
    pool_recycle=300,
    echo=True
)

AsyncDBSession = async_sessionmaker(async_engine, expire_on_commit=False, class_=AsyncSession)

async def create_db_and_tables():
    print("Creating tables...")
    async with async_engine.begin() as conn:
        await conn.run_sync(SQLModel.metadata.create_all)


@asynccontextmanager
async def lifespan(app):
    # await create_db_and_tables()
    yield


async def get_session():
    session = AsyncDBSession()
    try:
        yield session
    finally:
        await session.close()
    # async with AsyncDBSession() as session:
    #     yield session
