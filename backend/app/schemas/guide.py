import uuid
from datetime import datetime
from pydantic import BaseModel


class GuideCreate(BaseModel):
    bio_ar: str | None = None
    bio_en: str | None = None
    region_id: uuid.UUID
    specializations: list[str] = []
    languages: list[str] = ["ar"]
    daily_rate: float
    years_experience: int = 0


class GuideUpdate(BaseModel):
    bio_ar: str | None = None
    bio_en: str | None = None
    region_id: uuid.UUID | None = None
    specializations: list[str] | None = None
    languages: list[str] | None = None
    daily_rate: float | None = None
    years_experience: int | None = None
    is_available: bool | None = None


class GuideOut(BaseModel):
    model_config = {"from_attributes": True}

    id: uuid.UUID
    user_id: uuid.UUID
    bio_ar: str | None
    bio_en: str | None
    region_id: uuid.UUID
    specializations: list[str] | None
    languages: list[str] | None
    daily_rate: float
    rating: float
    review_count: int
    is_available: bool
    is_verified: bool
    years_experience: int
    created_at: datetime
