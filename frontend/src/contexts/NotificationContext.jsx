import { createContext, useContext, useState } from "react";
import toast from "react-hot-toast";

const NotificationContext = createContext(null);

export function NotificationProvider({ children }) {
  const notify = {
    success: (msg) => toast.success(msg, { duration: 3000 }),
    error: (msg) => toast.error(msg, { duration: 4000 }),
    info: (msg) => toast(msg, { icon: "ℹ️", duration: 3000 }),
  };

  return (
    <NotificationContext.Provider value={{ notify }}>
      {children}
    </NotificationContext.Provider>
  );
}

export function useNotification() {
  const ctx = useContext(NotificationContext);
  if (!ctx) throw new Error("useNotification must be used inside NotificationProvider");
  return ctx;
}
