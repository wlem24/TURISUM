import time
import structlog
from fastapi import FastAPI, Request

logger = structlog.get_logger("http")


def add_request_logging(app: FastAPI) -> None:
    @app.middleware("http")
    async def logging_middleware(request: Request, call_next):
        start = time.perf_counter()
        response = await call_next(request)
        duration_ms = (time.perf_counter() - start) * 1000
        logger.info(
            "http_request",
            method=request.method,
            path=request.url.path,
            status_code=response.status_code,
            duration_ms=round(duration_ms, 2),
        )
        return response
