import { useState } from "react";
import { useQuery } from "@tanstack/react-query";
import { useSearchParams } from "react-router-dom";
import PageWrapper from "@/components/layout/PageWrapper";
import SpotGrid from "@/components/spots/SpotGrid";
import { spotsAPI } from "@/api/spots";
import { useLanguage } from "@/contexts/LanguageContext";
import { SPOT_TYPES, ACCESS_DIFFICULTY } from "@/constants/spotTypes";
import Button from "@/components/common/Button";

export default function ExploreSpots() {
  const { isArabic } = useLanguage();
  const [searchParams, setSearchParams] = useSearchParams();
  const [filters, setFilters] = useState({
    spot_type: searchParams.get("type") || "",
    access_difficulty: searchParams.get("difficulty") || "",
    requires_4x4: searchParams.get("4x4") || "",
    page: 1,
    page_size: 20,
  });

  const { data, isLoading } = useQuery({
    queryKey: ["spots", filters],
    queryFn: () => spotsAPI.list({ ...filters, requires_4x4: filters.requires_4x4 || undefined }),
    select: (res) => res.data,
  });

  const updateFilter = (key, value) => {
    setFilters((prev) => ({ ...prev, [key]: value, page: 1 }));
  };

  return (
    <PageWrapper>
      {/* Hero */}
      <div className="text-center mb-10">
        <h1 className="text-4xl font-black text-gray-900 mb-3">
          {isArabic ? "استكشف المواقع الخفية 🗺️" : "Discover Hidden Spots 🗺️"}
        </h1>
        <p className="text-lg text-gray-500 max-w-2xl mx-auto">
          {isArabic
            ? "مواقع طبيعية وأثرية لم يكتشفها معظم الناس، مقدّمة من السكان المحليين"
            : "Natural and archaeological sites undiscovered by most, submitted by local residents"}
        </p>
      </div>

      {/* Filters */}
      <div className="flex flex-wrap gap-3 mb-8 p-4 bg-white rounded-2xl border border-gray-100 shadow-sm">
        <div className="flex flex-col gap-1 flex-1 min-w-32">
          <label className="text-xs font-medium text-gray-500">{isArabic ? "نوع الموقع" : "Spot Type"}</label>
          <select
            className="input-field text-sm"
            value={filters.spot_type}
            onChange={(e) => updateFilter("spot_type", e.target.value)}
          >
            <option value="">{isArabic ? "الكل" : "All Types"}</option>
            {SPOT_TYPES.map((t) => (
              <option key={t.value} value={t.value}>
                {t.icon} {isArabic ? t.label_ar : t.label_en}
              </option>
            ))}
          </select>
        </div>

        <div className="flex flex-col gap-1 flex-1 min-w-32">
          <label className="text-xs font-medium text-gray-500">{isArabic ? "صعوبة الوصول" : "Difficulty"}</label>
          <select
            className="input-field text-sm"
            value={filters.access_difficulty}
            onChange={(e) => updateFilter("access_difficulty", e.target.value)}
          >
            <option value="">{isArabic ? "الكل" : "All"}</option>
            {ACCESS_DIFFICULTY.map((d) => (
              <option key={d.value} value={d.value}>
                {isArabic ? d.label_ar : d.label_en}
              </option>
            ))}
          </select>
        </div>

        <div className="flex flex-col gap-1 flex-1 min-w-32">
          <label className="text-xs font-medium text-gray-500">{isArabic ? "4×4 مطلوب" : "4×4 Required"}</label>
          <select
            className="input-field text-sm"
            value={filters.requires_4x4}
            onChange={(e) => updateFilter("requires_4x4", e.target.value)}
          >
            <option value="">{isArabic ? "الكل" : "All"}</option>
            <option value="false">{isArabic ? "لا يحتاج" : "Not required"}</option>
            <option value="true">{isArabic ? "يحتاج 4×4" : "Requires 4×4"}</option>
          </select>
        </div>

        <div className="flex items-end">
          <Button
            variant="ghost"
            onClick={() => setFilters({ spot_type: "", access_difficulty: "", requires_4x4: "", page: 1, page_size: 20 })}
          >
            {isArabic ? "إعادة تعيين" : "Reset"}
          </Button>
        </div>
      </div>

      {/* Stats */}
      {data && (
        <p className="text-sm text-gray-400 mb-4">
          {isArabic
            ? `${data.total} موقع سياحي مكتشف`
            : `${data.total} spots discovered`}
        </p>
      )}

      <SpotGrid spots={data?.items} loading={isLoading} />

      {/* Pagination */}
      {data && data.pages > 1 && (
        <div className="flex items-center justify-center gap-4 mt-10">
          <Button
            variant="secondary"
            disabled={filters.page <= 1}
            onClick={() => updateFilter("page", filters.page - 1)}
          >
            {isArabic ? "السابق" : "Previous"}
          </Button>
          <span className="text-sm text-gray-500">
            {filters.page} / {data.pages}
          </span>
          <Button
            variant="secondary"
            disabled={filters.page >= data.pages}
            onClick={() => updateFilter("page", filters.page + 1)}
          >
            {isArabic ? "التالي" : "Next"}
          </Button>
        </div>
      )}
    </PageWrapper>
  );
}
