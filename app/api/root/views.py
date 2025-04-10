from fastapi import APIRouter
from starlette import status

from app.api.root.schemas import HealthCheckSchema

router = APIRouter()


@router.get(
    "/info",
    tags=["info"],
    response_model=HealthCheckSchema,
    status_code=status.HTTP_200_OK,
    summary="Health check",
)
async def get_info():
    return {"message": "_hello Morda!"}
