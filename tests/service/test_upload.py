import pytest

from src.domain.services.sync_service import SyncService


@pytest.mark.asyncio
async def test_upload(async_session, recipes_list, upload_payload, user):
    async_session.add(user)
    await async_session.commit()
    await async_session.refresh(user)  # refresh is needed to get user.id

    sync_service = SyncService(async_session)

    async_session.add_all(recipes_list)
    await async_session.commit()

    result = await sync_service.upload(body=upload_payload, user=user)

    categories = result.categories
    ingredients = result.ingredients
    recipes = result.recipes
    links = result.recipe_ingredients_links

    assert len(categories) == 2
    assert len(ingredients) == 3
    assert len(recipes) == 2
    assert len(links) == 6

    categories_updated_at = {c.updated_at for c in categories}
    recipes_titles = {r.title for r in recipes}
    ingredients_titles = {i.title for i in ingredients}

    test_link = None
    for l in links:
        if l.ingredient_local_id==3 and l.recipe_local_id==7:
            test_link = l

    assert test_link is not None
    assert test_link.is_delete == True
    assert recipes_titles == {"Edited Soup Title", "Kapusta"}
    # Checking out for lowercase for ingredients titles
    assert ingredients_titles == {"kapusta", "petrushka", "kurochka"}
    assert categories_updated_at != {None}
