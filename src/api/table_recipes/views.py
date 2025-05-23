from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from starlette import status

from src.api.table_recipes.schemas import RecipeSchema
from src.dependencies.db import get_db
from src.domain.table_recipes import TableRecipe

router = APIRouter(tags=["recipe"])


@router.get(
    path="/recipe/{recipe_id}",
    summary="Getting recipes from old DB.",
    status_code=status.HTTP_200_OK,
)
async def recipe(
        recipe_id: int,
    db: AsyncSession = Depends(get_db),
) -> RecipeSchema:
    result = await db.execute(select(TableRecipe).where(TableRecipe.id == recipe_id))
    recipe_raw = result.scalar_one_or_none()
    if not recipe_raw:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Recipe was not found",
        )
    return RecipeSchema(
        id = recipe_raw.id,
        recipe_title = recipe_raw.recipe_title,
        recipe = recipe_raw.recipe,
        category_id = recipe_raw.category_id,
        make = recipe_raw.make,
        sub_category_id = recipe_raw.sub_category_id,
        image = recipe_raw.image,
    )
