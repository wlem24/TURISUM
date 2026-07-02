from typing import Any, Generic, TypeVar
from uuid import UUID

from sqlalchemy import select, func
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.base import Base

ModelT = TypeVar("ModelT", bound=Base)


class BaseRepository(Generic[ModelT]):
    def __init__(self, model: type[ModelT], session: AsyncSession):
        self.model = model
        self.session = session

    async def get_by_id(self, id: UUID) -> ModelT | None:
        result = await self.session.execute(select(self.model).where(self.model.id == id))
        return result.scalar_one_or_none()

    async def list_all(self, offset: int = 0, limit: int = 20) -> list[ModelT]:
        result = await self.session.execute(
            select(self.model).offset(offset).limit(limit)
        )
        return list(result.scalars().all())

    async def count(self) -> int:
        result = await self.session.execute(select(func.count()).select_from(self.model))
        return result.scalar_one()

    async def create(self, **kwargs: Any) -> ModelT:
        instance = self.model(**kwargs)
        self.session.add(instance)
        await self.session.flush()
        await self.session.refresh(instance)
        return instance

    async def update(self, instance: ModelT, **kwargs: Any) -> ModelT:
        for key, value in kwargs.items():
            if value is not None:
                setattr(instance, key, value)
        self.session.add(instance)
        await self.session.flush()
        await self.session.refresh(instance)
        return instance

    async def delete(self, instance: ModelT) -> None:
        await self.session.delete(instance)
        await self.session.flush()

    async def save(self, instance: ModelT) -> ModelT:
        self.session.add(instance)
        await self.session.flush()
        await self.session.refresh(instance)
        return instance
