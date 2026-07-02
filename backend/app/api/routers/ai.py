from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.dependencies import get_db, get_current_user
from app.schemas.ai import ChatMessage, ChatResponse, SpotSuggestionQuery, SpotSuggestion, AIChatHistoryOut
from app.ai.rag.spot_rag import find_similar_spots
from app.ai.prompts.discovery_prompt import DISCOVERY_SYSTEM_PROMPT
from app.repositories.ai_chat_repo import AIChatRepository
from app.models.user import User
from app.core.config import settings

router = APIRouter(prefix="/ai", tags=["AI"])


@router.post("/chat", response_model=ChatResponse)
async def ai_chat(
    message: ChatMessage,
    current_user: User = Depends(get_current_user),
    session: AsyncSession = Depends(get_db),
):
    chat_repo = AIChatRepository(session)
    history = await chat_repo.get_user_history(current_user.id, limit=10)

    messages = [{"role": h.role, "content": h.content} for h in history]
    messages.append({"role": "user", "content": message.content})

    reply = ""
    suggested_spot_ids = []

    if settings.ANTHROPIC_API_KEY:
        import anthropic
        client = anthropic.Anthropic(api_key=settings.ANTHROPIC_API_KEY)
        try:
            response = client.messages.create(
                model="claude-sonnet-4-6",
                max_tokens=1024,
                system=DISCOVERY_SYSTEM_PROMPT,
                messages=messages,
            )
            reply = response.content[0].text
        except Exception as e:
            reply = "عذراً، حدث خطأ في الاتصال بالذكاء الاصطناعي. حاول مرة أخرى." if message.language == "ar" else "Sorry, AI service is temporarily unavailable."
    else:
        reply = "خدمة الذكاء الاصطناعي غير متاحة حالياً. يرجى إعداد مفتاح API." if message.language == "ar" else "AI service is not configured. Please set ANTHROPIC_API_KEY."

    # Save to history
    await chat_repo.create(user_id=current_user.id, role="user", content=message.content)
    await chat_repo.create(user_id=current_user.id, role="assistant", content=reply)

    # Find similar spots via RAG
    try:
        suggestions = await find_similar_spots(message.content, session, top_k=3, region_id=message.region_id)
        suggested_spot_ids = [s.spot_id for s in suggestions]
    except Exception:
        pass

    await session.commit()
    return ChatResponse(reply=reply, suggested_spots=suggested_spot_ids)


@router.post("/suggest", response_model=list[SpotSuggestion])
async def suggest_spots(
    query: SpotSuggestionQuery,
    current_user: User = Depends(get_current_user),
    session: AsyncSession = Depends(get_db),
):
    suggestions = await find_similar_spots(
        query.query, session, top_k=query.top_k, region_id=query.region_id
    )
    return suggestions


@router.get("/history", response_model=list[AIChatHistoryOut])
async def get_chat_history(
    current_user: User = Depends(get_current_user),
    session: AsyncSession = Depends(get_db),
):
    repo = AIChatRepository(session)
    history = await repo.get_user_history(current_user.id, limit=50)
    return [AIChatHistoryOut.model_validate(h) for h in history]
