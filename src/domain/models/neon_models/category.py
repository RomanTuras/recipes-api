from typing import Optional

from src.domain.models.neon_models.base import IDOrmModel

from sqlalchemy import ForeignKey, String, Integer, Index
from sqlalchemy.orm import (
    Mapped,
    mapped_column,
)


class Category(IDOrmModel):
    """Category table, `local_id` - incoming from remote device"""

    __tablename__ = "category"

    local_id: Mapped[int] = mapped_column(Integer, index=True)
    title: Mapped[str] = mapped_column(String(255), nullable=False)
    parent_local_id: Mapped[Optional[int]] = mapped_column(Integer)
    user_id: Mapped[int] = mapped_column(Integer, ForeignKey("user.id"))

    __table_args__ = (Index("idx_category_user_updated", "user_id", "updated_at"),)
