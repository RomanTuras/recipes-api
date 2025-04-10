# app/models/table_sub_cat.py

from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import declarative_base

Base = declarative_base()


class TableSubCat(Base):
    """Old database subcategories table"""

    __tablename__ = "tableSubCat"

    _id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    hierarchy = Column(Integer, nullable=True)
    parent_id = Column(Integer, nullable=True)
