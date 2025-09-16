from typing import List

from sqlmodel.ext.asyncio.session import AsyncSession

from src.domain.neon_models import Recipe
from src.domain.schemas.neon.recipe import RecipeBase
from src.domain.schemas.neon.user import UserResponse


class RecipeRepository:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def create_recipes(self, body: List[RecipeBase], user: UserResponse):
        """Creating recipes using transaction"""
        try:
            async with self.session.begin():
                for item in body:
                    recipe = Recipe(**item.model_dump(exclude_unset=True), user=user)
                    self.session.add(recipe)
                return f"Inserted {len(body)} recipes"
        except Exception as e:
            await self.session.rollback()
            return f"Transaction failed, rolled back. Error: {e}"
