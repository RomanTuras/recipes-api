# src/sqlite_models/table_main.py

from sqlalchemy import Column, String
from sqlalchemy.orm import Mapped, mapped_column

from src.domain.models.sqlite_models.base import MinimalBase


class TableMain(MinimalBase):
    """Old database main categories table"""

    __tablename__ = "tableMain"

    id: Mapped[int] = mapped_column(name="_id", primary_key=True)
    category = Column(String, nullable=False)
