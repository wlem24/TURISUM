import { Link, useNavigate } from "react-router-dom";
import { useAuth } from "@/contexts/AuthContext";
import { useLanguage } from "@/contexts/LanguageContext";
import { useTheme } from "@/contexts/ThemeContext";
import { hasRole, ROLES } from "@/constants/roles";
import AtharIcon from "@/components/common/AtharIcon";

export default function Navbar() {
  const { user, logout } = useAuth();
  const { lang, switchLanguage, isArabic } = useLanguage();
  const { isDark, toggleTheme } = useTheme();
  const navigate = useNavigate();

  return (
    <nav className="sticky top-0 z-40 bg-primary-800/95 backdrop-blur-sm border-b border-primary-600/40 shadow-sm">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div className="flex items-center justify-between h-16">
          {/* Logo */}
          <Link to="/" className="flex items-center gap-2">
            <AtharIcon size={36} />
            <span className="font-bold text-primary-100 text-lg hidden sm:block">
              {isArabic ? "أثر" : "Athar"}
            </span>
          </Link>

          {/* Nav links */}
          <div className="hidden md:flex items-center gap-1">
            <Link to="/explore" className="px-4 py-2 text-sm font-medium text-primary-200 hover:text-primary-50 hover:bg-primary-700 rounded-lg transition-colors">
              {isArabic ? "استكشاف" : "Explore"}
            </Link>
            <Link to="/guides" className="px-4 py-2 text-sm font-medium text-primary-200 hover:text-primary-50 hover:bg-primary-700 rounded-lg transition-colors">
              {isArabic ? "المرشدون" : "Guides"}
            </Link>
            <Link to="/hotels" className="px-4 py-2 text-sm font-medium text-primary-200 hover:text-primary-50 hover:bg-primary-700 rounded-lg transition-colors">
              {isArabic ? "الفنادق" : "Hotels"}
            </Link>
            <Link to="/ai-explorer" className="px-4 py-2 text-sm font-medium text-primary-200 hover:text-primary-50 hover:bg-primary-700 rounded-lg transition-colors">
              {isArabic ? "🤖 المستكشف الذكي" : "🤖 AI Explorer"}
            </Link>
          </div>

          {/* Right side */}
          <div className="flex items-center gap-3">
            <button
              onClick={toggleTheme}
              title={isArabic ? "الوضع الداكن" : "Dark mode"}
              className="text-sm px-2.5 py-1.5 rounded-lg border border-primary-600 text-primary-200 hover:text-primary-50 hover:border-primary-400 transition-colors"
            >
              {isDark ? "☀️" : "🌙"}
            </button>
            <button
              onClick={() => switchLanguage(isArabic ? "en" : "ar")}
              className="text-sm font-medium px-3 py-1.5 rounded-lg border border-primary-600 text-primary-200 hover:text-primary-50 hover:border-primary-400 transition-colors"
            >
              {isArabic ? "EN" : "عربي"}
            </button>

            {user ? (
              <div className="flex items-center gap-2">
                {hasRole(user.role, ROLES.LOCAL) && (
                  <Link to="/submit-spot" className="btn-primary text-sm px-4 py-2 rounded-xl hidden sm:block">
                    {isArabic ? "+ أضف موقع" : "+ Add Spot"}
                  </Link>
                )}
                {hasRole(user.role, ROLES.ADMIN) && (
                  <Link to="/admin" className="text-sm font-medium text-primary-200 hover:text-primary-50 hidden sm:block">
                    {isArabic ? "لوحة التحكم" : "Dashboard"}
                  </Link>
                )}
                <div className="relative group">
                  <button className="w-9 h-9 bg-sand-500 rounded-full flex items-center justify-center text-primary-800 font-bold text-sm hover:brightness-105 transition-colors">
                    {(user.full_name || "U").charAt(0).toUpperCase()}
                  </button>
                  <div className="absolute end-0 top-full mt-2 w-48 bg-white rounded-xl shadow-lg border border-gray-100 py-1 opacity-0 group-hover:opacity-100 invisible group-hover:visible transition-all duration-200">
                    <Link to="/profile" className="block px-4 py-2 text-sm text-gray-700 hover:bg-gray-50">
                      {isArabic ? "ملفي الشخصي" : "My Profile"}
                    </Link>
                    <Link to="/bookings" className="block px-4 py-2 text-sm text-gray-700 hover:bg-gray-50">
                      {isArabic ? "حجوزاتي" : "My Bookings"}
                    </Link>
                    <button
                      onClick={logout}
                      className="block w-full text-start px-4 py-2 text-sm text-red-600 hover:bg-red-50"
                    >
                      {isArabic ? "تسجيل الخروج" : "Logout"}
                    </button>
                  </div>
                </div>
              </div>
            ) : (
              <div className="flex items-center gap-2">
                <Link to="/login" className="text-sm font-medium text-primary-200 hover:text-primary-50">
                  {isArabic ? "دخول" : "Login"}
                </Link>
                <Link to="/register" className="btn-primary text-sm px-4 py-2 rounded-xl">
                  {isArabic ? "سجّل مجاناً" : "Sign Up Free"}
                </Link>
              </div>
            )}
          </div>
        </div>
      </div>
    </nav>
  );
}
