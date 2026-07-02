from uuid import UUID
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.booking import Booking
from .base import BaseRepository


class BookingRepository(BaseRepository[Booking]):
    def __init__(self, session: AsyncSession):
        super().__init__(Booking, session)

    async def list_by_visitor(self, visitor_id: UUID, offset: int = 0, limit: int = 20) -> list[Booking]:
        result = await self.session.execute(
            select(Booking)
            .where(Booking.visitor_id == visitor_id)
            .order_by(Booking.created_at.desc())
            .offset(offset).limit(limit)
        )
        return list(result.scalars().all())

    async def list_by_guide(self, guide_id: UUID, offset: int = 0, limit: int = 20) -> list[Booking]:
        result = await self.session.execute(
            select(Booking)
            .where(Booking.guide_id == guide_id)
            .order_by(Booking.created_at.desc())
            .offset(offset).limit(limit)
        )
        return list(result.scalars().all())
