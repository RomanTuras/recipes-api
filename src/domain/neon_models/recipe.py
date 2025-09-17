from typing import Optional, List, TYPE_CHECKING
from sqlalchemy import String, Boolean, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.domain.neon_models import Category
from src.domain.neon_models.base import IDOrmModel
from src.domain.neon_models.recipe_ingredient_link import RecipeIngredientLink  # Ensure this link model is defined

if TYPE_CHECKING:
    from src.domain.neon_models.ingredient import Ingredient
    from src.domain.neon_models.user import User


class Recipe(IDOrmModel):
    __tablename__ = "recipe"

    title: Mapped[str] = mapped_column(String(255), index=True)
    text: Mapped[Optional[str]] = mapped_column(String, nullable=True)
    image: Mapped[Optional[str]] = mapped_column(String, nullable=True)
    is_favorite: Mapped[bool] = mapped_column(Boolean, default=False)
    cook_it: Mapped[bool] = mapped_column(Boolean, default=False)

    user_id: Mapped[Optional[int]] = mapped_column(ForeignKey("user.id"), nullable=True)
    category_id: Mapped[Optional[int]] = mapped_column(ForeignKey("category.id"), nullable=True)

    # Relationships
    category: Mapped[Optional["Category"]] = relationship(back_populates="recipes")
    user: Mapped[Optional["User"]] = relationship(back_populates="recipes")
    ingredients: Mapped[List["Ingredient"]] = relationship(
        secondary=RecipeIngredientLink.__table__, back_populates="recipes"
    )
