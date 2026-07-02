import api from "./axios";
import { ENDPOINTS } from "@/constants/api";

export const regionsAPI = {
  list: () => api.get(ENDPOINTS.REGIONS.LIST),
};
