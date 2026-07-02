import uuid
from datetime import datetime
from pydantic import BaseModel


class HotelCreate(BaseModel):
    name_ar: str
    name_en: str | None = None
    region_id: uuid.UUID
    latitude: float
    longitude: float
    stars: int = 3
    price_per_night: float
    commission_rate: float = 0.10
    contact_phone: str | None = None
    website_url: str | None = None


class HotelOut(BaseModel):
    model_config = {"from_attributes": True}

    id: uuid.UUID
    name_ar: str
    name_en: str | None
    region_id: uuid.UUID
    latitude: float
    longitude: float
    stars: int
    price_per_night: float
    rating: float
    commission_rate: float
    contact_phone: str | None
    website_url: str | None
    created_at: datetime
