import api from "./axios";
import { ENDPOINTS } from "@/constants/api";

export const guidesAPI = {
  list: (params) => api.get(ENDPOINTS.GUIDES.LIST, { params }),
  getById: (id) => api.get(ENDPOINTS.GUIDES.BY_ID(id)),
  getMe: () => api.get(ENDPOINTS.GUIDES.ME),
  create: (data) => api.post(ENDPOINTS.GUIDES.CREATE, data),
  update: (id, data) => api.patch(ENDPOINTS.GUIDES.BY_ID(id), data),
  verify: (id) => api.post(ENDPOINTS.GUIDES.VERIFY(id)),
};
