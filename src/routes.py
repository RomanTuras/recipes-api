from fastapi import APIRouter, FastAPI

from src.api.v1.user.user import router as user_router
from src.api.v1.categories.categories import router as category_router
from src.api.v1.user.auth import router as auth_router
from src.core.config import get_settings


def register_routes(fastapi_app: FastAPI):
    """Function to register all API routers in one place."""

    settings = get_settings()
    v1_router = APIRouter(prefix=settings.API_V1_PREFIX)

    v1_router.include_router(user_router)
    v1_router.include_router(category_router)
    v1_router.include_router(auth_router)

    # main level
    fastapi_app.include_router(v1_router)
