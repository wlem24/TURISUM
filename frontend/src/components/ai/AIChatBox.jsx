import { useState, useRef, useEffect } from "react";
import { useLanguage } from "@/contexts/LanguageContext";
import { aiAPI } from "@/api/ai";
import Button from "@/components/common/Button";
import Spinner from "@/components/common/Spinner";

export default function AIChatBox({ regionId, presetQuestion }) {
  const { isArabic, lang } = useLanguage();
  const [messages, setMessages] = useState([
    {
      role: "assistant",
      content: isArabic
        ? "مرحباً! أنا مساعدك الذكي لاكتشاف المواقع السياحية الخفية في المملكة العربية السعودية. كيف أستطيع مساعدتك اليوم؟ 🗺️"
        : "Hello! I'm your AI assistant for discovering hidden tourist spots in Saudi Arabia. How can I help you today? 🗺️",
    },
  ]);
  const [input, setInput] = useState("");
  const [loading, setLoading] = useState(false);
  const bottomRef = useRef(null);

  useEffect(() => {
    bottomRef.current?.scrollIntoView({ behavior: "smooth" });
  }, [messages]);

  useEffect(() => {
    if (presetQuestion?.text) setInput(presetQuestion.text);
  }, [presetQuestion]);

  const sendMessage = async () => {
    const text = input.trim();
    if (!text || loading) return;

    setMessages((prev) => [...prev, { role: "user", content: text }]);
    setInput("");
    setLoading(true);

    try {
      const { data } = await aiAPI.chat({ content: text, region_id: regionId, language: lang });
      setMessages((prev) => [...prev, { role: "assistant", content: data.reply }]);
    } catch {
      setMessages((prev) => [
        ...prev,
        {
          role: "assistant",
          content: isArabic
            ? "عذراً، حدث خطأ. يرجى المحاولة مرة أخرى."
            : "Sorry, an error occurred. Please try again.",
        },
      ]);
    } finally {
      setLoading(false);
    }
  };

  const handleKeyDown = (e) => {
    if (e.key === "Enter" && !e.shiftKey) {
      e.preventDefault();
      sendMessage();
    }
  };

  return (
    <div className="flex flex-col h-full bg-white rounded-2xl border border-gray-100 shadow-sm overflow-hidden">
      {/* Header */}
      <div className="p-4 border-b border-gray-100 bg-gradient-to-r from-primary-50 to-primary-100">
        <div className="flex items-center gap-3">
          <div className="w-10 h-10 bg-primary-500 rounded-full flex items-center justify-center text-white text-xl">🤖</div>
          <div>
            <h3 className="font-bold text-gray-900">{isArabic ? "المستكشف الذكي" : "AI Explorer"}</h3>
            <p className="text-xs text-gray-500">{isArabic ? "مدعوم بـ Claude AI" : "Powered by Claude AI"}</p>
          </div>
          <div className="ms-auto w-2 h-2 bg-green-500 rounded-full animate-pulse" />
        </div>
      </div>

      {/* Messages */}
      <div className="flex-1 overflow-y-auto p-4 space-y-4">
        {messages.map((msg, i) => (
          <div key={i} className={`flex ${msg.role === "user" ? "justify-end" : "justify-start"}`}>
            <div
              className={`max-w-[80%] rounded-2xl px-4 py-3 text-sm leading-relaxed ${
                msg.role === "user"
                  ? "bg-primary-500 text-white rounded-ee-sm"
                  : "bg-gray-100 text-gray-800 rounded-es-sm"
              }`}
            >
              {msg.content}
            </div>
          </div>
        ))}
        {loading && (
          <div className="flex justify-start">
            <div className="bg-gray-100 rounded-2xl rounded-es-sm px-4 py-3 flex items-center gap-2">
              <span className="w-2 h-2 bg-gray-400 rounded-full animate-bounce" style={{ animationDelay: "0ms" }} />
              <span className="w-2 h-2 bg-gray-400 rounded-full animate-bounce" style={{ animationDelay: "150ms" }} />
              <span className="w-2 h-2 bg-gray-400 rounded-full animate-bounce" style={{ animationDelay: "300ms" }} />
            </div>
          </div>
        )}
        <div ref={bottomRef} />
      </div>

      {/* Input */}
      <div className="p-4 border-t border-gray-100">
        <div className="flex gap-2">
          <textarea
            value={input}
            onChange={(e) => setInput(e.target.value)}
            onKeyDown={handleKeyDown}
            placeholder={isArabic ? "اسأل عن أي موقع سياحي خفي في المملكة..." : "Ask about any hidden spot in Saudi Arabia..."}
            className="flex-1 border border-gray-200 rounded-xl px-4 py-2.5 text-sm resize-none focus:outline-none focus:ring-2 focus:ring-primary-500 focus:border-transparent"
            rows={2}
          />
          <Button onClick={sendMessage} loading={loading} disabled={!input.trim()}>
            {isArabic ? "إرسال" : "Send"}
          </Button>
        </div>
      </div>
    </div>
  );
}
