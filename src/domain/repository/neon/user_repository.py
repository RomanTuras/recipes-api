from pydantic import EmailStr
from sqlmodel import select
from datetime import datetime

from sqlalchemy.ext.asyncio import AsyncSession

from src.domain.models.neon_models.user import User
from src.domain.schemas.neon.user import UserCreate


class UserRepository:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def get_user_by_id(self, user_id: int) -> User | None:
        """Getting user by ID"""
        query = select(User).where(User.id == user_id)
        response = await self.session.execute(query)
        return response.scalar_one_or_none()

    async def get_user_by_username(self, username: str) -> User | None:
        """Getting used by username"""
        query = select(User).where(User.username == username)
        result = await self.session.execute(query)
        return result.scalar_one_or_none()

    async def get_user_by_email(self, email: EmailStr) -> User | None:
        """Getting user by email"""
        query = select(User).where(User.email == email)
        response = await self.session.execute(query)
        return response.scalar_one_or_none()

    async def create_user(self, body: UserCreate) -> User:
        """Creating a new User"""
        user = User(
            **body.model_dump(exclude_unset=True, exclude={"password"}),
            hashed_password=body.password,
            updated_at=datetime.now(),
        )
        self.session.add(user)
        await self.session.commit()
        await self.session.refresh(user)
        return user

    async def confirmed_email(self, email: EmailStr) -> User | None:
        """Saving to DB that user email is completely confirmed"""
        user = await self.get_user_by_email(email)
        if user is None:
            return None

        user.confirmed = True
        user.updated_at = datetime.now()
        await self.session.commit()
        await self.session.refresh(user)
        return user
