from sqlalchemy import Integer, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column
from src.domain.models.neon_models.base import MinimalBase


class RecipeIngredientLink(MinimalBase):
    __tablename__ = "recipe_ingredient_link"

    recipe_id: Mapped[int] = mapped_column(
        Integer, ForeignKey("recipe.id"), primary_key=True
    )
    ingredient_id: Mapped[int] = mapped_column(
        Integer, ForeignKey("ingredient.id"), primary_key=True
    )
