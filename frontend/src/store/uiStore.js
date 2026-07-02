import { create } from "zustand";

export const useUIStore = create((set) => ({
  sidebarOpen: false,
  mapView: false,
  toggleSidebar: () => set((s) => ({ sidebarOpen: !s.sidebarOpen })),
  setSidebarOpen: (val) => set({ sidebarOpen: val }),
  setMapView: (val) => set({ mapView: val }),
}));
