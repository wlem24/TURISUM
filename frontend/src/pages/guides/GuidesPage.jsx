import { useQuery } from "@tanstack/react-query";
import PageWrapper from "@/components/layout/PageWrapper";
import GuideCard from "@/components/guides/GuideCard";
import Spinner from "@/components/common/Spinner";
import { guidesAPI } from "@/api/guides";
import { useLanguage } from "@/contexts/LanguageContext";

export default function GuidesPage() {
  const { isArabic } = useLanguage();

  const { data: guides, isLoading } = useQuery({
    queryKey: ["guides"],
    queryFn: () => guidesAPI.list({}).then((r) => r.data),
  });

  return (
    <PageWrapper>
      <div className="mb-8">
        <h1 className="page-title">{isArabic ? "المرشدون السياحيون المحليون 🧭" : "Local Tour Guides 🧭"}</h1>
        <p className="text-gray-500 mt-2">
          {isArabic
            ? "مرشدون محليون موثّقون يعرفون كل زاوية في المملكة"
            : "Verified local guides who know every corner of the Kingdom"}
        </p>
      </div>

      {isLoading ? (
        <div className="flex justify-center py-20"><Spinner size="lg" /></div>
      ) : !guides?.length ? (
        <div className="text-center py-20 text-gray-400">
          <div className="text-5xl mb-4">🧭</div>
          <p>{isArabic ? "لا يوجد مرشدون متاحون حالياً" : "No guides available yet"}</p>
        </div>
      ) : (
        <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-6">
          {guides.map((g) => <GuideCard key={g.id} guide={g} />)}
        </div>
      )}
    </PageWrapper>
  );
}
