"use client";

import { useState } from "react";
import {
  BarChart2,
  Sparkles,
  TrendingUp,
  Users,
  Target,
  DollarSign,
  Calendar,
  Megaphone,
  Loader2,
  CheckCircle2,
  Info,
  RotateCcw,
} from "lucide-react";
import {
  AreaChart,
  Area,
  XAxis,
  YAxis,
  CartesianGrid,
  Tooltip,
  ResponsiveContainer,
} from "recharts";
import { Sidebar } from "@/components/sidebar/Sidebar";
import { Navbar } from "@/components/navbar/Navbar";
import { Button } from "@/components/ui/button";
import { Badge } from "@/components/ui/badge";
import { Card, CardHeader, CardTitle, CardDescription, CardContent } from "@/components/ui/card";
import { StaggerContainer, StaggerItem, FadeInUp } from "@/components/ui/motion";
import { cn } from "@/lib/utils";

/* ── Constants ─────────────────────────────────────────────── */
const C = { brand: "#7C6FCD", low: "#2D9E6A", medium: "#E8920A", border: "#E2DFF0", faint: "#9B96AF" };
const tooltipStyle = { backgroundColor: "#fff", border: `1px solid ${C.border}`, borderRadius: 10, fontSize: 12 };

const PLATFORMS = ["Google Search", "Facebook", "Instagram", "WhatsApp", "LinkedIn"];
const AUDIENCES  = ["Working Professional", "SMB Owner", "Startup Founder", "Parent & Caregiver", "Student"];
const GOALS      = ["Brand Awareness", "Lead Generation", "Product Sales", "App Installs", "Website Traffic"];

/* ── Simulation output ─────────────────────────────────────── */
function computeResults(budget: number, duration: number, platformCount: number) {
  const dailyReach    = Math.round((budget / duration) * 12 * platformCount);
  const totalReach    = dailyReach * duration;
  const clicks        = Math.round(totalReach * 0.047);
  const conversions   = Math.round(clicks * 0.023);
  const revenue       = conversions * 1400;
  const roi           = Math.round((revenue / budget - 1) * 100);
  const cpc           = +(budget / clicks).toFixed(1);
  const cpl           = +(budget / conversions).toFixed(0);

  // Daily projection
  const projection = Array.from({ length: duration }, (_, i) => {
    const day      = i + 1;
    const rampup   = Math.min(1, day / 4);
    const dayReach = Math.round(dailyReach * rampup * (0.9 + Math.random() * 0.2));
    const dayClicks = Math.round(dayReach * 0.047 * (0.85 + Math.random() * 0.3));
    return { day: `D${day}`, reach: dayReach, clicks: dayClicks };
  });

  return { totalReach, clicks, conversions, revenue, roi, cpc, cpl, projection };
}

/* ── Range slider ───────────────────────────────────────────── */
function Slider({ label, value, min, max, step = 1, onChange, format }: {
  label: string; value: number; min: number; max: number; step?: number;
  onChange: (v: number) => void; format: (v: number) => string;
}) {
  return (
    <div className="space-y-2">
      <div className="flex items-center justify-between">
        <span className="text-sm font-medium text-ink">{label}</span>
        <span className="text-sm font-bold text-brand-600 dark:text-brand-400">{format(value)}</span>
      </div>
      <input
        type="range"
        min={min}
        max={max}
        step={step}
        value={value}
        onChange={(e) => onChange(Number(e.target.value))}
        className="w-full accent-brand-500 cursor-pointer"
      />
      <div className="flex justify-between text-xs text-ink-faint">
        <span>{format(min)}</span>
        <span>{format(max)}</span>
      </div>
    </div>
  );
}

import { AiLoadingState, AnimatedCounter } from "@/components/ui";

const SIMULATION_STEPS = [
  "Configuring audience parameters",
  "Calculating CPM & CPC benchmarks",
  "Predicting CTR trajectory",
  "Calculating conversion revenue",
  "Finalizing ROI model",
];

/* ── Result metric card ─────────────────────────────────────── */
function ResultCard({ icon: Icon, label, value, sub, accent }: {
  icon: typeof BarChart2; label: string; value: string; sub: string;
  accent: "brand" | "low" | "medium";
}) {
  const colors = {
    brand: "text-brand-500 bg-brand-50 dark:bg-brand-100/10 border-brand-200 dark:border-brand-600/30",
    low:   "text-pain-low bg-pain-low-bg border-pain-low/20",
    medium:"text-pain-medium bg-pain-medium-bg border-pain-medium/20",
  };
  return (
    <Card className="flex flex-col gap-3 h-full hover-lift">
      <div className={cn("h-9 w-9 rounded-xl flex items-center justify-center border", colors[accent])}>
        <Icon className="h-4.5 w-4.5" />
      </div>
      <div>
        <p className="text-2xl font-black text-ink leading-none">
          <AnimatedCounter value={value} />
        </p>
        <p className="text-sm font-semibold text-ink-muted mt-1">{label}</p>
        <p className="text-xs text-ink-faint mt-0.5">{sub}</p>
      </div>
    </Card>
  );
}

/* ── Page ──────────────────────────────────────────────────── */
export default function SimulatorPage() {
  const [sidebarOpen, setSidebarOpen] = useState(false);
  const [budget, setBudget] = useState(20000);
  const [duration, setDuration] = useState(14);
  const [selectedPlatforms, setSelectedPlatforms] = useState(["Google Search", "Facebook"]);
  const [selectedAudience, setSelectedAudience] = useState("Working Professional");
  const [selectedGoal, setSelectedGoal] = useState("Lead Generation");
  const [running, setRunning] = useState(false);
  const [results, setResults] = useState<ReturnType<typeof computeResults> | null>(null);

  const togglePlatform = (p: string) => {
    setSelectedPlatforms((prev) =>
      prev.includes(p) ? (prev.length > 1 ? prev.filter((x) => x !== p) : prev) : [...prev, p]
    );
  };

  const [simulationStep, setSimulationStep] = useState(0);

  const handleRun = async () => {
    setRunning(true);
    setResults(null);
    setSimulationStep(0);

    for (let i = 0; i < SIMULATION_STEPS.length; i++) {
      await new Promise((r) => setTimeout(r, 350));
      setSimulationStep(i);
    }
    await new Promise((r) => setTimeout(r, 200));

    setResults(computeResults(budget, duration, selectedPlatforms.length));
    setRunning(false);
  };

  const handleReset = () => {
    setResults(null);
    setBudget(20000);
    setDuration(14);
    setSelectedPlatforms(["Google Search", "Facebook"]);
  };

  const formatINR = (v: number) => `₹${(v).toLocaleString("en-IN")}`;
  const formatDays = (v: number) => `${v} days`;

  return (
    <div className="flex min-h-dvh bg-surface-bg">
      <Sidebar isOpen={sidebarOpen} onClose={() => setSidebarOpen(false)} />
      <div className="flex flex-1 flex-col lg:pl-64">
        <Navbar onMobileMenuToggle={() => setSidebarOpen(true)} />

        <main className="flex-1 p-5 lg:p-8 space-y-6">
          {/* Header */}
          <div className="flex flex-col sm:flex-row sm:items-center sm:justify-between gap-4">
            <div>
              <h1 className="text-2xl font-bold text-ink tracking-tight">ROI Simulator</h1>
              <p className="text-sm text-ink-muted mt-0.5">
                Predict reach, clicks, conversions & ROI — before you spend a single rupee.
              </p>
            </div>
            <Badge variant="brand">
              <Sparkles className="h-3.5 w-3.5" />
              Pre-spend forecasting
            </Badge>
          </div>

          <div className={cn("grid gap-6", results ? "grid-cols-1 lg:grid-cols-5" : "grid-cols-1 max-w-xl")}>
            {/* ── Input panel ── */}
            <Card className={cn(results ? "lg:col-span-2" : "")}>
              <CardHeader>
                <CardTitle>Campaign Parameters</CardTitle>
                <CardDescription>Adjust inputs to model different scenarios</CardDescription>
              </CardHeader>
              <CardContent className="space-y-6">
                <Slider label="Total Budget" value={budget} min={5000} max={200000} step={1000} onChange={setBudget} format={formatINR} />
                <Slider label="Campaign Duration" value={duration} min={7} max={90} step={1} onChange={setDuration} format={formatDays} />

                {/* Platforms */}
                <div className="space-y-2">
                  <span className="text-sm font-medium text-ink">Platforms</span>
                  <div className="flex flex-wrap gap-2">
                    {PLATFORMS.map((p) => {
                      const active = selectedPlatforms.includes(p);
                      return (
                        <button
                          key={p}
                          onClick={() => togglePlatform(p)}
                          className={cn(
                            "rounded-lg border px-3 py-1.5 text-xs font-medium transition-all",
                            active
                              ? "bg-brand-500 text-white border-brand-500"
                              : "bg-surface-card border-surface-border text-ink-muted hover:border-brand-300"
                          )}
                        >
                          {p}
                        </button>
                      );
                    })}
                  </div>
                </div>

                {/* Audience */}
                <div className="space-y-2">
                  <span className="text-sm font-medium text-ink">Target Audience</span>
                  <div className="flex flex-wrap gap-2">
                    {AUDIENCES.map((a) => (
                      <button
                        key={a}
                        onClick={() => setSelectedAudience(a)}
                        className={cn(
                          "rounded-lg border px-3 py-1.5 text-xs font-medium transition-all",
                          selectedAudience === a
                            ? "bg-brand-500 text-white border-brand-500"
                            : "bg-surface-card border-surface-border text-ink-muted hover:border-brand-300"
                        )}
                      >
                        {a.split(" ")[0]}
                      </button>
                    ))}
                  </div>
                </div>

                {/* Goal */}
                <div className="space-y-2">
                  <span className="text-sm font-medium text-ink">Campaign Goal</span>
                  <div className="flex flex-wrap gap-2">
                    {GOALS.map((g) => (
                      <button
                        key={g}
                        onClick={() => setSelectedGoal(g)}
                        className={cn(
                          "rounded-lg border px-3 py-1.5 text-xs font-medium transition-all",
                          selectedGoal === g
                            ? "bg-brand-500 text-white border-brand-500"
                            : "bg-surface-card border-surface-border text-ink-muted hover:border-brand-300"
                        )}
                      >
                        {g}
                      </button>
                    ))}
                  </div>
                </div>

                <div className="flex gap-2">
                  <Button
                    className="flex-1"
                    loading={running}
                    leftIcon={!running ? <Sparkles className="h-4 w-4" /> : undefined}
                    onClick={handleRun}
                  >
                    Run Simulation
                  </Button>
                  {results && (
                    <Button variant="ghost" size="md" onClick={handleReset} title="Reset">
                      <RotateCcw className="h-4 w-4" />
                    </Button>
                  )}
                </div>
              </CardContent>
            </Card>

            {/* ── Results panel ── */}
            {running && (
              <div className="lg:col-span-3">
                <AiLoadingState
                  title="Predicting Campaign Performance & ROI"
                  subtitle={`Modeling ${formatINR(budget)} across ${selectedPlatforms.length} platform(s) over ${duration} days...`}
                  steps={SIMULATION_STEPS}
                  currentStepIndex={simulationStep}
                />
              </div>
            )}

            {results && !running && (
              <div className="lg:col-span-3 space-y-5">
                {/* Summary callout */}
                <FadeInUp className="rounded-xl border border-pain-low/30 bg-pain-low-bg p-4 flex items-start gap-3">
                  <CheckCircle2 className="h-5 w-5 text-pain-low shrink-0 mt-0.5" />
                  <div>
                    <p className="font-semibold text-ink text-sm">
                      Projected ROI: <span className="text-pain-low">{results.roi}%</span> on a{" "}
                      {formatINR(budget)} budget over {duration} days
                    </p>
                    <p className="text-xs text-ink-muted mt-0.5">
                      Based on pain-point-driven campaigns targeting {selectedAudience}s on{" "}
                      {selectedPlatforms.join(", ")} for {selectedGoal}.
                    </p>
                  </div>
                </FadeInUp>

                {/* Metric cards */}
                <StaggerContainer className="grid grid-cols-2 sm:grid-cols-3 gap-3">
                  <StaggerItem><ResultCard icon={Users}    label="Total Reach"    value={results.totalReach.toLocaleString("en-IN")} sub="Unique impressions"     accent="brand" /></StaggerItem>
                  <StaggerItem><ResultCard icon={Target}   label="Est. Clicks"    value={results.clicks.toLocaleString("en-IN")}     sub={`₹${results.cpc}/click`} accent="brand" /></StaggerItem>
                  <StaggerItem><ResultCard icon={Megaphone}label="Conversions"    value={results.conversions.toLocaleString("en-IN")} sub={`₹${results.cpl} CPL`} accent="low" /></StaggerItem>
                  <StaggerItem><ResultCard icon={DollarSign}label="Est. Revenue"  value={formatINR(results.revenue)}                 sub="At ₹1,400 avg. LTV"     accent="low" /></StaggerItem>
                  <StaggerItem><ResultCard icon={TrendingUp}label="Predicted ROI" value={`${results.roi}%`}                          sub="Return on spend"         accent={results.roi > 200 ? "low" : "medium"} /></StaggerItem>
                  <StaggerItem><ResultCard icon={Calendar} label="Duration"       value={`${duration} days`}                         sub={formatINR(Math.round(budget / duration)) + "/day"} accent="brand" /></StaggerItem>
                </StaggerContainer>

                {/* Projection chart */}
                <Card>
                  <CardHeader>
                    <CardTitle>Daily Reach & Clicks Projection</CardTitle>
                    <CardDescription>
                      Simulated {duration}-day campaign trajectory — ramp-up period shown
                    </CardDescription>
                  </CardHeader>
                  <CardContent>
                    <ResponsiveContainer width="100%" height={200}>
                      <AreaChart data={results.projection} margin={{ top: 4, right: 8, left: -20, bottom: 0 }}>
                        <defs>
                          <linearGradient id="reachGrad" x1="0" y1="0" x2="0" y2="1">
                            <stop offset="5%"  stopColor={C.brand} stopOpacity={0.18} />
                            <stop offset="95%" stopColor={C.brand} stopOpacity={0} />
                          </linearGradient>
                          <linearGradient id="clicksGrad" x1="0" y1="0" x2="0" y2="1">
                            <stop offset="5%"  stopColor={C.low} stopOpacity={0.18} />
                            <stop offset="95%" stopColor={C.low} stopOpacity={0} />
                          </linearGradient>
                        </defs>
                        <CartesianGrid strokeDasharray="3 3" stroke={C.border} vertical={false} />
                        <XAxis dataKey="day" tick={{ fontSize: 10, fill: C.faint }} axisLine={false} tickLine={false} interval={Math.ceil(duration / 7)} />
                        <YAxis tick={{ fontSize: 10, fill: C.faint }} axisLine={false} tickLine={false} />
                        <Tooltip contentStyle={tooltipStyle} />
                        <Area type="monotone" dataKey="reach"  name="Reach"  stroke={C.brand} fill="url(#reachGrad)"  strokeWidth={2} dot={false} isAnimationActive animationDuration={800} />
                        <Area type="monotone" dataKey="clicks" name="Clicks" stroke={C.low}   fill="url(#clicksGrad)" strokeWidth={2} dot={false} isAnimationActive animationDuration={800} />
                      </AreaChart>
                    </ResponsiveContainer>
                    <div className="flex justify-center gap-4 mt-2">
                      {[{ label: "Reach", color: "bg-brand-500" }, { label: "Clicks", color: "bg-pain-low" }].map((l) => (
                        <div key={l.label} className="flex items-center gap-1.5 text-xs text-ink-faint">
                          <div className={`h-2 w-2 rounded-full ${l.color}`} />
                          {l.label}
                        </div>
                      ))}
                    </div>
                  </CardContent>
                </Card>

                <div className="flex items-start gap-2 text-xs text-ink-faint">
                  <Info className="h-3.5 w-3.5 shrink-0 mt-0.5" />
                  Projections are based on historical CTR benchmarks for pain-point-driven campaigns in the Indian market.
                  Actual results may vary based on ad quality, audience targeting, and market conditions.
                </div>
              </div>
            )}

            {/* Initial prompt state */}
            {!results && !running && (
              <div className="flex flex-col items-center justify-center py-16 text-center lg:col-span-3">
                <div className="h-16 w-16 rounded-2xl bg-brand-50 dark:bg-brand-100/10 border border-brand-200 dark:border-brand-600/30 flex items-center justify-center mb-5">
                  <BarChart2 className="h-8 w-8 text-brand-400" />
                </div>
                <h3 className="font-semibold text-ink text-lg">Set your parameters</h3>
                <p className="text-sm text-ink-muted mt-2 max-w-xs">
                  Configure budget, duration, platforms and audience on the left, then click Run Simulation.
                </p>
              </div>
            )}
          </div>
        </main>
      </div>
    </div>
  );
}
