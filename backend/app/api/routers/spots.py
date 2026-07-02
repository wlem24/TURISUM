from uuid import UUID
from fastapi import APIRouter, Depends, Query
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.dependencies import get_db, get_current_user, require_local, require_admin
from app.schemas.spot import SpotCreate, SpotUpdate, SpotOut, SpotApproval
from app.schemas import SpotListParams
from app.services.spot_service import SpotService
from app.services.notification_service import NotificationService
from app.utils.pagination import PaginatedResponse
from app.models.user import User

router = APIRouter(prefix="/spots", tags=["Spots"])


@router.get("", response_model=PaginatedResponse[SpotOut])
async def list_spots(
    region_id: UUID | None = Query(None),
    spot_type: str | None = Query(None),
    access_difficulty: str | None = Query(None),
    requires_4x4: bool | None = Query(None),
    page: int = Query(1, ge=1),
    page_size: int = Query(20, ge=1, le=100),
    session: AsyncSession = Depends(get_db),
):
    service = SpotService(session)
    params = SpotListParams(
        region_id=region_id,
        spot_type=spot_type or None,
        access_difficulty=access_difficulty or None,
        requires_4x4=requires_4x4,
        page=page,
        page_size=page_size,
    )
    spots, total = await service.list_spots(params)
    return PaginatedResponse.build(
        items=[SpotOut.model_validate(s) for s in spots],
        total=total,
        page=page,
        page_size=page_size,
    )


@router.post("", response_model=SpotOut, status_code=201)
async def submit_spot(
    data: SpotCreate,
    current_user: User = Depends(require_local),
    session: AsyncSession = Depends(get_db),
):
    service = SpotService(session)
    spot = await service.submit_spot(data, current_user)

    # Kick off AI analysis asynchronously via Celery if configured
    try:
        from app.tasks.ai_tasks import analyze_spot_task
        analyze_spot_task.delay(str(spot.id))
    except Exception:
        pass

    return SpotOut.model_validate(spot)


@router.get("/{spot_id}", response_model=SpotOut)
async def get_spot(spot_id: UUID, session: AsyncSession = Depends(get_db)):
    service = SpotService(session)
    spot = await service.get_spot(spot_id)
    return SpotOut.model_validate(spot)


@router.patch("/{spot_id}", response_model=SpotOut)
async def update_spot(
    spot_id: UUID,
    data: SpotUpdate,
    current_user: User = Depends(get_current_user),
    session: AsyncSession = Depends(get_db),
):
    service = SpotService(session)
    spot = await service.update_spot(spot_id, data, current_user)
    return SpotOut.model_validate(spot)


@router.post("/{spot_id}/approve", response_model=SpotOut)
async def approve_spot(
    spot_id: UUID,
    approval: SpotApproval,
    admin: User = Depends(require_admin),
    session: AsyncSession = Depends(get_db),
):
    service = SpotService(session)
    spot = await service.approve_spot(spot_id, approval, admin)

    notif_service = NotificationService(session)
    if spot.submitted_by_id:
        if approval.approved:
            await notif_service.notify_spot_approved(spot.submitted_by_id, spot.name_ar)
        else:
            await notif_service.notify_spot_rejected(
                spot.submitted_by_id, spot.name_ar, approval.rejection_reason or ""
            )
    await session.commit()
    return SpotOut.model_validate(spot)
