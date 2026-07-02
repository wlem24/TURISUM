import { create } from "zustand";
import { authService } from "@/services/authService";

export const useAuthStore = create((set) => ({
  user: authService.getUser(),
  token: authService.getToken(),
  setAuth: (user, token) => {
    authService.setUser(user);
    authService.setToken(token);
    set({ user, token });
  },
  clearAuth: () => {
    authService.clear();
    set({ user: null, token: null });
  },
}));
