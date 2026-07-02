// Client-side, direct-to-Anthropic AI path — SEPARATE from api/ai.js.
//
// SECURITY NOTE: this calls api.anthropic.com straight from the browser using
// VITE_ANTHROPIC_API_KEY, which ships inside the built JS bundle and is visible
// to anyone who opens devtools. That is a real tradeoff, accepted here only for
// local prototyping / offline demos where the FastAPI backend isn't running.
// The production chat path (aiAPI.chat() in api/ai.js -> POST /ai/chat) keeps
// the Anthropic key server-side and should remain the default for real users.
// Do not call api.anthropic.com from anywhere else in the frontend.

const ANTHROPIC_ENDPOINT = "https://api.anthropic.com/v1/messages";

export const ATHAR_DIRECT_SYSTEM_PROMPT = `أنت أثر (Athar) — مساعد سياحي ذكي متخصص في اكتشاف المواقع السياحية الخفية والمجهولة في المملكة العربية السعودية.

- ساعد المسافرين في اكتشاف أماكن غير مشهورة وجميلة في المملكة
- أجب باللغة التي يكتب بها المستخدم (عربية أو إنجليزية)
- لا تختلق أماكن غير موجودة
- اذكر متطلبات السلامة، أفضل موسم للزيارة، والحاجة لمركبة دفع رباعي إن وُجدت

You are Athar (أثر) — an AI tourism assistant specialized in discovering hidden, undiscovered spots across Saudi Arabia. Respond in the user's language. Never invent locations that don't exist. Mention safety notes, best season, and 4x4 requirements when relevant.`;

export async function callClaudeDirect(messages, systemPrompt = ATHAR_DIRECT_SYSTEM_PROMPT) {
  const apiKey = import.meta.env.VITE_ANTHROPIC_API_KEY;
  if (!apiKey) {
    throw new Error("VITE_ANTHROPIC_API_KEY is not set in .env — this direct path requires it.");
  }

  const res = await fetch(ANTHROPIC_ENDPOINT, {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
      "x-api-key": apiKey,
      "anthropic-version": "2023-06-01",
      "anthropic-dangerous-direct-browser-access": "true",
    },
    body: JSON.stringify({
      model: "claude-sonnet-4-6",
      max_tokens: 1000,
      system: systemPrompt,
      messages,
    }),
  });

  const data = await res.json();
  if (!res.ok) {
    throw new Error(data?.error?.message || `Anthropic API error: ${res.statusText}`);
  }
  return data.content[0].text;
}
