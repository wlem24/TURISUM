from .auth import router as auth_router
from .users import router as users_router
from .spots import router as spots_router
from .guides import router as guides_router
from .hotels import router as hotels_router
from .bookings import router as bookings_router
from .regions import router as regions_router
from .admin import router as admin_router
from .notifications import router as notifications_router
from .ai import router as ai_router

__all__ = [
    "auth_router", "users_router", "spots_router", "guides_router",
    "hotels_router", "bookings_router", "regions_router", "admin_router",
    "notifications_router", "ai_router",
]
