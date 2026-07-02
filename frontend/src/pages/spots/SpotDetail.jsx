import { useParams } from "react-router-dom";
import { useQuery } from "@tanstack/react-query";
import PageWrapper from "@/components/layout/PageWrapper";
import { spotsAPI } from "@/api/spots";
import { useLanguage } from "@/contexts/LanguageContext";
import Spinner from "@/components/common/Spinner";
import Badge from "@/components/common/Badge";
import GoogleMapView from "@/components/map/GoogleMapView";
import { SPOT_TYPES, ACCESS_DIFFICULTY } from "@/constants/spotTypes";
import { formatDuration, formatDistance } from "@/utils/formatters";

export default function SpotDetail() {
  const { id } = useParams();
  const { isArabic } = useLanguage();

  const { data: spot, isLoading, error } = useQuery({
    queryKey: ["spot", id],
    queryFn: () => spotsAPI.getById(id).then((r) => r.data),
  });

  if (isLoading) return (
    <PageWrapper>
      <div className="flex justify-center py-20"><Spinner size="lg" /></div>
    </PageWrapper>
  );

  if (error || !spot) return (
    <PageWrapper>
      <div className="text-center py-20 text-gray-400">
        {isArabic ? "لم يتم العثور على الموقع" : "Spot not found"}
      </div>
    </PageWrapper>
  );

  const spotType = SPOT_TYPES.find((t) => t.value === spot.spot_type);
  const difficulty = ACCESS_DIFFICULTY.find((d) => d.value === spot.access_difficulty);
  const primaryImage = spot.images?.find((i) => i.is_primary) || spot.images?.[0];

  return (
    <PageWrapper>
      <div className="max-w-4xl mx-auto">
        {/* Image */}
        <div className="relative h-80 bg-gradient-to-br from-primary-100 to-primary-200 rounded-2xl overflow-hidden mb-8">
          {primaryImage ? (
            <img src={primaryImage.image_url} alt={spot.name_ar} className="w-full h-full object-cover" />
          ) : (
            <div className="w-full h-full flex items-center justify-center text-8xl">
              {spotType?.icon || "🗺️"}
            </div>
          )}
          <div className="absolute bottom-4 start-4 flex gap-2">
            <Badge variant={spot.access_difficulty === "easy" ? "green" : spot.access_difficulty === "medium" ? "yellow" : "red"}>
              {isArabic ? difficulty?.label_ar : difficulty?.label_en}
            </Badge>
            {spot.requires_4x4 && <Badge variant="blue">4×4</Badge>}
            {!spot.has_phone_signal && <Badge variant="gray">📵</Badge>}
          </div>
        </div>

        {/* Header */}
        <div className="flex items-start justify-between gap-4 mb-6">
          <div>
            <h1 className="text-3xl font-black text-gray-900">
              {isArabic ? spot.name_ar : (spot.name_en || spot.name_ar)}
            </h1>
            {!isArabic && spot.name_ar !== spot.name_en && (
              <p className="text-gray-400 mt-1">{spot.name_ar}</p>
            )}
          </div>
          <div className="text-4xl">{spotType?.icon}</div>
        </div>

        {/* Quick Info */}
        <div className="grid grid-cols-2 sm:grid-cols-4 gap-4 mb-8">
          {spot.visit_duration_hours && (
            <div className="card p-4 text-center">
              <div className="text-2xl mb-1">⏱</div>
              <div className="text-sm font-medium">{formatDuration(spot.visit_duration_hours)}</div>
              <div className="text-xs text-gray-400">{isArabic ? "مدة الزيارة" : "Duration"}</div>
            </div>
          )}
          {spot.walking_distance_km && (
            <div className="card p-4 text-center">
              <div className="text-2xl mb-1">🚶</div>
              <div className="text-sm font-medium">{formatDistance(spot.walking_distance_km)}</div>
              <div className="text-xs text-gray-400">{isArabic ? "مسافة المشي" : "Walk distance"}</div>
            </div>
          )}
          {spot.best_season && (
            <div className="card p-4 text-center">
              <div className="text-2xl mb-1">🌤</div>
              <div className="text-sm font-medium">{spot.best_season}</div>
              <div className="text-xs text-gray-400">{isArabic ? "أفضل موسم" : "Best season"}</div>
            </div>
          )}
          <div className="card p-4 text-center">
            <div className="text-2xl mb-1">👁</div>
            <div className="text-sm font-medium">{spot.view_count.toLocaleString()}</div>
            <div className="text-xs text-gray-400">{isArabic ? "مشاهدة" : "Views"}</div>
          </div>
        </div>

        {/* Description */}
        <div className="card p-6 mb-6">
          <h2 className="section-title">{isArabic ? "عن الموقع" : "About this Spot"}</h2>
          <p className="text-gray-600 leading-relaxed">
            {isArabic ? spot.description_ar : (spot.description_en || spot.description_ar)}
          </p>
        </div>

        {/* Location */}
        <div className="card p-6">
          <h2 className="section-title">{isArabic ? "الموقع الجغرافي" : "Location"}</h2>
          <GoogleMapView
            lat={spot.latitude}
            lng={spot.longitude}
            title={isArabic ? spot.name_ar : (spot.name_en || spot.name_ar)}
          />
          <div className="flex items-center gap-2 text-gray-600 mt-4">
            <span>📍</span>
            <span className="font-mono text-sm">
              {spot.latitude.toFixed(6)}, {spot.longitude.toFixed(6)}
            </span>
            <a
              href={`https://maps.google.com/?q=${spot.latitude},${spot.longitude}`}
              target="_blank"
              rel="noopener noreferrer"
              className="text-primary-600 hover:underline text-sm"
            >
              {isArabic ? "افتح في الخريطة" : "Open in Maps"} →
            </a>
          </div>
        </div>
      </div>
    </PageWrapper>
  );
}
