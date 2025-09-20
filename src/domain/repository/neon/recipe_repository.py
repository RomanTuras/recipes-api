from typing import List
from datetime import datetime

from sqlalchemy.ext.asyncio import AsyncSession

from src.domain.models.neon_models.recipe import Recipe
from src.domain.models.neon_models.user import User
from src.domain.schemas.neon.recipe import RecipeBase


class RecipeRepository:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def create_recipes(self, body: List[RecipeBase], user: User):
        """Creating recipes using transaction"""
        recipes = []
        for item in body:
            data = item.model_dump(exclude_unset=True, exclude={"user_id"})
            data["user_id"] = user.id
            data["updated_at"] = datetime.now()
            recipes.append(Recipe(**data))
        self.session.add_all(recipes)
        return f"Inserted {len(body)} recipes"
