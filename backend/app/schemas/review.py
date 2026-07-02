import uuid
from datetime import datetime
from pydantic import BaseModel, field_validator


class ReviewCreate(BaseModel):
    spot_id: uuid.UUID | None = None
    guide_id: uuid.UUID | None = None
    rating: int
    comment_ar: str | None = None
    comment_en: str | None = None

    @field_validator("rating")
    @classmethod
    def validate_rating(cls, v: int) -> int:
        if not (1 <= v <= 5):
            raise ValueError("Rating must be between 1 and 5")
        return v


class ReviewOut(BaseModel):
    model_config = {"from_attributes": True}

    id: uuid.UUID
    spot_id: uuid.UUID | None
    guide_id: uuid.UUID | None
    reviewer_id: uuid.UUID
    rating: int
    comment_ar: str | None
    comment_en: str | None
    created_at: datetime
