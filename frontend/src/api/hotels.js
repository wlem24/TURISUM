import api from "./axios";
import { ENDPOINTS } from "@/constants/api";

export const hotelsAPI = {
  list: (params) => api.get(ENDPOINTS.HOTELS.LIST, { params }),
  getById: (id) => api.get(ENDPOINTS.HOTELS.BY_ID(id)),
  nearby: (lat, lng, radius_km) => api.get(ENDPOINTS.HOTELS.NEARBY, { params: { lat, lng, radius_km } }),
  create: (data) => api.post(ENDPOINTS.HOTELS.CREATE, data),
};
