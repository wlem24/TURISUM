from uuid import UUID
from fastapi import APIRouter, Depends, Query
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.dependencies import get_db, get_current_user, require_guide, require_admin
from app.schemas.guide import GuideCreate, GuideUpdate, GuideOut
from app.services.guide_service import GuideService
from app.models.user import User

router = APIRouter(prefix="/guides", tags=["Guides"])


@router.get("", response_model=list[GuideOut])
async def list_guides(
    region_id: UUID | None = Query(None),
    offset: int = Query(0, ge=0),
    limit: int = Query(20, ge=1, le=100),
    session: AsyncSession = Depends(get_db),
):
    service = GuideService(session)
    guides = await service.list_guides(region_id=region_id, offset=offset, limit=limit)
    return [GuideOut.model_validate(g) for g in guides]


@router.post("", response_model=GuideOut, status_code=201)
async def create_guide_profile(
    data: GuideCreate,
    current_user: User = Depends(require_guide),
    session: AsyncSession = Depends(get_db),
):
    service = GuideService(session)
    guide = await service.create_guide_profile(data, current_user)
    return GuideOut.model_validate(guide)


@router.get("/me", response_model=GuideOut)
async def get_my_guide_profile(
    current_user: User = Depends(require_guide),
    session: AsyncSession = Depends(get_db),
):
    from app.core.exceptions import GuideNotFound
    service = GuideService(session)
    guide = await service.get_guide_by_user(current_user.id)
    if not guide:
        raise GuideNotFound()
    return GuideOut.model_validate(guide)


@router.get("/{guide_id}", response_model=GuideOut)
async def get_guide(guide_id: UUID, session: AsyncSession = Depends(get_db)):
    service = GuideService(session)
    guide = await service.get_guide(guide_id)
    return GuideOut.model_validate(guide)


@router.patch("/{guide_id}", response_model=GuideOut)
async def update_guide(
    guide_id: UUID,
    data: GuideUpdate,
    current_user: User = Depends(get_current_user),
    session: AsyncSession = Depends(get_db),
):
    service = GuideService(session)
    guide = await service.update_guide(guide_id, data, current_user)
    return GuideOut.model_validate(guide)


@router.post("/{guide_id}/verify", response_model=GuideOut)
async def verify_guide(
    guide_id: UUID,
    _: User = Depends(require_admin),
    session: AsyncSession = Depends(get_db),
):
    service = GuideService(session)
    guide = await service.verify_guide(guide_id)
    return GuideOut.model_validate(guide)
