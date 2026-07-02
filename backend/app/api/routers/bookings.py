from uuid import UUID
from fastapi import APIRouter, Depends, Query
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.dependencies import get_db, get_current_user
from app.schemas.booking import BookingCreate, BookingOut, BookingStatusUpdate
from app.services.booking_service import BookingService
from app.services.notification_service import NotificationService
from app.models.user import User

router = APIRouter(prefix="/bookings", tags=["Bookings"])


@router.post("", response_model=BookingOut, status_code=201)
async def create_booking(
    data: BookingCreate,
    current_user: User = Depends(get_current_user),
    session: AsyncSession = Depends(get_db),
):
    service = BookingService(session)
    booking = await service.create_booking(data, current_user)

    notif = NotificationService(session)
    await notif.notify_booking_confirmed(current_user.id)
    await session.commit()

    return BookingOut.model_validate(booking)


@router.get("/me", response_model=list[BookingOut])
async def list_my_bookings(
    offset: int = Query(0, ge=0),
    limit: int = Query(20, ge=1, le=100),
    current_user: User = Depends(get_current_user),
    session: AsyncSession = Depends(get_db),
):
    service = BookingService(session)
    bookings = await service.list_visitor_bookings(current_user.id, offset=offset, limit=limit)
    return [BookingOut.model_validate(b) for b in bookings]


@router.get("/{booking_id}", response_model=BookingOut)
async def get_booking(
    booking_id: UUID,
    current_user: User = Depends(get_current_user),
    session: AsyncSession = Depends(get_db),
):
    service = BookingService(session)
    booking = await service.get_booking(booking_id)
    return BookingOut.model_validate(booking)


@router.patch("/{booking_id}/status", response_model=BookingOut)
async def update_booking_status(
    booking_id: UUID,
    data: BookingStatusUpdate,
    current_user: User = Depends(get_current_user),
    session: AsyncSession = Depends(get_db),
):
    service = BookingService(session)
    booking = await service.update_status(booking_id, data.status)
    return BookingOut.model_validate(booking)
