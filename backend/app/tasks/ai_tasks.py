import asyncio
from uuid import UUID

from app.tasks.celery_app import celery_app


@celery_app.task(name="analyze_spot", bind=True, max_retries=3)
def analyze_spot_task(self, spot_id: str):
    """Run AI quality analysis on a newly submitted spot."""
    async def _run():
        from app.db.session import AsyncSessionLocal
        from app.repositories.spot_repo import SpotRepository
        from app.ai.analyzers.spot_analyzer import analyze_spot_quality

        async with AsyncSessionLocal() as session:
            repo = SpotRepository(session)
            spot = await repo.get_by_id(UUID(spot_id))
            if not spot:
                return

            result = await analyze_spot_quality(
                name_ar=spot.name_ar,
                description_ar=spot.description_ar,
                spot_type=spot.spot_type,
                latitude=spot.latitude,
                longitude=spot.longitude,
            )

            spot.ai_quality_score = result.get("score")
            spot.ai_quality_notes = result.get("notes")
            await repo.save(spot)
            await session.commit()

    try:
        asyncio.run(_run())
    except Exception as exc:
        raise self.retry(exc=exc, countdown=60)


@celery_app.task(name="embed_spot", bind=True, max_retries=3)
def embed_spot_task(self, spot_id: str):
    """Generate and store embedding for an approved spot."""
    async def _run():
        from app.db.session import AsyncSessionLocal
        from app.repositories.spot_repo import SpotRepository
        from app.ai.embeddings.spot_embedder import embed_spot

        async with AsyncSessionLocal() as session:
            repo = SpotRepository(session)
            spot = await repo.get_by_id(UUID(spot_id))
            if not spot or spot.status != "approved":
                return

            embedding = embed_spot(
                name_ar=spot.name_ar,
                description_ar=spot.description_ar,
                name_en=spot.name_en or "",
                description_en=spot.description_en or "",
            )
            spot.embedding = embedding
            await repo.save(spot)
            await session.commit()

    try:
        asyncio.run(_run())
    except Exception as exc:
        raise self.retry(exc=exc, countdown=60)
