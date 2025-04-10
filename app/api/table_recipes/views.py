from typing import Any, Coroutine, Sequence

from fastapi import APIRouter, Depends, Query
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from starlette import status

from app.api.table_recipes.schemas import OldRecipeSchema
from app.dependencies.db import get_db
from app.domain.table_recipes import TableRecipe

router = APIRouter(tags=["old-recipes"])


@router.get(
    path="/old-recipes",
    summary="Getting recipes from old DB.",
    status_code=status.HTTP_200_OK,
)
async def list_old_recipes(
    offset: int = Query(0, ge=0),
    limit: int = Query(10, ge=1),
    db: AsyncSession = Depends(get_db),
) -> Sequence[OldRecipeSchema]:
    result = await db.execute(select(TableRecipe).offset(offset).limit(limit))
    recipes = result.scalars().all()
    return recipes
