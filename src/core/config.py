# settings.py
from pathlib import Path
from functools import lru_cache

from pydantic_settings import BaseSettings, SettingsConfigDict


BASE_DIR = Path(__file__).resolve().parent.parent
DB_PATH = BASE_DIR / "db" / "cook.db"


class Settings(BaseSettings):
    TITLE: str = "Recipes API V1"
    VERSION: str = "0.1.0"
    HOST: str = "0.0.0.0"
    PORT: int = 80

    DEBUG: bool = True
    IS_LOCAL_MODE: bool = False

    API_V1_PREFIX: str = "/api/v1"

    DATABASE_URL: str | None = None
    DATABASE_DRIVER: str | None = None
    DATABASE_URI: str = f"sqlite+aiosqlite:///{DB_PATH}"

    JWT_SECRET: str | None = None
    JWT_ALGORITHM: str | None = None
    JWT_EXPIRATION_SECONDS: float = 60 * 60 * 24 * 30

    # CORS
    ORIGINS: tuple[str, ...] = (
        "http://127.0.0.1:80",
        "http://localhost:80",
        "https://127.0.0.1:80",
        "https://localhost:80",
    )

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=True,
        extra="ignore",
    )


@lru_cache
def get_settings() -> Settings:
    return Settings()
