from typing import List

from fastapi import APIRouter, status, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from src.core.config import get_settings
from src.dependencies.neon_db import get_session
from src.dependencies.sqlite_db import get_db
from src.domain.repository.neon.recipe_repository import RecipeRepository
from src.domain.schemas.neon.category import CategoryResponse
from src.domain.schemas.neon.user import UserResponse
from src.domain.services.auth import get_current_user
from src.domain.services.category_service import CategoryService
from src.domain.services.sqlite_service import SqliteService

router = APIRouter(prefix="/categories", tags=["categories"])
settings = get_settings()


@router.get("/", response_model=List[CategoryResponse], status_code=status.HTTP_200_OK)
async def get_user_categories(
    user: UserResponse = Depends(get_current_user),
    session: AsyncSession = Depends(get_session),
):
    """Getting all user's categories"""
    category_service = CategoryService(session)
    return await category_service.get_user_categories(user.id)


@router.get("/migrate", status_code=status.HTTP_201_CREATED)
async def copy_main_categories(
    user: UserResponse = Depends(get_current_user),
    neon_session: AsyncSession = Depends(get_session),
    sqlite_session: AsyncSession = Depends(get_db)
):
    sqlite_service = SqliteService(sqlite_session)
    category_service = CategoryService(neon_session)
    recipe_repository = RecipeRepository(neon_session)

    categories = await sqlite_service.get_top_categories()
    await category_service.create_categories(categories, user)

    main_categories_recipes = await sqlite_service.get_sqlite_recipes(True)
    await recipe_repository.create_recipes(main_categories_recipes, user)

    last_category_id = await category_service.get_categories_last_id()
    sub_categories = await sqlite_service.get_sub_categories(sub_category_id_offset=last_category_id)
    await category_service.create_categories(sub_categories, user)

    sub_categories_recipes = await sqlite_service.get_sqlite_recipes(is_main_category=False, sub_category_id_offset=last_category_id)
    await recipe_repository.create_recipes(sub_categories_recipes, user)
