import api from "./axios";
import { ENDPOINTS } from "@/constants/api";

export const bookingsAPI = {
  create: (data) => api.post(ENDPOINTS.BOOKINGS.CREATE, data),
  listMine: (params) => api.get(ENDPOINTS.BOOKINGS.MY, { params }),
  getById: (id) => api.get(ENDPOINTS.BOOKINGS.BY_ID(id)),
  updateStatus: (id, status) => api.patch(ENDPOINTS.BOOKINGS.STATUS(id), { status }),
};
