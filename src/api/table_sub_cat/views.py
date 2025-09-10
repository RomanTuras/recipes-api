from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from starlette import status

from src.domain.table_main import TableMain
from src.api.table_sub_cat.schemas import ResponseSubCatSchema
from src.dependencies.db import get_db
from src.domain.table_sub_cat import TableSubCat
from src.domain.table_recipes import TableRecipe
from src.api.table_sub_cat.schemas import SubCatSchema, RecipeMainCategorySchema

router = APIRouter(tags=["category"])


@router.get(
    path="/category/{category_id}",
    summary="Getting a subcategories and recipes from main category.",
    status_code=status.HTTP_200_OK,
)
async def main_category(
    category_id: int,
    db: AsyncSession = Depends(get_db),
) -> ResponseSubCatSchema:
    """Getting a subcategories and recipes from main category"""

    query = select(TableMain.category).where(TableMain.id == category_id)
    result = await db.execute(query)
    main_category_name = result.scalar_one_or_none()
    print(main_category_name)
    if not main_category_name:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Category was not found",
        )

    # Select subcategories from main category
    query = select(TableSubCat).where(TableSubCat.parent_id == category_id)
    result = await db.execute(query)
    subcategories_raw = result.scalars().all()
    subcategories = [
        SubCatSchema(
            id=subcategory.id, name=subcategory.name, parent_id=subcategory.parent_id
        )
        for subcategory in subcategories_raw
    ]

    # Select recipes from main category
    query = select(TableRecipe).where(TableRecipe.category_id == category_id)
    result = await db.execute(query)
    recipes_raw = result.scalars().all()
    recipes = [
        RecipeMainCategorySchema(
            id=recipe.id,
            recipe_title=recipe.recipe_title,
            category_id=recipe.category_id,
            make=bool(recipe.make) if recipe.make is not None else False,
            image=recipe.image or "",
        )
        for recipe in recipes_raw
    ]

    return ResponseSubCatSchema(
        subcategories=subcategories,
        recipes=recipes,
        main_category_name=main_category_name,
    )
