from typing import List

from sqlalchemy.ext.asyncio import AsyncSession

from src.domain.neon_models import Recipe, User
from src.domain.schemas.neon.recipe import RecipeBase


class RecipeRepository:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def create_recipes(self, body: List[RecipeBase], user: User):
        """Creating recipes using transaction"""
        recipes = [
            Recipe(**item.model_dump(exclude_unset=True), user=user)
            for item in body
        ]
        self.session.add_all(recipes)
        return f"Inserted {len(body)} recipes"
