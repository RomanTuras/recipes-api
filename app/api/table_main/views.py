from typing import Sequence

from fastapi import APIRouter, Depends, Query
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from starlette import status

from app.api.table_main.schemas import TableMainSchema
from app.dependencies.db import get_db
from app.domain.table_main import TableMain

router = APIRouter(tags=["old-main-categories"])


@router.get(
    path="/old-main-categories",
    summary="Getting main categories from old DB.",
    status_code=status.HTTP_200_OK,
)
async def list_old_main_categories(
    offset: int = Query(0, ge=0),
    limit: int = Query(10, ge=1),
    db: AsyncSession = Depends(get_db),
) -> Sequence[TableMainSchema]:
    result = await db.execute(select(TableMain).offset(offset).limit(limit))
    categories = result.scalars().all()
    return categories
