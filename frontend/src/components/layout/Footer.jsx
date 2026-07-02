import { Link } from "react-router-dom";
import { useLanguage } from "@/contexts/LanguageContext";
import AtharIcon from "@/components/common/AtharIcon";

export default function Footer() {
  const { isArabic } = useLanguage();

  return (
    <footer className="bg-gray-900 text-gray-300 mt-auto">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-12">
        <div className="grid grid-cols-1 md:grid-cols-4 gap-8">
          <div>
            <div className="flex items-center gap-2 mb-4">
              <AtharIcon size={32} rounded="rounded-lg" />
              <span className="font-bold text-white text-lg">أثر</span>
            </div>
            <p className="text-sm text-gray-400 leading-relaxed">
              {isArabic
                ? "اكتشف ما تركه الزمان — مواقع طبيعية وأثرية لم تُكتشف بعد"
                : "Discover what time left behind — undiscovered natural and archaeological sites"}
            </p>
          </div>

          <div>
            <h4 className="font-semibold text-white mb-3">{isArabic ? "استكشاف" : "Explore"}</h4>
            <ul className="space-y-2 text-sm">
              <li><Link to="/explore" className="hover:text-primary-400 transition-colors">{isArabic ? "المواقع السياحية" : "Tourist Spots"}</Link></li>
              <li><Link to="/guides" className="hover:text-primary-400 transition-colors">{isArabic ? "المرشدون" : "Guides"}</Link></li>
              <li><Link to="/hotels" className="hover:text-primary-400 transition-colors">{isArabic ? "الفنادق" : "Hotels"}</Link></li>
              <li><Link to="/ai-explorer" className="hover:text-primary-400 transition-colors">{isArabic ? "المستكشف الذكي" : "AI Explorer"}</Link></li>
            </ul>
          </div>

          <div>
            <h4 className="font-semibold text-white mb-3">{isArabic ? "المناطق" : "Regions"}</h4>
            <ul className="space-y-2 text-sm">
              <li><Link to="/explore?region=asir" className="hover:text-primary-400 transition-colors">{isArabic ? "عسير" : "Asir"}</Link></li>
              <li><Link to="/explore?region=tabuk" className="hover:text-primary-400 transition-colors">{isArabic ? "تبوك" : "Tabuk"}</Link></li>
              <li><Link to="/explore?region=hail" className="hover:text-primary-400 transition-colors">{isArabic ? "حائل" : "Hail"}</Link></li>
              <li><Link to="/explore?region=bahah" className="hover:text-primary-400 transition-colors">{isArabic ? "الباحة" : "Al-Bahah"}</Link></li>
            </ul>
          </div>

          <div>
            <h4 className="font-semibold text-white mb-3">{isArabic ? "للمقيمين" : "For Locals"}</h4>
            <ul className="space-y-2 text-sm">
              <li><Link to="/submit-spot" className="hover:text-primary-400 transition-colors">{isArabic ? "أضف موقعاً سياحياً" : "Submit a Spot"}</Link></li>
              <li><Link to="/register" className="hover:text-primary-400 transition-colors">{isArabic ? "كن مرشداً سياحياً" : "Become a Guide"}</Link></li>
            </ul>
          </div>
        </div>

        <div className="border-t border-gray-800 mt-8 pt-8 flex flex-col sm:flex-row items-center justify-between gap-4 text-sm text-gray-500">
          <p>{isArabic ? "© 2030 أثر. جميع الحقوق محفوظة" : "© 2030 Athar. All rights reserved"}</p>
          <p>{isArabic ? "دعماً لرؤية 2030 🇸🇦" : "Supporting Vision 2030 🇸🇦"}</p>
        </div>
      </div>
    </footer>
  );
}
