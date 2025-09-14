from typing import List

from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.params import Query

from sqlmodel.ext.asyncio.session import AsyncSession

from src.dependencies.neon_db import get_session
from src.domain.neon_models.user import User
from src.domain.repository.neon.user_repository import UserRepository
from src.domain.schemas.neon.category import CategoryResponse
from src.domain.services.category_service import CategoryService

router = APIRouter(prefix="/user", tags=["user"])


@router.post("/", response_model=User)
async def create_user(user: User, session: AsyncSession = Depends(get_session)):
    session.add(user)
    await session.commit()
    await session.refresh(user)
    return user


@router.get("/categories", response_model=List[CategoryResponse])
async def get_user_categories(
        user_id: int | None = Query(None, gt=0),
        session: AsyncSession = Depends(get_session)):
    category_service = CategoryService(session)
    user_repository = UserRepository(session)
    user = await user_repository.get_user_by_id(user_id)
    print(user)
    if user is None:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Verification error")

    return await category_service.get_user_categories(user_id=user.id)
