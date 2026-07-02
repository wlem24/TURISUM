from datetime import datetime, timedelta, timezone
from uuid import UUID

from jose import JWTError, jwt

from app.core.config import settings


def create_access_token(user_id: UUID, role: str) -> str:
    expire = datetime.now(timezone.utc) + timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    payload = {"sub": str(user_id), "role": role, "type": "access", "exp": expire}
    return jwt.encode(payload, settings.SECRET_KEY, algorithm=settings.ALGORITHM)


def create_refresh_token(user_id: UUID) -> str:
    expire = datetime.now(timezone.utc) + timedelta(days=settings.REFRESH_TOKEN_EXPIRE_DAYS)
    payload = {"sub": str(user_id), "type": "refresh", "exp": expire}
    return jwt.encode(payload, settings.SECRET_KEY, algorithm=settings.ALGORITHM)


def decode_token(token: str) -> dict:
    try:
        payload = jwt.decode(token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])
        return payload
    except JWTError:
        return {}


def verify_access_token(token: str) -> dict | None:
    payload = decode_token(token)
    if not payload or payload.get("type") != "access":
        return None
    return payload


def verify_refresh_token(token: str) -> dict | None:
    payload = decode_token(token)
    if not payload or payload.get("type") != "refresh":
        return None
    return payload
