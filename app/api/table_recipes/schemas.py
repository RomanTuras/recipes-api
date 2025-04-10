from app.schemas import BaseSchema


class OldRecipeSchema(BaseSchema):
    """Schema for view old recipe (from old DB)."""

    _id: int
    recipe_title: str | None = None
    recipe: str | None = None
    category_id: int
    make: int
    sub_category_id: int
    image: str | None = None
