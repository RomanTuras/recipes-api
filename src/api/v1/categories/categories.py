from typing import List

from fastapi import APIRouter, status, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from src.core.config import get_settings
from src.dependencies.neon_db import get_session
from src.domain.schemas.neon.category import CategoryResponse
from src.domain.schemas.neon.user import UserResponse
from src.domain.services.auth import get_current_user
from src.domain.services.category_service import CategoryService
from src.domain.services.migrate_sqlite_to_neon import migrate_categories

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


@router.get("/copy-main-categories", status_code=status.HTTP_201_CREATED)
async def copy_main_categories():
    return await migrate_categories()
