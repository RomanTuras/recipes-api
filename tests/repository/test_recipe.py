from datetime import datetime
from unittest.mock import AsyncMock, MagicMock

import pytest

from src.domain.models.neon_models import Recipe
from src.domain.repository.neon.recipe_repository import RecipeRepository
from src.domain.schemas.neon.recipe import RecipeBase

from tests.utils.datetime_util import get_datetime_from_str


@pytest.mark.asyncio
async def test_create_recipe(mock_session, recipe_repository, recipe_data, user):
    # Act
    created_recipe = await recipe_repository.create_recipe(recipe_data, user)

    assert isinstance(created_recipe, RecipeBase)
    assert created_recipe.id is not None
    assert created_recipe.title == "Test Soup"
    assert created_recipe.user_id == user.id
    assert isinstance(created_recipe.updated_at, datetime)

    mock_session.commit.assert_awaited_once()
    # mock_session.refresh.assert_awaited_once_with(created_recipe)


@pytest.mark.asyncio
async def test_get_recipe(mock_session, recipe_repository, user, recipe_data):
    # Setup mock
    mock_result = MagicMock()
    mock_result.scalar_one_or_none.return_value = Recipe(
        **recipe_data.model_dump(exclude_unset=True)
    )
    mock_session.execute = AsyncMock(return_value=mock_result)
    # Call method
    recipe = await recipe_repository.get_recipe(local_id=7, user=user)
    # Assertions
    assert recipe is not None
    assert recipe.id == 1
    assert recipe.local_id == 7
    assert recipe.title == "Test Soup"


@pytest.mark.asyncio
async def test_update_recipe(mock_session, recipe_repository, user, recipe_data):
    # Setup
    existing_contact = Recipe(**recipe_data.model_dump(exclude_unset=True))
    mock_result = MagicMock()
    mock_result.scalar_one_or_none.return_value = existing_contact
    mock_session.execute = AsyncMock(return_value=mock_result)

    old_recipe_updated_at = recipe_data.updated_at
    # Call method
    data_to_update = RecipeBase(
        local_id=7,
        user_id=1,
        title="Updated title",
        is_favorite=True,
        updated_at=datetime.now(),
    )
    result = await recipe_repository.update_recipe(data_to_update, user=user)

    # Assertions
    assert result is not None
    assert result.title == "Updated title"
    assert result.is_favorite
    assert result.updated_at.date() > old_recipe_updated_at.date()

    mock_session.commit.assert_awaited_once()


@pytest.mark.asyncio
async def test_get_changed_recipes(async_session, user, recipes_list):
    # Setup
    async_session.add_all(recipes_list)
    await async_session.commit()

    repo = RecipeRepository(async_session)
    sync_date = get_datetime_from_str("2025-09-20 10:02:00")
    result = await repo.get_changed_recipes(last_update=sync_date, user=user)

    assert len(result) == 2

    local_ids = {r.local_id for r in result}
    titles = {r.title for r in result}

    assert local_ids == {8, 9}
    assert titles == {"Kapusta", "Bugenina is swinina"}
    assert titles != {"Test Soup"}


@pytest.mark.asyncio
async def test_update_my_recipe(async_session, user, recipes_list):
    # Setup
    async_session.add_all(recipes_list)
    await async_session.commit()

    repo = RecipeRepository(async_session)
    updated_recipe = await repo.update_recipe(
        RecipeBase(
            local_id=8,
            user_id=1,
            title="Updated Bugenina is swinina",
            cook_it=True,
            updated_at=datetime.now(),
        ),
        user=user,
    )

    assert updated_recipe.title == "Updated Bugenina is swinina"
    assert updated_recipe.cook_it


@pytest.mark.asyncio
async def test_get_recipes_by_category(async_session, user, recipes_list):
    async_session.add(user)
    await async_session.commit()
    await async_session.refresh(user)  # refresh is needed to get user.id

    async_session.add_all(recipes_list)
    await async_session.commit()

    repo = RecipeRepository(async_session)
    result = await repo.get_recipes_by_category(category_local_id=17, user=user)

    assert len(result) == 2

    categories = {r.category_local_id for r in result}
    titles = {r.title for r in result}

    assert categories == {17}
    assert titles == {"Test Soup", "Bugenina is swinina"}
    assert titles != {"Kapusta"}
