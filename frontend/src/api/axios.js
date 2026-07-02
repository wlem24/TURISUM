import axios from "axios";
import { API_BASE_URL } from "@/constants/api";
import { authService } from "@/services/authService";

const api = axios.create({
  baseURL: API_BASE_URL,
  headers: { "Content-Type": "application/json" },
  timeout: 15000,
});

api.interceptors.request.use((config) => {
  const token = authService.getToken();
  if (token) {
    config.headers.Authorization = `Bearer ${token}`;
  }
  return config;
});

api.interceptors.response.use(
  (response) => response,
  async (error) => {
    const original = error.config;
    if (error.response?.status === 401 && !original._retry) {
      original._retry = true;
      try {
        const refreshToken = localStorage.getItem("athar_refresh_token");
        if (!refreshToken) throw new Error("No refresh token");
        const { data } = await axios.post(`${API_BASE_URL}/auth/refresh`, {
          refresh_token: refreshToken,
        });
        authService.setToken(data.access_token);
        localStorage.setItem("athar_refresh_token", data.refresh_token || refreshToken);
        original.headers.Authorization = `Bearer ${data.access_token}`;
        return api(original);
      } catch {
        authService.clear();
        window.location.href = "/login";
      }
    }
    return Promise.reject(error);
  }
);

export default api;
