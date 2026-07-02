import { useQuery } from "@tanstack/react-query";
import PageWrapper from "@/components/layout/PageWrapper";
import { bookingsAPI } from "@/api/bookings";
import { useAuth } from "@/contexts/AuthContext";
import { useLanguage } from "@/contexts/LanguageContext";
import { useTheme } from "@/contexts/ThemeContext";
import { ROLE_LABELS } from "@/constants/roles";
import { formatPrice, formatDate } from "@/utils/formatters";
import Spinner from "@/components/common/Spinner";
import Badge from "@/components/common/Badge";

const STATUS_VARIANT = { pending: "yellow", confirmed: "green", completed: "blue", cancelled: "red" };
const STATUS_LABEL = {
  pending: { ar: "قيد الانتظار", en: "Pending" },
  confirmed: { ar: "مؤكد", en: "Confirmed" },
  completed: { ar: "مكتمل", en: "Completed" },
  cancelled: { ar: "ملغى", en: "Cancelled" },
};
const BOOKING_TYPE_LABEL = {
  guide: { ar: "حجز مرشد", en: "Guide Booking" },
  hotel: { ar: "حجز فندق", en: "Hotel Booking" },
  package: { ar: "حجز باقة", en: "Package Booking" },
};

export default function ProfilePage() {
  const { user } = useAuth();
  const { isArabic, switchLanguage } = useLanguage();
  const { isDark, toggleTheme } = useTheme();

  const { data: bookings, isLoading } = useQuery({
    queryKey: ["my-bookings"],
    queryFn: () => bookingsAPI.listMine({}).then((r) => r.data),
  });

  if (!user) return null;

  const roleLabel = ROLE_LABELS[user.role];

  return (
    <PageWrapper>
      <div className="max-w-3xl mx-auto">
        {/* Profile header */}
        <div className="card p-8 mb-8">
          <div className="flex items-center gap-6">
            <div className="w-20 h-20 bg-primary-100 rounded-full flex items-center justify-center text-primary-700 font-black text-3xl">
              {(user.full_name || "U").charAt(0).toUpperCase()}
            </div>
            <div>
              <h1 className="text-2xl font-black text-gray-900">
                {isArabic ? (user.full_name_ar || user.full_name) : user.full_name}
              </h1>
              <p className="text-gray-400">{user.email}</p>
              <div className="flex items-center gap-2 mt-2">
                <Badge variant="primary">
                  {isArabic ? roleLabel?.ar : roleLabel?.en}
                </Badge>
                {user.is_verified && (
                  <Badge variant="green">{isArabic ? "موثّق ✓" : "Verified ✓"}</Badge>
                )}
              </div>
            </div>
          </div>
        </div>

        {/* Settings */}
        <div className="card p-5 mb-8 space-y-1">
          <button
            onClick={() => switchLanguage(isArabic ? "en" : "ar")}
            className="w-full flex items-center justify-between px-2 py-2.5 rounded-lg hover:bg-primary-50 transition-colors"
          >
            <span className="text-sm font-medium text-gray-700">{isArabic ? "اللغة" : "Language"}</span>
            <span className="text-sm font-semibold text-primary-600">{isArabic ? "العربية" : "English"} ⇄</span>
          </button>
          <button
            onClick={toggleTheme}
            className="w-full flex items-center justify-between px-2 py-2.5 rounded-lg hover:bg-primary-50 transition-colors"
          >
            <span className="text-sm font-medium text-gray-700">{isArabic ? "الوضع الداكن" : "Dark mode"}</span>
            <span className="text-sm font-semibold text-primary-600">
              {isDark ? (isArabic ? "🌙 داكن" : "🌙 Dark") : (isArabic ? "☀️ فاتح" : "☀️ Light")} ⇄
            </span>
          </button>
        </div>

        {/* Bookings */}
        <div>
          <h2 className="section-title">{isArabic ? "حجوزاتي" : "My Bookings"}</h2>
          {isLoading ? (
            <Spinner />
          ) : !bookings?.length ? (
            <div className="card p-8 text-center text-gray-400">
              <div className="text-4xl mb-3">📅</div>
              <p>{isArabic ? "لا توجد حجوزات بعد" : "No bookings yet"}</p>
            </div>
          ) : (
            <div className="space-y-4">
              {bookings.map((b) => (
                <div key={b.id} className="card p-5">
                  <div className="flex items-center justify-between gap-4">
                    <div>
                      <p className="font-semibold text-gray-900">
                        {isArabic
                          ? (BOOKING_TYPE_LABEL[b.booking_type]?.ar || b.booking_type)
                          : (BOOKING_TYPE_LABEL[b.booking_type]?.en || b.booking_type)}
                      </p>
                      <p className="text-sm text-gray-400">{formatDate(b.booking_date, isArabic ? "ar" : "en")}</p>
                    </div>
                    <div className="text-end">
                      <p className="font-bold text-primary-600">{formatPrice(b.total_amount)}</p>
                      <Badge variant={STATUS_VARIANT[b.status] || "gray"}>
                        {isArabic
                          ? (STATUS_LABEL[b.status]?.ar || b.status)
                          : (STATUS_LABEL[b.status]?.en || b.status)}
                      </Badge>
                    </div>
                  </div>
                </div>
              ))}
            </div>
          )}
        </div>
      </div>
    </PageWrapper>
  );
}
