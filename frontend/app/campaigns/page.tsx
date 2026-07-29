"use client";

import { useState } from "react";
import {
  Sparkles,
  RefreshCw,
  Download,
  SlidersHorizontal,
  Languages,
} from "lucide-react";
import { Sidebar } from "@/components/sidebar/Sidebar";
import { Navbar } from "@/components/navbar/Navbar";
import { Button } from "@/components/ui/button";
import { Badge } from "@/components/ui/badge";
import { Card, CardHeader, CardTitle, CardDescription } from "@/components/ui/card";
import { StaggerContainer, StaggerItem } from "@/components/ui/motion";
import { AdCard, type AdType } from "@/components/ads/AdCard";
import { cn } from "@/lib/utils";

/* ── Config ────────────────────────────────────────────────── */
const AD_TYPES: { id: AdType; label: string; emoji: string }[] = [
  { id: "google-search",  label: "Google Search", emoji: "🔍" },
  { id: "facebook",       label: "Facebook",      emoji: "📘" },
  { id: "instagram",      label: "Instagram",     emoji: "📷" },
  { id: "whatsapp",       label: "WhatsApp",      emoji: "💬" },
  { id: "email",          label: "Email",         emoji: "📧" },
  { id: "seo",            label: "SEO / Blog",    emoji: "📝" },
  { id: "landing",        label: "Landing Page",  emoji: "🖥️" },
];

const LANGUAGES = ["English", "Hinglish", "Hindi", "Bengali"] as const;
const TONES     = ["Professional", "Conversational", "Urgent", "Friendly", "Empathetic"] as const;
const PERSONAS  = ["All", "Working Professional", "Parent & Caregiver", "Startup Founder", "SMB Owner"] as const;

type Language = typeof LANGUAGES[number];
type Tone     = typeof TONES[number];
type PersonaFilter = typeof PERSONAS[number];

/* ── Mock campaign data per type + persona ─────────────────── */
const buildMockAds = (type: AdType, lang: Language, tone: Tone, persona: PersonaFilter) => {
  const p = persona === "All" ? "Working Professional" : persona;
  return [
    {
      id: `${type}-1`,
      type,
      headline: `Stop Losing Customers to Painful ${type === "seo" ? "Onboarding Experiences" : "Onboarding"}`,
      body:
        `We analyzed 500+ real complaints from ${p}s just like yours. They leave because onboarding is confusing, support is slow, and pricing is hidden. Our AI figures out exactly what to fix — and writes the campaigns that will bring them back.`,
      cta: type === "email" ? "Read the Full Analysis →" : type === "whatsapp" ? "Chat with us now 💬" : "Start Free Today",
      persona: p,
      language: lang,
      tone,
      ctrPrediction: 4.7,
      audienceFitScore: 92,
      predictedRoi: 340,
    },
    {
      id: `${type}-2`,
      type,
      headline: `Your Customers Are Telling You What They Hate. Are You Listening?`,
      body:
        `Reddit, Quora, Google Reviews — real voices from real buyers. PainToAd AI scrapes the pain, maps the personas, and generates high-converting ad copy automatically.`,
      cta: type === "whatsapp" ? "Get instant demo on WhatsApp" : "Generate Campaign Now",
      persona: p,
      language: lang,
      tone,
      ctrPrediction: 3.9,
      audienceFitScore: 88,
      predictedRoi: 290,
    },
    {
      id: `${type}-3`,
      type,
      headline: `From Scraped Pain Point to High-ROI Campaign in 3 Minutes`,
      body:
        `No more guessing what your target audience wants. See top complaints ranked by emotional intensity, and launch multi-channel campaigns with pre-launch ROI estimates.`,
      cta: type === "email" ? "Get Your Custom Brief →" : "See Live Demo",
      persona: p,
      language: lang,
      tone,
      ctrPrediction: 5.1,
      audienceFitScore: 95,
      predictedRoi: 410,
    },
  ];
};

export default function CampaignsPage() {
  const [sidebarOpen, setSidebarOpen] = useState(false);
  const [activeType, setActiveType] = useState<AdType>("google-search");
  const [language, setLanguage]     = useState<Language>("English");
  const [tone, setTone]             = useState<Tone>("Professional");
  const [persona, setPersona]       = useState<PersonaFilter>("All");
  const [generating, setGenerating] = useState(false);
  const [regeneratingId, setRegeneratingId] = useState<string | null>(null);

  const ads = buildMockAds(activeType, language, tone, persona);

  const handleGenerate = async () => {
    setGenerating(true);
    await new Promise((r) => setTimeout(r, 1200));
    setGenerating(false);
  };

  const handleRegenerate = async (id: string) => {
    setRegeneratingId(id);
    await new Promise((r) => setTimeout(r, 800));
    setRegeneratingId(null);
  };

  return (
    <div className="flex min-h-dvh bg-surface-bg">
      <Sidebar isOpen={sidebarOpen} onClose={() => setSidebarOpen(false)} />
      <div className="flex flex-1 flex-col lg:pl-64">
        <Navbar onMobileMenuToggle={() => setSidebarOpen(true)} />

        <main className="flex-1 p-5 lg:p-8 space-y-6">
          {/* Header */}
          <div className="flex flex-col sm:flex-row sm:items-center sm:justify-between gap-4">
            <div>
              <h1 className="text-2xl font-bold text-ink tracking-tight">Campaign Generator</h1>
              <p className="text-sm text-ink-muted mt-0.5">
                Multi-channel ad copy generated directly from customer pain points.
              </p>
            </div>
            <div className="flex items-center gap-2">
              <Button variant="outline" size="sm" leftIcon={<Download className="h-3.5 w-3.5" />}>
                Export All Assets
              </Button>
              <Button
                size="sm"
                loading={generating}
                leftIcon={!generating ? <Sparkles className="h-3.5 w-3.5" /> : undefined}
                onClick={handleGenerate}
              >
                Regenerate All
              </Button>
            </div>
          </div>

          {/* Control Panel */}
          <Card>
            <CardHeader className="pb-3">
              <div className="flex items-center justify-between">
                <div className="flex items-center gap-2">
                  <SlidersHorizontal className="h-4 w-4 text-brand-500" />
                  <CardTitle>Campaign Controls</CardTitle>
                </div>
                <Badge variant="brand">AI Tone & Persona Engine</Badge>
              </div>
              <CardDescription>
                Customize language, tone, and target persona for real-time copy generation
              </CardDescription>
            </CardHeader>
            <div className="px-5 pb-5 space-y-4 border-t border-surface-border pt-4">
              <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
                {/* Language Picker */}
                <div className="space-y-1.5">
                  <label className="text-xs font-semibold uppercase tracking-wider text-ink-faint flex items-center gap-1">
                    <Languages className="h-3.5 w-3.5" /> Language
                  </label>
                  <div className="flex flex-wrap gap-1.5">
                    {LANGUAGES.map((l) => (
                      <button
                        key={l}
                        onClick={() => setLanguage(l)}
                        className={cn(
                          "rounded-lg border px-3 py-1.5 text-xs font-medium transition-all",
                          language === l
                            ? "bg-brand-500 text-white border-brand-500"
                            : "bg-surface-card border-surface-border text-ink-muted hover:border-brand-300 hover:text-ink"
                        )}
                      >
                        {l}
                      </button>
                    ))}
                  </div>
                </div>

                {/* Tone Picker */}
                <div className="space-y-1.5">
                  <label className="text-xs font-semibold uppercase tracking-wider text-ink-faint">
                    Tone of Voice
                  </label>
                  <div className="flex flex-wrap gap-1.5">
                    {TONES.map((t) => (
                      <button
                        key={t}
                        onClick={() => setTone(t)}
                        className={cn(
                          "rounded-lg border px-3 py-1.5 text-xs font-medium transition-all",
                          tone === t
                            ? "bg-brand-500 text-white border-brand-500"
                            : "bg-surface-card border-surface-border text-ink-muted hover:border-brand-300 hover:text-ink"
                        )}
                      >
                        {t}
                      </button>
                    ))}
                  </div>
                </div>

                {/* Persona Filter */}
                <div className="space-y-1.5">
                  <label className="text-xs font-semibold uppercase tracking-wider text-ink-faint">
                    Target Persona
                  </label>
                  <div className="flex flex-wrap gap-1.5">
                    {PERSONAS.map((p) => (
                      <button
                        key={p}
                        onClick={() => setPersona(p)}
                        className={cn(
                          "rounded-lg border px-3 py-1.5 text-xs font-medium transition-all",
                          persona === p
                            ? "bg-brand-500 text-white border-brand-500"
                            : "bg-surface-card border-surface-border text-ink-muted hover:border-brand-300 hover:text-ink"
                        )}
                      >
                        {p === "All" ? "All Personas" : p.split(" ")[0]}
                      </button>
                    ))}
                  </div>
                </div>
              </div>
            </div>
          </Card>

          {/* Channel type tabs */}
          <div className="flex items-center gap-1.5 overflow-x-auto pb-1 scrollbar-thin">
            {AD_TYPES.map((t) => (
              <button
                key={t.id}
                onClick={() => setActiveType(t.id)}
                className={cn(
                  "flex items-center gap-1.5 whitespace-nowrap rounded-xl border px-4 py-2 text-sm font-medium transition-all shrink-0",
                  activeType === t.id
                    ? "bg-brand-500 text-white border-brand-500 shadow-sm"
                    : "bg-surface-card border-surface-border text-ink-muted hover:border-brand-300 hover:text-ink"
                )}
              >
                <span>{t.emoji}</span>
                {t.label}
                {activeType === t.id && (
                  <Badge variant="default" className="ml-1 bg-white/20 text-white border-white/20 text-[10px]">
                    {ads.length}
                  </Badge>
                )}
              </button>
            ))}
          </div>

          {/* Active channel header */}
          <div className="flex items-center justify-between">
            <div>
              <h2 className="font-semibold text-ink">
                {AD_TYPES.find((t) => t.id === activeType)?.label} Campaigns
              </h2>
              <p className="text-xs text-ink-muted mt-0.5">
                {ads.length} variants · {language} · {tone} tone
                {persona !== "All" && ` · ${persona}`}
              </p>
            </div>
            <Button
              variant="ghost"
              size="sm"
              loading={generating}
              leftIcon={!generating ? <RefreshCw className="h-3.5 w-3.5" /> : undefined}
              onClick={handleGenerate}
            >
              Refresh tab
            </Button>
          </div>

          {/* Ad cards grid */}
          <StaggerContainer className="grid grid-cols-1 lg:grid-cols-2 xl:grid-cols-3 gap-4">
            {ads.map((ad) => (
              <StaggerItem key={ad.id}>
                <AdCard
                  {...ad}
                  onRegenerate={handleRegenerate}
                  regenerating={regeneratingId === ad.id}
                />
              </StaggerItem>
            ))}
          </StaggerContainer>

          {/* Bottom tip */}
          <div className="rounded-xl border border-surface-border bg-surface-subtle/60 p-4 flex items-start gap-3 text-sm text-ink-muted">
            <Sparkles className="h-4 w-4 text-brand-500 shrink-0 mt-0.5" />
            <p>
              <span className="font-medium text-ink">Tip:</span> Switch language to{" "}
              <strong>Hinglish</strong> or <strong>Hindi</strong> to see how the campaigns adapt
              for regional audiences. Tone changes affect formality and urgency of the copy.
            </p>
          </div>
        </main>
      </div>
    </div>
  );
}
