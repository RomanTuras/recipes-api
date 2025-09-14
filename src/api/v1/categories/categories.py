from typing import List

from fastapi import APIRouter, status, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from src.dependencies.neon_db import get_session
from src.domain.repository.neon.user_repository import UserRepository
from src.domain.schemas.neon.category import CategoryResponse, CategoryBase
from src.domain.services.category_service import CategoryService
from src.domain.services.migrate_sqlite_to_neon import migrate_categories

router = APIRouter(prefix="/category", tags=["category"])


@router.post("/", response_model=CategoryResponse, status_code=status.HTTP_201_CREATED)
async def create_category(
    body: CategoryBase, session: AsyncSession = Depends(get_session)
):
    category_service = CategoryService(session)
    user_repository = UserRepository(session)
    user = await user_repository.get_user_by_id(1)
    return await category_service.create_category(body, user)


@router.get(
    "/all", response_model=List[CategoryResponse], status_code=status.HTTP_200_OK
)
async def get_user_categories(session: AsyncSession = Depends(get_session)):
    category_service = CategoryService(session)
    user_repository = UserRepository(session)
    user = await user_repository.get_user_by_id(1)
    return await category_service.get_user_categories(user)


# @router.get("/copy-main-categories", status_code=status.HTTP_201_CREATED)
# async def copy_main_categories():
#     return await migrate_categories()
