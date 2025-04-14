# app/models/table_sub_cat.py

from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import declarative_base, Mapped, mapped_column

from domain.base import IDOrmModel

Base = declarative_base()


class TableSubCat(Base):
    """Old database subcategories table"""

    __tablename__ = "tableSubCat"

    # _id = Column(Integer, primary_key=True, index=True)
    id: Mapped[int] = mapped_column(name="_id", primary_key=True)
    name = Column(String, nullable=False)
    hierarchy = Column(Integer, nullable=True)
    parent_id = Column(Integer, nullable=True)
