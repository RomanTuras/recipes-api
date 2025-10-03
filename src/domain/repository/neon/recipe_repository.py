from typing import List
from datetime import datetime

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from src.core.app_exceptions import ResourceNotFoundException
from src.domain.models.neon_models.recipe import Recipe
from src.domain.models.neon_models.user import User
from src.domain.repository.neon.recipe_ingredient_link_repository import (
    RecipeIngredientLinkRepository,
)
from src.domain.schemas.neon.recipe import RecipeBase


class RecipeRepository:
    def __init__(self, session: AsyncSession):
        self.session = session
        self.recipe_ingredient_link_repository = RecipeIngredientLinkRepository(session)

    async def create_recipes(self, recipe_data: List[RecipeBase], user: User):
        """Creating user recipes from list"""
        recipes = []
        for item in recipe_data:
            data = item.model_dump(exclude_unset=True, exclude={"user_id"})
            data["user_id"] = user.id
            data["updated_at"] = datetime.now()
            recipes.append(Recipe(**data))
        self.session.add_all(recipes)
        return f"Inserted {len(recipe_data)} recipes"

    async def get_recipe(self, local_id: int, user: User) -> RecipeBase:
        """Getting user recipe by local_id"""
        query = (
            select(Recipe)
            .where(Recipe.local_id == local_id)
            .where(Recipe.user_id == user.id)
        )
        result = await self.session.execute(query)
        recipe = result.scalar_one_or_none()
        if recipe is None:
            raise ResourceNotFoundException(message="Recipe is not found")

        return RecipeBase.model_validate(recipe)

    async def get_changed_recipes(
        self, last_update: datetime, user: User
    ) -> List[RecipeBase]:
        """Getting user recipe, that was changed after last_update"""
        query = (
            select(Recipe)
            .where(Recipe.user_id == user.id)
            .where(Recipe.updated_at >= last_update)
        )
        result = await self.session.execute(query)
        recipes = result.scalars().all()

        return [RecipeBase.model_validate(recipe) for recipe in recipes]

    async def get_recipes_by_category(
        self, category_local_id: int, user: User
    ) -> List[RecipeBase]:
        """Getting user recipes by category"""
        query = (
            select(Recipe)
            .where(Recipe.category_local_id == category_local_id)
            .where(Recipe.user_id == user.id)
        )
        result = await self.session.execute(query)
        recipes = result.scalars().all()

        return [RecipeBase.model_validate(recipe) for recipe in recipes]

    async def create_recipe(self, recipe_data: RecipeBase, user: User) -> RecipeBase:
        """Creating user recipe"""
        recipe = Recipe(
            **recipe_data.model_dump(exclude_unset=True, exclude={"user_id"})
        )
        recipe.user_id = user.id
        recipe.updated_at = datetime.now()
        self.session.add(recipe)
        await self.session.commit()

        return RecipeBase.model_validate(recipe)

    async def update_recipe(self, recipe_data: RecipeBase, user: User) -> RecipeBase:
        """Updating user recipe by local_id"""
        recipe = await self.get_recipe(local_id=recipe_data.local_id, user=user)

        for field, value in recipe_data.model_dump(exclude_unset=True).items():
            setattr(recipe, field, value)
            recipe.updated_at = datetime.now()

        await self.session.commit()
        return RecipeBase.model_validate(recipe)

    async def delete_recipe(self, recipe_data: RecipeBase, user: User) -> RecipeBase:
        """Marking to delete user recipe by local_id"""
        recipe = await self.update_recipe(recipe_data=recipe_data, user=user)
        await self.recipe_ingredient_link_repository.delete_recipe_links(
            recipe_local_id=recipe.local_id, user_id=user.id
        )

        return RecipeBase.model_validate(recipe)
