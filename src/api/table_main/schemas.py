from src.schemas import BaseSchema


class MainCategoriesSchema(BaseSchema):
    """Schema for main categories (from old DB)."""
    id: int
    name: str
    subcategories: str
    recipes_count: int

