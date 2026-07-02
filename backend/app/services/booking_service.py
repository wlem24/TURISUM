from decimal import Decimal
from uuid import UUID
from datetime import date

from sqlalchemy.ext.asyncio import AsyncSession

from app.core.config import settings
from app.core.exceptions import GuideNotFound, HotelNotFound, BookingNotFound
from app.models.user import User
from app.repositories.booking_repo import BookingRepository
from app.repositories.guide_repo import GuideRepository
from app.repositories.hotel_repo import HotelRepository
from app.schemas.booking import BookingCreate
from app.models.booking import Booking


class BookingService:
    def __init__(self, session: AsyncSession):
        self._repo = BookingRepository(session)
        self._guide_repo = GuideRepository(session)
        self._hotel_repo = HotelRepository(session)
        self._session = session

    def _calculate_guide_amounts(self, daily_rate: float) -> tuple[Decimal, Decimal, Decimal]:
        total = Decimal(str(daily_rate))
        commission = (total * settings.COMMISSION_GUIDE).quantize(Decimal("0.01"))
        provider = (total - commission).quantize(Decimal("0.01"))
        return total, commission, provider

    def _calculate_hotel_amounts(self, price_per_night: float, commission_rate: float) -> tuple[Decimal, Decimal, Decimal]:
        total = Decimal(str(price_per_night))
        rate = Decimal(str(commission_rate))
        commission = (total * rate).quantize(Decimal("0.01"))
        provider = (total - commission).quantize(Decimal("0.01"))
        return total, commission, provider

    async def create_booking(self, data: BookingCreate, visitor: User) -> Booking:
        total = Decimal("0")
        commission = Decimal("0")
        provider = Decimal("0")

        if data.booking_type in ("guide", "package") and data.guide_id:
            guide = await self._guide_repo.get_by_id(data.guide_id)
            if not guide:
                raise GuideNotFound()
            t, c, p = self._calculate_guide_amounts(guide.daily_rate)
            total += t
            commission += c
            provider += p

        if data.booking_type in ("hotel", "package") and data.hotel_id:
            hotel = await self._hotel_repo.get_by_id(data.hotel_id)
            if not hotel:
                raise HotelNotFound()
            t, c, p = self._calculate_hotel_amounts(hotel.price_per_night, hotel.commission_rate)
            total += t
            commission += c
            provider += p

        booking = await self._repo.create(
            booking_type=data.booking_type,
            visitor_id=visitor.id,
            guide_id=data.guide_id,
            hotel_id=data.hotel_id,
            spot_id=data.spot_id,
            total_amount=total,
            commission_amount=commission,
            provider_amount=provider,
            status="pending",
            booking_date=data.booking_date,
            notes=data.notes,
        )
        await self._session.commit()
        return booking

    async def get_booking(self, booking_id: UUID) -> Booking:
        booking = await self._repo.get_by_id(booking_id)
        if not booking:
            raise BookingNotFound()
        return booking

    async def update_status(self, booking_id: UUID, status: str) -> Booking:
        booking = await self._repo.get_by_id(booking_id)
        if not booking:
            raise BookingNotFound()
        booking = await self._repo.update(booking, status=status)
        await self._session.commit()
        return booking

    async def list_visitor_bookings(self, visitor_id: UUID, offset: int = 0, limit: int = 20) -> list[Booking]:
        return await self._repo.list_by_visitor(visitor_id, offset=offset, limit=limit)

    async def list_guide_bookings(self, guide_id: UUID, offset: int = 0, limit: int = 20) -> list[Booking]:
        return await self._repo.list_by_guide(guide_id, offset=offset, limit=limit)
