from pydantic import BaseModel, ConfigDict
from typing import Optional


class RecipeBase(BaseModel):
    id: Optional[int] = None
    title: str
    text: Optional[str] = None
    image: Optional[str] = None
    is_favorite: bool = False
    cook_it: bool = False
    user_id: Optional[int] = None
    category_id: Optional[int] = None

    # allows to create RecipeBase directly from Recipe ORM model, expl: RecipeBase.model_validate(Recipe)
    model_config = ConfigDict(from_attributes=True)
