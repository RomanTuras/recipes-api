from typing import Optional, List, TYPE_CHECKING

from sqlalchemy import Column, DateTime
from sqlmodel import Field, SQLModel, Relationship
from datetime import datetime, timezone

if TYPE_CHECKING:
    from src.domain.neon_models.category import Category
    from src.domain.neon_models.recipe import Recipe
    from src.domain.neon_models.ingredient import Ingredient


class User(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    username: str = Field(nullable=False)
    email: str = Field(nullable=False, unique=True)
    hashed_password: str = Field(nullable=False)
    confirmed: bool = Field(default=False)
    created_at: datetime = Field(
        default_factory=lambda: datetime.now(timezone.utc),
        sa_column=Column(DateTime(timezone=True)),
    )

    # relations
    categories: List["Category"] = Relationship(back_populates="user")  # one-to-many
    recipes: List["Recipe"] = Relationship(back_populates="user")  # one-to-many
    ingredients: List["Ingredient"] = Relationship(back_populates="user")  # one-to-many
