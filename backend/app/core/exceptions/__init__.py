from .custom import (
    AppException, SpotNotFound, UserNotFound, GuideNotFound, HotelNotFound,
    BookingNotFound, UnauthorizedRole, InvalidCredentials, EmailAlreadyExists,
    InvalidToken, SpotNotApproved, InvalidCoordinates,
)
from .handlers import register_exception_handlers

__all__ = [
    "AppException", "SpotNotFound", "UserNotFound", "GuideNotFound",
    "HotelNotFound", "BookingNotFound", "UnauthorizedRole", "InvalidCredentials",
    "EmailAlreadyExists", "InvalidToken", "SpotNotApproved", "InvalidCoordinates",
    "register_exception_handlers",
]
