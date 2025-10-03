from datetime import datetime
from typing import List

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from src.core.app_exceptions import ResourceNotFoundException
from src.domain.models.neon_models import RecipeIngredientLink, User
from src.domain.schemas.neon.recipe_ingredient_link import RecipeIngredientLinkBase


class RecipeIngredientLinkRepository:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def create_link(
        self, link_data: RecipeIngredientLinkBase
    ) -> RecipeIngredientLinkBase:
        """Create a link recipe->ingredient"""
        link = RecipeIngredientLink(**link_data.model_dump(exclude_unset=True))
        link.updated_at = datetime.now()

        self.session.add(link)
        await self.session.commit()

        return RecipeIngredientLinkBase.model_validate(link)

    async def get_link(
        self, link_data: RecipeIngredientLinkBase
    ) -> RecipeIngredientLinkBase:
        """Fetch a user recipe->ingredient link"""
        query = (
            select(RecipeIngredientLink)
            .where(RecipeIngredientLink.recipe_local_id == link_data.recipe_local_id)
            .where(
                RecipeIngredientLink.ingredient_local_id
                == link_data.ingredient_local_id
            )
            .where(RecipeIngredientLink.user_id == link_data.user_id)
        )

        result = await self.session.execute(query)
        link = result.scalar_one_or_none()

        if link is None:
            raise ResourceNotFoundException(
                message="RecipeIngredientLink was not found"
            )

        return RecipeIngredientLinkBase.model_validate(link)

    async def get_changed_ingredient_links(
        self, last_update: datetime, user: User
    ) -> List[RecipeIngredientLinkBase]:
        """Getting all user recipe->ingredient links, changed after last_update date"""
        query = (
            select(RecipeIngredientLink)
            .where(RecipeIngredientLink.updated_at > last_update)
            .where(RecipeIngredientLink.user_id == user.id)
        )
        result = await self.session.execute(query)
        links = result.scalars().all()

        return [RecipeIngredientLinkBase.model_validate(link) for link in links]

    async def update_link(
        self, link_data: RecipeIngredientLinkBase
    ) -> RecipeIngredientLinkBase:
        """Updating a user recipe->ingredient link"""
        try:
            link = await self.get_link(link_data=link_data)
        except ResourceNotFoundException:
            raise ResourceNotFoundException(
                message="RecipeIngredientLink was not found"
            )

        for field, value in link_data.model_dump(exclude_unset=True).items():
            setattr(link, field, value)
            link.updated_at = datetime.now()

        await self.session.commit()
        return RecipeIngredientLinkBase.model_validate(link)

    async def delete_recipe_ingredient_link(
        self, link_data: RecipeIngredientLinkBase
    ) -> RecipeIngredientLinkBase:
        """Marking to delete certain user recipe->ingredient link"""

        link_data.is_delete = True

        return await self.update_link(link_data=link_data)
