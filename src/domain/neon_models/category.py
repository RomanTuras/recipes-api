from typing import Optional, List, TYPE_CHECKING
from sqlmodel import Field, SQLModel, Relationship

if TYPE_CHECKING:
    from src.domain.neon_models.recipe import Recipe
    from src.domain.neon_models.user import User


class Category(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    title: str = Field(index=True)
    parent_id: Optional[int] = Field(default=None, foreign_key="category.id")

    # foreign key to User (optional)
    user_id: Optional[int] = Field(default=None, foreign_key="user.id")

    # use string annotations so names are not evaluated at runtime
    recipes: List["Recipe"] = Relationship(back_populates="category")
    user: Optional["User"] = Relationship(back_populates="categories")
