from uuid import UUID
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.exceptions import GuideNotFound, UnauthorizedRole
from app.core.security.permissions import Role
from app.models.user import User
from app.repositories.guide_repo import GuideRepository
from app.schemas.guide import GuideCreate, GuideUpdate
from app.models.guide import Guide


class GuideService:
    def __init__(self, session: AsyncSession):
        self._repo = GuideRepository(session)
        self._session = session

    async def create_guide_profile(self, data: GuideCreate, user: User) -> Guide:
        guide = await self._repo.create(
            user_id=user.id,
            bio_ar=data.bio_ar,
            bio_en=data.bio_en,
            region_id=data.region_id,
            specializations=data.specializations,
            languages=data.languages,
            daily_rate=data.daily_rate,
            years_experience=data.years_experience,
        )
        await self._session.commit()
        return guide

    async def get_guide(self, guide_id: UUID) -> Guide:
        guide = await self._repo.get_by_id(guide_id)
        if not guide:
            raise GuideNotFound()
        return guide

    async def get_guide_by_user(self, user_id: UUID) -> Guide | None:
        return await self._repo.get_by_user_id(user_id)

    async def update_guide(self, guide_id: UUID, data: GuideUpdate, user: User) -> Guide:
        guide = await self._repo.get_by_id(guide_id)
        if not guide:
            raise GuideNotFound()
        if guide.user_id != user.id and user.role not in (Role.ADMIN, Role.MINISTRY):
            raise UnauthorizedRole(Role.ADMIN)

        updates = data.model_dump(exclude_none=True)
        guide = await self._repo.update(guide, **updates)
        await self._session.commit()
        return guide

    async def list_guides(self, region_id: UUID | None = None, offset: int = 0, limit: int = 20) -> list[Guide]:
        return await self._repo.list_available(region_id=region_id, offset=offset, limit=limit)

    async def verify_guide(self, guide_id: UUID) -> Guide:
        guide = await self._repo.get_by_id(guide_id)
        if not guide:
            raise GuideNotFound()
        guide = await self._repo.update(guide, is_verified=True)
        await self._session.commit()
        return guide
