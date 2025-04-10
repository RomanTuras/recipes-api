from pathlib import Path

from pydantic_settings import BaseSettings, SettingsConfigDict

BASE_DIR = Path(__file__).resolve().parent.parent  # -> table_recipes-api/
DB_PATH = BASE_DIR / "app" / "db" / "cook.db"


class Settings(BaseSettings):
    TITLE: str = "Recipes API"
    VERSION: str = "0.1.0"
    HOST: str = "127.0.0.1"
    PORT: int = 9000
    DEBUG: bool = True
    DATABASE_URI: str = f"sqlite+aiosqlite:///{DB_PATH}"
    ORIGINS: tuple = ("http://localhost:3000", "http://localhost:8080")

    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8")


# @lru_cache
def get_settings() -> Settings:
    return Settings()
