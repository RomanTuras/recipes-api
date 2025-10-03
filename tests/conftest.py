# conftest.py

import pytest
import pytest_asyncio
from unittest.mock import AsyncMock
from sqlalchemy import StaticPool
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine

from src.domain.models.neon_models.base import MinimalBase

from src.domain.models.neon_models import User, Recipe
from src.domain.schemas.neon.category import CategoryBase
from src.domain.schemas.neon.ingredient import IngredientBase
from src.domain.schemas.neon.recipe import RecipeBase
from src.domain.schemas.neon.recipe_ingredient_link import RecipeIngredientLinkBase
from src.domain.schemas.neon.sync_payload import SyncPayload
from src.domain.services.sync_service import SyncService
from tests.utils.datetime_util import get_datetime_from_str

from src.domain.repository.neon.recipe_repository import RecipeRepository


@pytest.fixture
def recipe_repository(mock_session):
    return RecipeRepository(session=mock_session)


@pytest.fixture
def sync_service(mock_session):
    return SyncService(session=mock_session)


@pytest.fixture
def user():
    return User(
        id=1,
        email="sky@walker.com",
        username="Luke",
        confirmed=True,
        hashed_password="$2b$12$hfKrv7iX9m8iPTnQG6fFGunPZt/Bf4wgNrGE6fmRT0O9vk2idd75W",
    )


@pytest.fixture
def recipe_data():
    """Fixture Recipe schema"""
    return RecipeBase(
        id=1,
        local_id=7,
        title="Test Soup",
        text="Boil water",
        user_id=1,
        is_favorite=False,
        cook_it=False,
        updated_at=get_datetime_from_str("2025-09-20 13:42:02"),
    )


@pytest.fixture
def recipes_list():
    """List of recipes (models)"""
    return [
        Recipe(
            id=1,
            local_id=7,
            category_local_id=17,
            title="Test Soup",
            text="Boil water",
            user_id=1,
            is_favorite=False,
            cook_it=False,
            updated_at=get_datetime_from_str("2025-09-10 13:42:02"),
        ),
        Recipe(
            id=2,
            local_id=8,
            category_local_id=17,
            title="Bugenina is swinina",
            text="Lorem ipsum swinin",
            user_id=1,
            is_favorite=True,
            cook_it=False,
            updated_at=get_datetime_from_str("2025-09-20 10:12:00"),
        ),
        Recipe(
            id=3,
            local_id=9,
            category_local_id=21,
            title="Kapusta",
            text="Lorem ipsum kapusta",
            user_id=1,
            is_favorite=False,
            cook_it=False,
            updated_at=get_datetime_from_str("2025-09-21 14:32:00"),
        ),
    ]


@pytest.fixture
def upload_payload():
    return SyncPayload(
        categories=[
            CategoryBase(local_id=1, title="First category", user_id=1),
            CategoryBase(
                local_id=7, title="Category to delete", user_id=1, is_delete=True
            ),
        ],
        ingredients=[
            IngredientBase(local_id=1, title="Kurochka", user_id=1),
            IngredientBase(local_id=2, title="Petrushka", user_id=1),
            IngredientBase(local_id=3, title="Kapusta", user_id=1),
        ],
        recipes=[
            RecipeBase(
                local_id=7,
                category_local_id=1,
                title="Edited Soup Title",
                text="Boil water",
                user_id=1,
                is_favorite=True,
                cook_it=True,
            ),
            RecipeBase(
                local_id=9,
                category_local_id=21,
                title="Kapusta",
                user_id=1,
                is_delete=True,
            ),
        ],
        recipe_ingredients_links=[
            RecipeIngredientLinkBase(
                recipe_local_id=7,
                ingredient_local_id=1,
                user_id=1,
            ),
            RecipeIngredientLinkBase(
                recipe_local_id=7,
                ingredient_local_id=2,
                user_id=1,
            ),
            RecipeIngredientLinkBase(
                recipe_local_id=7,
                ingredient_local_id=3,
                user_id=1,
                is_delete=True,
            ),
            RecipeIngredientLinkBase(
                recipe_local_id=9,
                ingredient_local_id=1,
                user_id=1,
            ),
            RecipeIngredientLinkBase(
                recipe_local_id=9,
                ingredient_local_id=2,
                user_id=1,
            ),
            RecipeIngredientLinkBase(
                recipe_local_id=9,
                ingredient_local_id=3,
                user_id=1,
            ),
        ],
    )


@pytest.fixture(scope="session")
def metadata():
    return MinimalBase.metadata


@pytest.fixture
def mock_session():
    mock_session = AsyncMock(spec=AsyncSession)
    return mock_session


@pytest_asyncio.fixture(scope="function")
async def async_session(metadata):
    engine = create_async_engine(
        "sqlite+aiosqlite:///:memory:",
        poolclass=StaticPool,  # Do not remove in-memory DB after closing each connection
        connect_args={"check_same_thread": False},
    )

    async with engine.begin() as conn:
        await conn.run_sync(metadata.create_all)

    AsyncSessionLocal = async_sessionmaker(
        bind=engine,
        expire_on_commit=False,
        class_=AsyncSession,
    )

    async with AsyncSessionLocal() as session:
        # Transaction begin
        await session.begin()
        try:
            yield session
        except Exception:
            await session.rollback()
            raise
        finally:
            # Rollback all changes
            await session.rollback()

    # Cleaning: drop all tables (good practice)
    async with engine.begin() as conn:
        await conn.run_sync(metadata.drop_all)
