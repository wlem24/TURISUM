from uuid import UUID
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.user import User
from .base import BaseRepository


class UserRepository(BaseRepository[User]):
    def __init__(self, session: AsyncSession):
        super().__init__(User, session)

    async def get_by_email(self, email: str) -> User | None:
        result = await self.session.execute(select(User).where(User.email == email))
        return result.scalar_one_or_none()

    async def get_active_by_id(self, user_id: UUID) -> User | None:
        result = await self.session.execute(
            select(User).where(User.id == user_id, User.is_active == True)
        )
        return result.scalar_one_or_none()

    async def list_by_role(self, role: str, offset: int = 0, limit: int = 20) -> list[User]:
        result = await self.session.execute(
            select(User).where(User.role == role).offset(offset).limit(limit)
        )
        return list(result.scalars().all())
