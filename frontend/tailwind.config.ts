import type { Config } from "tailwindcss";

const config: Config = {
  content: [
    "./src/pages/**/*.{js,ts,jsx,tsx,mdx}",
    "./src/components/**/*.{js,ts,jsx,tsx,mdx}",
    "./src/app/**/*.{js,ts,jsx,tsx,mdx}",
  ],
  theme: {
    extend: {
      colors: {
        primary: {
          50: "#f0fdf4",
          100: "#dcfce7",
          200: "#bbf7d0",
          300: "#86efac",
          400: "#4ade80",
          500: "#00A651",
          600: "#008C45",
          700: "#007038",
          800: "#005A2E",
          900: "#004524",
        },
        secondary: {
          50: "#eff6ff",
          100: "#dbeafe",
          200: "#bfdbfe",
          300: "#93c5fd",
          400: "#60a5fa",
          500: "#00A0DC",
          600: "#0084B8",
          700: "#006994",
          800: "#005070",
          900: "#00374C",
        },
        accent: {
          500: "#FDD116",
          600: "#E5BC14",
        },
      },
    },
  },
  plugins: [],
};
export default config;
