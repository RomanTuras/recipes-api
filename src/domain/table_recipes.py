# src/models/table_recipes.py

from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import declarative_base, Mapped, mapped_column

Base = declarative_base()

class TableRecipe(Base):
    """Old database table_recipes table"""

    __tablename__ = "tableRecipe"

    id: Mapped[int] = mapped_column(name="_id", primary_key=True)
    recipe_title = Column(String, nullable=False)
    recipe = Column(String, nullable=True)
    category_id = Column(Integer, nullable=True)
    make = Column(Integer, nullable=True)
    sub_category_id = Column(Integer, nullable=True)
    image = Column(String, nullable=True)

