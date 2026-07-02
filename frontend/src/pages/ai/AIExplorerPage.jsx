import { useState } from "react";
import PageWrapper from "@/components/layout/PageWrapper";
import AIChatBox from "@/components/ai/AIChatBox";
import { useLanguage } from "@/contexts/LanguageContext";
import { useAuth } from "@/contexts/AuthContext";
import { Link } from "react-router-dom";

export default function AIExplorerPage() {
  const { isArabic } = useLanguage();
  const { user } = useAuth();
  const [presetQuestion, setPresetQuestion] = useState(null);

  if (!user) {
    return (
      <PageWrapper>
        <div className="text-center py-20">
          <div className="text-6xl mb-4">🤖</div>
          <h2 className="text-2xl font-bold text-gray-900 mb-3">
            {isArabic ? "تسجيل الدخول مطلوب" : "Login Required"}
          </h2>
          <p className="text-gray-500 mb-6">
            {isArabic
              ? "يرجى تسجيل الدخول لاستخدام المستكشف الذكي"
              : "Please sign in to use the AI Explorer"}
          </p>
          <Link to="/login" className="btn-primary px-8 py-3 rounded-xl">
            {isArabic ? "تسجيل الدخول" : "Sign In"}
          </Link>
        </div>
      </PageWrapper>
    );
  }

  return (
    <PageWrapper>
      <div className="max-w-4xl mx-auto">
        <div className="mb-6">
          <h1 className="page-title">
            {isArabic ? "🤖 المستكشف الذكي" : "🤖 AI Explorer"}
          </h1>
          <p className="text-gray-500 mt-2">
            {isArabic
              ? "اسأل الذكاء الاصطناعي عن أي موقع خفي أو اكتشاف سياحي في المملكة العربية السعودية"
              : "Ask AI about any hidden spot or tourism discovery in Saudi Arabia"}
          </p>
        </div>

        <div className="h-[600px]">
          <AIChatBox presetQuestion={presetQuestion} />
        </div>

        <div className="mt-6 grid grid-cols-1 sm:grid-cols-3 gap-4">
          {[
            {
              ar: "أين أجمل الشلالات في عسير؟",
              en: "Where are the most beautiful waterfalls in Asir?",
            },
            {
              ar: "أقترح مواقع أثرية قريبة من تبوك",
              en: "Suggest archaeological sites near Tabuk",
            },
            {
              ar: "ما أفضل موسم لزيارة جبال الحجاز؟",
              en: "What's the best season to visit the Hejaz mountains?",
            },
          ].map((q, i) => (
            <button
              key={i}
              className="card p-4 text-sm text-start text-gray-600 hover:border-primary-300 hover:text-primary-700 hover:bg-primary-50 transition-all duration-200"
              onClick={() => setPresetQuestion({ text: isArabic ? q.ar : q.en, id: Date.now() })}
            >
              💡 {isArabic ? q.ar : q.en}
            </button>
          ))}
        </div>
      </div>
    </PageWrapper>
  );
}
