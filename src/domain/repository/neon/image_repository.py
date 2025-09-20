from datetime import datetime

from sqlalchemy import select, delete
from sqlalchemy.ext.asyncio import AsyncSession

from src.domain.models.neon_models.image import Image
from src.domain.schemas.neon.image import ImageResponse
from src.core.app_logger import logger


class ImageRepository:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def get_image_by_public_id(self, public_id: str) -> Image | None:
        """Getting image by public_id"""
        query = select(Image).where(Image.public_id == public_id)
        result = await self.session.execute(query)

        return result.scalar_one_or_none()

    async def insert_image(self, image_data: ImageResponse) -> Image | None:
        """Inserting a new Image"""
        image = Image(**image_data.model_dump(exclude_unset=True))
        image.updated_at = datetime.now()
        self.session.add(image)
        await self.session.commit()
        await self.session.refresh(image)

        return await self.get_image_by_public_id(image.public_id)

    async def update_image(self, new_image: ImageResponse) -> Image | None:
        logger.info("update_image")
        """Updating the image, public_id is uniq and already has a username"""
        if new_image.public_id is None:
            return None
        image = await self.get_image_by_public_id(new_image.public_id)

        if image is None:
            return None

        image.url = str(new_image.url)
        image.updated_at = datetime.now()

        # for key, value in image.model_dump(exclude_unset=True).items():
        #     setattr(image, key, value)

        await self.session.commit()
        await self.session.refresh(image)
        return image

    async def delete_image(self, user_id: int, local_id: int, recipe_local_id: int):
        """Deleting image by local_id and recipe_local_id"""
        query = (
            delete(Image)
            .where(Image.user_id == user_id)
            .where(Image.local_id == local_id)
            .where(Image.recipe_local_id == recipe_local_id)
        )
        result = await self.session.execute(query)
        print(result)
