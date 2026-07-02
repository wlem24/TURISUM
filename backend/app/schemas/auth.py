from pydantic import BaseModel, EmailStr, field_validator
from app.core.security.permissions import Role


class RegisterRequest(BaseModel):
    email: EmailStr
    password: str
    full_name: str
    full_name_ar: str | None = None
    role: Role = Role.VISITOR
    phone: str | None = None

    @field_validator("password")
    @classmethod
    def password_min_length(cls, v: str) -> str:
        if len(v) < 8:
            raise ValueError("Password must be at least 8 characters")
        return v

    @field_validator("role")
    @classmethod
    def role_must_be_registerable(cls, v: Role) -> Role:
        if v in (Role.ADMIN, Role.MINISTRY):
            raise ValueError("Cannot self-register as admin or ministry")
        return v


class LoginRequest(BaseModel):
    email: EmailStr
    password: str


class TokenResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"
    role: str
    user_id: str


class RefreshRequest(BaseModel):
    refresh_token: str
