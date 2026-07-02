import { useState } from "react";
import { Link, useNavigate } from "react-router-dom";
import { useForm } from "react-hook-form";
import { zodResolver } from "@hookform/resolvers/zod";
import { useAuth } from "@/contexts/AuthContext";
import { useLanguage } from "@/contexts/LanguageContext";
import { loginSchema } from "@/utils/validators";
import Input from "@/components/common/Input";
import Button from "@/components/common/Button";
import AtharIcon from "@/components/common/AtharIcon";
import toast from "react-hot-toast";

export default function LoginPage() {
  const { login } = useAuth();
  const { isArabic } = useLanguage();
  const navigate = useNavigate();
  const [serverError, setServerError] = useState("");

  const { register, handleSubmit, formState: { errors, isSubmitting } } = useForm({
    resolver: zodResolver(loginSchema),
    defaultValues: { email: "", password: "" },
  });

  const onSubmit = async (data) => {
    setServerError("");
    const result = await login(data.email, data.password);
    if (result.success) {
      toast.success(isArabic ? "مرحباً بعودتك!" : "Welcome back!");
      navigate("/explore");
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
            {isArabic ? "تسجيل الدخول" : "Sign In"}
          </h1>
          <p className="text-gray-500 mt-1">
            {isArabic ? "مرحباً بعودتك إلى أثر" : "Welcome back to Athar"}
          </p>
        </div>

        <div className="card p-8">
          <form onSubmit={handleSubmit(onSubmit)} className="space-y-5">
            <Input
              label={isArabic ? "البريد الإلكتروني" : "Email"}
              type="email"
              placeholder={isArabic ? "example@email.com" : "example@email.com"}
              error={errors.email?.message}
              {...register("email")}
            />
            <Input
              label={isArabic ? "كلمة المرور" : "Password"}
              type="password"
              placeholder="••••••••"
              error={errors.password?.message}
              {...register("password")}
            />

            {serverError && (
              <div className="p-3 bg-red-50 border border-red-200 rounded-xl text-sm text-red-600">
                {serverError}
              </div>
            )}

            <Button
              type="submit"
              loading={isSubmitting}
              className="w-full"
            >
              {isArabic ? "دخول" : "Sign In"}
            </Button>
          </form>

          <p className="text-center text-sm text-gray-500 mt-6">
            {isArabic ? "ليس لديك حساب؟" : "Don't have an account?"}{" "}
            <Link to="/register" className="text-primary-600 font-medium hover:underline">
              {isArabic ? "سجّل مجاناً" : "Sign up free"}
            </Link>
          </p>
        </div>
      </div>
    </div>
  );
}
