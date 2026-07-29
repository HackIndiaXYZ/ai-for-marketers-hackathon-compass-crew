"use client";

import { useState } from "react";
import {
  AlertTriangle,
  BarChart2,
  Megaphone,
  Users,
  TrendingUp,
  ArrowRight,
  RefreshCw,
  Sparkles,
} from "lucide-react";
import Link from "next/link";
import { Sidebar } from "@/components/sidebar/Sidebar";
import { Navbar } from "@/components/navbar/Navbar";
import { Card, CardHeader, CardTitle, CardDescription, CardContent } from "@/components/ui/card";
import { Button } from "@/components/ui/button";
import { Badge } from "@/components/ui/badge";
import { StaggerContainer, StaggerItem, FadeInUp } from "@/components/ui/motion";
import {
  StatCard,
  RecentPainRow,
  QuickActions,
} from "@/components/dashboard/Dashboard";
import {
  PainByPlatformBar,
  CampaignActivityArea,
  PainSeverityPie,
  CHART_COLORS,
} from "@/components/charts/Charts";

/* ──────────────────────────────────────────────────────────────
   Mock data — replace with API calls from services/ when ready
   ────────────────────────────────────────────────────────────── */
const STAT_CARDS = [
  {
    label: "Pain Points Found",
    value: "529",
    sub: "Across 7 platforms",
    trend: "up" as const,
    trendLabel: "+18% this week",
    accent: "high" as const,
    icon: AlertTriangle,
  },
  {
    label: "Campaigns Generated",
    value: "24",
    sub: "Google, Meta, WhatsApp",
    trend: "up" as const,
    trendLabel: "+5 today",
    accent: "brand" as const,
    icon: Megaphone,
  },
  {
    label: "Personas Created",
    value: "6",
    sub: "Across 3 topics",
    trend: "neutral" as const,
    trendLabel: "No change",
    accent: "low" as const,
    icon: Users,
  },
  {
    label: "Avg. Predicted ROI",
    value: "340%",
    sub: "Based on Simulator runs",
    trend: "up" as const,
    trendLabel: "+22 pts",
    accent: "medium" as const,
    icon: TrendingUp,
  },
];

const PLATFORM_DATA = [
  { platform: "Reddit",         count: 189, high: 89,  medium: 62, low: 38 },
  { platform: "Google Reviews", count: 156, high: 67,  medium: 54, low: 35 },
  { platform: "Quora",          count: 98,  high: 34,  medium: 38, low: 26 },
  { platform: "Twitter / X",    count: 47,  high: 18,  medium: 19, low: 10 },
  { platform: "MouthShut",      count: 24,  high: 11,  medium: 8,  low: 5  },
  { platform: "IndiaMART",      count: 15,  high: 6,   medium: 6,  low: 3  },
];

const ACTIVITY_DATA = [
  { day: "Mon", campaigns: 2,  insights: 1 },
  { day: "Tue", campaigns: 4,  insights: 2 },
  { day: "Wed", campaigns: 3,  insights: 3 },
  { day: "Thu", campaigns: 7,  insights: 4 },
  { day: "Fri", campaigns: 5,  insights: 2 },
  { day: "Sat", campaigns: 2,  insights: 1 },
  { day: "Sun", campaigns: 1,  insights: 1 },
];

const PIE_DATA = [
  { name: "High Impact",   value: 225, color: CHART_COLORS.high },
  { name: "Medium Impact", value: 187, color: CHART_COLORS.medium },
  { name: "Low Impact",    value: 117, color: CHART_COLORS.low },
];

const RECENT_PAINS = [
  {
    id: "p1",
    quote: "The onboarding takes forever and no one explains what happens after you sign up.",
    platform: "Reddit",
    mentions: 247,
    intensity: "high" as const,
    topic: "SaaS Onboarding",
  },
  {
    id: "p2",
    quote: "Customer support replies in 5 days. My issue was urgent and I lost money because of it.",
    platform: "Google Reviews",
    mentions: 189,
    intensity: "high" as const,
    topic: "Support SLA",
  },
  {
    id: "p3",
    quote: "The mobile app crashes during checkout. Fixed on web but not mobile.",
    platform: "MouthShut",
    mentions: 93,
    intensity: "medium" as const,
    topic: "Mobile UX",
  },
  {
    id: "p4",
    quote: "Hidden charges appear on invoice that were never mentioned during sales calls.",
    platform: "Quora",
    mentions: 41,
    intensity: "high" as const,
    topic: "Pricing Clarity",
  },
  {
    id: "p5",
    quote: "The free tier is too limited but paid plans jump in price aggressively.",
    platform: "Twitter / X",
    mentions: 23,
    intensity: "low" as const,
    topic: "Pricing",
  },
];

/* ──────────────────────────────────────────────────────────────
   Dashboard Page
   ────────────────────────────────────────────────────────────── */
export default function DashboardPage() {
  const [sidebarOpen, setSidebarOpen] = useState(false);
  const [refreshing, setRefreshing] = useState(false);

  const handleRefresh = async () => {
    setRefreshing(true);
    await new Promise((r) => setTimeout(r, 900));
    setRefreshing(false);
  };

  return (
    <div className="flex min-h-dvh bg-surface-bg">
      <Sidebar isOpen={sidebarOpen} onClose={() => setSidebarOpen(false)} />

      <div className="flex flex-1 flex-col lg:pl-64">
        <Navbar onMobileMenuToggle={() => setSidebarOpen(true)} />

        <main className="flex-1 p-5 lg:p-8 space-y-6">

          {/* ── Page Header ── */}
          <div className="flex flex-col sm:flex-row sm:items-center sm:justify-between gap-4">
            <div>
              <h1 className="text-2xl font-bold text-ink tracking-tight">Dashboard</h1>
              <p className="text-sm text-ink-muted mt-0.5">
                Good morning, Muskan ·{" "}
                <span className="text-brand-500 font-medium">Compass Crew</span>
              </p>
            </div>
            <div className="flex items-center gap-2.5">
              <Button
                variant="ghost"
                size="sm"
                loading={refreshing}
                leftIcon={!refreshing ? <RefreshCw className="h-3.5 w-3.5" /> : undefined}
                onClick={handleRefresh}
              >
                Refresh
              </Button>
              <Link href="/analyze">
                <Button size="sm" leftIcon={<Sparkles className="h-3.5 w-3.5" />}>
                  New Analysis
                </Button>
              </Link>
            </div>
          </div>

          {/* ── Stat Cards ── */}
          <StaggerContainer className="grid grid-cols-1 sm:grid-cols-2 xl:grid-cols-4 gap-4">
            {STAT_CARDS.map((s) => (
              <StaggerItem key={s.label}>
                <StatCard {...s} />
              </StaggerItem>
            ))}
          </StaggerContainer>

          {/* ── Row 2: Pain by Platform + Severity Pie ── */}
          <div className="grid grid-cols-1 lg:grid-cols-3 gap-5">
            {/* Platform bar chart */}
            <Card className="lg:col-span-2">
              <CardHeader>
                <div className="flex items-center justify-between">
                  <div>
                    <CardTitle>Pain Points by Platform</CardTitle>
                    <CardDescription>
                      Breakdown across 7 scraped voice-of-customer channels
                    </CardDescription>
                  </div>
                  <Badge variant="brand">7 Sources</Badge>
                </div>
              </CardHeader>
              <CardContent>
                <PainByPlatformBar data={PLATFORM_DATA} />
              </CardContent>
            </Card>

            {/* Severity pie chart */}
            <Card>
              <CardHeader>
                <CardTitle>Severity Distribution</CardTitle>
                <CardDescription>By emotional intensity score</CardDescription>
              </CardHeader>
              <CardContent className="flex flex-col items-center justify-center">
                <PainSeverityPie data={PIE_DATA} />
              </CardContent>
            </Card>
          </div>

          {/* ── Row 3: Activity Area + Quick Actions ── */}
          <div className="grid grid-cols-1 lg:grid-cols-3 gap-5">
            {/* Weekly activity */}
            <Card className="lg:col-span-2">
              <CardHeader>
                <div className="flex items-center justify-between">
                  <div>
                    <CardTitle>Generation Activity</CardTitle>
                    <CardDescription>
                      Campaigns & insights produced this week
                    </CardDescription>
                  </div>
                  <div className="flex items-center gap-3 text-xs text-ink-muted">
                    <span className="flex items-center gap-1.5">
                      <span className="h-2 w-2 rounded-full bg-brand-500" />
                      Campaigns
                    </span>
                    <span className="flex items-center gap-1.5">
                      <span className="h-2 w-2 rounded-full bg-pain-low" />
                      Insights
                    </span>
                  </div>
                </div>
              </CardHeader>
              <CardContent>
                <CampaignActivityArea data={ACTIVITY_DATA} />
              </CardContent>
            </Card>

            {/* Quick Actions */}
            <QuickActions />
          </div>

          {/* ── Row 4: Recent Pain Points Table ── */}
          <Card>
            <CardHeader>
              <div className="flex items-center justify-between">
                <div>
                  <CardTitle>Top Scraped Pain Points</CardTitle>
                  <CardDescription>
                    Highest urgency complaints driving current campaigns
                  </CardDescription>
                </div>
                <Link
                  href="/analyze"
                  className="text-xs font-semibold text-brand-600 dark:text-brand-400 hover:underline flex items-center gap-1"
                >
                  View All <ArrowRight className="h-3 w-3" />
                </Link>
              </div>
            </CardHeader>
            <CardContent noPadding>
              <div className="divide-y divide-surface-border">
                {RECENT_PAINS.map((pain) => (
                  <RecentPainRow key={pain.id} pain={pain} />
                ))}
              </div>
            </CardContent>
          </Card>

        </main>
      </div>
    </div>
  );
}
