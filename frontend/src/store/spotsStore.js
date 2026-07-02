import { create } from "zustand";

export const useSpotsStore = create((set) => ({
  spots: [],
  selectedSpot: null,
  filters: {
    region_id: null,
    spot_type: null,
    access_difficulty: null,
    requires_4x4: null,
  },
  setSpots: (spots) => set({ spots }),
  setSelectedSpot: (spot) => set({ selectedSpot: spot }),
  setFilter: (key, value) =>
    set((state) => ({ filters: { ...state.filters, [key]: value } })),
  clearFilters: () =>
    set({ filters: { region_id: null, spot_type: null, access_difficulty: null, requires_4x4: null } }),
}));
