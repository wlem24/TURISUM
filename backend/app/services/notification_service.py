from uuid import UUID
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from app.models.notification import Notification
from app.repositories.base import BaseRepository


class NotificationService:
    def __init__(self, session: AsyncSession):
        self._session = session

    async def create(
        self,
        user_id: UUID,
        type: str,
        title_ar: str,
        title_en: str,
        message_ar: str,
        message_en: str,
    ) -> Notification:
        n = Notification(
            user_id=user_id,
            type=type,
            title_ar=title_ar,
            title_en=title_en,
            message_ar=message_ar,
            message_en=message_en,
        )
        self._session.add(n)
        await self._session.flush()
        return n

    async def get_user_notifications(self, user_id: UUID, unread_only: bool = False) -> list[Notification]:
        q = select(Notification).where(Notification.user_id == user_id)
        if unread_only:
            q = q.where(Notification.is_read == False)
        q = q.order_by(Notification.created_at.desc()).limit(50)
        result = await self._session.execute(q)
        return list(result.scalars().all())

    async def mark_read(self, notification_id: UUID, user_id: UUID) -> None:
        result = await self._session.execute(
            select(Notification).where(
                Notification.id == notification_id,
                Notification.user_id == user_id,
            )
        )
        n = result.scalar_one_or_none()
        if n:
            n.is_read = True
            await self._session.flush()

    async def notify_spot_approved(self, user_id: UUID, spot_name: str) -> None:
        await self.create(
            user_id=user_id,
            type="spot_approved",
            title_ar="تمت الموافقة على الموقع",
            title_en="Spot Approved",
            message_ar=f"تمت الموافقة على موقعك '{spot_name}' وهو الآن متاح للجميع.",
            message_en=f"Your spot '{spot_name}' has been approved and is now live.",
        )

    async def notify_spot_rejected(self, user_id: UUID, spot_name: str, reason: str) -> None:
        await self.create(
            user_id=user_id,
            type="spot_rejected",
            title_ar="تم رفض الموقع",
            title_en="Spot Rejected",
            message_ar=f"تم رفض موقعك '{spot_name}'. السبب: {reason}",
            message_en=f"Your spot '{spot_name}' was rejected. Reason: {reason}",
        )

    async def notify_booking_confirmed(self, user_id: UUID) -> None:
        await self.create(
            user_id=user_id,
            type="booking_confirmed",
            title_ar="تم تأكيد الحجز",
            title_en="Booking Confirmed",
            message_ar="تم تأكيد حجزك بنجاح.",
            message_en="Your booking has been confirmed successfully.",
        )
