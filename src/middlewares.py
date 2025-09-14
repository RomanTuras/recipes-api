from fastapi import Request, HTTPException, FastAPI
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.middleware.cors import CORSMiddleware
from starlette.responses import JSONResponse
from time import time
from typing import Callable


class AuthenticationMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next: Callable):
        if request.url.path.startswith("/api/v1/admin"):
            try:
                print(request.headers.get("Authorization"))
                auth_header = request.headers.get("Authorization")
                if not auth_header == "Bearer super_secret_token":
                    return JSONResponse(
                        status_code=401, content={"detail": "Unauthorized"}
                    )

                response = await call_next(request)
                return response
            except HTTPException as exc:
                # If token validation fails due to HTTPException, return the error response
                return JSONResponse(
                    content={"detail": exc.detail}, status_code=exc.status_code
                )
            except Exception as exc:
                # If token validation fails due to other exceptions, return a generic error response
                return JSONResponse(
                    content={"detail": f"Error: {str(exc)}"}, status_code=500
                )
        else:
            response = await call_next(request)
            return response


class ProcessTimeMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next: Callable):
        start_time = time()
        response = await call_next(request)
        process_time = time() - start_time
        response.headers["X-Process-Time"] = str(f"{process_time:.4f} seconds")
        return response


# CORS middleware
def register_middleware(fastapi_app: FastAPI):
    # settings = get_settings()
    fastapi_app.add_middleware(
        CORSMiddleware,
        # allow_origins=settings.ORIGINS,
        allow_origins=["*"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    fastapi_app.add_middleware(AuthenticationMiddleware)
    fastapi_app.add_middleware(ProcessTimeMiddleware)
