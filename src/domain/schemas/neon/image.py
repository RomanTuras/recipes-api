from datetime import datetime
from typing import Optional

from pydantic import BaseModel, ConfigDict


class ImageBase(BaseModel):
    id: Optional[int] = None
    local_id: int
    url: Optional[str] = None
    recipe_local_id: int
    public_id: Optional[str] = None
    user_id: int
    updated_at: Optional[datetime] = None
    is_delete: Optional[bool] = None

    # allows to create ImageBase directly from Image ORM model, expl: ImageBase.model_validate(Image)
    model_config = ConfigDict(from_attributes=True, str_strip_whitespace=True)
