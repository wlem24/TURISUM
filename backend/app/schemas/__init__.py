from .auth import RegisterRequest, LoginRequest, TokenResponse, RefreshRequest
from .user import UserOut, UserUpdate
from .spot import SpotCreate, SpotUpdate, SpotOut, SpotApproval, SpotListParams, SpotImageOut
from .guide import GuideCreate, GuideUpdate, GuideOut
from .hotel import HotelCreate, HotelOut
from .booking import BookingCreate, BookingOut, BookingStatusUpdate
from .review import ReviewCreate, ReviewOut
from .ai import ChatMessage, ChatResponse, SpotSuggestionQuery, SpotSuggestion, AIChatHistoryOut

__all__ = [
    "RegisterRequest", "LoginRequest", "TokenResponse", "RefreshRequest",
    "UserOut", "UserUpdate",
    "SpotCreate", "SpotUpdate", "SpotOut", "SpotApproval", "SpotListParams", "SpotImageOut",
    "GuideCreate", "GuideUpdate", "GuideOut",
    "HotelCreate", "HotelOut",
    "BookingCreate", "BookingOut", "BookingStatusUpdate",
    "ReviewCreate", "ReviewOut",
    "ChatMessage", "ChatResponse", "SpotSuggestionQuery", "SpotSuggestion", "AIChatHistoryOut",
]
