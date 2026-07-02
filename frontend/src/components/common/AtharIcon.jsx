// Athar (أثر) brand mark — layered rectangles representing ancient ruins / layers of history.
// Do not redesign into a compass or generic map pin; the layered-rectangle concept is the brand icon.
export default function AtharIcon({ size = 36, className = "", rounded = "rounded-xl" }) {
  return (
    <div
      className={`bg-primary-500 flex items-center justify-center flex-shrink-0 ${rounded} ${className}`}
      style={{ width: size, height: size }}
    >
      <svg width={size * 0.62} height={size * 0.62} viewBox="0 0 48 48" role="img" aria-label="أثر">
        <rect x="0" y="14" width="48" height="34" rx="5" fill="#1a3320" />
        <rect x="6" y="22" width="36" height="22" rx="4" fill="#27500A" />
        <rect x="12" y="8" width="24" height="16" rx="3" fill="#3B6D11" />
        <rect x="18" y="2" width="12" height="8" rx="2" fill="#639922" />
        <circle cx="24" cy="36" r="3" fill="#97C459" />
      </svg>
    </div>
  );
}
