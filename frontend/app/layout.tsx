import type { Metadata, Viewport } from "next";
import { Inter } from "next/font/google";
import { ThemeProvider } from "next-themes";
import "./globals.css";

const inter = Inter({
  subsets: ["latin"],
  variable: "--font-inter",
  display: "swap",
});

export const metadata: Metadata = {
  title: {
    default: "PainToAd AI — Turn Customer Pain Points into Winning Campaigns",
    template: "%s | PainToAd AI",
  },
  description:
    "AI-powered marketing intelligence platform. Scrape real customer pain points from Reddit, Quora, Google Reviews & more — then generate ROI-predicted ad campaigns instantly.",
  keywords: [
    "AI marketing",
    "pain point analysis",
    "ad campaign generator",
    "customer intelligence",
    "ROI prediction",
    "Compass Crew",
  ],
  authors: [{ name: "Compass Crew" }],
  openGraph: {
    title: "PainToAd AI",
    description: "Turn Customer Pain Points into Winning Campaigns",
    type: "website",
  },
};

export const viewport: Viewport = {
  themeColor: [
    { media: "(prefers-color-scheme: light)", color: "#F8F8FB" },
    { media: "(prefers-color-scheme: dark)",  color: "#14121E" },
  ],
  width: "device-width",
  initialScale: 1,
};

export default function RootLayout({
  children,
}: {
  children: React.ReactNode;
}) {
  return (
    <html lang="en" suppressHydrationWarning className={inter.variable}>
      <body>
        <ThemeProvider
          attribute="class"
          defaultTheme="light"
          enableSystem
          disableTransitionOnChange={false}
          storageKey="paintoad-theme"
        >
          {children}
        </ThemeProvider>
      </body>
    </html>
  );
}
