import clsx from "clsx";
import { forwardRef } from "react";

const Input = forwardRef(function Input(
  { label, error, className = "", hint, ...props },
  ref
) {
  return (
    <div className="flex flex-col gap-1">
      {label && (
        <label className="text-sm font-medium text-gray-700">{label}</label>
      )}
      <input
        ref={ref}
        className={clsx(
          "w-full border rounded-xl px-4 py-2.5 text-sm transition-all duration-200 bg-white focus:outline-none focus:ring-2 focus:ring-primary-500 focus:border-transparent",
          error ? "border-red-400 bg-red-50" : "border-gray-200",
          className
        )}
        {...props}
      />
      {hint && !error && <p className="text-xs text-gray-400">{hint}</p>}
      {error && <p className="text-xs text-red-500">{error}</p>}
    </div>
  );
});

export default Input;
