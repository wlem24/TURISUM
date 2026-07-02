import { useQuery } from "@tanstack/react-query";
import PageWrapper from "@/components/layout/PageWrapper";
import HotelCard from "@/components/hotels/HotelCard";
import Spinner from "@/components/common/Spinner";
import { hotelsAPI } from "@/api/hotels";
import { useLanguage } from "@/contexts/LanguageContext";

export default function HotelsPage() {
  const { isArabic } = useLanguage();

  const { data: hotels, isLoading } = useQuery({
    queryKey: ["hotels"],
    queryFn: () => hotelsAPI.list({}).then((r) => r.data),
  });

  return (
    <PageWrapper>
      <div className="mb-8">
        <h1 className="page-title">{isArabic ? "الفنادق القريبة من المواقع الخفية 🏨" : "Hotels Near Hidden Spots 🏨"}</h1>
        <p className="text-gray-500 mt-2">
          {isArabic ? "احجز إقامتك القريبة من أجمل المواقع السياحية" : "Book accommodation near the most beautiful spots"}
        </p>
      </div>

      {isLoading ? (
        <div className="flex justify-center py-20"><Spinner size="lg" /></div>
      ) : !hotels?.length ? (
        <div className="text-center py-20 text-gray-400">
          <div className="text-5xl mb-4">🏨</div>
          <p>{isArabic ? "لا توجد فنادق متاحة حالياً" : "No hotels available yet"}</p>
        </div>
      ) : (
        <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 xl:grid-cols-4 gap-6">
          {hotels.map((h) => <HotelCard key={h.id} hotel={h} />)}
        </div>
      )}
    </PageWrapper>
  );
}
