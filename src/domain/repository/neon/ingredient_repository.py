from datetime import datetime
from typing import List

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from src.core.app_exceptions import ResourceNotFoundException
from src.domain.models.neon_models import Ingredient, User
from src.domain.schemas.neon.ingredient import IngredientBase


class IngredientRepository:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def create_ingredient(
        self, ingredient_data: IngredientBase, user: User
    ) -> IngredientBase:
        """Creating a new user ingredient"""
        ingredient = Ingredient(**ingredient_data.model_dump(exclude_unset=True))
        ingredient.updated_at = datetime.now()
        ingredient.user_id = user.id

        self.session.add(ingredient)
        await self.session.commit()

        return IngredientBase.model_validate(ingredient)

    async def get_changed_ingredients(
        self, last_update: datetime, user: User
    ) -> List[IngredientBase]:
        """Getting all user recipe ingredients, changed after last_update date"""
        query = (
            select(Ingredient)
            .where(Ingredient.updated_at > last_update)
            .where(Ingredient.user_id == user.id)
        )
        result = await self.session.execute(query)
        ingredients = result.scalars().all()

        return [IngredientBase.model_validate(ingredient) for ingredient in ingredients]

    async def get_ingredient(self, local_id: int, user: User) -> IngredientBase:
        """Getting a user ingredient by local_id"""
        query = (
            select(Ingredient)
            .where(Ingredient.local_id == local_id)
            .where(Ingredient.user_id == user.id)
        )
        result = await self.session.execute(query)
        ingredient = result.scalar_one_or_none()
        if ingredient is None:
            raise ResourceNotFoundException(message="Ingredient was not found")

        return IngredientBase.model_validate(ingredient)

    async def update_ingredient(
        self, ingredient_data: IngredientBase, user: User
    ) -> IngredientBase:
        """Updating a user ingredient"""
        try:
            ingredient = await self.get_ingredient(
                local_id=ingredient_data.local_id, user=user
            )
        except ResourceNotFoundException:
            raise ResourceNotFoundException(message="Ingredient was not found")

        for field, value in ingredient_data.model_dump(exclude_unset=True).items():
            setattr(ingredient, field, value)
            ingredient.updated_at = datetime.now()

        await self.session.commit()
        return IngredientBase.model_validate(ingredient)

    async def delete_ingredient(
        self, ingredient_data: IngredientBase, user: User
    ) -> IngredientBase:
        """Marking to delete certain user ingredient"""
        ingredient_data.is_delete = True
        return await self.update_ingredient(ingredient_data=ingredient_data, user=user)
