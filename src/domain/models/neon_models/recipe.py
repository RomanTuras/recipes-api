from typing import Optional
from sqlalchemy import String, Boolean, ForeignKey, Integer
from sqlalchemy.orm import Mapped, mapped_column

from src.domain.models.neon_models.base import IDOrmModel


class Recipe(IDOrmModel):
    """Recipe table, `local_id` - incoming from remote device"""
    __tablename__ = "recipe"

    local_id: Mapped[int] = mapped_column(Integer)
    title: Mapped[str] = mapped_column(String(255), index=True)
    text: Mapped[Optional[str]] = mapped_column(String, nullable=True)
    image: Mapped[Optional[str]] = mapped_column(String, nullable=True)
    is_favorite: Mapped[bool] = mapped_column(Boolean, default=False)
    cook_it: Mapped[bool] = mapped_column(Boolean, default=False)

    category_local_id: Mapped[Optional[int]] = mapped_column(Integer)
    user_id: Mapped[int] = mapped_column(Integer, ForeignKey("user.id"))
