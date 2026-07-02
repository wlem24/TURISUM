import { createContext, useContext, useState, useEffect, useCallback } from "react";
import { authAPI } from "@/api/auth";
import { authService } from "@/services/authService";

const AuthContext = createContext(null);

export function AuthProvider({ children }) {
  const [user, setUser] = useState(() => authService.getUser());
  const [token, setToken] = useState(() => authService.getToken());
  const [loading, setLoading] = useState(false);

  const login = useCallback(async (email, password) => {
    setLoading(true);
    try {
      const { data } = await authAPI.login({ email, password });
      authService.setToken(data.access_token);
      if (data.refresh_token) {
        localStorage.setItem("athar_refresh_token", data.refresh_token);
      }
      setToken(data.access_token);

      const meResp = await authAPI.getMe();
      authService.setUser(meResp.data);
      setUser(meResp.data);
      return { success: true };
    } catch (error) {
      const msg = error.response?.data?.detail || "فشل تسجيل الدخول";
      return { success: false, error: msg };
    } finally {
      setLoading(false);
    }
  }, []);

  const register = useCallback(async (data) => {
    setLoading(true);
    try {
      await authAPI.register(data);
      return { success: true };
    } catch (error) {
      const msg = error.response?.data?.detail || "فشل إنشاء الحساب";
      return { success: false, error: msg };
    } finally {
      setLoading(false);
    }
  }, []);

  const logout = useCallback(async () => {
    try {
      await authAPI.logout();
    } catch {}
    authService.clear();
    setToken(null);
    setUser(null);
    window.location.href = "/login";
  }, []);

  const refreshUser = useCallback(async () => {
    if (!authService.getToken()) return;
    try {
      const { data } = await authAPI.getMe();
      authService.setUser(data);
      setUser(data);
    } catch {}
  }, []);

  useEffect(() => {
    if (token && !user) {
      refreshUser();
    }
  }, [token, user, refreshUser]);

  return (
    <AuthContext.Provider value={{ user, token, loading, login, register, logout, refreshUser }}>
      {children}
    </AuthContext.Provider>
  );
}

export function useAuth() {
  const ctx = useContext(AuthContext);
  if (!ctx) throw new Error("useAuth must be used inside AuthProvider");
  return ctx;
}
