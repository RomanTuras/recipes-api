from typing import List

from sqlmodel.ext.asyncio.session import AsyncSession

from src.domain.neon_models import User, Category
from src.domain.repository.neon.category_repository import CategoryRepository
from src.domain.schemas.neon.category import CategoryBase, CategoryResponse


class CategoryService:
    def __init__(self, db: AsyncSession):
        self.category_repository = CategoryRepository(db)

    async def create_category(self, body: CategoryBase, user: User) -> Category:
        return await self.category_repository.create_category(body, user=user)

    async def get_user_categories(self, user_id: int) -> List[CategoryResponse]:
        return await self.category_repository.get_user_categories(user_id=user_id)
