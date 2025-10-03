from typing import List

from pydantic import BaseModel, Field

from src.domain.schemas.neon.category import CategoryBase
from src.domain.schemas.neon.ingredient import IngredientBase
from src.domain.schemas.neon.recipe import RecipeBase
from src.domain.schemas.neon.recipe_ingredient_link import RecipeIngredientLinkBase


# OperationType = Literal["create", "update", "delete"]
#
#
# class IngredientChange(BaseModel):
#     operation: OperationType
#     ingredient: IngredientBase
#
#
# class CategoryChange(BaseModel):
#     operation: OperationType
#     category: CategoryBase
#
#
# class RecipeChange(BaseModel):
#     operation: OperationType
#     recipe: RecipeBase
#
#
# class SyncPayload(BaseModel):
#     ingredients: List[IngredientChange] = Field(default_factory=list)
#     categories: List[CategoryChange] = Field(default_factory=list)
#     recipes: List[RecipeChange] = Field(default_factory=list)


class SyncPayload(BaseModel):
    ingredients: List[IngredientBase] = Field(default_factory=list)
    categories: List[CategoryBase] = Field(default_factory=list)
    recipes: List[RecipeBase] = Field(default_factory=list)
    recipe_ingredients_links: List[RecipeIngredientLinkBase] = Field(
        default_factory=list
    )
