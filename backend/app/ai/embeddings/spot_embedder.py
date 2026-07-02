from functools import lru_cache
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from sentence_transformers import SentenceTransformer


@lru_cache(maxsize=1)
def _get_model() -> "SentenceTransformer":
    from sentence_transformers import SentenceTransformer
    return SentenceTransformer("sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2")


def embed_spot(name_ar: str, description_ar: str, name_en: str = "", description_en: str = "") -> list[float]:
    model = _get_model()
    text = f"{name_ar} {description_ar} {name_en} {description_en}".strip()
    embedding = model.encode(text, normalize_embeddings=True)
    return embedding.tolist()


def embed_query(query: str) -> list[float]:
    model = _get_model()
    embedding = model.encode(query, normalize_embeddings=True)
    return embedding.tolist()
