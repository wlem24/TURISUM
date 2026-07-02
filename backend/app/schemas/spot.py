import uuid
from datetime import datetime
from pydantic import BaseModel, field_validator, model_validator
from typing import Literal

SAUDI_LAT_MIN, SAUDI_LAT_MAX = 16.0, 32.5
SAUDI_LNG_MIN, SAUDI_LNG_MAX = 34.5, 56.0

SpotType = Literal["archaeological", "nature", "waterfall", "desert", "coastal", "village"]
AccessDifficulty = Literal["easy", "medium", "hard"]
SpotStatus = Literal["pending", "approved", "rejected"]


class SpotImageOut(BaseModel):
    model_config = {"from_attributes": True}
    id: uuid.UUID
    image_url: str
    is_primary: bool


class SpotCreate(BaseModel):
    name_ar: str
    name_en: str | None = None
    description_ar: str
    description_en: str | None = None
    region_id: uuid.UUID
    spot_type: SpotType
    latitude: float
    longitude: float
    access_difficulty: AccessDifficulty = "medium"
    best_season: str | None = None
    walking_distance_km: float | None = None
    visit_duration_hours: float | None = None
    requires_4x4: bool = False
    has_phone_signal: bool = True

    @field_validator("latitude")
    @classmethod
    def validate_lat(cls, v: float) -> float:
        if not (SAUDI_LAT_MIN <= v <= SAUDI_LAT_MAX):
            raise ValueError(f"Latitude must be within Saudi Arabia ({SAUDI_LAT_MIN}–{SAUDI_LAT_MAX})")
        return v

    @field_validator("longitude")
    @classmethod
    def validate_lng(cls, v: float) -> float:
        if not (SAUDI_LNG_MIN <= v <= SAUDI_LNG_MAX):
            raise ValueError(f"Longitude must be within Saudi Arabia ({SAUDI_LNG_MIN}–{SAUDI_LNG_MAX})")
        return v


class SpotUpdate(BaseModel):
    name_ar: str | None = None
    name_en: str | None = None
    description_ar: str | None = None
    description_en: str | None = None
    access_difficulty: AccessDifficulty | None = None
    best_season: str | None = None
    walking_distance_km: float | None = None
    visit_duration_hours: float | None = None
    requires_4x4: bool | None = None
    has_phone_signal: bool | None = None


class SpotOut(BaseModel):
    model_config = {"from_attributes": True}

    id: uuid.UUID
    name_ar: str
    name_en: str | None
    description_ar: str
    description_en: str | None
    region_id: uuid.UUID
    spot_type: str
    latitude: float
    longitude: float
    access_difficulty: str
    best_season: str | None
    walking_distance_km: float | None
    visit_duration_hours: float | None
    requires_4x4: bool
    has_phone_signal: bool
    status: str
    view_count: int
    ai_quality_score: float | None
    images: list[SpotImageOut] = []
    created_at: datetime


class SpotApproval(BaseModel):
    approved: bool
    rejection_reason: str | None = None


class SpotListParams(BaseModel):
    region_id: uuid.UUID | None = None
    spot_type: SpotType | None = None
    access_difficulty: AccessDifficulty | None = None
    requires_4x4: bool | None = None
    page: int = 1
    page_size: int = 20
