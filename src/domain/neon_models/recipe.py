from typing import Optional, List, TYPE_CHECKING
from sqlmodel import Field, SQLModel, Relationship
from src.domain.neon_models.recipe_ingredient_link import RecipeIngredientLink

if TYPE_CHECKING:
    from src.domain.neon_models.category import Category
    from src.domain.neon_models.ingredient import Ingredient
    from src.domain.neon_models.user import User


class Recipe(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    title: str = Field(index=True, nullable=False)
    text: str = Field(default=None, nullable=True)
    image: str = Field(default=None, nullable=True)
    is_favorite: bool = Field(default=False)
    cook_it: bool = Field(default=False)

    user_id: Optional[int] = Field(default=None, foreign_key="user.id")  # FK
    category_id: Optional[int] = Field(default=None, foreign_key="category.id")  # FK

    category: Optional["Category"] = Relationship(back_populates="recipes")
    user: Optional["User"] = Relationship(back_populates="recipes")
    ingredients: List["Ingredient"] = Relationship(
        back_populates="recipes", link_model=RecipeIngredientLink
    )
