import api from "./axios";
import { ENDPOINTS } from "@/constants/api";

export const aiAPI = {
  chat: (data) => api.post(ENDPOINTS.AI.CHAT, data),
  suggest: (data) => api.post(ENDPOINTS.AI.SUGGEST, data),
  getHistory: () => api.get(ENDPOINTS.AI.HISTORY),
};
