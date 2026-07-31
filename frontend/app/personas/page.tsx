"use client";

import { useState, useEffect } from "react";
import { Users, Sparkles, RefreshCw, ArrowRight } from "lucide-react";
import Link from "next/link";
import { Sidebar } from "@/components/sidebar/Sidebar";
import { Navbar } from "@/components/navbar/Navbar";
import { Button } from "@/components/ui/button";
import { Badge } from "@/components/ui/badge";
import { Card } from "@/components/ui/card";
import { StaggerContainer, StaggerItem } from "@/components/ui/motion";
import { PersonaCard, type PersonaCardProps } from "@/components/personas/PersonaCard";

const PERSONAS: (PersonaCardProps & { id: string })[] = [
  {
    id: "p1",
    emoji: "💼",
    name: "Working Professional",
    ageRange: "25–40 years · Urban India",
    description:
      "Tech-savvy, time-poor, values efficiency. Uses multiple SaaS tools daily and is quick to churn if onboarding is painful.",
    needs: [
      "Quick setup with no learning curve",
      "Mobile-first experience",
      "Reliable integrations with existing tools",
      "24/7 responsive support",
    ],
    purchasingPower: "high",
    channels: ["LinkedIn", "Google Search", "Email", "Twitter / X"],
    topPains: [
      "Slow or confusing onboarding flows",
      "Poor mobile app experience",
      "Delayed customer support responses",
    ],
    color: "brand",
  },
  {
    id: "p2",
    emoji: "👨‍👩‍👧",
    name: "Parent & Caregiver",
    ageRange: "30–50 years · Tier 1 & 2 cities",
    description:
      "Value-conscious, trust-driven buyer. Makes purchase decisions carefully and reads reviews before committing.",
    needs: [
      "Clear pricing with no hidden fees",
      "Simple, accessible UI",
      "Trustworthy brand with social proof",
      "Hindi / regional language support",
    ],
    purchasingPower: "medium",
    channels: ["WhatsApp", "Facebook", "Justdial", "Google Reviews"],
    topPains: [
      "Hidden charges on invoice",
      "Complex billing and refund processes",
      "Lack of regional language support",
    ],
    color: "medium",
  },
  {
    id: "p3",
    emoji: "🚀",
    name: "Startup Founder & SMB Owner",
    ageRange: "28–45 years · Metros",
    description:
      "ROI-obsessed, agile decision-maker. Needs tools that move fast, scale efficiently, and don't require heavy setup.",
    needs: [
      "Fast deployment and quick time-to-value",
      "Flexible, transparent pricing",
      "Direct ROI tracking and analytics",
      "Self-serve onboarding",
    ],
    purchasingPower: "premium",
    channels: ["Twitter / X", "LinkedIn", "Reddit", "Google Search"],
    topPains: [
      "Aggressive pricing jumps on scaling",
      "Lack of self-serve custom controls",
      "Vague marketing ROI promises",
    ],
    color: "high",
  },
];

export default function PersonasPage() {
  const [sidebarOpen, setSidebarOpen] = useState(false);
  const [filterPower, setFilterPower] = useState<"all" | "low" | "medium" | "high" | "premium">("all");
  const [personasData, setPersonasData] = useState<(PersonaCardProps & { id: string })[]>(PERSONAS);

  useEffect(() => {
    try {
      const stored = localStorage.getItem("painToAdData");
      if (stored) {
        const parsed = JSON.parse(stored);
        const aiPersonas = parsed.personas?.personas || [];
        
        if (aiPersonas.length > 0) {
          const formatted = aiPersonas.map((p: any, index: number) => {
            let power: "low" | "medium" | "high" | "premium" = "medium";
            const inc = (p.income_level || p.customer_value || "").toLowerCase();
            if (inc.includes("high") || inc.includes("premium")) power = "high";
            if (inc.includes("low") || inc.includes("budget")) power = "low";

            return {
              id: `ai-persona-${index}`,
              emoji: ["💼", "👨‍👩‍👧", "🚀", "🎯", "🎓", "📱"][index % 6],
              name: p.persona_name || "Target Persona",
              ageRange: `${p.age_group || "Unknown"} · ${p.occupation || ""}`,
              description: p.buying_behaviour || p.marketing_message || "Target customer based on AI analysis.",
              needs: p.primary_goals || p.decision_factors || ["Reliability", "Trust"],
              purchasingPower: power,
              channels: p.preferred_channels || ["Digital Platforms"],
              topPains: p.pain_points || ["Various frustrations"],
              color: power === "high" || power === "premium" ? "high" : power === "medium" ? "medium" : "brand",
            };
          });
          setPersonasData(formatted);
        }
      }
    } catch (e) {
      console.error("Failed to load AI personas", e);
    }
  }, []);

  const filtered = personasData.filter((p) => {
    if (filterPower === "all") return true;
    return p.purchasingPower === filterPower || (filterPower === "high" && p.purchasingPower === "premium");
  });

  return (
    <div className="flex min-h-dvh bg-surface-bg">
      <Sidebar isOpen={sidebarOpen} onClose={() => setSidebarOpen(false)} />
      <div className="flex flex-1 flex-col lg:pl-64">
        <Navbar onMobileMenuToggle={() => setSidebarOpen(true)} />

        <main className="flex-1 p-5 lg:p-8 space-y-6">
          {/* Header */}
          <div className="flex flex-col sm:flex-row sm:items-center sm:justify-between gap-4">
            <div>
              <h1 className="text-2xl font-bold text-ink tracking-tight">Persona Intelligence</h1>
              <p className="text-sm text-ink-muted mt-0.5">
                AI-synthesized target customer profiles derived from scraped pain points.
              </p>
            </div>
            <div className="flex items-center gap-2">
              <Badge variant="brand">
                <Sparkles className="h-3.5 w-3.5" />
                {personasData.length} Active Personas
              </Badge>
            </div>
          </div>

          {/* Stats summary */}
          <StaggerContainer className="grid grid-cols-2 sm:grid-cols-4 gap-4">
            {[
              { label: "Total Personas",    value: personasData.length,                                             sub: "Across all topics" },
              { label: "High Spenders",     value: personasData.filter((p) => p.purchasingPower === "high" || p.purchasingPower === "premium").length, sub: "Premium + High" },
              { label: "Budget Conscious",  value: personasData.filter((p) => p.purchasingPower === "low").length,  sub: "Price-sensitive" },
              { label: "Channels Covered",  value: 10,                                                          sub: "Across all personas" },
            ].map((s) => (
              <StaggerItem key={s.label}>
                <Card className="flex flex-col gap-1">
                  <span className="text-2xl font-bold text-ink">{s.value}</span>
                  <span className="text-sm text-ink-muted leading-tight">{s.label}</span>
                  <span className="text-xs text-ink-faint">{s.sub}</span>
                </Card>
              </StaggerItem>
            ))}
          </StaggerContainer>

          {/* Filter */}
          <div className="flex items-center gap-3">
            <Users className="h-4 w-4 text-ink-faint" />
            <div className="flex items-center rounded-lg border border-surface-border bg-surface-card overflow-hidden">
              {(["all", "low", "medium", "high", "premium"] as const).map((f) => (
                <button
                  key={f}
                  onClick={() => setFilterPower(f)}
                  className={`px-3 py-1.5 text-xs font-medium capitalize transition-colors ${
                    filterPower === f
                      ? "bg-brand-500 text-white"
                      : "text-ink-muted hover:text-ink hover:bg-surface-subtle"
                  }`}
                >
                  {f === "all" ? "All" : f}
                </button>
              ))}
            </div>
            <span className="text-xs text-ink-faint">
              {filtered.length} persona{filtered.length !== 1 ? "s" : ""}
            </span>
          </div>

          {/* Persona grid */}
          <StaggerContainer className="grid grid-cols-1 md:grid-cols-2 xl:grid-cols-3 gap-5">
            {filtered.map((persona) => {
              const { id, ...rest } = persona;
              return (
                <StaggerItem key={id}>
                  <PersonaCard {...rest} />
                </StaggerItem>
              );
            })}
          </StaggerContainer>

          {filtered.length === 0 && (
            <Card className="text-center py-12">
              <p className="text-ink-muted text-sm">No personas match this filter.</p>
              <Button variant="ghost" size="sm" className="mt-3" onClick={() => setFilterPower("all")}>
                Clear filter
              </Button>
            </Card>
          )}

          {/* CTA to campaigns */}
          <div className="rounded-xl border border-brand-200 dark:border-brand-600/30 bg-brand-50 dark:bg-brand-100/10 p-5 flex flex-col sm:flex-row sm:items-center sm:justify-between gap-4">
            <div className="flex items-start gap-3">
              <Sparkles className="h-5 w-5 text-brand-500 mt-0.5 shrink-0" />
              <div>
                <p className="font-semibold text-ink text-sm">Ready to generate campaigns?</p>
                <p className="text-sm text-ink-muted mt-0.5">
                  Use these personas to generate targeted ads, WhatsApp messages, and email campaigns.
                </p>
              </div>
            </div>
            <Link href="/campaigns" className="shrink-0">
              <Button size="sm" rightIcon={<ArrowRight className="h-3.5 w-3.5" />}>
                Go to Campaigns
              </Button>
            </Link>
          </div>
        </main>
      </div>
    </div>
  );
}
