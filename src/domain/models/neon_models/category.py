from typing import Optional

from src.domain.models.neon_models.base import IDOrmModel

from sqlalchemy import ForeignKey, String, Integer
from sqlalchemy.orm import (
    Mapped,
    mapped_column,
)


class Category(IDOrmModel):
    """Category table, `local_id` - incoming from remote device"""
    __tablename__ = "category"

    local_id: Mapped[int] = mapped_column(Integer)
    title: Mapped[str] = mapped_column(String(255), nullable=False, index=True)
    parent_local_id: Mapped[Optional[int]] = mapped_column(Integer)
    user_id: Mapped[int] = mapped_column(Integer, ForeignKey("user.id"))
