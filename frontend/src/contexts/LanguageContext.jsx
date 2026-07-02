import { createContext, useContext, useState, useEffect } from "react";
import { useTranslation } from "react-i18next";

const LanguageContext = createContext(null);

export function LanguageProvider({ children }) {
  const { i18n } = useTranslation();
  const [lang, setLang] = useState(() => localStorage.getItem("athar_lang") || "ar");

  const switchLanguage = (newLang) => {
    setLang(newLang);
    localStorage.setItem("athar_lang", newLang);
    i18n.changeLanguage(newLang);
    document.documentElement.setAttribute("lang", newLang);
    document.documentElement.setAttribute("dir", newLang === "ar" ? "rtl" : "ltr");
  };

  useEffect(() => {
    document.documentElement.setAttribute("lang", lang);
    document.documentElement.setAttribute("dir", lang === "ar" ? "rtl" : "ltr");
    i18n.changeLanguage(lang);
  }, [lang, i18n]);

  return (
    <LanguageContext.Provider value={{ lang, isArabic: lang === "ar", switchLanguage }}>
      {children}
    </LanguageContext.Provider>
  );
}

export function useLanguage() {
  const ctx = useContext(LanguageContext);
  if (!ctx) throw new Error("useLanguage must be used inside LanguageProvider");
  return ctx;
}
