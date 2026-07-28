"use client";

import { useState } from "react";
import {
  TrendingUp,
  Sparkles,
  Trophy,
  Target,
  Users,
  DollarSign,
  ArrowRight,
  RefreshCw,
  Info,
} from "lucide-react";
import {
  BarChart,
  Bar,
  XAxis,
  YAxis,
  CartesianGrid,
  Tooltip,
  ResponsiveContainer,
  RadarChart,
  Radar,
  PolarGrid,
  PolarAngleAxis,
  PolarRadiusAxis,
} from "recharts";
import { Sidebar } from "@/components/sidebar/Sidebar";
import { Navbar } from "@/components/navbar/Navbar";
import { Button } from "@/components/ui/button";
import { Badge } from "@/components/ui/badge";
import { Card, CardHeader, CardTitle, CardDescription, CardContent } from "@/components/ui/card";
import { StaggerContainer, StaggerItem, FadeInUp } from "@/components/ui/motion";
import { cn } from "@/lib/utils";

/* ── Chart colors ───────────────────────────────────────────── */
const C = { brand: "#7C6FCD", high: "#F04444", medium: "#E8920A", low: "#2D9E6A", faint: "#9B96AF", border: "#E2DFF0" };
const tooltipStyle = { backgroundColor: "#fff", border: `1px solid ${C.border}`, borderRadius: 10, fontSize: 12 };

/* ── Variant data ───────────────────────────────────────────── */
const VARIANTS = [
  {
    id: "A",
    label: "Variant A",
    headline: "Stop Losing Customers to Painful Onboarding",
    body: "We read 500+ real complaints so you don't have to. PainToAd AI turns customer pain into winning campaigns with predicted ROI.",
    persona: "Working Professional",
    tone: "Urgent",
    ctr: 4.7,
    convRate: 2.3,
    cpc: 18,
    audienceMatch: 88,
    reach: 42000,
    score: 87,
  },
  {
    id: "B",
    label: "Variant B",
    headline: "Your Customers Are Telling You What They Hate. Are You Listening?",
    body: "Real voices from Reddit, Quora & Google Reviews turned into ROI-predicted ad campaigns. Know what hurts before you spend.",
    persona: "Startup Founder",
    tone: "Conversational",
    ctr: 3.9,
    convRate: 2.8,
    cpc: 14,
    audienceMatch: 74,
    reach: 38000,
    score: 79,
  },
];

const BAR_DATA = [
  { metric: "CTR (%)",       A: 4.7,  B: 3.9  },
  { metric: "Conv. Rate (%)",A: 2.3,  B: 2.8  },
  { metric: "Audience Match",A: 88,   B: 74   },
];

const RADAR_DATA = [
  { metric: "Relevance",   A: 90, B: 72 },
  { metric: "Urgency",     A: 88, B: 62 },
  { metric: "Clarity",     A: 82, B: 85 },
  { metric: "Empathy",     A: 76, B: 90 },
  { metric: "CTA Strength",A: 88, B: 74 },
];

const BUDGET_SPLIT = { A: 65, B: 35 };

/* ── Metric card ────────────────────────────────────────────── */
function MetricCard({
  label, valA, valB, unit = "", higherIsBetter = true, format,
}: {
  label: string; valA: number; valB: number; unit?: string; higherIsBetter?: boolean; format?: (v: number) => string;
}) {
  const aWins = higherIsBetter ? valA >= valB : valA <= valB;
  const fmt = format ?? ((v: number) => `${v}${unit}`);

  return (
    <div className="rounded-xl border border-surface-border bg-surface-card p-4 flex flex-col gap-3">
      <span className="text-xs font-semibold uppercase tracking-wider text-ink-faint">{label}</span>
      <div className="flex items-end gap-3">
        <div className={cn("flex-1 rounded-lg p-3 text-center border", aWins ? "bg-pain-low-bg border-pain-low/30" : "bg-surface-subtle border-surface-border")}>
          <p className="text-xl font-bold text-ink">{fmt(valA)}</p>
          <p className="text-xs text-ink-muted mt-0.5">Variant A</p>
          {aWins && <Badge variant="low" className="mt-1.5 text-[10px]">Winner</Badge>}
        </div>
        <div className={cn("flex-1 rounded-lg p-3 text-center border", !aWins ? "bg-pain-low-bg border-pain-low/30" : "bg-surface-subtle border-surface-border")}>
          <p className="text-xl font-bold text-ink">{fmt(valB)}</p>
          <p className="text-xs text-ink-muted mt-0.5">Variant B</p>
          {!aWins && <Badge variant="low" className="mt-1.5 text-[10px]">Winner</Badge>}
        </div>
      </div>
    </div>
  );
}

/* ── Page ──────────────────────────────────────────────────── */
export default function OptimizerPage() {
  const [sidebarOpen, setSidebarOpen] = useState(false);
  const [optimizing, setOptimizing] = useState(false);
  const [winner] = useState<"A" | "B">("A");

  const handleOptimize = async () => {
    setOptimizing(true);
    await new Promise((r) => setTimeout(r, 1200));
    setOptimizing(false);
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
              <h1 className="text-2xl font-bold text-ink tracking-tight">Campaign Optimizer</h1>
              <p className="text-sm text-ink-muted mt-0.5">
                A/B compare campaign variants — CTR prediction, audience fit & budget split.
              </p>
            </div>
            <div className="flex items-center gap-2">
              <Button
                size="sm"
                loading={optimizing}
                leftIcon={!optimizing ? <RefreshCw className="h-3.5 w-3.5" /> : undefined}
                onClick={handleOptimize}
              >
                Re-run Analysis
              </Button>
            </div>
          </div>

          {/* Winner banner */}
          <FadeInUp className="rounded-xl border border-pain-low/30 bg-pain-low-bg p-4 flex items-center gap-4">
            <div className="h-10 w-10 rounded-xl bg-pain-low/20 border border-pain-low/30 flex items-center justify-center shrink-0">
              <Trophy className="h-5 w-5 text-pain-low" />
            </div>
            <div className="flex-1 min-w-0">
              <p className="font-semibold text-ink text-sm">
                Variant {winner} is the recommended winner — Score {VARIANTS.find(v => v.id === winner)?.score}/100
              </p>
              <p className="text-xs text-ink-muted mt-0.5">
                Higher CTR, better audience match score, and lower CPC. Allocate 65% of budget here.
              </p>
            </div>
            <Badge variant="low">
              <Trophy className="h-3 w-3" />
              Winner
            </Badge>
          </FadeInUp>

          {/* Variant copy side-by-side */}
          <StaggerContainer className="grid grid-cols-1 md:grid-cols-2 gap-5">
            {VARIANTS.map((v) => (
              <StaggerItem key={v.id}>
                <Card className={cn("relative h-full", v.id === winner && "ring-2 ring-pain-low ring-offset-2 ring-offset-surface-bg")}>
                  {v.id === winner && (
                    <div className="absolute -top-3 left-4">
                      <Badge variant="low" className="shadow-sm">
                        <Trophy className="h-3 w-3" /> Recommended
                      </Badge>
                    </div>
                  )}
                  <div className="flex items-center justify-between mb-3">
                    <Badge variant={v.id === winner ? "low" : "default"}>Variant {v.id}</Badge>
                    <div className="flex items-center gap-2 text-xs text-ink-faint">
                      <span>👤 {v.persona}</span>
                      <span>·</span>
                      <span>{v.tone}</span>
                    </div>
                  </div>
                  <p className="font-semibold text-ink text-sm leading-snug">{v.headline}</p>
                  <p className="text-sm text-ink-muted mt-2 leading-relaxed">{v.body}</p>
                  <div className="mt-4 flex items-center gap-4">
                    <div className="text-center">
                      <p className="text-lg font-bold text-ink">{v.score}</p>
                      <p className="text-[10px] text-ink-faint">AI Score</p>
                    </div>
                    <div className="text-center">
                      <p className="text-lg font-bold text-ink">{v.ctr}%</p>
                      <p className="text-[10px] text-ink-faint">CTR</p>
                    </div>
                    <div className="text-center">
                      <p className="text-lg font-bold text-ink">₹{v.cpc}</p>
                      <p className="text-[10px] text-ink-faint">CPC</p>
                    </div>
                    <div className="text-center">
                      <p className="text-lg font-bold text-ink">{v.audienceMatch}%</p>
                      <p className="text-[10px] text-ink-faint">Audience</p>
                    </div>
                  </div>
                </Card>
              </StaggerItem>
            ))}
          </StaggerContainer>

          {/* Metric comparison cards */}
          <StaggerContainer className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-4">
            <StaggerItem><MetricCard label="CTR Prediction"    valA={4.7}  valB={3.9}  unit="%" /></StaggerItem>
            <StaggerItem><MetricCard label="Conv. Rate"         valA={2.3}  valB={2.8}  unit="%" /></StaggerItem>
            <StaggerItem><MetricCard label="Cost Per Click"     valA={18}   valB={14}   unit="" higherIsBetter={false} format={(v) => `₹${v}`} /></StaggerItem>
            <StaggerItem><MetricCard label="Audience Match"     valA={88}   valB={74}   unit="%" /></StaggerItem>
          </StaggerContainer>

          {/* Charts row */}
          <div className="grid grid-cols-1 lg:grid-cols-2 gap-5">
            {/* Bar chart */}
            <Card>
              <CardHeader>
                <CardTitle>Performance Comparison</CardTitle>
                <CardDescription>CTR, conversion rate & audience match</CardDescription>
              </CardHeader>
              <CardContent>
                <ResponsiveContainer width="100%" height={200}>
                  <BarChart data={BAR_DATA} barSize={20} barGap={4}>
                    <CartesianGrid strokeDasharray="3 3" stroke={C.border} vertical={false} />
                    <XAxis dataKey="metric" tick={{ fontSize: 11, fill: C.faint }} axisLine={false} tickLine={false} />
                    <YAxis tick={{ fontSize: 11, fill: C.faint }} axisLine={false} tickLine={false} />
                    <Tooltip contentStyle={tooltipStyle} />
                    <Bar dataKey="A" name="Variant A" fill={C.low} radius={[4, 4, 0, 0]} isAnimationActive animationDuration={800} />
                    <Bar dataKey="B" name="Variant B" fill={C.medium} radius={[4, 4, 0, 0]} isAnimationActive animationDuration={800} />
                  </BarChart>
                </ResponsiveContainer>
                <div className="flex justify-center gap-4 mt-2">
                  {[{ label: "Variant A", color: "bg-pain-low" }, { label: "Variant B", color: "bg-pain-medium" }].map((l) => (
                    <div key={l.label} className="flex items-center gap-1.5 text-xs text-ink-faint">
                      <div className={`h-2 w-2 rounded-full ${l.color}`} />
                      {l.label}
                    </div>
                  ))}
                </div>
              </CardContent>
            </Card>

            {/* Radar chart */}
            <Card>
              <CardHeader>
                <CardTitle>Copy Quality Radar</CardTitle>
                <CardDescription>AI-scored dimensions per variant</CardDescription>
              </CardHeader>
              <CardContent>
                <ResponsiveContainer width="100%" height={200}>
                  <RadarChart data={RADAR_DATA}>
                    <PolarGrid stroke={C.border} />
                    <PolarAngleAxis dataKey="metric" tick={{ fontSize: 10, fill: C.faint }} />
                    <PolarRadiusAxis domain={[0, 100]} tick={{ fontSize: 9, fill: C.faint }} axisLine={false} />
                    <Radar name="A" dataKey="A" stroke={C.low}   fill={C.low}   fillOpacity={0.2} isAnimationActive animationDuration={800} />
                    <Radar name="B" dataKey="B" stroke={C.brand} fill={C.brand} fillOpacity={0.15} isAnimationActive animationDuration={800} />
                    <Tooltip contentStyle={tooltipStyle} />
                  </RadarChart>
                </ResponsiveContainer>
              </CardContent>
            </Card>
          </div>

          {/* Budget split */}
          <Card>
            <CardHeader>
              <CardTitle>Recommended Budget Split</CardTitle>
              <CardDescription>
                Based on predicted CTR, conversion rate, and audience match scores
              </CardDescription>
            </CardHeader>
            <CardContent>
              <div className="space-y-3">
                {Object.entries(BUDGET_SPLIT).map(([variant, pct]) => (
                  <div key={variant} className="flex items-center gap-4">
                    <span className="text-sm font-semibold text-ink w-20 shrink-0">Variant {variant}</span>
                    <div className="flex-1 h-6 rounded-full bg-surface-subtle overflow-hidden">
                      <div
                        className={cn("h-full rounded-full flex items-center justify-end pr-2 transition-all duration-700", variant === "A" ? "bg-pain-low" : "bg-pain-medium")}
                        style={{ width: `${pct}%` }}
                      >
                        <span className="text-[10px] font-bold text-white">{pct}%</span>
                      </div>
                    </div>
                    <div className="flex items-center gap-1.5 text-xs text-ink-muted w-20 shrink-0">
                      <DollarSign className="h-3.5 w-3.5" />
                      {variant === "A" ? "₹13,000" : "₹7,000"}
                    </div>
                  </div>
                ))}
                <div className="flex items-start gap-2 mt-3 text-xs text-ink-faint pt-3 border-t border-surface-border">
                  <Info className="h-3.5 w-3.5 shrink-0 mt-0.5" />
                  Based on a ₹20,000 total campaign budget. Allocate more to Variant A to maximize CTR,
                  or keep Variant B to reach the Startup Founder segment with higher conversion potential.
                </div>
              </div>
            </CardContent>
          </Card>
        </main>
      </div>
    </div>
  );
}
