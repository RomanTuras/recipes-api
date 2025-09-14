#!venv/bin/python
import uvicorn

from src.core.config import get_settings

if __name__ == "__main__":
    settings = get_settings()

    uvicorn.run(
        app="src.main:app",
        host=settings.HOST,
        port=settings.PORT,
        reload=settings.DEBUG,
    )
