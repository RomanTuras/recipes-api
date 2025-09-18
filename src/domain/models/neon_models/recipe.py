from typing import Optional
from sqlalchemy import String, Boolean, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column

from src.domain.models.neon_models.base import IDOrmModel


class Recipe(IDOrmModel):
    __tablename__ = "recipe"

    title: Mapped[str] = mapped_column(String(255), index=True)
    text: Mapped[Optional[str]] = mapped_column(String, nullable=True)
    image: Mapped[Optional[str]] = mapped_column(String, nullable=True)
    is_favorite: Mapped[bool] = mapped_column(Boolean, default=False)
    cook_it: Mapped[bool] = mapped_column(Boolean, default=False)

    category_id: Mapped[Optional[int]] = mapped_column(
        ForeignKey("category.id"), nullable=True
    )
    user_id: Mapped[Optional[int]] = mapped_column(ForeignKey("user.id"), nullable=True)
