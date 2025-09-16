from typing import List

from sqlmodel import select, desc
from sqlmodel.ext.asyncio.session import AsyncSession

from src.domain.neon_models import Category
from src.domain.schemas.neon.category import CategoryBase, CategoryResponse
from src.domain.schemas.neon.user import UserResponse


class CategoryRepository:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def create_category(self, body: CategoryBase, user: UserResponse) -> Category:
        """Creating a new category"""
        category = Category(**body.model_dump(exclude_unset=True), user=user)
        self.session.add(category)
        await self.session.commit()
        await self.session.refresh(category)
        return category

    async def create_categories(self, body: List[CategoryBase], user: UserResponse):
        """Creating categories using transaction"""
        try:
            async with self.session.begin():
                for item in body:
                    category = Category(**item.model_dump(exclude_unset=True), user=user)
                    self.session.add(category)
                return f"Inserted {len(body)} categories"
        except Exception as e:
            await self.session.rollback()
            return f"Transaction failed, rolled back. Error: {e}"


    async def get_user_categories(self, user_id: int) -> List[CategoryResponse]:
        """Getting all user's categories"""
        query = select(Category).where(Category.user_id == user_id)
        result = await self.session.exec(query)
        categories = result.all()
        return [CategoryResponse.model_validate(cat) for cat in categories]


    async def get_categories_last_id(self) -> int:
        """Getting the last ID from table categories"""
        query = select(Category).order_by(desc(Category.id)).limit(1)
        result = await self.session.exec(query)
        last_category = result.first()
        last_category_id = last_category.id if last_category is not None else 1
        return last_category_id
