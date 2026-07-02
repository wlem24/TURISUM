import uuid
from datetime import datetime, date
from decimal import Decimal
from typing import Literal
from pydantic import BaseModel

BookingType = Literal["guide", "hotel", "package"]
BookingStatus = Literal["pending", "confirmed", "completed", "cancelled"]


class BookingCreate(BaseModel):
    booking_type: BookingType
    guide_id: uuid.UUID | None = None
    hotel_id: uuid.UUID | None = None
    spot_id: uuid.UUID | None = None
    booking_date: date
    notes: str | None = None


class BookingOut(BaseModel):
    model_config = {"from_attributes": True}

    id: uuid.UUID
    booking_type: str
    visitor_id: uuid.UUID
    guide_id: uuid.UUID | None
    hotel_id: uuid.UUID | None
    spot_id: uuid.UUID | None
    total_amount: Decimal
    commission_amount: Decimal
    provider_amount: Decimal
    status: str
    booking_date: date
    notes: str | None
    created_at: datetime


class BookingStatusUpdate(BaseModel):
    status: BookingStatus
