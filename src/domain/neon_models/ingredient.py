from typing import Optional, List, TYPE_CHECKING
from sqlalchemy import String, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.domain.neon_models.base import IDOrmModel
from src.domain.neon_models.recipe_ingredient_link import RecipeIngredientLink

if TYPE_CHECKING:
    from src.domain.neon_models.recipe import Recipe
    from src.domain.neon_models.user import User


class Ingredient(IDOrmModel):
    __tablename__ = "ingredient"

    title: Mapped[str] = mapped_column(String(255), index=True)
    user_id: Mapped[Optional[int]] = mapped_column(ForeignKey("user.id"), nullable=True)

    # Relationships
    user: Mapped[Optional["User"]] = relationship(back_populates="ingredients")
    recipes: Mapped[List["Recipe"]] = relationship(
        secondary=RecipeIngredientLink.__table__, back_populates="ingredients"
    )