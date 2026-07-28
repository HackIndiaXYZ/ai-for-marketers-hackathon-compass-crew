import type { Config } from "tailwindcss";

const config: Config = {
  darkMode: "class",
  content: [
    "./app/**/*.{ts,tsx,js,jsx,mdx}",
    "./components/**/*.{ts,tsx,js,jsx,mdx}",
    "./pages/**/*.{ts,tsx,js,jsx,mdx}",
  ],
  theme: {
    extend: {
      colors: {
        // ── Brand ──────────────────────────────────────────────
        brand: {
          50:  "rgb(var(--brand-50) / <alpha-value>)",
          100: "rgb(var(--brand-100) / <alpha-value>)",
          200: "rgb(var(--brand-200) / <alpha-value>)",
          300: "rgb(var(--brand-300) / <alpha-value>)",
          400: "rgb(var(--brand-400) / <alpha-value>)",
          500: "rgb(var(--brand-500) / <alpha-value>)",
          600: "rgb(var(--brand-600) / <alpha-value>)",
          700: "rgb(var(--brand-700) / <alpha-value>)",
        },
        // ── Semantic surfaces ───────────────────────────────────
        surface: {
          bg:      "rgb(var(--surface-bg) / <alpha-value>)",
          card:    "rgb(var(--surface-card) / <alpha-value>)",
          subtle:  "rgb(var(--surface-subtle) / <alpha-value>)",
          border:  "rgb(var(--surface-border) / <alpha-value>)",
        },
        // ── Text ────────────────────────────────────────────────
        ink: {
          DEFAULT: "rgb(var(--ink) / <alpha-value>)",
          muted:   "rgb(var(--ink-muted) / <alpha-value>)",
          faint:   "rgb(var(--ink-faint) / <alpha-value>)",
        },
        // ── Status pastels ──────────────────────────────────────
        pain: {
          high:   "rgb(var(--pain-high) / <alpha-value>)",
          medium: "rgb(var(--pain-medium) / <alpha-value>)",
          low:    "rgb(var(--pain-low) / <alpha-value>)",
          "high-bg":   "rgb(var(--pain-high-bg) / <alpha-value>)",
          "medium-bg": "rgb(var(--pain-medium-bg) / <alpha-value>)",
          "low-bg":    "rgb(var(--pain-low-bg) / <alpha-value>)",
        },
      },
      fontFamily: {
        sans: ["var(--font-inter)", "Inter", "ui-sans-serif", "system-ui", "sans-serif"],
      },
      borderRadius: {
        card: "14px",
        lg: "12px",
        xl: "16px",
        "2xl": "20px",
      },
      boxShadow: {
        card:    "0 1px 4px 0 rgba(0,0,0,0.06), 0 4px 16px 0 rgba(0,0,0,0.06)",
        "card-hover": "0 2px 8px 0 rgba(0,0,0,0.08), 0 8px 28px 0 rgba(0,0,0,0.10)",
        glow:    "0 0 0 3px rgba(124,111,205,0.35)",
      },
      keyframes: {
        "fade-up": {
          "0%":   { opacity: "0", transform: "translateY(12px)" },
          "100%": { opacity: "1", transform: "translateY(0)" },
        },
        "fade-in": {
          "0%":   { opacity: "0" },
          "100%": { opacity: "1" },
        },
        shimmer: {
          "0%":   { backgroundPosition: "-200% 0" },
          "100%": { backgroundPosition: "200% 0" },
        },
      },
      animation: {
        "fade-up":  "fade-up 0.4s ease-out both",
        "fade-in":  "fade-in 0.3s ease-out both",
        shimmer:    "shimmer 1.6s linear infinite",
      },
    },
  },
  plugins: [],
};

export default config;
