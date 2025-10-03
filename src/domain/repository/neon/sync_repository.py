from typing import List

from sqlalchemy.ext.asyncio import AsyncSession

from src.core.app_exceptions import ResourceNotFoundException
from src.domain.models.neon_models import User
from src.domain.repository.neon.category_repository import CategoryRepository
from src.domain.repository.neon.ingredient_repository import (
    IngredientRepository,
)
from src.domain.repository.neon.recipe_ingredient_link_repository import (
    RecipeIngredientLinkRepository,
)
from src.domain.repository.neon.recipe_repository import RecipeRepository
from src.domain.schemas.neon.category import CategoryBase
from src.domain.schemas.neon.ingredient import IngredientBase
from src.domain.schemas.neon.recipe import RecipeBase
from src.domain.schemas.neon.recipe_ingredient_link import RecipeIngredientLinkBase


class SyncRepository:
    def __init__(self, session: AsyncSession):
        self.session = session
        self.category_repository = CategoryRepository(session)
        self.ingredient_repository = IngredientRepository(session)
        self.recipe_repository = RecipeRepository(session)
        self.recipe_ingredient_link_repository = RecipeIngredientLinkRepository(session)

    async def process_categories(
        self, categories: List[CategoryBase], user: User
    ) -> List[CategoryBase]:
        """Trying to update categories, if category is not exists - insert a new category"""
        processed_categories = []
        for category in categories:
            try:
                updated_category = await self.category_repository.update_category(
                    category_data=category, user=user
                )
                processed_categories.append(updated_category)
            except ResourceNotFoundException:
                inserted_category = await self.category_repository.create_category(
                    category_data=category, user=user
                )
                processed_categories.append(inserted_category)

        return processed_categories

    async def process_ingredients(
        self, ingredients: List[IngredientBase], user: User
    ) -> List[IngredientBase]:
        """Trying to update ingredients, if ingredient is not exists - insert a new ingredient"""
        processed_ingredients = []
        for ingredient in ingredients:
            try:
                updated_ingredient = await self.ingredient_repository.update_ingredient(
                    ingredient_data=ingredient, user=user
                )
                processed_ingredients.append(updated_ingredient)
            except ResourceNotFoundException:
                inserted_ingredient = (
                    await self.ingredient_repository.create_ingredient(
                        ingredient_data=ingredient, user=user
                    )
                )
                processed_ingredients.append(inserted_ingredient)

        return processed_ingredients

    async def process_recipes(
        self, recipes: List[RecipeBase], user: User
    ) -> List[RecipeBase]:
        """Trying to update recipes, if recipe is not exists - insert a new recipe"""
        processed_recipes = []
        for recipe in recipes:
            try:
                updated_recipe = await self.recipe_repository.update_recipe(
                    recipe_data=recipe, user=user
                )
                processed_recipes.append(updated_recipe)
            except ResourceNotFoundException:
                inserted_recipe = await self.recipe_repository.create_recipe(
                    recipe_data=recipe, user=user
                )
                processed_recipes.append(inserted_recipe)

        return processed_recipes

    async def process_recipe_ingredient_links(
        self, links: List[RecipeIngredientLinkBase], user: User
    ) -> List[RecipeIngredientLinkBase]:
        """Trying to update recipe->ingredient links, if link is not exists - insert a new link"""
        processed_links = []
        for link in links:
            try:
                updated_link = await self.recipe_ingredient_link_repository.update_link(
                    link_data=link
                )
                processed_links.append(updated_link)
                print(f"link {link.recipe_local_id}-{link.ingredient_local_id} was found - update")
            except ResourceNotFoundException:
                print(f"link {link.recipe_local_id}-{link.ingredient_local_id} NOT found - inserted")
                inserted_link = (
                    await self.recipe_ingredient_link_repository.create_link(
                        link_data=link
                    )
                )
                processed_links.append(inserted_link)

        return processed_links
