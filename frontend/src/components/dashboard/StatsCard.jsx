export default function StatsCard({ title, value, icon, color = "primary", change }) {
  const colors = {
    primary: "bg-primary-50 text-primary-600",
    blue: "bg-blue-50 text-blue-600",
    yellow: "bg-yellow-50 text-yellow-600",
    red: "bg-red-50 text-red-600",
    green: "bg-green-50 text-green-600",
  };

  return (
    <div className="card p-5">
      <div className="flex items-start justify-between">
        <div>
          <p className="text-sm font-medium text-gray-500">{title}</p>
          <p className="text-3xl font-bold text-gray-900 mt-1">{value}</p>
          {change !== undefined && (
            <p className={`text-xs mt-1 ${change >= 0 ? "text-green-600" : "text-red-500"}`}>
              {change >= 0 ? "↑" : "↓"} {Math.abs(change)}%
            </p>
          )}
        </div>
        <div className={`w-12 h-12 rounded-xl flex items-center justify-center text-2xl ${colors[color]}`}>
          {icon}
        </div>
      </div>
    </div>
  );
}
