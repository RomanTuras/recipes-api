from typing import Optional
from sqlalchemy import String, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column

from src.domain.models.neon_models.base import IDOrmModel


class Ingredient(IDOrmModel):
    __tablename__ = "ingredient"

    title: Mapped[str] = mapped_column(String(255), index=True)
    recipe_id: Mapped[Optional[int]] = mapped_column(
        ForeignKey("recipe.id"), nullable=True
    )
    user_id: Mapped[Optional[int]] = mapped_column(ForeignKey("user.id"), nullable=True)
