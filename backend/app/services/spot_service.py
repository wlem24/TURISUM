from uuid import UUID
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.exceptions import SpotNotFound, UnauthorizedRole
from app.core.security.permissions import Role
from app.models.user import User
from app.repositories.spot_repo import SpotRepository
from app.repositories.user_repo import UserRepository
from app.schemas.spot import SpotCreate, SpotUpdate, SpotApproval, SpotListParams
from app.models.spot import Spot


class SpotService:
    def __init__(self, session: AsyncSession):
        self._repo = SpotRepository(session)
        self._session = session

    async def submit_spot(self, data: SpotCreate, submitter: User) -> Spot:
        spot = await self._repo.create(
            name_ar=data.name_ar,
            name_en=data.name_en,
            description_ar=data.description_ar,
            description_en=data.description_en,
            region_id=data.region_id,
            spot_type=data.spot_type,
            latitude=data.latitude,
            longitude=data.longitude,
            access_difficulty=data.access_difficulty,
            best_season=data.best_season,
            walking_distance_km=data.walking_distance_km,
            visit_duration_hours=data.visit_duration_hours,
            requires_4x4=data.requires_4x4,
            has_phone_signal=data.has_phone_signal,
            submitted_by_id=submitter.id,
            status="pending",
        )
        await self._session.commit()
        # reload with images eagerly to avoid lazy-load in async context
        return await self._repo.get_with_images(spot.id)

    async def get_spot(self, spot_id: UUID) -> Spot:
        spot = await self._repo.get_with_images(spot_id)
        if not spot:
            raise SpotNotFound(str(spot_id))
        await self._repo.increment_view(spot_id)
        await self._session.commit()
        return spot

    async def list_spots(self, params: SpotListParams) -> tuple[list[Spot], int]:
        offset = (params.page - 1) * params.page_size
        return await self._repo.list_approved(
            region_id=params.region_id,
            spot_type=params.spot_type,
            access_difficulty=params.access_difficulty,
            requires_4x4=params.requires_4x4,
            offset=offset,
            limit=params.page_size,
        )

    async def update_spot(self, spot_id: UUID, data: SpotUpdate, user: User) -> Spot:
        spot = await self._repo.get_by_id(spot_id)
        if not spot:
            raise SpotNotFound(str(spot_id))
        if spot.submitted_by_id != user.id and user.role not in (Role.ADMIN, Role.MINISTRY):
            raise UnauthorizedRole(Role.ADMIN)

        updates = data.model_dump(exclude_none=True)
        await self._repo.update(spot, **updates)
        await self._session.commit()
        return await self._repo.get_with_images(spot.id)

    async def approve_spot(self, spot_id: UUID, approval: SpotApproval, admin: User) -> Spot:
        spot = await self._repo.get_by_id(spot_id)
        if not spot:
            raise SpotNotFound(str(spot_id))

        was_approved = spot.status == "approved"

        if approval.approved:
            spot.status = "approved"
            spot.approved_by_id = admin.id
            spot.rejection_reason = None
        else:
            spot.status = "rejected"
            spot.rejection_reason = approval.rejection_reason

        await self._repo.save(spot)
        if approval.approved and not was_approved:
            await self._repo.adjust_region_spot_count(spot.region_id, delta=1)
        elif not approval.approved and was_approved:
            await self._repo.adjust_region_spot_count(spot.region_id, delta=-1)
        await self._session.commit()
        return await self._repo.get_with_images(spot.id)

    async def list_pending(self, offset: int = 0, limit: int = 20) -> list[Spot]:
        return await self._repo.list_pending(offset=offset, limit=limit)

    async def vector_search(self, embedding: list[float], top_k: int = 5, region_id: UUID | None = None) -> list[Spot]:
        return await self._repo.vector_search(embedding, top_k=top_k, region_id=region_id)
