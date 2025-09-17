from typing import List, Optional, TYPE_CHECKING

from src.domain.neon_models.base import IDOrmModel

from sqlalchemy import ForeignKey, String, Integer
from sqlalchemy.orm import (
    Mapped,
    mapped_column,
    relationship,
)
if TYPE_CHECKING:
    from src.domain.neon_models import Recipe, User


class Category(IDOrmModel):
    __tablename__ = "category"

    local_id: Mapped[int] = mapped_column(Integer)
    title: Mapped[str] = mapped_column(String(255), nullable=False)
    parent_id: Mapped[Optional[int]] = mapped_column(ForeignKey("category.id"))

    # foreign key to User
    user_id: Mapped[Optional[int]] = mapped_column(ForeignKey("user.id"))

    recipes: Mapped[List["Recipe"]] = relationship(back_populates="category")
    user: Mapped[Optional["User"]] = relationship(back_populates="categories")
