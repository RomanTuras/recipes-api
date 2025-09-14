from pydantic import BaseModel, ConfigDict
from typing import Optional


class CategoryBase(BaseModel):
    id: Optional[int] = None
    title: str
    parent_id: Optional[int] = None
    user_id: Optional[int] = None


class CategoryResponse(CategoryBase):
    id: int

    model_config = ConfigDict(from_attributes=True, str_strip_whitespace=True)
