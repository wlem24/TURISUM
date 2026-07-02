import clsx from "clsx";

export default function Button({
  children,
  variant = "primary",
  size = "md",
  loading = false,
  disabled = false,
  className = "",
  type = "button",
  onClick,
  ...props
}) {
  const base = "inline-flex items-center justify-center font-semibold rounded-xl transition-all duration-200 active:scale-95 disabled:opacity-50 disabled:cursor-not-allowed";
  const variants = {
    primary: "bg-primary-500 hover:bg-primary-600 text-white shadow-sm hover:shadow-md",
    secondary: "bg-white border border-gray-200 text-gray-700 hover:bg-gray-50",
    danger: "bg-red-500 hover:bg-red-600 text-white",
    ghost: "text-primary-600 hover:bg-primary-50",
    outline: "border border-primary-500 text-primary-600 hover:bg-primary-50",
  };
  const sizes = {
    sm: "text-sm px-4 py-1.5",
    md: "text-sm px-6 py-2.5",
    lg: "text-base px-8 py-3",
  };

  return (
    <button
      type={type}
      onClick={onClick}
      disabled={disabled || loading}
      className={clsx(base, variants[variant], sizes[size], className)}
      {...props}
    >
      {loading && (
        <svg className="animate-spin -ms-1 me-2 h-4 w-4" fill="none" viewBox="0 0 24 24">
          <circle className="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" strokeWidth="4" />
          <path className="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4z" />
        </svg>
      )}
      {children}
    </button>
  );
}
