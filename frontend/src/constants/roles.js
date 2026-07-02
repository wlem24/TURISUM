export const ROLES = {
  VISITOR: "visitor",
  LOCAL: "local",
  GUIDE: "guide",
  ADMIN: "admin",
  MINISTRY: "ministry",
};

export const ROLE_LABELS = {
  visitor: { ar: "زائر", en: "Visitor" },
  local: { ar: "مقيم محلي", en: "Local Resident" },
  guide: { ar: "مرشد سياحي", en: "Tour Guide" },
  admin: { ar: "مدير", en: "Admin" },
  ministry: { ar: "وزارة السياحة", en: "Ministry of Tourism" },
};

export const ROLE_HIERARCHY = {
  visitor: 0,
  local: 1,
  guide: 2,
  admin: 3,
  ministry: 4,
};

export function hasRole(userRole, requiredRole) {
  return (ROLE_HIERARCHY[userRole] ?? -1) >= (ROLE_HIERARCHY[requiredRole] ?? 999);
}
