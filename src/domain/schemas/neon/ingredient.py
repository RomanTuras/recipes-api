from typing import Optional
from datetime import datetime

from pydantic import BaseModel, ConfigDict, field_validator


class IngredientBase(BaseModel):
    id: Optional[int] = None
    local_id: int
    title: str
    user_id: int
    updated_at: Optional[datetime] = None
    is_delete: Optional[bool] = None

    # allows to create IngredientBase directly from Ingredient ORM model, expl: IngredientBase.model_validate(Ingredient)
    model_config = ConfigDict(from_attributes=True, str_strip_whitespace=True)

    @field_validator("title", mode="before")
    def normalize_title(cls, v: str):
        return v.casefold().strip()
