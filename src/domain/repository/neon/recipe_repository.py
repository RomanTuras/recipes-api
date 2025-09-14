from typing import List

from sqlmodel.ext.asyncio.session import AsyncSession

from src.domain.neon_models import User, Recipe
from src.domain.schemas.neon.recipe import RecipeBase


class RecipeRepository:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def create_recipes(self, body: List[RecipeBase], user: User):
        for item in body:
            recipe = Recipe(**item.model_dump(exclude_unset=True), user=user)
            self.session.add(recipe)

        await self.session.commit()
        return f"Inserted {len(body)} recipes"
