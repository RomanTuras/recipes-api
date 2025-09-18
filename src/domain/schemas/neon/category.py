from pydantic import BaseModel, ConfigDict
from typing import Optional


class CategoryBase(BaseModel):
    id: Optional[int] = None
    local_id: int
    parent_local_id: Optional[int] = None
    title: str
    user_id: int


class CategoryResponse(CategoryBase):
    # allows to create CategoryResponse directly from Category ORM model, expl: CategoryResponse.model_validate(Category)
    model_config = ConfigDict(from_attributes=True, str_strip_whitespace=True)
