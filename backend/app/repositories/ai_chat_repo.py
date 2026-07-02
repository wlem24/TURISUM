from uuid import UUID
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.ai_chat import AIChatHistory
from .base import BaseRepository


class AIChatRepository(BaseRepository[AIChatHistory]):
    def __init__(self, session: AsyncSession):
        super().__init__(AIChatHistory, session)

    async def get_user_history(self, user_id: UUID, limit: int = 20) -> list[AIChatHistory]:
        result = await self.session.execute(
            select(AIChatHistory)
            .where(AIChatHistory.user_id == user_id)
            .order_by(AIChatHistory.created_at.asc())
            .limit(limit)
        )
        return list(result.scalars().all())
