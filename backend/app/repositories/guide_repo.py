from uuid import UUID
from sqlalchemy import select
from sqlalchemy.orm import selectinload
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.guide import Guide
from .base import BaseRepository


class GuideRepository(BaseRepository[Guide]):
    def __init__(self, session: AsyncSession):
        super().__init__(Guide, session)

    async def get_by_user_id(self, user_id: UUID) -> Guide | None:
        result = await self.session.execute(
            select(Guide).where(Guide.user_id == user_id)
        )
        return result.scalar_one_or_none()

    async def list_available(
        self,
        region_id: UUID | None = None,
        offset: int = 0,
        limit: int = 20,
    ) -> list[Guide]:
        q = select(Guide).where(Guide.is_available == True)
        if region_id:
            q = q.where(Guide.region_id == region_id)
        q = q.order_by(Guide.rating.desc()).offset(offset).limit(limit)
        result = await self.session.execute(q)
        return list(result.scalars().all())
