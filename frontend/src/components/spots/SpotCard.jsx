import { Link } from "react-router-dom";
import { useLanguage } from "@/contexts/LanguageContext";
import Badge from "@/components/common/Badge";
import { ACCESS_DIFFICULTY, SPOT_TYPES } from "@/constants/spotTypes";
import { formatDuration, formatDistance } from "@/utils/formatters";

const DIFFICULTY_VARIANT = { easy: "green", medium: "yellow", hard: "red" };

export default function SpotCard({ spot }) {
  const { isArabic } = useLanguage();
  const spotType = SPOT_TYPES.find((t) => t.value === spot.spot_type);
  const difficulty = ACCESS_DIFFICULTY.find((d) => d.value === spot.access_difficulty);
  const primaryImage = spot.images?.find((i) => i.is_primary) || spot.images?.[0];

  return (
    <Link to={`/spots/${spot.id}`} className="card hover:shadow-md transition-all duration-200 group block">
      <div className="relative h-48 bg-gradient-to-br from-primary-100 to-primary-200 overflow-hidden">
        {primaryImage ? (
          <img
            src={primaryImage.image_url}
            alt={isArabic ? spot.name_ar : (spot.name_en || spot.name_ar)}
            className="w-full h-full object-cover group-hover:scale-105 transition-transform duration-300"
          />
        ) : (
          <div className="w-full h-full flex items-center justify-center text-5xl">
            {spotType?.icon || "🗺️"}
          </div>
        )}
        <div className="absolute top-3 start-3">
          <Badge variant={DIFFICULTY_VARIANT[spot.access_difficulty] || "gray"}>
            {isArabic ? difficulty?.label_ar : difficulty?.label_en}
          </Badge>
        </div>
        {spot.requires_4x4 && (
          <div className="absolute top-3 end-3">
            <Badge variant="blue">4×4</Badge>
          </div>
        )}
      </div>

      <div className="p-4">
        <div className="flex items-start justify-between gap-2 mb-2">
          <h3 className="font-bold text-gray-900 text-base leading-tight">
            {isArabic ? spot.name_ar : (spot.name_en || spot.name_ar)}
          </h3>
          <span className="text-xl flex-shrink-0">{spotType?.icon}</span>
        </div>

        <p className="text-sm text-gray-500 line-clamp-2 mb-3">
          {isArabic ? spot.description_ar : (spot.description_en || spot.description_ar)}
        </p>

        <div className="flex items-center gap-3 text-xs text-gray-400">
          {spot.visit_duration_hours && (
            <span>⏱ {formatDuration(spot.visit_duration_hours)}</span>
          )}
          {spot.walking_distance_km && (
            <span>🚶 {formatDistance(spot.walking_distance_km)}</span>
          )}
          {!spot.has_phone_signal && (
            <span title={isArabic ? "لا يوجد إشارة" : "No signal"}>📵</span>
          )}
        </div>

        {spot.best_season && (
          <div className="mt-2 text-xs text-gray-400">
            🌤 {isArabic ? "أفضل موسم: " : "Best season: "}{spot.best_season}
          </div>
        )}
      </div>
    </Link>
  );
}
