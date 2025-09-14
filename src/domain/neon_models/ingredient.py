from typing import Optional, List, TYPE_CHECKING
from sqlmodel import Field, SQLModel, Relationship
from src.domain.neon_models.recipe_ingredient_link import RecipeIngredientLink

if TYPE_CHECKING:
    from src.domain.neon_models.recipe import Recipe
    from src.domain.neon_models.user import User


class Ingredient(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    title: str = Field(index=True)
    user_id: Optional[int] = Field(default=None, foreign_key="user.id")

    user: Optional["User"] = Relationship(back_populates="ingredients")
    recipes: List["Recipe"] = Relationship(
        back_populates="ingredients", link_model=RecipeIngredientLink
    )
