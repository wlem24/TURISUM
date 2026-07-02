import { Navigate } from "react-router-dom";
import { useAuth } from "@/contexts/AuthContext";
import { hasRole } from "@/constants/roles";

export default function RoleRoute({ children, requiredRole }) {
  const { user } = useAuth();

  if (!user || !hasRole(user.role, requiredRole)) {
    return <Navigate to="/explore" replace />;
  }

  return children;
}
