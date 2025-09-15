from typing import List

from sqlmodel import select
from sqlmodel.ext.asyncio.session import AsyncSession

from src.domain.neon_models import User, Category
from src.domain.schemas.neon.category import CategoryBase, CategoryResponse


class CategoryRepository:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def create_category(self, body: CategoryBase, user: User) -> Category:
        category = Category(**body.model_dump(exclude_unset=True), user=user)
        self.session.add(category)
        await self.session.commit()
        await self.session.refresh(category)
        return category

    async def create_categories(self, body: List[CategoryBase], user: User):
        for item in body:
            category = Category(**item.model_dump(exclude_unset=True), user=user)
            self.session.add(category)

        await self.session.commit()
        return f"Inserted {len(body)} categories"

    async def get_user_categories(self, user_id: int) -> List[CategoryResponse]:
        query = select(Category).where(Category.user_id == user_id)
        result = await self.session.exec(query)
        categories = result.all()
        return [CategoryResponse.model_validate(cat) for cat in categories]
