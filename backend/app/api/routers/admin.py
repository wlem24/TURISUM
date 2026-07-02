from fastapi import APIRouter, Depends, Query
from sqlalchemy import select, func
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.dependencies import get_db, require_admin
from app.models.user import User
from app.models.spot import Spot
from app.models.booking import Booking
from app.schemas.spot import SpotOut
from app.schemas.user import UserOut
from app.services.spot_service import SpotService
from app.repositories.user_repo import UserRepository
from pydantic import BaseModel

router = APIRouter(prefix="/admin", tags=["Admin"])


class DashboardStats(BaseModel):
    total_users: int
    total_spots: int
    pending_spots: int
    approved_spots: int
    total_bookings: int
    total_revenue: float


@router.get("/dashboard", response_model=DashboardStats)
async def get_dashboard(
    _: User = Depends(require_admin),
    session: AsyncSession = Depends(get_db),
):
    total_users = (await session.execute(select(func.count()).select_from(User))).scalar_one()
    total_spots = (await session.execute(select(func.count()).select_from(Spot))).scalar_one()
    pending = (await session.execute(
        select(func.count()).select_from(Spot).where(Spot.status == "pending")
    )).scalar_one()
    approved = (await session.execute(
        select(func.count()).select_from(Spot).where(Spot.status == "approved")
    )).scalar_one()
    total_bookings = (await session.execute(select(func.count()).select_from(Booking))).scalar_one()
    revenue_result = await session.execute(
        select(func.sum(Booking.commission_amount)).where(Booking.status == "completed")
    )
    total_revenue = float(revenue_result.scalar_one() or 0)

    return DashboardStats(
        total_users=total_users,
        total_spots=total_spots,
        pending_spots=pending,
        approved_spots=approved,
        total_bookings=total_bookings,
        total_revenue=total_revenue,
    )


@router.get("/spots/pending", response_model=list[SpotOut])
async def list_pending_spots(
    offset: int = Query(0, ge=0),
    limit: int = Query(20, ge=1, le=100),
    _: User = Depends(require_admin),
    session: AsyncSession = Depends(get_db),
):
    service = SpotService(session)
    spots = await service.list_pending(offset=offset, limit=limit)
    return [SpotOut.model_validate(s) for s in spots]


@router.get("/users", response_model=list[UserOut])
async def list_users(
    role: str | None = Query(None),
    offset: int = Query(0, ge=0),
    limit: int = Query(20, ge=1, le=100),
    _: User = Depends(require_admin),
    session: AsyncSession = Depends(get_db),
):
    repo = UserRepository(session)
    if role:
        users = await repo.list_by_role(role, offset=offset, limit=limit)
    else:
        users = await repo.list_all(offset=offset, limit=limit)
    return [UserOut.model_validate(u) for u in users]


@router.patch("/users/{user_id}/deactivate", response_model=UserOut)
async def deactivate_user(
    user_id: str,
    _: User = Depends(require_admin),
    session: AsyncSession = Depends(get_db),
):
    import uuid as _uuid
    repo = UserRepository(session)
    user = await repo.get_by_id(_uuid.UUID(user_id))
    if not user:
        from app.core.exceptions import UserNotFound
        raise UserNotFound(user_id)
    user = await repo.update(user, is_active=False)
    await session.commit()
    return UserOut.model_validate(user)
