from pydantic import EmailStr
from sqlmodel.ext.asyncio.session import AsyncSession

from src.domain.neon_models import User
from src.domain.repository.neon.user_repository import UserRepository
from src.domain.schemas.neon.user import UserResponse, UserCreate


class UserService:
    def __init__(self, session: AsyncSession):
        self.user_repository = UserRepository(session)

    async def get_user_by_username(self, username: str) -> User:
        return await self.user_repository.get_user_by_username(username)

    async def get_user_by_email(self, email: EmailStr) -> UserResponse:
        return await self.user_repository.get_user_by_email(email)

    async def create_user(self, body: UserCreate) -> UserResponse:
        return await self.user_repository.create_user(body=body)

    async def confirmed_email(self, email: EmailStr):
        return await self.user_repository.confirmed_email(email)
