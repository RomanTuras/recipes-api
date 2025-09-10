from fastapi import APIRouter, Depends
from sqlalchemy import select, func
from sqlalchemy.ext.asyncio import AsyncSession
from starlette import status

from src.domain.table_recipes import TableRecipe
from src.domain.table_sub_cat import TableSubCat
from src.dependencies.db import get_db
from src.domain.table_main import TableMain
from sqlalchemy import or_, and_
from src.api.table_main.schemas import MainCategoriesSchema

router = APIRouter(tags=["main-categories"])


@router.get(
    path="/main-categories",
    summary="Getting main categories.",
    status_code=status.HTTP_200_OK,
)
async def list_main_categories(
    db: AsyncSession = Depends(get_db),
) -> list[MainCategoriesSchema]:
    # subquery from tableSubCat
    subquery_name = (
        select(func.group_concat(TableSubCat.name, ", "))
        .where(TableSubCat.parent_id == TableMain.id)
        .correlate(TableMain)
        .scalar_subquery()
    )

    # subquery from TableRecipe
    subquery_recipe_count = (
        select(func.count())
        .select_from(TableRecipe)
        .join(
            TableSubCat,
            TableRecipe.sub_category_id == TableSubCat.id,
            isouter=True,  # do not skip if it don't have subcat
        )
        .where(
            or_(
                TableRecipe.category_id == TableMain.id,
                and_(
                    TableRecipe.sub_category_id != -1,
                    TableSubCat.parent_id == TableMain.id,
                ),
            )
        )
        .correlate(TableMain)
        .scalar_subquery()
    )

    stmt = select(
        TableMain.id,
        TableMain.category.label("name"),
        subquery_name.label("subcategories"),
        subquery_recipe_count.label("recipes_count"),
    )

    result = await db.execute(stmt)
    rows = result.all()

    response = []
    for row in rows:
        response.append(
            MainCategoriesSchema(
                id=row[0] if row[0] else 0,
                name=row[1] if row[1] else "",
                subcategories=row[2] if row[2] else "",
                recipes_count=row[3] if row[3] else 0,
            )
        )
    return response
