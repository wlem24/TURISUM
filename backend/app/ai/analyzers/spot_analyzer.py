import anthropic
from app.core.config import settings


async def analyze_spot_quality(
    name_ar: str,
    description_ar: str,
    spot_type: str,
    latitude: float,
    longitude: float,
) -> dict:
    """Run AI quality analysis on a submitted spot. Returns score and notes."""
    if not settings.ANTHROPIC_API_KEY:
        return {"score": 0.5, "notes": "AI analysis unavailable — API key not configured"}

    client = anthropic.Anthropic(api_key=settings.ANTHROPIC_API_KEY)

    prompt = f"""قيّم جودة الموقع السياحي التالي المقدّم من أحد السكان المحليين في المملكة العربية السعودية.

الاسم: {name_ar}
النوع: {spot_type}
الوصف: {description_ar}
الإحداثيات: {latitude}, {longitude}

قيّم الموقع من 0 إلى 1 وأعطِ ملاحظات قصيرة (3-5 جمل) حول:
1. اكتمال الوصف
2. الأهمية السياحية المحتملة
3. اعتبارات السلامة
4. اقتراحات للتحسين

أجب بتنسيق JSON فقط:
{{"score": 0.0-1.0, "notes": "ملاحظاتك هنا", "safety_flags": [], "improvement_suggestions": []}}"""

    try:
        message = client.messages.create(
            model="claude-sonnet-4-6",
            max_tokens=500,
            messages=[{"role": "user", "content": prompt}],
        )
        import json
        text = message.content[0].text.strip()
        # Extract JSON from response
        start = text.find("{")
        end = text.rfind("}") + 1
        if start >= 0 and end > start:
            return json.loads(text[start:end])
    except Exception:
        pass

    return {"score": 0.5, "notes": "تعذّر إجراء التحليل التلقائي", "safety_flags": [], "improvement_suggestions": []}
