import cloudinary
import cloudinary.uploader
from fastapi import HTTPException
from starlette import status

from src.core.config import get_settings

settings = get_settings()


class CloudinaryService:
    _instance = None

    def __new__(cls, *args, **kwargs):
        if not cls._instance:
            cls._instance = super(CloudinaryService, cls).__new__(cls)
            # You can also call the init method here if needed
            # For this example, it's better to configure it once in __init__
        return cls._instance

    def __init__(self):
        # The __init__ method will be called every time you "create" an instance,
        # but the actual object will be the same.
        # This is where you put the configuration logic, ensuring it runs only once.
        if not hasattr(self, "_configured"):
            cloudinary.config(
                cloud_name=settings.CLOUDINARY_NAME,
                api_key=settings.CLOUDINARY_API_KEY,
                api_secret=settings.CLOUDINARY_API_SECRET,
                secure=True,
            )
            self._configured = True  # Set a flag to ensure configuration runs only once

    @staticmethod
    def upload_image(file, username: str, public_id: str) -> dict:
        """Upload optimized image. Override image by public_id if already exists"""
        response = cloudinary.uploader.upload(
            file.file,
            public_id=public_id,
            tags=[f"{username}"],
            overwrite=True,
            quality="auto:good",
            transformation=[{"width": 2000, "height": 2000, "crop": "limit"}],
        )
        return response

    @staticmethod
    def delete_image(public_id: str):
        """Delete image from Cloudinary by public_id"""
        try:
            response = cloudinary.uploader.destroy(public_id)
            return response
        except Exception as e:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Error when deleting. {e}",
            )
