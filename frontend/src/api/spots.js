import api from "./axios";
import { ENDPOINTS } from "@/constants/api";

export const spotsAPI = {
  list: (params) => api.get(ENDPOINTS.SPOTS.LIST, { params }),
  getById: (id) => api.get(ENDPOINTS.SPOTS.BY_ID(id)),
  create: (data) => api.post(ENDPOINTS.SPOTS.CREATE, data),
  update: (id, data) => api.patch(ENDPOINTS.SPOTS.BY_ID(id), data),
  approve: (id, data) => api.post(ENDPOINTS.SPOTS.APPROVE(id), data),
};
