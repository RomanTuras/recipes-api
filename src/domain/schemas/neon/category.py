from datetime import datetime

from pydantic import BaseModel, ConfigDict
from typing import Optional


class CategoryBase(BaseModel):
    id: Optional[int] = None
    local_id: int
    parent_local_id: Optional[int] = None
    title: str
    user_id: int
    updated_at: Optional[datetime] = None
    is_delete: Optional[bool] = None

    # allows to create CategoryBase directly from Category ORM model, expl: CategoryBase.model_validate(Category)
    model_config = ConfigDict(from_attributes=True, str_strip_whitespace=True)
