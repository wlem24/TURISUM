/** @type {import('tailwindcss').Config} */
export default {
  content: ["./index.html", "./src/**/*.{js,jsx,ts,tsx}"],
  darkMode: ["selector", '[data-theme="dark"]'],
  theme: {
    extend: {
      colors: {
        // Athar (أثر) brand ramp — primary-500 is the declared "primary base" (#3B6D11)
        // used pervasively across components as the default action color.
        primary: {
          50: "#F5F2EC",
          100: "#EAF3DE",
          200: "#C0DD97",
          300: "#97C459",
          400: "#639922",
          500: "#3B6D11",
          600: "#27500A",
          700: "#173404",
          800: "#0D1F12",
          900: "#0A160D",
        },
        // Athar gold accent ramp — sand-500 is the declared CTA/highlight gold.
        sand: {
          50: "#FAEEDA",
          100: "#FAEEDA",
          200: "#FAC775",
          300: "#FAC775",
          400: "#EF9F27",
          500: "#EF9F27",
          600: "#BA7517",
          700: "#BA7517",
          800: "#412402",
          900: "#2B1801",
        },
      },
      fontFamily: {
        arabic: ["Cairo", "Noto Sans Arabic", "sans-serif"],
        latin: ["Inter", "Plus Jakarta Sans", "sans-serif"],
      },
    },
  },
  plugins: [],
};
