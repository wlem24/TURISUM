import SpotCard from "./SpotCard";
import Spinner from "@/components/common/Spinner";
import { useLanguage } from "@/contexts/LanguageContext";

export default function SpotGrid({ spots, loading, emptyMessage }) {
  const { isArabic } = useLanguage();

  if (loading) {
    return (
      <div className="flex items-center justify-center py-20">
        <Spinner size="lg" />
      </div>
    );
  }

  if (!spots?.length) {
    return (
      <div className="text-center py-20 text-gray-400">
        <div className="text-5xl mb-4">🗺️</div>
        <p className="text-lg font-medium">
          {emptyMessage || (isArabic ? "لا توجد مواقع حالياً" : "No spots found")}
        </p>
      </div>
    );
  }

  return (
    <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 xl:grid-cols-4 gap-6">
      {spots.map((spot) => (
        <SpotCard key={spot.id} spot={spot} />
      ))}
    </div>
  );
}
