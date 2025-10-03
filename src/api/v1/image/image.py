from fastapi import APIRouter, Depends, UploadFile, File, Form, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from starlette import status

from src.dependencies.neon_db import get_session
from src.domain.models.neon_models import User
from src.domain.schemas.neon.image import ImageBase
from src.domain.services.auth import get_current_user
from src.domain.services.cloudinary_service import CloudinaryService
from src.domain.services.image_service import ImageService
from src.utils.cloudinary_util import create_public_id

router = APIRouter(prefix="/image", tags=["image"])
cloudinary_service = CloudinaryService()


@router.post("/", response_model=ImageBase, status_code=status.HTTP_200_OK)
async def upload_image(
    local_id: int = Form(),
    recipe_local_id: int = Form(),
    file: UploadFile = File(),
    user: User = Depends(get_current_user),
    session: AsyncSession = Depends(get_session),
):
    """Upload recipe image"""
    image_service = ImageService(session)
    public_id = create_public_id(
        username=user.username, local_id=local_id, recipe_local_id=recipe_local_id
    )

    try:
        response = CloudinaryService.upload_image(
            file, username=user.username, public_id=public_id
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Cloudinary error. {e}",
        )

    image_data = ImageBase(
        local_id=local_id,
        recipe_local_id=recipe_local_id,
        url=response.get("url"),
        public_id=response.get("public_id"),
        user_id=user.id,
    )

    image_response = await image_service.upsert_image(image_data)

    if image_response is None:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Cloudinary error",
        )

    return image_response
