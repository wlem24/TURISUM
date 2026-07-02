from sqlalchemy.ext.asyncio import AsyncSession

from app.core.security import (
    hash_password, verify_password,
    create_access_token, create_refresh_token, verify_refresh_token,
)
from app.core.exceptions import (
    InvalidCredentials, EmailAlreadyExists, InvalidToken, UserNotFound,
)
from app.repositories.user_repo import UserRepository
from app.schemas.auth import RegisterRequest, TokenResponse
from app.models.user import User


class AuthService:
    def __init__(self, session: AsyncSession):
        self._repo = UserRepository(session)
        self._session = session

    async def register(self, data: RegisterRequest) -> User:
        existing = await self._repo.get_by_email(data.email)
        if existing:
            raise EmailAlreadyExists(data.email)

        hashed = hash_password(data.password)
        user = await self._repo.create(
            email=data.email,
            hashed_password=hashed,
            full_name=data.full_name,
            full_name_ar=data.full_name_ar,
            role=data.role.value,
            phone=data.phone,
        )
        await self._session.commit()
        return user

    async def login(self, email: str, password: str) -> dict:
        user = await self._repo.get_by_email(email)
        if not user or not verify_password(password, user.hashed_password):
            raise InvalidCredentials()
        if not user.is_active:
            raise InvalidCredentials()

        access = create_access_token(user.id, user.role)
        refresh = create_refresh_token(user.id)
        return {
            "access_token": access,
            "refresh_token": refresh,
            "token_type": "bearer",
            "role": user.role,
            "user_id": str(user.id),
        }

    async def refresh(self, refresh_token: str) -> dict:
        payload = verify_refresh_token(refresh_token)
        if not payload:
            raise InvalidToken()

        user_id = payload.get("sub")
        user = await self._repo.get_active_by_id(user_id)
        if not user:
            raise UserNotFound(user_id)

        access = create_access_token(user.id, user.role)
        new_refresh = create_refresh_token(user.id)
        return {
            "access_token": access,
            "refresh_token": new_refresh,
            "token_type": "bearer",
            "role": user.role,
            "user_id": str(user.id),
        }
