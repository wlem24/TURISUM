import { BrowserRouter } from "react-router-dom";
import { QueryClient, QueryClientProvider } from "@tanstack/react-query";
import { Toaster } from "react-hot-toast";
import { AuthProvider } from "@/contexts/AuthContext";
import { LanguageProvider } from "@/contexts/LanguageContext";
import { ThemeProvider } from "@/contexts/ThemeContext";
import { NotificationProvider } from "@/contexts/NotificationContext";
import AppRoutes from "@/routes/AppRoutes";
import "@/styles/globals.css";

const queryClient = new QueryClient({
  defaultOptions: {
    queries: {
      retry: 1,
      staleTime: 5 * 60 * 1000, // 5 minutes
      refetchOnWindowFocus: false,
    },
  },
});

export default function App() {
  return (
    <BrowserRouter>
      <QueryClientProvider client={queryClient}>
        <LanguageProvider>
          <ThemeProvider>
            <AuthProvider>
              <NotificationProvider>
                <AppRoutes />
                <Toaster
                  position="top-center"
                  toastOptions={{
                    duration: 3000,
                    style: {
                      background: "#fff",
                      color: "#111827",
                      borderRadius: "12px",
                      boxShadow: "0 4px 20px rgba(0,0,0,0.1)",
                      fontFamily: "Cairo, Inter, sans-serif",
                    },
                    success: { iconTheme: { primary: "#3B6D11", secondary: "#fff" } },
                  }}
                />
              </NotificationProvider>
            </AuthProvider>
          </ThemeProvider>
        </LanguageProvider>
      </QueryClientProvider>
    </BrowserRouter>
  );
}
