import api from "./axios";
import { ENDPOINTS } from "@/constants/api";

export const adminAPI = {
  getDashboard: () => api.get(ENDPOINTS.ADMIN.DASHBOARD),
  getPendingSpots: (params) => api.get(ENDPOINTS.ADMIN.PENDING_SPOTS, { params }),
  getUsers: (params) => api.get(ENDPOINTS.ADMIN.USERS, { params }),
  deactivateUser: (id) => api.patch(`/admin/users/${id}/deactivate`),
};
