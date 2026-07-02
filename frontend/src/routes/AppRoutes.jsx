import { Routes, Route, Navigate } from "react-router-dom";
import ProtectedRoute from "./ProtectedRoute";
import RoleRoute from "./RoleRoute";

import LoginPage from "@/pages/auth/LoginPage";
import RegisterPage from "@/pages/auth/RegisterPage";
import ExploreSpots from "@/pages/spots/ExploreSpots";
import SpotDetail from "@/pages/spots/SpotDetail";
import SubmitSpot from "@/pages/spots/SubmitSpot";
import GuidesPage from "@/pages/guides/GuidesPage";
import HotelsPage from "@/pages/hotels/HotelsPage";
import AIExplorerPage from "@/pages/ai/AIExplorerPage";
import AdminDashboard from "@/pages/admin/AdminDashboard";
import PendingSpots from "@/pages/admin/PendingSpots";
import ProfilePage from "@/pages/profile/ProfilePage";
import { ROLES } from "@/constants/roles";

export default function AppRoutes() {
  return (
    <Routes>
      <Route path="/" element={<Navigate to="/explore" replace />} />

      {/* Public */}
      <Route path="/login" element={<LoginPage />} />
      <Route path="/register" element={<RegisterPage />} />
      <Route path="/explore" element={<ExploreSpots />} />
      <Route path="/spots/:id" element={<SpotDetail />} />
      <Route path="/guides" element={<GuidesPage />} />
      <Route path="/hotels" element={<HotelsPage />} />
      <Route path="/ai-explorer" element={<AIExplorerPage />} />

      {/* Protected — any authenticated user */}
      <Route path="/profile" element={<ProtectedRoute><ProfilePage /></ProtectedRoute>} />
      <Route path="/bookings" element={<ProtectedRoute><ProfilePage /></ProtectedRoute>} />

      {/* Protected — local+ */}
      <Route path="/submit-spot" element={
        <ProtectedRoute>
          <RoleRoute requiredRole={ROLES.LOCAL}>
            <SubmitSpot />
          </RoleRoute>
        </ProtectedRoute>
      } />

      {/* Protected — admin+ */}
      <Route path="/admin" element={
        <ProtectedRoute>
          <RoleRoute requiredRole={ROLES.ADMIN}>
            <AdminDashboard />
          </RoleRoute>
        </ProtectedRoute>
      } />
      <Route path="/admin/pending-spots" element={
        <ProtectedRoute>
          <RoleRoute requiredRole={ROLES.ADMIN}>
            <PendingSpots />
          </RoleRoute>
        </ProtectedRoute>
      } />

      {/* Fallback */}
      <Route path="*" element={<Navigate to="/explore" replace />} />
    </Routes>
  );
}
