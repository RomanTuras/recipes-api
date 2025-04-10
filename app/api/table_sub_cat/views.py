from typing import Sequence

from fastapi import APIRouter, Depends, Query
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from starlette import status

from app.api.table_sub_cat.schemas import TableSubCatSchema
from app.dependencies.db import get_db
from app.domain.table_sub_cat import TableSubCat

router = APIRouter(tags=["old-sub-categories"])


@router.get(
    path="/old-sub-categories",
    summary="Getting subcategories from old DB.",
    status_code=status.HTTP_200_OK,
)
async def list_old_sub_categories(
    offset: int = Query(0, ge=0),
    limit: int = Query(10, ge=1),
    db: AsyncSession = Depends(get_db),
) -> Sequence[TableSubCatSchema]:
    result = await db.execute(select(TableSubCat).offset(offset).limit(limit))
    categories = result.scalars().all()
    return categories
