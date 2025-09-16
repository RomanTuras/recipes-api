from typing import List
from sqlmodel import select
from sqlmodel.ext.asyncio.session import AsyncSession
from src.domain.schemas.neon.category import CategoryBase
from src.domain.schemas.neon.recipe import RecipeBase
from src.domain.sqlite_models.table_main import TableMain
from src.domain.sqlite_models.table_recipes import TableRecipe
from src.domain.sqlite_models.table_sub_cat import TableSubCat


class SqliteRepository:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def get_sqlite_recipes(self, is_main_category: bool, sub_category_id_offset: int = 0) -> List[RecipeBase]:
        query = select(TableRecipe).where(
            TableRecipe.category_id > 0 if is_main_category else TableRecipe.sub_category_id > 0)
        result = await self.session.exec(query)
        rows = result.all()

        print(
            f"Found {len(rows)} recipes in {'main' if is_main_category else 'sub'} categories"
        )

        recipes: List[RecipeBase] = []
        for row in rows:
            recipes.append(
                RecipeBase(
                    id=row.id,
                    title=row.recipe_title.strip(),
                    text=row.recipe,
                    image=row.image,
                    is_favorite=True if row.make == 1 else False,
                    category_id=row.category_id
                    if is_main_category
                    else row.sub_category_id + sub_category_id_offset,
                    user_id=1,
                )
            )

        return recipes

    async def get_top_categories(self) -> List[CategoryBase]:
        result = await self.session.exec(select(TableMain))
        rows = result.all()

        print(f"Found {len(rows)} categories in sqlite")

        categories: List[CategoryBase] = []
        for row in rows:
            categories.append(
                CategoryBase(
                    id=row.id,
                    title=row.category.strip(),
                    parent_id=None,
                    user_id=1,
                )
            )

        return categories

    async def get_sub_categories(self, sub_category_id_offset: int) -> List[CategoryBase]:
        result = await self.session.exec(select(TableSubCat))
        rows = result.all()

        print(f"Found {len(rows)} subcategories in sqlite")

        categories: List[CategoryBase] = []
        for row in rows:
            categories.append(
                CategoryBase(
                    id=row.id + sub_category_id_offset,
                    title=row.name.strip(),
                    parent_id=row.parent_id,
                    user_id=1,
                )
            )

        return categories