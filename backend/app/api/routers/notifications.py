from uuid import UUID
from fastapi import APIRouter, Depends, Query
from sqlalchemy.ext.asyncio import AsyncSession
from pydantic import BaseModel
from datetime import datetime

from app.api.dependencies import get_db, get_current_user
from app.services.notification_service import NotificationService
from app.models.user import User

router = APIRouter(prefix="/notifications", tags=["Notifications"])


class NotificationOut(BaseModel):
    model_config = {"from_attributes": True}
    id: UUID
    type: str
    title_ar: str
    title_en: str
    message_ar: str
    message_en: str
    is_read: bool
    created_at: datetime


@router.get("", response_model=list[NotificationOut])
async def get_notifications(
    unread_only: bool = Query(False),
    current_user: User = Depends(get_current_user),
    session: AsyncSession = Depends(get_db),
):
    service = NotificationService(session)
    notifications = await service.get_user_notifications(current_user.id, unread_only)
    return [NotificationOut.model_validate(n) for n in notifications]


@router.patch("/{notification_id}/read", status_code=204)
async def mark_notification_read(
    notification_id: UUID,
    current_user: User = Depends(get_current_user),
    session: AsyncSession = Depends(get_db),
):
    service = NotificationService(session)
    await service.mark_read(notification_id, current_user.id)
    await session.commit()
