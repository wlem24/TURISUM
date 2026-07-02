import { useQuery } from "@tanstack/react-query";
import { Link } from "react-router-dom";
import PageWrapper from "@/components/layout/PageWrapper";
import StatsCard from "@/components/dashboard/StatsCard";
import { adminAPI } from "@/api/admin";
import { useLanguage } from "@/contexts/LanguageContext";
import Spinner from "@/components/common/Spinner";
import { formatPrice } from "@/utils/formatters";

export default function AdminDashboard() {
  const { isArabic } = useLanguage();

  const { data: stats, isLoading } = useQuery({
    queryKey: ["admin-dashboard"],
    queryFn: () => adminAPI.getDashboard().then((r) => r.data),
  });

  if (isLoading) return (
    <PageWrapper>
      <div className="flex justify-center py-20"><Spinner size="lg" /></div>
    </PageWrapper>
  );

  return (
    <PageWrapper>
      <div className="mb-8">
        <h1 className="page-title">{isArabic ? "لوحة تحكم الإدارة 📊" : "Admin Dashboard 📊"}</h1>
      </div>

      {stats && (
        <div className="grid grid-cols-2 lg:grid-cols-3 xl:grid-cols-6 gap-4 mb-8">
          <StatsCard title={isArabic ? "المستخدمون" : "Users"} value={stats.total_users} icon="👥" color="blue" />
          <StatsCard title={isArabic ? "المواقع" : "Spots"} value={stats.total_spots} icon="🗺️" color="primary" />
          <StatsCard title={isArabic ? "بانتظار الموافقة" : "Pending"} value={stats.pending_spots} icon="⏳" color="yellow" />
          <StatsCard title={isArabic ? "المواقع المعتمدة" : "Approved"} value={stats.approved_spots} icon="✅" color="green" />
          <StatsCard title={isArabic ? "الحجوزات" : "Bookings"} value={stats.total_bookings} icon="📅" color="primary" />
          <StatsCard title={isArabic ? "الإيرادات" : "Revenue"} value={formatPrice(stats.total_revenue)} icon="💰" color="green" />
        </div>
      )}

      <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
        <Link to="/admin/pending-spots" className="card p-6 hover:shadow-md transition-all text-center">
          <div className="text-4xl mb-3">⏳</div>
          <h3 className="font-bold text-gray-900">{isArabic ? "مراجعة المواقع المعلّقة" : "Review Pending Spots"}</h3>
          {stats?.pending_spots > 0 && (
            <span className="inline-block mt-2 bg-yellow-100 text-yellow-700 text-sm px-3 py-1 rounded-full">
              {stats.pending_spots} {isArabic ? "بانتظار المراجعة" : "pending"}
            </span>
          )}
        </Link>
        <Link to="/admin/users" className="card p-6 hover:shadow-md transition-all text-center">
          <div className="text-4xl mb-3">👥</div>
          <h3 className="font-bold text-gray-900">{isArabic ? "إدارة المستخدمين" : "Manage Users"}</h3>
        </Link>
        <Link to="/admin/guides" className="card p-6 hover:shadow-md transition-all text-center">
          <div className="text-4xl mb-3">🧭</div>
          <h3 className="font-bold text-gray-900">{isArabic ? "توثيق المرشدين" : "Verify Guides"}</h3>
        </Link>
      </div>
    </PageWrapper>
  );
}
