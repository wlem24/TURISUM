export function formatPrice(amount, currency = "SAR", lang = "ar") {
  return new Intl.NumberFormat(lang === "ar" ? "ar-SA" : "en-SA", {
    style: "currency",
    currency,
    minimumFractionDigits: 0,
  }).format(amount);
}

export function formatDate(dateStr, lang = "ar") {
  return new Intl.DateTimeFormat(lang === "ar" ? "ar-SA" : "en-SA", {
    year: "numeric",
    month: "long",
    day: "numeric",
  }).format(new Date(dateStr));
}

export function formatDistance(km) {
  if (km < 1) return `${Math.round(km * 1000)} م`;
  return `${km.toFixed(1)} كم`;
}

export function formatDuration(hours) {
  if (hours < 1) return `${Math.round(hours * 60)} دقيقة`;
  if (hours === 1) return "ساعة واحدة";
  if (hours === 2) return "ساعتان";
  return `${hours} ساعات`;
}
