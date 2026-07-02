import uuid
from datetime import datetime
from pydantic import BaseModel, EmailStr
from app.core.security.permissions import Role


class UserOut(BaseModel):
    model_config = {"from_attributes": True}

    id: uuid.UUID
    email: EmailStr
    full_name: str
    full_name_ar: str | None
    role: str
    region_id: uuid.UUID | None
    avatar_url: str | None
    phone: str | None
    is_active: bool
    is_verified: bool
    created_at: datetime


class UserUpdate(BaseModel):
    full_name: str | None = None
    full_name_ar: str | None = None
    phone: str | None = None
    region_id: uuid.UUID | None = None
    avatar_url: str | None = None
