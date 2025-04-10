# app/models/table_recipes.py

from sqlalchemy import Column, Integer, String, MetaData
from sqlalchemy.orm import declarative_base

Base = declarative_base()
metadata_ = MetaData()

class TableRecipe(Base):
    """Old database table_recipes table"""

    __tablename__ = "tableRecipe"

    _id = Column(Integer, primary_key=True, index=True)
    recipe_title = Column(String, nullable=False)
    recipe = Column(String, nullable=True)
    category_id = Column(Integer, nullable=True)
    make = Column(Integer, nullable=True)
    sub_category_id = Column(Integer, nullable=True)
    image = Column(String, nullable=True)

    metadata = metadata_
