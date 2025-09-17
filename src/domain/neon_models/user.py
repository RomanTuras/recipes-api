from typing import List, TYPE_CHECKING
from sqlalchemy import String, Boolean, func
from sqlalchemy.orm import Mapped, mapped_column, relationship
from datetime import datetime

from src.domain.neon_models.base import IDOrmModel

if TYPE_CHECKING:
    from src.domain.neon_models.category import Category
    from src.domain.neon_models.recipe import Recipe
    from src.domain.neon_models.ingredient import Ingredient


class User(IDOrmModel):
    __tablename__ = "user"

    username: Mapped[str] = mapped_column(String(100), unique=True)
    email: Mapped[str] = mapped_column(String(100), unique=True)
    hashed_password: Mapped[str] = mapped_column(String)
    confirmed: Mapped[bool] = mapped_column(Boolean, default=False)
    created_at: Mapped[datetime] = mapped_column(nullable=False, default=func.now())
    # created_at: Mapped[datetime] = mapped_column(
    #     DateTime(timezone=True), default_factory=lambda: datetime.now(timezone.utc)
    # )

    # Relationships
    categories: Mapped[List["Category"]] = relationship(back_populates="user")
    recipes: Mapped[List["Recipe"]] = relationship(back_populates="user")
    ingredients: Mapped[List["Ingredient"]] = relationship(back_populates="user")