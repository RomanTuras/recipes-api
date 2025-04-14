from src.schemas import BaseSchema


class RecipeSchema(BaseSchema):
    """Schema for recipe (from old DB)."""

    id: int
    recipe_title: str
    recipe: str | None = None
    category_id: int
    make: bool | None = None
    sub_category_id: int
    image: str | None = None
