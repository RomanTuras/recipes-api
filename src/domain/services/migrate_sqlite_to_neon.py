from typing import List

from sqlmodel import desc
from sqlalchemy import select

from src.dependencies.neon_db import get_session as get_pg_session
from src.dependencies.sqlite_db import get_db as get_sqlite_session
from src.domain.neon_models import Category
from src.domain.repository.neon.recipe_repository import RecipeRepository
from src.domain.repository.neon.user_repository import UserRepository
from src.domain.schemas.neon.recipe import RecipeBase
from src.domain.sqlite_models.table_main import TableMain

from src.domain.repository.neon.category_repository import CategoryRepository
from src.domain.schemas.neon.category import CategoryBase
from src.domain.sqlite_models.table_recipes import TableRecipe
from src.domain.sqlite_models.table_sub_cat import TableSubCat


async def migrate_categories():
    categories = await get_top_categories()
    await store_new_categories(categories)

    main_categories_recipes = await get_sqlite_recipes(True)
    await store_new_recipes(main_categories_recipes)

    last_category_id = await get_categories_last_id()
    sub_categories = await get_sub_categories(sub_category_id_offset=last_category_id)
    await store_new_categories(sub_categories)

    sub_categories_recipes = await get_sqlite_recipes(
        is_main_category=False, sub_category_id_offset=last_category_id
    )
    await store_new_recipes(sub_categories_recipes)


async def get_sqlite_recipes(
    is_main_category: bool, sub_category_id_offset: int = 0
) -> List[RecipeBase]:
    rows = 0
    async for sqlite_session in get_sqlite_session():
        rows = (
            (
                await sqlite_session.execute(
                    select(TableRecipe).where(
                        TableRecipe.category_id > 0
                        if is_main_category
                        else TableRecipe.sub_category_id > 0
                    )
                )
            )
            .scalars()
            .all()
        )

    print(
        f"Found {len(rows)} recipes in {'main' if is_main_category else 'sub'} categories"
    )

    recipes: List[RecipeBase] = []
    for row in rows:
        recipes.append(
            RecipeBase(
                id=row.id,
                title=row.recipe_title.strip(),
                text=row.recipe,
                image=row.image,
                is_favorite=True if row.make == 1 else False,
                category_id=row.category_id
                if is_main_category
                else row.sub_category_id + sub_category_id_offset,
                user_id=1,
            )
        )

    return recipes


async def get_categories_last_id() -> int:
    last_category_id = 0
    async for pg_session in get_pg_session():
        query = select(Category).order_by(desc(Category.id)).limit(1)
        result = await pg_session.exec(query)
        last_category = result.scalars().first()
        last_category_id = last_category.id
    return last_category_id


async def get_sub_categories(sub_category_id_offset: int) -> List[CategoryBase]:
    rows = 0
    async for sqlite_session in get_sqlite_session():
        rows = (await sqlite_session.execute(select(TableSubCat))).scalars().all()

    print(f"Found {len(rows)} subcategories in sqlite")

    categories: List[CategoryBase] = []
    for row in rows:
        categories.append(
            CategoryBase(
                id=row.id + sub_category_id_offset,
                title=row.name.strip(),
                parent_id=row.parent_id,
                user_id=1,
            )
        )

    return categories


async def get_top_categories() -> List[CategoryBase]:
    rows = 0
    async for sqlite_session in get_sqlite_session():
        rows = (await sqlite_session.execute(select(TableMain))).scalars().all()

    print(f"Found {len(rows)} categories in sqlite")

    categories: List[CategoryBase] = []
    for row in rows:
        categories.append(
            CategoryBase(
                id=row.id,
                title=row.category.strip(),
                parent_id=None,
                user_id=1,
            )
        )

    return categories


async def store_new_categories(categories: List[CategoryBase]):
    async for pg_session in get_pg_session():
        user_repository = UserRepository(pg_session)
        user = await user_repository.get_user_by_id(1)
        repo = CategoryRepository(pg_session)
        result = await repo.create_categories(categories, user)
        print(result)


async def store_new_recipes(recipes: List[RecipeBase]):
    async for pg_session in get_pg_session():
        user_repository = UserRepository(pg_session)
        user = await user_repository.get_user_by_id(1)
        repo = RecipeRepository(pg_session)
        result = await repo.create_recipes(recipes, user)
        print(result)
