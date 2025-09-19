from sqlalchemy import Integer, String, ForeignKey, Index
from sqlalchemy.orm import Mapped, mapped_column

from src.domain.models.neon_models.base import IDOrmModel


class Image(IDOrmModel):
    """Image table, `local_id` - incoming from remote device"""
    __tablename__ = "image"

    local_id: Mapped[int] = mapped_column(Integer)
    name: Mapped[str] = mapped_column(String, nullable=False)
    recipe_local_id: Mapped[int] = mapped_column(Integer)
    user_id: Mapped[int] = mapped_column(Integer, ForeignKey("user.id"))

    __table_args__ = (
        Index('idx_user_updated', 'user_id', 'updated_at'),
        Index('idx_user_recipe_id', 'user_id', 'recipe_local_id'),
    )