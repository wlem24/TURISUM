import api from "./axios";
import { ENDPOINTS } from "@/constants/api";

export const authAPI = {
  register: (data) => api.post(ENDPOINTS.AUTH.REGISTER, data),
  login: (data) => api.post(ENDPOINTS.AUTH.LOGIN, data),
  refresh: (refreshToken) => api.post(ENDPOINTS.AUTH.REFRESH, { refresh_token: refreshToken }),
  logout: () => api.post(ENDPOINTS.AUTH.LOGOUT),
  getMe: () => api.get(ENDPOINTS.USERS.ME),
  updateMe: (data) => api.patch(ENDPOINTS.USERS.ME, data),
};
