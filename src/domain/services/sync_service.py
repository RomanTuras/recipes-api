from sqlalchemy.ext.asyncio import AsyncSession

from src.domain.models.neon_models import User
from src.domain.repository.neon.sync_repository import SyncRepository
from src.domain.schemas.neon.sync_payload import SyncPayload


class SyncService:
    def __init__(self, session: AsyncSession):
        self.sync_repository = SyncRepository(session)

    async def upload(self, body: SyncPayload, user: User) -> SyncPayload:
        """Uploading sync payload to server"""
        categories = await self.sync_repository.process_categories(
            body.categories, user
        )
        ingredients = await self.sync_repository.process_ingredients(
            body.ingredients, user
        )
        recipes = await self.sync_repository.process_recipes(body.recipes, user)

        links = await self.sync_repository.process_recipe_ingredient_links(
            body.recipe_ingredients_links, user
        )

        return SyncPayload(
            categories=categories,
            ingredients=ingredients,
            recipes=recipes,
            recipe_ingredients_links=links,
        )
