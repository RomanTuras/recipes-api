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


class ImageResponse(ImageBase):
    # allows to create ImageResponse directly from Image ORM model, expl: ImageResponse.model_validate(Image)
    model_config = ConfigDict(from_attributes=True, str_strip_whitespace=True)
