from uuid import UUID
from sqlalchemy import select, func, update
from sqlalchemy.orm import selectinload
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.region import Region
from app.models.spot import Spot, SpotImage
from .base import BaseRepository


class SpotRepository(BaseRepository[Spot]):
    def __init__(self, session: AsyncSession):
        super().__init__(Spot, session)

    async def get_with_images(self, spot_id: UUID) -> Spot | None:
        result = await self.session.execute(
            select(Spot)
            .options(selectinload(Spot.images))
            .where(Spot.id == spot_id)
        )
        return result.scalar_one_or_none()

    async def list_approved(
        self,
        region_id: UUID | None = None,
        spot_type: str | None = None,
        access_difficulty: str | None = None,
        requires_4x4: bool | None = None,
        offset: int = 0,
        limit: int = 20,
    ) -> tuple[list[Spot], int]:
        q = select(Spot).options(selectinload(Spot.images)).where(Spot.status == "approved")
        count_q = select(func.count()).select_from(Spot).where(Spot.status == "approved")

        if region_id:
            q = q.where(Spot.region_id == region_id)
            count_q = count_q.where(Spot.region_id == region_id)
        if spot_type:
            q = q.where(Spot.spot_type == spot_type)
            count_q = count_q.where(Spot.spot_type == spot_type)
        if access_difficulty:
            q = q.where(Spot.access_difficulty == access_difficulty)
            count_q = count_q.where(Spot.access_difficulty == access_difficulty)
        if requires_4x4 is not None:
            q = q.where(Spot.requires_4x4 == requires_4x4)
            count_q = count_q.where(Spot.requires_4x4 == requires_4x4)

        total_result = await self.session.execute(count_q)
        total = total_result.scalar_one()

        q = q.order_by(Spot.created_at.desc()).offset(offset).limit(limit)
        result = await self.session.execute(q)
        return list(result.scalars().all()), total

    async def list_pending(self, offset: int = 0, limit: int = 20) -> list[Spot]:
        result = await self.session.execute(
            select(Spot)
            .options(selectinload(Spot.images))
            .where(Spot.status == "pending")
            .order_by(Spot.created_at.asc())
            .offset(offset).limit(limit)
        )
        return list(result.scalars().all())

    async def increment_view(self, spot_id: UUID) -> None:
        await self.session.execute(
            update(Spot).where(Spot.id == spot_id).values(view_count=Spot.view_count + 1)
        )

    async def adjust_region_spot_count(self, region_id: UUID, delta: int) -> None:
        await self.session.execute(
            update(Region)
            .where(Region.id == region_id)
            .values(spot_count=func.greatest(Region.spot_count + delta, 0))
        )

    async def vector_search(self, embedding: list[float], top_k: int = 5, region_id: UUID | None = None) -> list[Spot]:
        from pgvector.sqlalchemy import Vector
        q = select(Spot).where(Spot.status == "approved", Spot.embedding.isnot(None))
        if region_id:
            q = q.where(Spot.region_id == region_id)
        q = q.order_by(Spot.embedding.cosine_distance(embedding)).limit(top_k)
        result = await self.session.execute(q)
        return list(result.scalars().all())
