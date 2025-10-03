from typing import List

from sqlalchemy.ext.asyncio import AsyncSession

from src.domain.models.neon_models.user import User
from src.domain.repository.neon.category_repository import CategoryRepository
from src.domain.schemas.neon.category import CategoryBase


class CategoryService:
    def __init__(self, db: AsyncSession):
        self.category_repository = CategoryRepository(db)

    async def create_category(self, body: CategoryBase, user: User) -> CategoryBase:
        return await self.category_repository.create_category(body, user=user)

    async def get_categories(self, user_id: int) -> List[CategoryBase]:
        return await self.category_repository.get_categories(user_id=user_id)

    async def get_categories_last_id(self) -> int:
        return await self.category_repository.get_categories_last_id()

    async def create_categories(self, body: List[CategoryBase], user: User):
        await self.category_repository.create_categories(body, user)
