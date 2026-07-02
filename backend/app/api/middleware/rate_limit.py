import time
from collections import defaultdict
from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse


_request_counts: dict[str, list[float]] = defaultdict(list)
WINDOW = 60.0
MAX_REQUESTS = 120


def add_rate_limit(app: FastAPI) -> None:
    @app.middleware("http")
    async def rate_limit_middleware(request: Request, call_next):
        client_ip = request.client.host if request.client else "unknown"
        now = time.time()
        window_start = now - WINDOW

        counts = _request_counts[client_ip]
        _request_counts[client_ip] = [t for t in counts if t > window_start]
        _request_counts[client_ip].append(now)

        if len(_request_counts[client_ip]) > MAX_REQUESTS:
            return JSONResponse(
                status_code=429,
                content={"detail": "Too many requests. Please slow down."},
            )
        return await call_next(request)
