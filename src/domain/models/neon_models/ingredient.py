from sqlalchemy import String, ForeignKey, Integer, Index
from sqlalchemy.orm import Mapped, mapped_column

from src.domain.models.neon_models.base import IDOrmModel


class Ingredient(IDOrmModel):
    """Ingredient table, `local_id` - incoming from remote device"""

    __tablename__ = "ingredient"

    local_id: Mapped[int] = mapped_column(Integer)
    title: Mapped[str] = mapped_column(String(255))
    user_id: Mapped[int] = mapped_column(Integer, ForeignKey("user.id"))

    __table_args__ = (Index("idx_ingredient_user_updated", "user_id", "updated_at"),)
