from fastapi import APIRouter, status, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from src.core.config import get_settings
from src.dependencies.neon_db import get_session
from src.domain.models.neon_models import User
from src.domain.schemas.neon.sync_payload import SyncPayload
from src.domain.services.auth import get_current_user
from src.domain.services.sync_service import SyncService

router = APIRouter(prefix="/sync", tags=["sync"])
settings = get_settings()


@router.post("/", response_model=SyncPayload, status_code=status.HTTP_200_OK)
async def upload(
    body: SyncPayload,
    user: User = Depends(get_current_user),
    session: AsyncSession = Depends(get_session),
):
    """Upload to server, response: SyncPayload with only required fields"""

    sync_service = SyncService(session)
    updated_payload = await sync_service.upload(body=body, user=user)

    return updated_payload


# @router.get("/{timestamp}", response_model=SyncPayload, status_code=status.HTTP_200_OK)
# async def download(
#     timestamp: datetime,
#     user: User = Depends(get_current_user),
#     session: AsyncSession = Depends(get_session),
# ):
#     """
#     Downloads all changes from the server that occurred after the given timestamp.
#     """
#
