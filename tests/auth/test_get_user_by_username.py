import pytest
from unittest.mock import AsyncMock

import pytest_asyncio

from src.domain.schemas.neon.user import UserResponse
from src.domain.services.user_service import UserService


@pytest_asyncio.fixture
async def mock_user_repository():
    mock_repo = AsyncMock()
    mock_repo.get_user_by_username.return_value = UserResponse(
        id=1, username="testuser", email="test@example.com"
    )
    return mock_repo


@pytest.mark.asyncio
async def test_get_user_by_username_returns_user(mock_user_repository):
    # Arrange
    service = UserService.__new__(UserService)  # create without call __init__
    service.user_repository = mock_user_repository

    # Act
    user = await service.get_user_by_username("testuser")

    # Assert
    assert user.username == "testuser"
    assert user.email == "test@example.com"
    mock_user_repository.get_user_by_username.assert_awaited_once_with("testuser")
