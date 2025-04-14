from src.schemas import BaseSchema


class SubCatSchema(BaseSchema):
    """Schema for subcategories (from old DB)."""

    id: int
    name: str
    parent_id: int


class RecipeMainCategorySchema(BaseSchema):
    """Schema for recipes from main category (from old DB)."""

    id: int
    recipe_title: str
    category_id: int
    make: bool
    image: str


class ResponseSubCatSchema(BaseSchema):
    """Schema of response from main category (used old DB)."""

    subcategories: list[SubCatSchema]
    recipes: list[RecipeMainCategorySchema]
    main_category_name: str
