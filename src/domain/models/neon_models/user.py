from sqlalchemy import String, Boolean, func
from sqlalchemy.orm import Mapped, mapped_column
from datetime import datetime

from src.domain.models.neon_models.base import IDOrmModel


class User(IDOrmModel):
    __tablename__ = "user"

    username: Mapped[str] = mapped_column(String(100), unique=True)
    email: Mapped[str] = mapped_column(String(100), unique=True)
    hashed_password: Mapped[str] = mapped_column(String)
    confirmed: Mapped[bool] = mapped_column(Boolean, default=False)
    created_at: Mapped[datetime] = mapped_column(nullable=False, default=func.now())
