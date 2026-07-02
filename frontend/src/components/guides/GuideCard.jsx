import { Link } from "react-router-dom";
import { useLanguage } from "@/contexts/LanguageContext";
import Badge from "@/components/common/Badge";
import { formatPrice } from "@/utils/formatters";

export default function GuideCard({ guide }) {
  const { isArabic } = useLanguage();

  const renderStars = (rating) => {
    return "★".repeat(Math.round(rating)) + "☆".repeat(5 - Math.round(rating));
  };

  return (
    <div className="card p-5 hover:shadow-md transition-all duration-200">
      <div className="flex items-start gap-4 mb-4">
        <div className="w-14 h-14 bg-primary-100 rounded-full flex items-center justify-center text-primary-700 font-bold text-xl flex-shrink-0">
          {guide.user_id?.toString().charAt(0).toUpperCase() || "أ"}
        </div>
        <div className="flex-1 min-w-0">
          <div className="flex items-center gap-2 flex-wrap">
            <h3 className="font-bold text-gray-900">
              {isArabic ? "مرشد سياحي" : "Tour Guide"}
            </h3>
            {guide.is_verified && (
              <Badge variant="green">{isArabic ? "موثّق ✓" : "Verified ✓"}</Badge>
            )}
          </div>
          <div className="flex items-center gap-1 mt-0.5">
            <span className="text-yellow-500 text-sm">{renderStars(guide.rating || 0)}</span>
            <span className="text-xs text-gray-400">({guide.review_count || 0})</span>
          </div>
        </div>
      </div>

      <p className="text-sm text-gray-500 line-clamp-2 mb-4">
        {isArabic ? guide.bio_ar : (guide.bio_en || guide.bio_ar) || (isArabic ? "مرشد سياحي محلي متخصص" : "Specialized local tour guide")}
      </p>

      <div className="flex flex-wrap gap-1.5 mb-4">
        {guide.specializations?.slice(0, 3).map((spec) => (
          <Badge key={spec} variant="primary">{spec}</Badge>
        ))}
      </div>

      <div className="flex items-center justify-between">
        <div>
          <span className="text-lg font-bold text-primary-600">{formatPrice(guide.daily_rate)}</span>
          <span className="text-xs text-gray-400 ms-1">/{isArabic ? "يوم" : "day"}</span>
        </div>
        <Link
          to={`/guides/${guide.id}`}
          className="btn-primary text-sm px-4 py-2 rounded-xl"
        >
          {isArabic ? "احجز الآن" : "Book Now"}
        </Link>
      </div>
    </div>
  );
}
