"use client";

import { useState } from "react";
import {
  Search,
  Sparkles,
  Filter,
  SlidersHorizontal,
  CheckSquare,
  Square,
  ChevronDown,
  X,
  Loader2,
} from "lucide-react";
import { Sidebar } from "@/components/sidebar/Sidebar";
import { Navbar } from "@/components/navbar/Navbar";
import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";
import { Badge } from "@/components/ui/badge";
import { Card, CardHeader, CardTitle, CardDescription } from "@/components/ui/card";
import { PainCard, type PainCardProps, type Intensity } from "@/components/paincards/PainCard";
import { cn } from "@/lib/utils";

/* ── Platforms ─────────────────────────────────────────────── */
const PLATFORMS = [
  { id: "reddit",        label: "Reddit",         emoji: "🔴" },
  { id: "quora",         label: "Quora",           emoji: "🔵" },
  { id: "google",        label: "Google Reviews",  emoji: "⭐" },
  { id: "mouthshut",     label: "MouthShut",       emoji: "💬" },
  { id: "twitter",       label: "Twitter / X",     emoji: "🐦" },
  { id: "justdial",      label: "Justdial",        emoji: "📞" },
  { id: "indiamart",     label: "IndiaMART",       emoji: "🏪" },
];

/* ── Scraping steps animation ──────────────────────────────── */
const SCRAPE_STEPS = [
  "Connecting to platforms...",
  "Collecting customer reviews & posts...",
  "Running NLP pain extraction agents...",
  "Ranking by frequency & emotional intensity...",
  "Generating impact scores...",
  "Analysis complete ✓",
];

/* ── Mock result data ──────────────────────────────────────── */
const MOCK_RESULTS: PainCardProps[] = [
  {
    id: "r1",
    quote: "The onboarding is so confusing — I signed up three times and still don't know what the product does.",
    topic: "Onboarding UX",
    platform: "Reddit",
    mentions: 247,
    intensity: "high",
    impactScore: 94,
    emotionTags: ["Confused", "Frustrated", "Churned"],
    supportingQuotes: [
      "Setup took me 2 hours and I still haven't connected my account properly.",
      "No welcome email, no tutorial. Just a blank dashboard.",
    ],
  },
  {
    id: "r2",
    quote: "Support takes 5 days to reply to a billing issue. I lost business because of it.",
    topic: "Customer Support",
    platform: "Google Reviews",
    mentions: 189,
    intensity: "high",
    impactScore: 88,
    emotionTags: ["Angry", "Helpless", "Lost Revenue"],
    supportingQuotes: [
      "Opened a ticket 6 days ago. Still no resolution.",
      "Auto-reply said 24–48 hours. It's been a week.",
    ],
  },
  {
    id: "r3",
    quote: "The pricing page doesn't explain what I'm actually paying for. Very deceptive.",
    topic: "Pricing Clarity",
    platform: "Quora",
    mentions: 134,
    intensity: "high",
    impactScore: 79,
    emotionTags: ["Distrustful", "Hesitant"],
    supportingQuotes: [
      "Hidden fees showed up only at checkout.",
    ],
  },
  {
    id: "r4",
    quote: "Mobile app crashes every time I try to checkout. Web works fine — why not mobile?",
    topic: "App Stability",
    platform: "MouthShut",
    mentions: 98,
    intensity: "medium",
    impactScore: 67,
    emotionTags: ["Annoyed", "Inconvenienced"],
    supportingQuotes: [
      "This has been a bug for 3+ months with no fix.",
    ],
  },
  {
    id: "r5",
    quote: "Free plan is too limited but the paid plan jumps 10x in price with no middle option.",
    topic: "Pricing Tiers",
    platform: "Twitter / X",
    mentions: 76,
    intensity: "medium",
    impactScore: 58,
    emotionTags: ["Price Sensitive", "Comparing Alternatives"],
    supportingQuotes: [],
  },
  {
    id: "r6",
    quote: "Integration with Google Sheets doesn't work half the time. Very unreliable.",
    topic: "Integrations",
    platform: "Reddit",
    mentions: 54,
    intensity: "medium",
    impactScore: 51,
    emotionTags: ["Frustrated", "Time-wasted"],
    supportingQuotes: [],
  },
  {
    id: "r7",
    quote: "The dashboard is overwhelming on first use. Too many options with no guidance.",
    topic: "UI Complexity",
    platform: "Google Reviews",
    mentions: 43,
    intensity: "low",
    impactScore: 38,
    emotionTags: ["Overwhelmed"],
    supportingQuotes: [],
  },
  {
    id: "r8",
    quote: "Would love a dark mode — not a dealbreaker but would make daily use much nicer.",
    topic: "UI Preferences",
    platform: "Justdial",
    mentions: 22,
    intensity: "low",
    impactScore: 19,
    emotionTags: ["Wishful"],
    supportingQuotes: [],
  },
];

/* ── Filter types ──────────────────────────────────────────── */
type FilterIntensity = "all" | Intensity;
type SortOption = "impact" | "mentions" | "intensity";

/* ── Page ──────────────────────────────────────────────────── */
export default function AnalyzePage() {
  const [sidebarOpen, setSidebarOpen] = useState(false);
  const [topic, setTopic] = useState("");
  const [selectedPlatforms, setSelectedPlatforms] = useState<string[]>(
    PLATFORMS.map((p) => p.id)
  );
  const [isAnalyzing, setIsAnalyzing] = useState(false);
  const [currentStep, setCurrentStep] = useState(0);
  const [results, setResults] = useState<PainCardProps[] | null>(null);
  const [filterIntensity, setFilterIntensity] = useState<FilterIntensity>("all");
  const [sortBy, setSortBy] = useState<SortOption>("impact");
  const [showFilters, setShowFilters] = useState(false);

  const togglePlatform = (id: string) => {
    setSelectedPlatforms((prev) =>
      prev.includes(id) ? prev.filter((p) => p !== id) : [...prev, id]
    );
  };

  const handleAnalyze = async () => {
    if (!topic.trim()) return;
    setIsAnalyzing(true);
    setResults(null);
    setCurrentStep(0);

    for (let i = 0; i < SCRAPE_STEPS.length; i++) {
      await new Promise((r) => setTimeout(r, 700));
      setCurrentStep(i);
    }
    await new Promise((r) => setTimeout(r, 400));
    setResults(MOCK_RESULTS);
    setIsAnalyzing(false);
  };

  const filtered = (results ?? [])
    .filter((r) => filterIntensity === "all" || r.intensity === filterIntensity)
    .sort((a, b) => {
      if (sortBy === "impact")    return b.impactScore - a.impactScore;
      if (sortBy === "mentions")  return b.mentions - a.mentions;
      if (sortBy === "intensity") {
        const order = { high: 0, medium: 1, low: 2 };
        return order[a.intensity] - order[b.intensity];
      }
      return 0;
    });

  const counts = results
    ? {
        high:   results.filter((r) => r.intensity === "high").length,
        medium: results.filter((r) => r.intensity === "medium").length,
        low:    results.filter((r) => r.intensity === "low").length,
      }
    : null;

  return (
    <div className="flex min-h-dvh bg-surface-bg">
      <Sidebar isOpen={sidebarOpen} onClose={() => setSidebarOpen(false)} />
      <div className="flex flex-1 flex-col lg:pl-64">
        <Navbar onMobileMenuToggle={() => setSidebarOpen(true)} />

        <main className="flex-1 p-5 lg:p-8 space-y-6">
          {/* Page header */}
          <div>
            <h1 className="text-2xl font-bold text-ink tracking-tight">Analyze Pain Points</h1>
            <p className="text-sm text-ink-muted mt-0.5">
              Enter a business topic to discover what customers are really struggling with.
            </p>
          </div>

          {/* Input card */}
          <Card>
            <div className="space-y-4">
              {/* Topic input */}
              <div className="flex gap-3">
                <div className="flex-1">
                  <Input
                    placeholder='e.g. "SaaS onboarding", "fintech app", "food delivery in Mumbai"'
                    value={topic}
                    onChange={(e) => setTopic(e.target.value)}
                    onKeyDown={(e) => e.key === "Enter" && handleAnalyze()}
                    leftAdornment={<Search className="h-4 w-4" />}
                    fullWidth
                    label="Business Topic"
                    disabled={isAnalyzing}
                  />
                </div>
                <div className="self-end">
                  <Button
                    onClick={handleAnalyze}
                    loading={isAnalyzing}
                    disabled={!topic.trim() || selectedPlatforms.length === 0}
                    leftIcon={!isAnalyzing ? <Sparkles className="h-4 w-4" /> : undefined}
                    size="md"
                    className="whitespace-nowrap"
                  >
                    Analyze Now
                  </Button>
                </div>
              </div>

              {/* Platform toggles */}
              <div>
                <div className="flex items-center justify-between mb-2">
                  <span className="text-xs font-semibold uppercase tracking-wider text-ink-faint">
                    Platforms to scrape
                  </span>
                  <button
                    className="text-xs text-brand-600 dark:text-brand-400 hover:underline"
                    onClick={() =>
                      setSelectedPlatforms(
                        selectedPlatforms.length === PLATFORMS.length
                          ? []
                          : PLATFORMS.map((p) => p.id)
                      )
                    }
                  >
                    {selectedPlatforms.length === PLATFORMS.length ? "Deselect all" : "Select all"}
                  </button>
                </div>
                <div className="flex flex-wrap gap-2">
                  {PLATFORMS.map((p) => {
                    const active = selectedPlatforms.includes(p.id);
                    return (
                      <button
                        key={p.id}
                        onClick={() => togglePlatform(p.id)}
                        className={cn(
                          "inline-flex items-center gap-1.5 rounded-full border px-3 py-1.5 text-xs font-medium transition-all",
                          active
                            ? "bg-brand-50 border-brand-300 text-brand-700 dark:bg-brand-100/15 dark:border-brand-600/50 dark:text-brand-400"
                            : "bg-surface-subtle border-surface-border text-ink-muted hover:border-brand-200 hover:text-ink"
                        )}
                      >
                        {active ? (
                          <CheckSquare className="h-3.5 w-3.5 shrink-0" />
                        ) : (
                          <Square className="h-3.5 w-3.5 shrink-0" />
                        )}
                        {p.emoji} {p.label}
                      </button>
                    );
                  })}
                </div>
              </div>
            </div>
          </Card>

          {/* Loading state */}
          {isAnalyzing && (
            <Card>
              <div className="flex flex-col items-center py-8 gap-5">
                <div className="relative h-16 w-16">
                  <div className="absolute inset-0 rounded-2xl bg-brand-100 dark:bg-brand-100/10 flex items-center justify-center">
                    <Sparkles className="h-8 w-8 text-brand-500 animate-pulse" />
                  </div>
                  <div className="absolute -inset-1 rounded-[20px] border-2 border-brand-300/40 animate-ping" />
                </div>

                <div className="text-center">
                  <p className="font-semibold text-ink text-base">
                    {SCRAPE_STEPS[currentStep]}
                  </p>
                  <p className="text-sm text-ink-muted mt-1">
                    Analyzing &ldquo;{topic}&rdquo; across {selectedPlatforms.length} platforms
                  </p>
                </div>

                {/* Step progress */}
                <div className="w-full max-w-sm space-y-2">
                  {SCRAPE_STEPS.map((step, i) => (
                    <div key={step} className="flex items-center gap-3">
                      <div
                        className={cn(
                          "h-5 w-5 rounded-full flex items-center justify-center shrink-0 transition-all duration-300",
                          i < currentStep
                            ? "bg-pain-low text-white"
                            : i === currentStep
                            ? "bg-brand-500 text-white"
                            : "bg-surface-border"
                        )}
                      >
                        {i < currentStep ? (
                          <span className="text-[10px]">✓</span>
                        ) : i === currentStep ? (
                          <Loader2 className="h-3 w-3 animate-spin" />
                        ) : (
                          <span className="h-2 w-2 rounded-full bg-surface-border" />
                        )}
                      </div>
                      <span
                        className={cn(
                          "text-xs transition-colors",
                          i <= currentStep ? "text-ink" : "text-ink-faint"
                        )}
                      >
                        {step}
                      </span>
                    </div>
                  ))}
                </div>
              </div>
            </Card>
          )}

          {/* Results */}
          {results && !isAnalyzing && (
            <div className="space-y-4 animate-fade-up">
              {/* Results header + filters */}
              <div className="flex flex-col sm:flex-row sm:items-center gap-3 justify-between">
                <div className="flex items-center gap-3 flex-wrap">
                  <h2 className="text-base font-semibold text-ink">
                    {filtered.length} pain points found
                  </h2>
                  {counts && (
                    <div className="flex items-center gap-2">
                      <Badge variant="high">{counts.high} High</Badge>
                      <Badge variant="medium">{counts.medium} Med</Badge>
                      <Badge variant="low">{counts.low} Low</Badge>
                    </div>
                  )}
                </div>

                <div className="flex items-center gap-2">
                  {/* Filter by severity */}
                  <div className="flex items-center rounded-lg border border-surface-border bg-surface-card overflow-hidden">
                    {(["all", "high", "medium", "low"] as const).map((f) => (
                      <button
                        key={f}
                        onClick={() => setFilterIntensity(f)}
                        className={cn(
                          "px-3 py-1.5 text-xs font-medium transition-colors capitalize",
                          filterIntensity === f
                            ? "bg-brand-500 text-white"
                            : "text-ink-muted hover:text-ink hover:bg-surface-subtle"
                        )}
                      >
                        {f === "all" ? "All" : f.charAt(0).toUpperCase() + f.slice(1)}
                      </button>
                    ))}
                  </div>

                  {/* Sort */}
                  <div className="relative">
                    <select
                      value={sortBy}
                      onChange={(e) => setSortBy(e.target.value as SortOption)}
                      className="appearance-none pl-3 pr-7 py-1.5 text-xs font-medium text-ink bg-surface-card border border-surface-border rounded-lg focus:outline-none focus:ring-2 focus:ring-brand-500 cursor-pointer"
                    >
                      <option value="impact">Sort: Impact</option>
                      <option value="mentions">Sort: Mentions</option>
                      <option value="intensity">Sort: Severity</option>
                    </select>
                    <ChevronDown className="absolute right-2 top-1/2 -translate-y-1/2 h-3.5 w-3.5 text-ink-faint pointer-events-none" />
                  </div>

                  <Button
                    variant="ghost"
                    size="sm"
                    leftIcon={<X className="h-3.5 w-3.5" />}
                    onClick={() => {
                      setResults(null);
                      setTopic("");
                    }}
                  >
                    Clear
                  </Button>
                </div>
              </div>

              {/* Pain cards grid */}
              <div className="grid grid-cols-1 md:grid-cols-2 xl:grid-cols-3 gap-4">
                {filtered.map((pain) => (
                  <PainCard key={pain.id} {...pain} />
                ))}
              </div>

              {filtered.length === 0 && (
                <Card className="text-center py-10">
                  <Filter className="h-8 w-8 text-ink-faint mx-auto mb-3" />
                  <p className="text-ink-muted text-sm">No pain points match this filter.</p>
                  <Button variant="ghost" size="sm" className="mt-3" onClick={() => setFilterIntensity("all")}>
                    Clear filter
                  </Button>
                </Card>
              )}
            </div>
          )}

          {/* Empty initial state */}
          {!results && !isAnalyzing && (
            <Card className="flex flex-col items-center justify-center py-16 text-center">
              <div className="h-16 w-16 rounded-2xl bg-brand-50 dark:bg-brand-100/10 border border-brand-200 dark:border-brand-600/30 flex items-center justify-center mb-5">
                <Search className="h-8 w-8 text-brand-400" />
              </div>
              <h3 className="font-semibold text-ink text-lg">Ready to analyze</h3>
              <p className="text-sm text-ink-muted mt-2 max-w-sm">
                Enter a business topic above and select platforms to start discovering what your
                customers are really complaining about.
              </p>
              <div className="mt-5 flex flex-wrap justify-center gap-2">
                {["SaaS onboarding", "fintech app", "food delivery", "e-commerce returns"].map((s) => (
                  <button
                    key={s}
                    onClick={() => setTopic(s)}
                    className="rounded-full border border-surface-border px-3 py-1 text-xs text-ink-muted hover:border-brand-300 hover:text-brand-600 dark:hover:text-brand-400 transition-colors"
                  >
                    {s}
                  </button>
                ))}
              </div>
            </Card>
          )}
        </main>
      </div>
    </div>
  );
}
