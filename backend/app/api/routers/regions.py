from fastapi import APIRouter, Depends
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from pydantic import BaseModel
import uuid
from datetime import datetime

from app.api.dependencies import get_db
from app.models.region import Region

router = APIRouter(prefix="/regions", tags=["Regions"])


class RegionOut(BaseModel):
    model_config = {"from_attributes": True}
    id: uuid.UUID
    name_ar: str
    name_en: str
    spot_count: int
    latitude: float | None
    longitude: float | None


@router.get("", response_model=list[RegionOut])
async def list_regions(session: AsyncSession = Depends(get_db)):
    result = await session.execute(select(Region).order_by(Region.name_en))
    return [RegionOut.model_validate(r) for r in result.scalars().all()]


@router.get("/{region_id}", response_model=RegionOut)
async def get_region(region_id: uuid.UUID, session: AsyncSession = Depends(get_db)):
    result = await session.execute(select(Region).where(Region.id == region_id))
    region = result.scalar_one_or_none()
    if not region:
        from fastapi import HTTPException
        raise HTTPException(status_code=404, detail="Region not found")
    return RegionOut.model_validate(region)
