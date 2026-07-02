from uuid import UUID
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.exceptions import HotelNotFound
from app.repositories.hotel_repo import HotelRepository
from app.schemas.hotel import HotelCreate
from app.models.hotel import Hotel


class HotelService:
    def __init__(self, session: AsyncSession):
        self._repo = HotelRepository(session)
        self._session = session

    async def create_hotel(self, data: HotelCreate) -> Hotel:
        hotel = await self._repo.create(**data.model_dump())
        await self._session.commit()
        return hotel

    async def get_hotel(self, hotel_id: UUID) -> Hotel:
        hotel = await self._repo.get_by_id(hotel_id)
        if not hotel:
            raise HotelNotFound()
        return hotel

    async def list_hotels(self, region_id: UUID | None = None, offset: int = 0, limit: int = 20) -> list[Hotel]:
        if region_id:
            return await self._repo.list_by_region(region_id, offset=offset, limit=limit)
        return await self._repo.list_all(offset=offset, limit=limit)

    async def list_nearby(self, lat: float, lng: float, radius_km: float = 50) -> list[Hotel]:
        return await self._repo.list_nearby(lat, lng, radius_km)
