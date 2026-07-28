import Link from "next/link";
import { Sparkles, ArrowRight } from "lucide-react";
import { Button } from "@/components/ui/button";

const LINKS = {
  product: [
    { label: "Dashboard", href: "/dashboard" },
    { label: "Analyze Pains", href: "/analyze" },
    { label: "Personas", href: "/personas" },
    { label: "Campaigns", href: "/campaigns" },
    { label: "Insights", href: "/insights" },
    { label: "Optimizer", href: "/optimizer" },
    { label: "Simulator", href: "/simulator" },
  ],
  team: [
    { label: "Muskan — UI/UX", href: "#" },
    { label: "Sanjana — AI/Agents", href: "#" },
    { label: "Krrish — Backend", href: "#" },
    { label: "Saloni — Analytics/ML", href: "#" },
    { label: "Kamal — Architecture", href: "#" },
  ],
};

export function Footer() {
  return (
    <footer className="border-t border-surface-border bg-surface-subtle/60 mt-auto">
      <div className="mx-auto max-w-7xl px-4 sm:px-6 lg:px-8 py-12">
        <div className="grid grid-cols-1 md:grid-cols-3 gap-10">
          {/* Brand */}
          <div className="space-y-4">
            <div className="flex items-center gap-2.5">
              <div className="flex h-9 w-9 items-center justify-center rounded-xl bg-brand-500 text-white shadow-sm">
                <Sparkles className="h-5 w-5" />
              </div>
              <span className="font-semibold text-lg tracking-tight text-ink">
                PainToAd<span className="text-brand-500">AI</span>
              </span>
            </div>
            <p className="text-sm text-ink-muted leading-relaxed max-w-xs">
              AI-powered marketing intelligence. Turn real customer pain points
              into winning, ROI-predicted campaigns.
            </p>
            <div className="flex items-center gap-2 pt-1">
              <Link href="/dashboard">
                <Button variant="primary" size="sm" rightIcon={<ArrowRight className="h-3.5 w-3.5" />}>
                  Launch App
                </Button>
              </Link>
            </div>
          </div>

          {/* Product Links */}
          <div>
            <h3 className="text-xs font-semibold uppercase tracking-wider text-ink-faint mb-4">
              Product
            </h3>
            <ul className="space-y-2.5">
              {LINKS.product.map((l) => (
                <li key={l.href}>
                  <Link
                    href={l.href}
                    className="text-sm text-ink-muted hover:text-ink transition-colors"
                  >
                    {l.label}
                  </Link>
                </li>
              ))}
            </ul>
          </div>

          {/* Team */}
          <div>
            <h3 className="text-xs font-semibold uppercase tracking-wider text-ink-faint mb-4">
              Team — Compass Crew
            </h3>
            <ul className="space-y-2.5">
              {LINKS.team.map((l) => (
                <li key={l.label} className="text-sm text-ink-muted">
                  {l.label}
                </li>
              ))}
            </ul>
          </div>
        </div>

        <div className="mt-10 pt-6 border-t border-surface-border flex flex-col sm:flex-row items-center justify-between gap-3 text-xs text-ink-faint">
          <p>© 2025 PainToAd AI · Compass Crew · AI for Marketers Hackathon</p>
          <p>Built with Next.js, Tailwind, and a lot of caffeine ☕</p>
        </div>
      </div>
    </footer>
  );
}
