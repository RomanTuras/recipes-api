from pydantic import EmailStr
from sqlalchemy.ext.asyncio import AsyncSession
from sqlmodel import select

from src.domain.neon_models import User
from src.domain.schemas.neon.user import UserResponse, UserCreate


class UserRepository:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def get_user_by_id(self, user_id: int) -> UserResponse | None:
        """Getting user by ID"""
        query = select(User).where(User.id == user_id)
        user = await self.session.execute(query)
        return user.scalar_one_or_none()

    async def get_user_by_username(self, username: str) -> UserResponse | None:
        """Getting user by username"""
        query = select(User).where(User.username == username)
        user = await self.session.execute(query)
        return user.scalar_one_or_none()

    async def get_user_by_email(self, email: EmailStr) -> UserResponse | None:
        """Getting user by email"""
        query = select(User).where(User.email == email)
        user = await self.session.execute(query)
        return user.scalar_one_or_none()

    async def create_user(self, body: UserCreate) -> UserResponse:
        """Creating a new User"""
        user = User(
            **body.model_dump(exclude_unset=True, exclude={"password"}),
            hashed_password=body.password,
        )
        self.session.add(user)
        await self.session.commit()
        await self.session.refresh(user)
        return UserResponse.model_validate(user)

    async def confirmed_email(self, email: EmailStr) -> None:
        """Saving to DB that user email is completely confirmed"""
        user = await self.get_user_by_email(email)
        user.confirmed = True
        await self.session.commit()
