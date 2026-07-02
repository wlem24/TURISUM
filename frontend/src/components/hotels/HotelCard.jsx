import { Link } from "react-router-dom";
import { useLanguage } from "@/contexts/LanguageContext";
import { formatPrice } from "@/utils/formatters";

export default function HotelCard({ hotel }) {
  const { isArabic } = useLanguage();

  const stars = "★".repeat(hotel.stars) + "☆".repeat(5 - hotel.stars);

  return (
    <div className="card hover:shadow-md transition-all duration-200">
      <div className="h-40 bg-gradient-to-br from-sand-100 to-sand-200 flex items-center justify-center text-5xl">
        🏨
      </div>
      <div className="p-4">
        <h3 className="font-bold text-gray-900 mb-1">
          {isArabic ? hotel.name_ar : (hotel.name_en || hotel.name_ar)}
        </h3>
        <div className="text-yellow-500 text-sm mb-3">{stars}</div>

        <div className="flex items-center justify-between">
          <div>
            <span className="text-lg font-bold text-primary-600">{formatPrice(hotel.price_per_night)}</span>
            <span className="text-xs text-gray-400 ms-1">/{isArabic ? "ليلة" : "night"}</span>
          </div>
          <Link
            to={`/hotels/${hotel.id}`}
            className="btn-primary text-sm px-4 py-2 rounded-xl"
          >
            {isArabic ? "احجز" : "Book"}
          </Link>
        </div>
      </div>
    </div>
  );
}
