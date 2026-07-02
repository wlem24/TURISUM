import { z } from "zod";

export const loginSchema = z.object({
  email: z.string().email("بريد إلكتروني غير صالح"),
  password: z.string().min(8, "كلمة المرور يجب أن تكون 8 أحرف على الأقل"),
});

export const registerSchema = z.object({
  email: z.string().email("بريد إلكتروني غير صالح"),
  password: z.string().min(8, "كلمة المرور يجب أن تكون 8 أحرف على الأقل"),
  full_name: z.string().min(3, "الاسم يجب أن يكون 3 أحرف على الأقل"),
  full_name_ar: z.string().optional(),
  role: z.enum(["visitor", "local", "guide"]),
  phone: z.string().optional(),
});

export const spotSchema = z.object({
  name_ar: z.string().min(3, "اسم الموقع مطلوب"),
  name_en: z.string().optional(),
  description_ar: z.string().min(20, "الوصف يجب أن يكون 20 حرف على الأقل"),
  description_en: z.string().optional(),
  region_id: z.string().uuid("يرجى اختيار المنطقة"),
  spot_type: z.enum(["archaeological", "nature", "waterfall", "desert", "coastal", "village"]),
  latitude: z.number().min(16).max(32.5),
  longitude: z.number().min(34.5).max(56),
  access_difficulty: z.enum(["easy", "medium", "hard"]).default("medium"),
  requires_4x4: z.boolean().default(false),
  has_phone_signal: z.boolean().default(true),
  best_season: z.string().optional(),
  walking_distance_km: z.number().optional(),
  visit_duration_hours: z.number().optional(),
});

export const bookingSchema = z.object({
  booking_type: z.enum(["guide", "hotel", "package"]),
  booking_date: z.string().min(1, "التاريخ مطلوب"),
  notes: z.string().optional(),
});
