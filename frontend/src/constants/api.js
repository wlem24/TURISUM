export const API_BASE_URL = import.meta.env.VITE_API_BASE_URL || "http://localhost:8000/api/v1";

export const ENDPOINTS = {
  AUTH: {
    REGISTER: "/auth/register",
    LOGIN: "/auth/login",
    REFRESH: "/auth/refresh",
    LOGOUT: "/auth/logout",
  },
  USERS: {
    ME: "/users/me",
    BY_ID: (id) => `/users/${id}`,
  },
  SPOTS: {
    LIST: "/spots",
    CREATE: "/spots",
    BY_ID: (id) => `/spots/${id}`,
    APPROVE: (id) => `/spots/${id}/approve`,
  },
  GUIDES: {
    LIST: "/guides",
    CREATE: "/guides",
    ME: "/guides/me",
    BY_ID: (id) => `/guides/${id}`,
    VERIFY: (id) => `/guides/${id}/verify`,
  },
  HOTELS: {
    LIST: "/hotels",
    CREATE: "/hotels",
    BY_ID: (id) => `/hotels/${id}`,
    NEARBY: "/hotels/nearby",
  },
  BOOKINGS: {
    CREATE: "/bookings",
    MY: "/bookings/me",
    BY_ID: (id) => `/bookings/${id}`,
    STATUS: (id) => `/bookings/${id}/status`,
  },
  REGIONS: {
    LIST: "/regions",
  },
  ADMIN: {
    DASHBOARD: "/admin/dashboard",
    PENDING_SPOTS: "/admin/spots/pending",
    USERS: "/admin/users",
  },
  AI: {
    CHAT: "/ai/chat",
    SUGGEST: "/ai/suggest",
    HISTORY: "/ai/history",
  },
  NOTIFICATIONS: {
    LIST: "/notifications",
    READ: (id) => `/notifications/${id}/read`,
  },
};
