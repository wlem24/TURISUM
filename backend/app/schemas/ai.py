import uuid
from datetime import datetime
from pydantic import BaseModel


class ChatMessage(BaseModel):
    content: str
    region_id: uuid.UUID | None = None
    language: str = "ar"


class ChatResponse(BaseModel):
    reply: str
    suggested_spots: list[uuid.UUID] = []
    session_id: str | None = None


class SpotSuggestionQuery(BaseModel):
    query: str
    region_id: uuid.UUID | None = None
    top_k: int = 5


class SpotSuggestion(BaseModel):
    spot_id: uuid.UUID
    name_ar: str
    name_en: str | None
    similarity_score: float
    explanation: str


class AIChatHistoryOut(BaseModel):
    model_config = {"from_attributes": True}

    id: uuid.UUID
    role: str
    content: str
    created_at: datetime
