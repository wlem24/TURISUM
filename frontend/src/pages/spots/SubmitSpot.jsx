import { useState } from "react";
import { useNavigate } from "react-router-dom";
import { useForm } from "react-hook-form";
import { zodResolver } from "@hookform/resolvers/zod";
import { useQuery } from "@tanstack/react-query";
import PageWrapper from "@/components/layout/PageWrapper";
import { spotsAPI } from "@/api/spots";
import { regionsAPI } from "@/api/regions";
import { useLanguage } from "@/contexts/LanguageContext";
import { spotSchema } from "@/utils/validators";
import { SPOT_TYPES, ACCESS_DIFFICULTY } from "@/constants/spotTypes";
import Input from "@/components/common/Input";
import Button from "@/components/common/Button";
import toast from "react-hot-toast";

export default function SubmitSpot() {
  const { isArabic } = useLanguage();
  const navigate = useNavigate();
  const [serverError, setServerError] = useState("");

  const { data: regions, isLoading: regionsLoading } = useQuery({
    queryKey: ["regions"],
    queryFn: () => regionsAPI.list().then((r) => r.data),
  });

  const { register, handleSubmit, formState: { errors, isSubmitting } } = useForm({
    resolver: zodResolver(spotSchema),
    defaultValues: {
      spot_type: "nature",
      access_difficulty: "medium",
      requires_4x4: false,
      has_phone_signal: true,
    },
  });

  const onSubmit = async (data) => {
    setServerError("");
    try {
      await spotsAPI.create({
        ...data,
        latitude: Number(data.latitude),
        longitude: Number(data.longitude),
        walking_distance_km: data.walking_distance_km ? Number(data.walking_distance_km) : undefined,
        visit_duration_hours: data.visit_duration_hours ? Number(data.visit_duration_hours) : undefined,
      });
      toast.success(isArabic ? "تم تقديم الموقع بنجاح! سيتم مراجعته قريباً." : "Spot submitted! It will be reviewed soon.");
      navigate("/explore");
    } catch (err) {
      setServerError(err.response?.data?.detail || (isArabic ? "حدث خطأ" : "An error occurred"));
    }
  };

  return (
    <PageWrapper>
      <div className="max-w-2xl mx-auto">
        <div className="mb-8">
          <h1 className="page-title">{isArabic ? "أضف موقعاً سياحياً خفياً 🗺️" : "Submit a Hidden Spot 🗺️"}</h1>
          <p className="text-gray-500 mt-2">
            {isArabic
              ? "شارك معرفتك بالأماكن الجميلة والمجهولة في منطقتك مع العالم"
              : "Share your knowledge of beautiful undiscovered places in your area with the world"}
          </p>
        </div>

        <div className="card p-8">
          <form onSubmit={handleSubmit(onSubmit)} className="space-y-5">
            <Input
              label={isArabic ? "اسم الموقع (عربي) *" : "Spot Name (Arabic) *"}
              placeholder="شلالات عسير"
              error={errors.name_ar?.message}
              {...register("name_ar")}
            />
            <Input
              label={isArabic ? "اسم الموقع (إنجليزي)" : "Spot Name (English)"}
              placeholder="Asir Waterfalls"
              {...register("name_en")}
            />

            <div className="flex flex-col gap-1">
              <label className="text-sm font-medium text-gray-700">
                {isArabic ? "وصف الموقع (عربي) *" : "Description (Arabic) *"}
              </label>
              <textarea
                rows={4}
                placeholder={isArabic ? "صِف الموقع بالتفصيل: ما الذي يميزه؟ كيف تصل إليه؟" : "Describe the spot in detail..."}
                className={`input-field ${errors.description_ar ? "border-red-400 bg-red-50" : ""}`}
                {...register("description_ar")}
              />
              {errors.description_ar && <p className="text-xs text-red-500">{errors.description_ar.message}</p>}
            </div>

            <div className="flex flex-col gap-1">
              <label className="text-sm font-medium text-gray-700">
                {isArabic ? "وصف الموقع (إنجليزي)" : "Description (English)"}
              </label>
              <textarea rows={3} className="input-field" {...register("description_en")} />
            </div>

            <div className="grid grid-cols-2 gap-4">
              <div className="flex flex-col gap-1">
                <label className="text-sm font-medium text-gray-700">{isArabic ? "نوع الموقع" : "Spot Type"} *</label>
                <select className="input-field" {...register("spot_type")}>
                  {SPOT_TYPES.map((t) => (
                    <option key={t.value} value={t.value}>
                      {t.icon} {isArabic ? t.label_ar : t.label_en}
                    </option>
                  ))}
                </select>
              </div>
              <div className="flex flex-col gap-1">
                <label className="text-sm font-medium text-gray-700">{isArabic ? "صعوبة الوصول" : "Difficulty"}</label>
                <select className="input-field" {...register("access_difficulty")}>
                  {ACCESS_DIFFICULTY.map((d) => (
                    <option key={d.value} value={d.value}>
                      {isArabic ? d.label_ar : d.label_en}
                    </option>
                  ))}
                </select>
              </div>
            </div>

            <div className="flex flex-col gap-1">
              <label className="text-sm font-medium text-gray-700">
                {isArabic ? "المنطقة *" : "Region *"}
              </label>
              <select
                className={`input-field ${errors.region_id ? "border-red-400 bg-red-50" : ""}`}
                disabled={regionsLoading}
                defaultValue=""
                {...register("region_id")}
              >
                <option value="" disabled>
                  {regionsLoading
                    ? (isArabic ? "جارِ التحميل..." : "Loading...")
                    : (isArabic ? "اختر المنطقة" : "Select a region")}
                </option>
                {regions?.map((r) => (
                  <option key={r.id} value={r.id}>
                    {isArabic ? r.name_ar : r.name_en}
                  </option>
                ))}
              </select>
              {errors.region_id && <p className="text-xs text-red-500">{errors.region_id.message}</p>}
            </div>

            <div className="grid grid-cols-2 gap-4">
              <Input
                label={isArabic ? "خط العرض *" : "Latitude *"}
                type="number"
                step="0.000001"
                placeholder="24.7136"
                error={errors.latitude?.message}
                {...register("latitude", { valueAsNumber: true })}
              />
              <Input
                label={isArabic ? "خط الطول *" : "Longitude *"}
                type="number"
                step="0.000001"
                placeholder="46.6753"
                error={errors.longitude?.message}
                {...register("longitude", { valueAsNumber: true })}
              />
            </div>

            <div className="grid grid-cols-2 gap-4">
              <Input
                label={isArabic ? "مسافة المشي (كم)" : "Walking Distance (km)"}
                type="number"
                step="0.1"
                {...register("walking_distance_km", { valueAsNumber: true })}
              />
              <Input
                label={isArabic ? "مدة الزيارة (ساعات)" : "Visit Duration (hours)"}
                type="number"
                step="0.5"
                {...register("visit_duration_hours", { valueAsNumber: true })}
              />
            </div>

            <Input
              label={isArabic ? "أفضل موسم للزيارة" : "Best Season to Visit"}
              placeholder={isArabic ? "مثال: الشتاء (نوفمبر – فبراير)" : "e.g. Winter (Nov – Feb)"}
              {...register("best_season")}
            />

            <div className="flex items-center gap-6">
              <label className="flex items-center gap-2 cursor-pointer">
                <input type="checkbox" className="w-4 h-4 accent-primary-500" {...register("requires_4x4")} />
                <span className="text-sm text-gray-700">{isArabic ? "يحتاج مركبة 4×4" : "Requires 4×4 vehicle"}</span>
              </label>
              <label className="flex items-center gap-2 cursor-pointer">
                <input type="checkbox" className="w-4 h-4 accent-primary-500" defaultChecked {...register("has_phone_signal")} />
                <span className="text-sm text-gray-700">{isArabic ? "توجد إشارة هاتف" : "Has phone signal"}</span>
              </label>
            </div>

            {serverError && (
              <div className="p-3 bg-red-50 border border-red-200 rounded-xl text-sm text-red-600">
                {serverError}
              </div>
            )}

            <Button type="submit" loading={isSubmitting} className="w-full" size="lg">
              {isArabic ? "تقديم الموقع للمراجعة 🚀" : "Submit for Review 🚀"}
            </Button>
          </form>
        </div>
      </div>
    </PageWrapper>
  );
}
