from sqlalchemy.ext.asyncio import AsyncSession

from src.domain.repository.neon.image_repository import ImageRepository
from src.domain.schemas.neon.image import ImageBase


class ImageService:
    def __init__(self, session: AsyncSession):
        self.image_repository = ImageRepository(session)

    async def upsert_image(self, image_data: ImageBase) -> ImageBase | None:
        """Updating or Inserting image data"""
        if image_data.public_id is None:
            return None
        image = await self.image_repository.get_image_by_public_id(image_data.public_id)

        if image is not None:
            updated_image = await self.image_repository.update_image(
                new_image=image_data
            )
            return ImageBase.model_validate(updated_image)

        inserted_image = await self.image_repository.insert_image(image_data=image_data)
        return ImageBase.model_validate(inserted_image)
