from fastapi import FastAPI

from src.core.config import get_settings
from src.dependencies.neon_db import lifespan
from src.middlewares import register_middleware
from pathlib import Path
from fastapi.staticfiles import StaticFiles

from src.routes import register_routes

settings = get_settings()


BASE_DIR = Path(__file__).parent.parent

app = FastAPI(title=settings.TITLE, version=settings.VERSION, lifespan=lifespan)
app.mount("/static", StaticFiles(directory=BASE_DIR / "static"), name="static")


register_middleware(fastapi_app=app)
register_routes(fastapi_app=app)
