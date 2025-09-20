from typing import List
from datetime import datetime

from sqlalchemy import select, desc
from sqlalchemy.ext.asyncio import AsyncSession

from src.domain.models.neon_models.category import Category
from src.domain.models.neon_models.user import User
from src.domain.schemas.neon.category import CategoryBase, CategoryResponse
from src.domain.schemas.neon.user import UserResponse


class CategoryRepository:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def create_category(self, body: CategoryBase, user: UserResponse) -> Category:
        """Creating a new category"""
        category = Category(**body.model_dump(exclude_unset=True), user=user)
        category.updated_at = datetime.now()
        self.session.add(category)
        await self.session.commit()
        await self.session.refresh(category)
        return category

    async def create_categories(self, body: List[CategoryBase], user: User):
        """Creating categories using transaction"""
        categories = []
        for item in body:
            data = item.model_dump(exclude_unset=True, exclude={"user_id"})
            data["user_id"] = user.id
            data["updated_at"] = datetime.now()
            categories.append(Category(**data))
        self.session.add_all(categories)
        await self.session.commit()
        return f"Inserted {len(body)} categories"

    async def get_user_categories(self, user_id: int) -> List[CategoryResponse]:
        """Getting all user's categories"""
        query = select(Category).where(Category.user_id == user_id)
        result = await self.session.execute(query)
        categories = result.scalars().all()
        return [CategoryResponse.model_validate(cat) for cat in categories]

    async def get_categories_last_id(self) -> int:
        """Getting the last ID from table categories"""
        query = select(Category).order_by(desc(Category.id)).limit(1)
        result = await self.session.execute(query)
        last_category = result.scalar_one_or_none()
        last_category_id = last_category.id if last_category is not None else 1
        return last_category_id
