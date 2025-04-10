# app/models/table_main.py

from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import declarative_base

Base = declarative_base()


class TableMain(Base):
    """Old database main categories table"""

    __tablename__ = "tableMain"

    _id = Column(Integer, primary_key=True, index=True)
    category = Column(String, nullable=False)
