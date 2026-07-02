from uuid import UUID
from sqlalchemy.ext.asyncio import AsyncSession

from app.ai.embeddings.spot_embedder import embed_query
from app.repositories.spot_repo import SpotRepository
from app.schemas.ai import SpotSuggestion


async def find_similar_spots(
    query: str,
    session: AsyncSession,
    top_k: int = 5,
    region_id: UUID | None = None,
) -> list[SpotSuggestion]:
    query_embedding = embed_query(query)
    repo = SpotRepository(session)
    spots = await repo.vector_search(query_embedding, top_k=top_k, region_id=region_id)

    suggestions = []
    for i, spot in enumerate(spots):
        score = 1.0 - (i * 0.1)  # approximate rank-based score
        suggestions.append(SpotSuggestion(
            spot_id=spot.id,
            name_ar=spot.name_ar,
            name_en=spot.name_en,
            similarity_score=round(score, 3),
            explanation=f"يتطابق مع بحثك عن '{query}'" if _is_arabic(query) else f"Matches your search for '{query}'",
        ))
    return suggestions


def _is_arabic(text: str) -> bool:
    return sum(1 for c in text if "؀" <= c <= "ۿ") > len(text) * 0.3
