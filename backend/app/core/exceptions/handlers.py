from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse

from .custom import AppException


def register_exception_handlers(app: FastAPI) -> None:
    @app.exception_handler(AppException)
    async def app_exception_handler(request: Request, exc: AppException):
        return JSONResponse(
            status_code=exc.status_code,
            content={"detail": exc.message, "type": type(exc).__name__},
        )

    @app.exception_handler(Exception)
    async def unhandled_exception_handler(request: Request, exc: Exception):
        import logging
        logging.error("Unhandled error on %s %s: %s", request.method, request.url, exc, exc_info=True)
        return JSONResponse(
            status_code=500,
            content={"detail": "Internal server error", "type": "InternalError"},
        )
