from app.schemas import BaseSchema


class TableMainSchema(BaseSchema):
    """Schema for view old main categories (from old DB)."""

    _id: int
    category: str | None = None
