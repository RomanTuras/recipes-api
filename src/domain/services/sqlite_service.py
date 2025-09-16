from typing import List

from sqlmodel.ext.asyncio.session import AsyncSession

from src.domain.repository.sqlite_repository import SqliteRepository
from src.domain.schemas.neon.category import CategoryBase
from src.domain.schemas.neon.recipe import RecipeBase


class SqliteService:
    def __init__(self, session: AsyncSession):
        self.sqlite_repository = SqliteRepository(session)

    async def get_sqlite_recipes(self, is_main_category: bool, sub_category_id_offset: int = 0) -> List[RecipeBase]:
        return await self.sqlite_repository.get_sqlite_recipes(is_main_category, sub_category_id_offset)

    async def get_top_categories(self) -> List[CategoryBase]:
        return await self.sqlite_repository.get_top_categories()

    async def get_sub_categories(self, sub_category_id_offset: int) -> List[CategoryBase]:
        return await self.sqlite_repository.get_sub_categories(sub_category_id_offset)
