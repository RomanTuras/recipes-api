from typing import List
from datetime import datetime

from sqlalchemy import select, desc
from sqlalchemy.ext.asyncio import AsyncSession

from src.core.app_exceptions import ResourceNotFoundException
from src.domain.models.neon_models.category import Category
from src.domain.models.neon_models.user import User
from src.domain.repository.neon.recipe_repository import RecipeRepository
from src.domain.schemas.neon.category import CategoryBase


class CategoryRepository:
    def __init__(self, session: AsyncSession):
        self.session = session
        self.recipe_repository = RecipeRepository(session)

    async def get_category(self, local_id: int, user: User) -> CategoryBase:
        """Getting user category by local id"""
        query = (
            select(Category)
            .where(Category.user_id == user.id)
            .where(Category.local_id == local_id)
        )

        result = await self.session.execute(query)
        category = result.scalar_one_or_none()
        if category is None:
            raise ResourceNotFoundException(message="Category was not found")

        return CategoryBase.model_validate(category)

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

    async def create_category(
        self, category_data: CategoryBase, user: User
    ) -> CategoryBase:
        """Create user category"""
        category = Category(**category_data.model_dump(exclude_unset=True))
        category.user_id = user.id
        category.updated_at = datetime.now()
        self.session.add(category)
        await self.session.commit()

        return CategoryBase.model_validate(category)

    async def update_category(
        self, category_data: CategoryBase, user: User
    ) -> CategoryBase:
        """Updating user category by local id"""
        try:
            category = await self.get_category(category_data.local_id, user=user)
        except ResourceNotFoundException:
            raise ResourceNotFoundException(
                message=f"Category with id={category_data.local_id} was not found for user {user.id}"
            )

        for field, value in category_data.model_dump(exclude_unset=True).items():
            setattr(category, field, value)
            category.updated_at = datetime.now()

        await self.session.commit()
        return CategoryBase.model_validate(category)

    async def get_categories(self, user_id: int) -> List[CategoryBase]:
        """Getting all user's categories"""
        query = select(Category).where(Category.user_id == user_id)
        result = await self.session.execute(query)
        categories = result.scalars().all()
        return [CategoryBase.model_validate(cat) for cat in categories]

    async def get_changed_categories(
        self, last_update: datetime, user_id: int
    ) -> List[CategoryBase]:
        """Getting changed user's categories, that was changed after last_update date"""
        query = (
            select(Category)
            .where(Category.user_id == user_id)
            .where(Category.updated_at > last_update)
        )
        result = await self.session.execute(query)
        categories = result.scalars().all()
        return [CategoryBase.model_validate(cat) for cat in categories]

    async def get_categories_by_parent(
        self, parent_local_id: int, user_id: int
    ) -> List[CategoryBase]:
        """Getting user's categories by parent category"""
        query = (
            select(Category)
            .where(Category.user_id == user_id)
            .where(Category.parent_local_id == parent_local_id)
        )
        result = await self.session.execute(query)
        categories = result.scalars().all()
        return [CategoryBase.model_validate(cat) for cat in categories]

    async def get_categories_last_id(self) -> int:
        """Getting the last ID from table categories"""
        query = select(Category).order_by(desc(Category.id)).limit(1)
        result = await self.session.execute(query)
        last_category = result.scalar_one_or_none()
        last_category_id = last_category.id if last_category is not None else 1
        return last_category_id
