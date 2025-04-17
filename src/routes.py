from fastapi import APIRouter, FastAPI

from src.api.root.views import router as root_router
from src.api.table_recipes.views import router as table_recipes_router
from src.api.table_main.views import router as table_main
from src.api.table_sub_cat.views import router as table_sub_cat


def register_routes(fastapi_app: FastAPI):
    """Function to register all API routers in one place."""
    v1_router = APIRouter(prefix="/api/v1")

    v1_admin_router = APIRouter(prefix="/api/v1/admin")
    v1_admin_router.include_router(root_router)

    v1_router.include_router(table_recipes_router)
    v1_router.include_router(table_main)
    v1_router.include_router(table_sub_cat)

    # main level
    fastapi_app.include_router(v1_router)
    fastapi_app.include_router(v1_admin_router)
