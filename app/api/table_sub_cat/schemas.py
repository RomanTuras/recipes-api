from app.schemas import BaseSchema


class TableSubCatSchema(BaseSchema):
    """Schema for view old subcategories (from old DB)."""

    _id: int
    name: str | None = None
    hierarchy: int | None = None
    parent_id: int