from sqlalchemy import Integer, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column
from src.domain.models.neon_models.base import IDOrmModel


class RecipeIngredientLink(IDOrmModel):
    """RecipeIngredientLink table, `local_id` - incoming from remote device"""
    __tablename__ = "recipe_ingredient_link"

    recipe_local_id: Mapped[int] = mapped_column(Integer)
    ingredient_local_id: Mapped[int] = mapped_column(Integer)

    user_id: Mapped[int] = mapped_column(Integer, ForeignKey("user.id"))
