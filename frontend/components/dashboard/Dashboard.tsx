"use client";

import {
  TrendingUp,
  TrendingDown,
  Minus,
  ArrowRight,
  MessageSquare,
  Sparkles,
  Search,
  Users,
  Megaphone,
  BarChart2,
  Lightbulb,
  TrendingUp as Optimizer,
} from "lucide-react";
import Link from "next/link";
import { cn } from "@/lib/utils";
import { Button } from "@/components/ui/button";
import { Badge } from "@/components/ui/badge";
import { Card, CardHeader, CardTitle, CardDescription } from "@/components/ui/card";

/* ──────────────────────────────────────────────────────────────
   StatCard
   ────────────────────────────────────────────────────────────── */
interface StatCardProps {
  label: string;
  value: string;
  sub?: string;
  trend?: "up" | "down" | "neutral";
  trendLabel?: string;
  accent?: "brand" | "high" | "medium" | "low";
  icon: React.ElementType;
}

const accentMap = {
  brand:  { bg: "bg-brand-50 dark:bg-brand-100/10",   icon: "text-brand-500 dark:text-brand-400",   border: "border-brand-200 dark:border-brand-600/30" },
  high:   { bg: "bg-pain-high-bg",                    icon: "text-pain-high",                        border: "border-pain-high/20" },
  medium: { bg: "bg-pain-medium-bg",                  icon: "text-pain-medium",                      border: "border-pain-medium/20" },
  low:    { bg: "bg-pain-low-bg",                     icon: "text-pain-low",                         border: "border-pain-low/20" },
};

export function StatCard({ label, value, sub, trend, trendLabel, accent = "brand", icon: Icon }: StatCardProps) {
  const a = accentMap[accent];
  return (
    <Card className="flex flex-col gap-4">
      <div className="flex items-start justify-between">
        <div className={cn("h-10 w-10 rounded-xl flex items-center justify-center border", a.bg, a.border)}>
          <Icon className={cn("h-5 w-5", a.icon)} />
        </div>
        {trend && trendLabel && (
          <div className={cn(
            "flex items-center gap-1 text-xs font-medium rounded-full px-2 py-0.5",
            trend === "up"      && "text-pain-low bg-pain-low-bg",
            trend === "down"    && "text-pain-high bg-pain-high-bg",
            trend === "neutral" && "text-ink-faint bg-surface-subtle",
          )}>
            {trend === "up"      && <TrendingUp className="h-3 w-3" />}
            {trend === "down"    && <TrendingDown className="h-3 w-3" />}
            {trend === "neutral" && <Minus className="h-3 w-3" />}
            {trendLabel}
          </div>
        )}
      </div>
      <div>
        <p className="text-3xl font-bold text-ink tracking-tight leading-none">{value}</p>
        <p className="text-sm text-ink-muted mt-1">{label}</p>
        {sub && <p className="text-xs text-ink-faint mt-0.5">{sub}</p>}
      </div>
    </Card>
  );
}

/* ──────────────────────────────────────────────────────────────
   RecentPainRow — single pain point row in the feed
   ────────────────────────────────────────────────────────────── */
interface PainPoint {
  id: string;
  quote: string;
  platform: string;
  mentions: number;
  intensity: "high" | "medium" | "low";
  topic: string;
}

const intensityLabel = { high: "High", medium: "Medium", low: "Low" } as const;

export function RecentPainRow({ pain }: { pain: PainPoint }) {
  return (
    <div className="flex gap-3 py-3 border-b border-surface-border last:border-0 group cursor-default">
      <div className="shrink-0 mt-0.5">
        <Badge variant={pain.intensity} className="text-[10px] px-1.5 py-0.5">
          {intensityLabel[pain.intensity]}
        </Badge>
      </div>
      <div className="min-w-0 flex-1">
        <p className="text-sm text-ink leading-snug line-clamp-2 italic">
          &ldquo;{pain.quote}&rdquo;
        </p>
        <div className="mt-1 flex flex-wrap items-center gap-x-2.5 gap-y-0.5 text-xs text-ink-faint">
          <span className="flex items-center gap-1">
            <MessageSquare className="h-3 w-3" />
            {pain.platform}
          </span>
          <span>·</span>
          <span>{pain.mentions} mentions</span>
          <span>·</span>
          <span>{pain.topic}</span>
        </div>
      </div>
    </div>
  );
}

/* ──────────────────────────────────────────────────────────────
   QuickAction — shortcut card
   ────────────────────────────────────────────────────────────── */
const QUICK_ACTIONS = [
  { label: "Analyze new topic",     desc: "Scrape pain points",          href: "/analyze",   icon: Search,    accent: "brand" as const },
  { label: "View personas",         desc: "Customer segments",            href: "/personas",  icon: Users,     accent: "low" as const },
  { label: "Generate campaign",     desc: "Create ad creatives",          href: "/campaigns", icon: Megaphone, accent: "medium" as const },
  { label: "Read insights",         desc: "AI market briefs",             href: "/insights",  icon: Lightbulb, accent: "brand" as const },
  { label: "Optimize variants",     desc: "CTR A/B comparison",           href: "/optimizer", icon: Optimizer, accent: "low" as const },
  { label: "Run simulator",         desc: "Pre-spend ROI forecast",       href: "/simulator", icon: BarChart2, accent: "medium" as const },
];

export function QuickActions() {
  return (
    <div className="grid grid-cols-2 sm:grid-cols-3 gap-3">
      {QUICK_ACTIONS.map((action) => {
        const Icon = action.icon;
        const a = accentMap[action.accent];
        return (
          <Link key={action.href} href={action.href}>
            <div className={cn(
              "flex items-center gap-3 p-3.5 rounded-xl border transition-all duration-150 cursor-pointer",
              "bg-surface-card hover:bg-surface-subtle border-surface-border hover:border-brand-200 dark:hover:border-brand-600/40",
              "hover:shadow-card group"
            )}>
              <div className={cn("h-8 w-8 rounded-lg flex items-center justify-center border shrink-0", a.bg, a.border)}>
                <Icon className={cn("h-4 w-4", a.icon)} />
              </div>
              <div className="min-w-0">
                <p className="text-sm font-medium text-ink leading-tight truncate group-hover:text-brand-600 dark:group-hover:text-brand-400 transition-colors">
                  {action.label}
                </p>
                <p className="text-xs text-ink-faint truncate">{action.desc}</p>
              </div>
            </div>
          </Link>
        );
      })}
    </div>
  );
}

/* ──────────────────────────────────────────────────────────────
   EmptyAnalyzePrompt — shown when no data yet
   ────────────────────────────────────────────────────────────── */
export function EmptyAnalyzePrompt() {
  return (
    <div className="flex flex-col items-center justify-center py-12 text-center">
      <div className="h-14 w-14 rounded-2xl bg-brand-50 dark:bg-brand-100/10 border border-brand-200 dark:border-brand-600/30 flex items-center justify-center mb-4">
        <Sparkles className="h-7 w-7 text-brand-500" />
      </div>
      <h3 className="font-semibold text-ink text-base">No pain points yet</h3>
      <p className="text-sm text-ink-muted mt-1.5 max-w-xs">
        Run your first analysis to start seeing real customer pain points from Reddit, Quora, and more.
      </p>
      <Link href="/analyze" className="mt-5">
        <Button variant="primary" size="sm" rightIcon={<ArrowRight className="h-3.5 w-3.5" />}>
          Analyze a Topic
        </Button>
      </Link>
    </div>
  );
}
