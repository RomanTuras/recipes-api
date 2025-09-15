from fastapi import Request, FastAPI
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.middleware.cors import CORSMiddleware
from time import time
from typing import Callable

from src.core.config import get_settings


class ProcessTimeMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next: Callable):
        start_time = time()
        response = await call_next(request)
        process_time = time() - start_time
        response.headers["X-Process-Time"] = str(f"{process_time:.4f} seconds")
        return response


# CORS middleware
def register_middleware(fastapi_app: FastAPI):
    settings = get_settings()
    fastapi_app.add_middleware(
        CORSMiddleware,
        allow_origins=settings.ORIGINS,
        # allow_origins=["*"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    fastapi_app.add_middleware(ProcessTimeMiddleware)
