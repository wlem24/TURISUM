from uuid import UUID
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.hotel import Hotel
from .base import BaseRepository


class HotelRepository(BaseRepository[Hotel]):
    def __init__(self, session: AsyncSession):
        super().__init__(Hotel, session)

    async def list_by_region(self, region_id: UUID, offset: int = 0, limit: int = 20) -> list[Hotel]:
        result = await self.session.execute(
            select(Hotel)
            .where(Hotel.region_id == region_id)
            .order_by(Hotel.rating.desc())
            .offset(offset).limit(limit)
        )
        return list(result.scalars().all())

    async def list_nearby(self, lat: float, lng: float, radius_km: float = 50, limit: int = 10) -> list[Hotel]:
        # Haversine approximation via bounding box first, then sort by distance
        lat_delta = radius_km / 111.0
        lng_delta = radius_km / (111.0 * abs(lat) + 0.01)
        result = await self.session.execute(
            select(Hotel).where(
                Hotel.latitude.between(lat - lat_delta, lat + lat_delta),
                Hotel.longitude.between(lng - lng_delta, lng + lng_delta),
            ).limit(limit)
        )
        return list(result.scalars().all())
