import { useState } from "react";
import { Link, useNavigate } from "react-router-dom";
import { useForm } from "react-hook-form";
import { zodResolver } from "@hookform/resolvers/zod";
import { useAuth } from "@/contexts/AuthContext";
import { useLanguage } from "@/contexts/LanguageContext";
import { registerSchema } from "@/utils/validators";
import Input from "@/components/common/Input";
import Button from "@/components/common/Button";
import AtharIcon from "@/components/common/AtharIcon";
import toast from "react-hot-toast";

const ROLE_OPTIONS = [
  { value: "visitor", label_ar: "زائر / سائح", label_en: "Visitor / Tourist" },
  { value: "local", label_ar: "مقيم محلي (أضف مواقع)", label_en: "Local Resident (Submit spots)" },
  { value: "guide", label_ar: "مرشد سياحي", label_en: "Tour Guide" },
];

export default function RegisterPage() {
  const { register: registerUser } = useAuth();
  const { isArabic } = useLanguage();
  const navigate = useNavigate();
  const [serverError, setServerError] = useState("");

  const { register, handleSubmit, formState: { errors, isSubmitting } } = useForm({
    resolver: zodResolver(registerSchema),
    defaultValues: { role: "visitor" },
  });

  const onSubmit = async (data) => {
    setServerError("");
    const result = await registerUser(data);
    if (result.success) {
      toast.success(isArabic ? "تم إنشاء الحساب بنجاح!" : "Account created successfully!");
      navigate("/login");
    } else {
      setServerError(result.error);
    }
  };

  return (
    <div className="min-h-screen bg-gradient-to-br from-primary-50 via-white to-sand-50 flex items-center justify-center p-4">
      <div className="w-full max-w-md">
        <div className="text-center mb-8">
          <Link to="/" className="inline-flex items-center gap-2 mb-6">
            <AtharIcon size={48} rounded="rounded-2xl" className="shadow-lg" />
          </Link>
          <h1 className="text-2xl font-bold text-gray-900">
            {isArabic ? "إنشاء حساب جديد" : "Create Account"}
          </h1>
          <p className="text-gray-500 mt-1">
            {isArabic ? "انضم إلى مجتمع أثر" : "Join the Athar community"}
          </p>
        </div>

        <div className="card p-8">
          <form onSubmit={handleSubmit(onSubmit)} className="space-y-4">
            <Input
              label={isArabic ? "الاسم الكامل" : "Full Name"}
              placeholder={isArabic ? "الاسم بالإنجليزية" : "Your full name"}
              error={errors.full_name?.message}
              {...register("full_name")}
            />
            <Input
              label={isArabic ? "الاسم بالعربية (اختياري)" : "Arabic Name (optional)"}
              placeholder="محمد العمري"
              error={errors.full_name_ar?.message}
              {...register("full_name_ar")}
            />
            <Input
              label={isArabic ? "البريد الإلكتروني" : "Email"}
              type="email"
              placeholder="example@email.com"
              error={errors.email?.message}
              {...register("email")}
            />
            <Input
              label={isArabic ? "كلمة المرور" : "Password"}
              type="password"
              placeholder="••••••••"
              hint={isArabic ? "8 أحرف على الأقل" : "At least 8 characters"}
              error={errors.password?.message}
              {...register("password")}
            />
            <Input
              label={isArabic ? "رقم الجوال (اختياري)" : "Phone (optional)"}
              type="tel"
              placeholder="+966 5X XXX XXXX"
              {...register("phone")}
            />

            <div className="flex flex-col gap-1">
              <label className="text-sm font-medium text-gray-700">
                {isArabic ? "نوع الحساب" : "Account Type"}
              </label>
              <select className="input-field" {...register("role")}>
                {ROLE_OPTIONS.map((r) => (
                  <option key={r.value} value={r.value}>
                    {isArabic ? r.label_ar : r.label_en}
                  </option>
                ))}
              </select>
              {errors.role && <p className="text-xs text-red-500">{errors.role.message}</p>}
            </div>

            {serverError && (
              <div className="p-3 bg-red-50 border border-red-200 rounded-xl text-sm text-red-600">
                {serverError}
              </div>
            )}

            <Button type="submit" loading={isSubmitting} className="w-full mt-2">
              {isArabic ? "إنشاء الحساب" : "Create Account"}
            </Button>
          </form>

          <p className="text-center text-sm text-gray-500 mt-6">
            {isArabic ? "لديك حساب بالفعل؟" : "Already have an account?"}{" "}
            <Link to="/login" className="text-primary-600 font-medium hover:underline">
              {isArabic ? "سجّل دخولك" : "Sign in"}
            </Link>
          </p>
        </div>
      </div>
    </div>
  );
}
