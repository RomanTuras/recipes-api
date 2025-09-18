# app/sqlite_models/table_sub_cat.py

from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import Mapped, mapped_column

from src.domain.models.sqlite_models.base import MinimalBase


class TableSubCat(MinimalBase):
    """Old database subcategories table"""

    __tablename__ = "tableSubCat"

    id: Mapped[int] = mapped_column(name="_id", primary_key=True)
    name = Column(String, nullable=False)
    hierarchy = Column(Integer, nullable=True)
    parent_id = Column(Integer, nullable=True)
