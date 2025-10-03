from datetime import datetime

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from src.core.app_exceptions import ResourceNotFoundException
from src.domain.models.neon_models.image import Image
from src.core.app_logger import logger
from src.domain.schemas.neon.image import ImageBase


class ImageRepository:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def get_image_by_public_id(self, public_id: str) -> Image:
        """Getting image by public_id"""
        if public_id is None:
            raise ResourceNotFoundException(message="Image was not found")

        query = select(Image).where(Image.public_id == public_id)
        result = await self.session.execute(query)
        image = result.scalar_one_or_none()
        if image is None:
            raise ResourceNotFoundException(message="Image was not found")

        return image

    async def insert_image(self, image_data: ImageBase) -> Image:
        """Inserting a new Image"""
        image = Image(**image_data.model_dump(exclude_unset=True))
        image.updated_at = datetime.now()
        self.session.add(image)
        await self.session.commit()

        return image

    async def update_image(self, new_image: ImageBase) -> Image:
        logger.info("update_image")
        """Updating the image, public_id is uniq and already has a username"""
        image = await self.get_image_by_public_id(new_image.public_id)

        for field, value in new_image.model_dump(exclude_unset=True).items():
            setattr(image, field, value)
            image.updated_at = datetime.now()

        await self.session.commit()
        return image
