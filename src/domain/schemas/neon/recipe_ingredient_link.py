from datetime import datetime
from typing import Optional

from pydantic import BaseModel, ConfigDict


class RecipeIngredientLinkBase(BaseModel):
    id: Optional[int] = None
    ingredient_local_id: int
    recipe_local_id: int
    user_id: int
    updated_at: Optional[datetime] = None
    is_delete: Optional[bool] = False

    # allows to create RecipeBase directly from Recipe ORM model, expl: RecipeBase.model_validate(Recipe)
    model_config = ConfigDict(from_attributes=True)
