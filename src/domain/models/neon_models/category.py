from typing import Optional

from src.domain.models.neon_models.base import IDOrmModel

from sqlalchemy import ForeignKey, String
from sqlalchemy.orm import (
    Mapped,
    mapped_column,
)


class Category(IDOrmModel):
    __tablename__ = "category"

    title: Mapped[str] = mapped_column(String(255), nullable=False)
    parent_id: Mapped[Optional[int]] = mapped_column(ForeignKey("category.id"))
    user_id: Mapped[Optional[int]] = mapped_column(ForeignKey("user.id"))
