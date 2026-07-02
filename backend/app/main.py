from fastapi import FastAPI
from fastapi.responses import JSONResponse

from app.core.config import settings
from app.core.logging import configure_logging
from app.core.exceptions import register_exception_handlers
from app.api.middleware import add_cors, add_rate_limit, add_request_logging
from app.api.routers import (
    auth_router, users_router, spots_router, guides_router,
    hotels_router, bookings_router, regions_router, admin_router,
    notifications_router, ai_router,
)

configure_logging()

app = FastAPI(
    title=settings.APP_NAME,
    version=settings.VERSION,
    description="AI-powered platform to discover hidden tourist spots across Saudi Arabia — أثر Athar",
    docs_url="/docs" if not settings.is_production else None,
    redoc_url="/redoc" if not settings.is_production else None,
)

# Middleware (order matters: CORS first, then rate limit, then logging)
add_cors(app)
add_rate_limit(app)
add_request_logging(app)

# Exception handlers
register_exception_handlers(app)

# Routers
API_PREFIX = "/api/v1"
app.include_router(auth_router, prefix=API_PREFIX)
app.include_router(users_router, prefix=API_PREFIX)
app.include_router(spots_router, prefix=API_PREFIX)
app.include_router(guides_router, prefix=API_PREFIX)
app.include_router(hotels_router, prefix=API_PREFIX)
app.include_router(bookings_router, prefix=API_PREFIX)
app.include_router(regions_router, prefix=API_PREFIX)
app.include_router(admin_router, prefix=API_PREFIX)
app.include_router(notifications_router, prefix=API_PREFIX)
app.include_router(ai_router, prefix=API_PREFIX)


@app.get("/", include_in_schema=False)
async def health():
    return JSONResponse({"status": "ok", "app": settings.APP_NAME, "version": settings.VERSION})


@app.get("/health", include_in_schema=False)
async def health_check():
    return JSONResponse({"status": "healthy"})
