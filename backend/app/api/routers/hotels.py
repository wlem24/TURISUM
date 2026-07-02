from uuid import UUID
from fastapi import APIRouter, Depends, Query
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.dependencies import get_db, require_admin
from app.schemas.hotel import HotelCreate, HotelOut
from app.services.hotel_service import HotelService
from app.models.user import User

router = APIRouter(prefix="/hotels", tags=["Hotels"])


@router.get("", response_model=list[HotelOut])
async def list_hotels(
    region_id: UUID | None = Query(None),
    offset: int = Query(0, ge=0),
    limit: int = Query(20, ge=1, le=100),
    session: AsyncSession = Depends(get_db),
):
    service = HotelService(session)
    hotels = await service.list_hotels(region_id=region_id, offset=offset, limit=limit)
    return [HotelOut.model_validate(h) for h in hotels]


@router.get("/nearby", response_model=list[HotelOut])
async def get_nearby_hotels(
    lat: float = Query(...),
    lng: float = Query(...),
    radius_km: float = Query(50.0),
    session: AsyncSession = Depends(get_db),
):
    service = HotelService(session)
    hotels = await service.list_nearby(lat, lng, radius_km)
    return [HotelOut.model_validate(h) for h in hotels]


@router.post("", response_model=HotelOut, status_code=201)
async def create_hotel(
    data: HotelCreate,
    _: User = Depends(require_admin),
    session: AsyncSession = Depends(get_db),
):
    service = HotelService(session)
    hotel = await service.create_hotel(data)
    return HotelOut.model_validate(hotel)


@router.get("/{hotel_id}", response_model=HotelOut)
async def get_hotel(hotel_id: UUID, session: AsyncSession = Depends(get_db)):
    service = HotelService(session)
    hotel = await service.get_hotel(hotel_id)
    return HotelOut.model_validate(hotel)
