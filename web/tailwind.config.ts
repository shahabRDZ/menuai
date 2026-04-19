import type { Config } from "tailwindcss";

const config: Config = {
  content: ["./src/**/*.{ts,tsx}"],
  theme: {
    extend: {
      colors: {
        ink: {
          50: "#f7f6f3",
          100: "#eae7df",
          200: "#d4ccbc",
          500: "#6b6252",
          700: "#3a3427",
          900: "#1a1712",
        },
        accent: {
          500: "#e26a2c",
          600: "#c9581f",
        },
      },
      fontFamily: {
        sans: ["ui-sans-serif", "system-ui", "-apple-system", "Segoe UI", "Roboto", "sans-serif"],
        display: ["ui-serif", "Georgia", "serif"],
      },
    },
  },
  plugins: [],
};

export default config;
