# src/db/session.py
import contextlib

from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.ext.asyncio import (
    create_async_engine,
    async_sessionmaker,
    AsyncEngine,
    AsyncSession,
)

from src.core.config import get_settings


class DatabaseSessionManager:
    def __init__(self, url: str) -> None:
        self._url = url
        self._engine: AsyncEngine = create_async_engine(
            self._url, echo=False, future=True
        )
        self._session_maker: async_sessionmaker[AsyncSession] = async_sessionmaker(
            bind=self._engine, autoflush=False, autocommit=False, expire_on_commit=False
        )

    @contextlib.asynccontextmanager
    async def session(self):
        if self._session_maker is None:
            error = "Database session is not initialized"
            raise Exception(error)  # noqa: TRY002
        session = self._session_maker()
        try:
            yield session
        except SQLAlchemyError:
            await session.rollback()
            raise  # Re-raise the original error
        finally:
            await session.close()
            await self._engine.dispose()


async def get_db():
    settings = get_settings()
    sessionmanager = DatabaseSessionManager(settings.DATABASE_URI)
    async with sessionmanager.session() as session:
        yield session
