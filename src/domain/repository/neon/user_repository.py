from typing import List

from sqlalchemy.ext.asyncio import AsyncSession
from sqlmodel import select

from src.domain.neon_models import User, Category
from src.domain.schemas.neon.category import CategoryResponse


class UserRepository:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def get_user_by_id(self, user_id: int) -> User | None:
        query = select(User).where(User.id == user_id)
        user = await self.session.execute(query)
        return user.scalar_one_or_none()
