from fastapi import FastAPI

from src.conf import get_settings
from pathlib import Path
from fastapi import Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from datetime import UTC, datetime
from collections.abc import Callable


from src.routes import register_routes

settings = get_settings()


BASE_DIR = Path(__file__).parent.parent

fastapi_app = FastAPI(title=settings.TITLE, version=settings.VERSION)
fastapi_app.mount("/static", StaticFiles(directory=BASE_DIR / "static"), name="static")


# CORS middleware
fastapi_app.add_middleware(
    CORSMiddleware,
    # allow_origins=settings.ORIGINS,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@fastapi_app.middleware("http")
async def add_process_time_header(request: Request, call_next: Callable):
    """Middleware to add process time header to the response."""
    start_time = datetime.now(tz=UTC)
    response = await call_next(request)
    process_time = datetime.now(tz=UTC) - start_time
    response.headers["X-Process-Time"] = str(process_time)
    return response


register_routes(fastapi_app=fastapi_app)
