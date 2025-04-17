# src/models/table_main.py

from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import declarative_base, Mapped, mapped_column

Base = declarative_base()


class TableMain(Base):
    """Old database main categories table"""

    __tablename__ = "tableMain"

    id: Mapped[int] = mapped_column(name="_id", primary_key=True)
    category = Column(String, nullable=False)
