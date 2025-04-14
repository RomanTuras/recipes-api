#!venv/bin/python
import uvicorn

from src.conf import get_settings

if __name__ == "__main__":
    settings = get_settings()

    uvicorn.run(
        app="src.main:fastapi_app",
        host=settings.HOST,
        port=settings.PORT,
        reload=settings.DEBUG,
    )
