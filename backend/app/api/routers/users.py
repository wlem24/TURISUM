from uuid import UUID
from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.dependencies import get_db, get_current_user, require_admin
from app.schemas.user import UserOut, UserUpdate
from app.repositories.user_repo import UserRepository
from app.models.user import User

router = APIRouter(prefix="/users", tags=["Users"])


@router.get("/me", response_model=UserOut)
async def get_me(current_user: User = Depends(get_current_user)):
    return current_user


@router.patch("/me", response_model=UserOut)
async def update_me(
    data: UserUpdate,
    current_user: User = Depends(get_current_user),
    session: AsyncSession = Depends(get_db),
):
    repo = UserRepository(session)
    updates = data.model_dump(exclude_none=True)
    user = await repo.update(current_user, **updates)
    await session.commit()
    return user


@router.get("/{user_id}", response_model=UserOut)
async def get_user(
    user_id: UUID,
    _: User = Depends(require_admin),
    session: AsyncSession = Depends(get_db),
):
    repo = UserRepository(session)
    user = await repo.get_by_id(user_id)
    if not user:
        from app.core.exceptions import UserNotFound
        raise UserNotFound(str(user_id))
    return user
