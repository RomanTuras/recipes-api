from typing import Optional

from sqlalchemy import String, Boolean, func, DateTime
from sqlalchemy.orm import Mapped, mapped_column
from datetime import datetime

from src.domain.models.neon_models.base import IDOrmModel


class User(IDOrmModel):
    """User table"""
    __tablename__ = "user"

    username: Mapped[str] = mapped_column(String(100), unique=True, index=True)
    email: Mapped[str] = mapped_column(String(100), unique=True, index=True)
    hashed_password: Mapped[str] = mapped_column(String)
    confirmed: Mapped[bool] = mapped_column(Boolean, default=False)
    created_at: Mapped[datetime] = mapped_column(nullable=False, default=func.now())
    last_activity: Mapped[Optional[datetime]] = mapped_column(DateTime)
