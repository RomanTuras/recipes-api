from sqlmodel.ext.asyncio.session import AsyncSession

from src.domain.repository.neon.user_repository import UserRepository


class UserService:
    def __init__(self, db: AsyncSession):
        self.user_repository = UserRepository(db)