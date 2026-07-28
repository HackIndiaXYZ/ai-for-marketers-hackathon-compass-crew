"use client";

import Link from "next/link";
import { motion } from "framer-motion";
import {
  ArrowRight,
  Sparkles,
  MessageSquare,
  Users,
  Megaphone,
  TrendingUp,
  Gauge,
  BarChart2,
  Lightbulb,
  Globe2,
  CheckCircle2,
  Search,
  Brain,
  Zap,
} from "lucide-react";
import { Navbar } from "@/components/navbar/Navbar";
import { Footer } from "@/components/footer/Footer";
import { Button } from "@/components/ui/button";
import { Badge } from "@/components/ui/badge";
import { Card } from "@/components/ui/card";
import { FadeInUp, StaggerContainer, StaggerItem } from "@/components/ui/motion";

/* ─── Data ──────────────────────────────────────────────────── */

const PLATFORMS = [
  { name: "Reddit", color: "bg-orange-50 text-orange-600 border-orange-200 dark:bg-orange-900/20 dark:text-orange-400" },
  { name: "Quora", color: "bg-red-50 text-red-600 border-red-200 dark:bg-red-900/20 dark:text-red-400" },
  { name: "Google Reviews", color: "bg-blue-50 text-blue-600 border-blue-200 dark:bg-blue-900/20 dark:text-blue-400" },
  { name: "MouthShut", color: "bg-purple-50 text-purple-600 border-purple-200 dark:bg-purple-900/20 dark:text-purple-400" },
  { name: "Twitter / X", color: "bg-neutral-50 text-neutral-700 border-neutral-200 dark:bg-neutral-800/40 dark:text-neutral-300" },
  { name: "Justdial", color: "bg-yellow-50 text-yellow-700 border-yellow-200 dark:bg-yellow-900/20 dark:text-yellow-400" },
  { name: "IndiaMART", color: "bg-green-50 text-green-700 border-green-200 dark:bg-green-900/20 dark:text-green-400" },
];

const HOW_IT_WORKS = [
  {
    step: "01",
    icon: Search,
    title: "Collect Customer Voices",
    description:
      "Enter any business topic or product. Our AI agents scrape real complaints, reviews, and discussions from 7 platforms in seconds.",
    color: "bg-brand-50 text-brand-600 dark:bg-brand-100/10 dark:text-brand-400",
    borderColor: "border-brand-200 dark:border-brand-600/30",
  },
  {
    step: "02",
    icon: Brain,
    title: "Analyze Pain Points",
    description:
      "NLP agents rank pain points by frequency, emotional intensity, and business impact. You see what actually matters — not just noise.",
    color: "bg-pain-medium-bg text-pain-medium",
    borderColor: "border-pain-medium/20",
  },
  {
    step: "03",
    icon: Zap,
    title: "Generate Winning Campaigns",
    description:
      "Persona-aware campaign agents write Google Ads, Facebook creatives, WhatsApp messages, and more — with ROI predictions before you spend a rupee.",
    color: "bg-pain-low-bg text-pain-low",
    borderColor: "border-pain-low/20",
  },
];

const FEATURES = [
  {
    icon: BarChart2,
    title: "Dashboard",
    desc: "Real-time overview of campaigns, pain points, personas, and AI insights.",
  },
  {
    icon: Search,
    title: "Pain Analyzer",
    desc: "Frequency heatmaps, emotional intensity scoring, and quote extraction from live reviews.",
  },
  {
    icon: Users,
    title: "Persona Engine",
    desc: "Auto-generated customer segments with purchasing power, needs, and best channel tags.",
  },
  {
    icon: Megaphone,
    title: "Campaign Generator",
    desc: "Google Ads, Meta, WhatsApp, Email, SEO in English, Hinglish, Hindi, Bengali — tone-controlled.",
  },
  {
    icon: Lightbulb,
    title: "Insights Briefs",
    desc: "Plain-language market intelligence reports your team can actually read and act on.",
  },
  {
    icon: TrendingUp,
    title: "Optimizer",
    desc: "A/B variant comparison with CTR predictions and audience-budget split recommendations.",
  },
  {
    icon: Gauge,
    title: "ROI Simulator",
    desc: "Pre-launch predictions: reach, clicks, conversions, revenue — before spending any budget.",
  },
  {
    icon: Globe2,
    title: "Brand Memory",
    desc: "Persist your brand voice, tone, and audience across all campaigns automatically.",
  },
];

const PAIN_EXAMPLES = [
  {
    text: '"The onboarding takes forever and no one explains what happens after you sign up."',
    platform: "Reddit",
    intensity: "High",
    variant: "high" as const,
    freq: "247 mentions",
  },
  {
    text: '"Customer support replies in 5 days. My issue was urgent and I lost money because of it."',
    platform: "Google Reviews",
    intensity: "High",
    variant: "high" as const,
    freq: "189 mentions",
  },
  {
    text: '"The mobile app crashes during checkout. Fixed on web but not mobile."',
    platform: "MouthShut",
    intensity: "Medium",
    variant: "medium" as const,
    freq: "93 mentions",
  },
];

/* ─── Page ─────────────────────────────────────────────────── */

export default function LandingPage() {
  return (
    <div className="flex min-h-dvh flex-col bg-surface-bg">
      <Navbar />

      {/* ══════════ HERO ══════════ */}
      <section className="relative overflow-hidden px-4 pt-20 pb-24 sm:pt-28 sm:pb-32">
        {/* Decorative background blobs */}
        <div
          aria-hidden="true"
          className="pointer-events-none absolute -top-32 left-1/2 -translate-x-1/2 w-[800px] h-[600px] rounded-full opacity-20 blur-[120px]"
          style={{ background: "radial-gradient(ellipse at center, hsl(248 60% 70%), transparent 70%)" }}
        />

        <div className="relative mx-auto max-w-4xl text-center">
          {/* Pill badge */}
          <FadeInUp delay={0}>
            <div className="mb-6 inline-flex items-center gap-2 rounded-full border border-brand-200 dark:border-brand-600/40 bg-brand-50 dark:bg-brand-100/10 px-4 py-1.5 text-sm font-medium text-brand-600 dark:text-brand-400">
              <Sparkles className="h-3.5 w-3.5" />
              AI for Marketers Hackathon · Compass Crew
            </div>
          </FadeInUp>

          {/* Headline */}
          <FadeInUp delay={0.08}>
            <h1 className="mt-4 text-5xl sm:text-6xl lg:text-7xl font-bold tracking-tight text-ink leading-[1.08]">
              Turn Customer{" "}
              <span
                className="inline-block"
                style={{
                  background: "linear-gradient(135deg, hsl(248 60% 58%), hsl(268 70% 65%))",
                  WebkitBackgroundClip: "text",
                  WebkitTextFillColor: "transparent",
                  backgroundClip: "text",
                }}
              >
                Pain Points
              </span>
              <br />
              into Winning Campaigns
            </h1>
          </FadeInUp>

          {/* Subheadline */}
          <FadeInUp delay={0.16}>
            <p className="mt-6 mx-auto max-w-2xl text-lg sm:text-xl text-ink-muted leading-relaxed">
              PainToAd AI scrapes real complaints from Reddit, Quora, Google Reviews & 4
              more platforms — then generates ROI-predicted ad campaigns tailored to your
              audience. Know what hurts before you spend.
            </p>
          </FadeInUp>

          {/* CTA */}
          <FadeInUp delay={0.24}>
            <div className="mt-10 flex flex-wrap items-center justify-center gap-3">
              <Link href="/login">
                <Button size="lg" rightIcon={<ArrowRight className="h-4 w-4" />}>
                  Try It Free
                </Button>
              </Link>
            </div>
          </FadeInUp>

          {/* Trust indicators */}
          <FadeInUp delay={0.32}>
            <div className="mt-10 flex flex-wrap items-center justify-center gap-5 text-sm text-ink-faint">
              {["No credit card needed", "7 platforms scraped", "Live AI generation"].map((t) => (
                <div key={t} className="flex items-center gap-1.5">
                  <CheckCircle2 className="h-4 w-4 text-pain-low shrink-0" />
                  {t}
                </div>
              ))}
            </div>
          </FadeInUp>
        </div>

        {/* Hero Demo Card with gentle float animation */}
        <FadeInUp delay={0.4} className="relative mx-auto mt-16 max-w-3xl">
          <motion.div
            animate={{ y: [0, -6, 0] }}
            transition={{ duration: 4, repeat: Infinity, ease: "easeInOut" }}
            className="rounded-2xl border border-surface-border bg-surface-card shadow-card-hover overflow-hidden"
          >
            {/* Fake browser chrome */}
            <div className="flex items-center gap-2 px-4 py-3 bg-surface-subtle border-b border-surface-border">
              <div className="flex gap-1.5">
                <div className="h-3 w-3 rounded-full bg-pain-high/60" />
                <div className="h-3 w-3 rounded-full bg-pain-medium/60" />
                <div className="h-3 w-3 rounded-full bg-pain-low/60" />
              </div>
              <div className="flex-1 mx-4 rounded-md bg-surface-bg border border-surface-border text-xs text-ink-faint px-3 py-1 text-center">
                paintoad.ai/analyze
              </div>
            </div>

            {/* Pain cards demo */}
            <div className="p-5 space-y-3">
              <div className="flex items-center justify-between mb-4">
                <div>
                  <p className="text-xs font-semibold uppercase tracking-wider text-ink-faint">Pain Analysis</p>
                  <p className="font-semibold text-ink mt-0.5">Topic: &ldquo;SaaS Onboarding&rdquo;</p>
                </div>
                <Badge variant="brand">
                  <Sparkles className="h-3 w-3" />
                  529 mentions analyzed
                </Badge>
              </div>

              {PAIN_EXAMPLES.map((p, i) => (
                <div
                  key={i}
                  className="flex gap-3 p-3.5 rounded-xl bg-surface-subtle border border-surface-border"
                >
                  <div className="flex flex-col items-center gap-1 shrink-0">
                    <Badge variant={p.variant} className="text-[10px] px-1.5 py-0.5">
                      {p.intensity}
                    </Badge>
                    <MessageSquare className="h-4 w-4 text-ink-faint mt-1" />
                  </div>
                  <div className="min-w-0">
                    <p className="text-sm text-ink leading-snug italic">{p.text}</p>
                    <div className="mt-1.5 flex items-center gap-2 text-xs text-ink-faint">
                      <span>{p.platform}</span>
                      <span>·</span>
                      <span>{p.freq}</span>
                    </div>
                  </div>
                </div>
              ))}
            </div>
          </motion.div>
        </FadeInUp>
      </section>

      {/* ══════════ PLATFORMS ══════════ */}
      <section className="border-y border-surface-border bg-surface-subtle/50 py-8 px-4">
        <div className="mx-auto max-w-5xl">
          <p className="text-center text-xs font-semibold uppercase tracking-wider text-ink-faint mb-6">
            Collecting real voices from
          </p>
          <div className="flex flex-wrap justify-center gap-2">
            {PLATFORMS.map((p) => (
              <span
                key={p.name}
                className={`inline-flex items-center rounded-full border px-4 py-1.5 text-sm font-medium ${p.color}`}
              >
                {p.name}
              </span>
            ))}
          </div>
        </div>
      </section>

      {/* ══════════ PROBLEM / SOLUTION ══════════ */}
      <section className="py-20 px-4" id="features">
        <div className="mx-auto max-w-5xl">
          <StaggerContainer className="grid md:grid-cols-2 gap-6">
            {/* Problem */}
            <StaggerItem>
              <Card className="border-pain-high/30 bg-pain-high-bg/30 dark:bg-pain-high-bg">
                <div className="mb-4 inline-flex items-center gap-2 rounded-full bg-pain-high-bg text-pain-high border border-pain-high/20 px-3 py-1 text-xs font-semibold">
                  😤 The Problem
                </div>
                <h2 className="text-xl font-bold text-ink mb-3">
                  Marketers guess. Campaigns fail.
                </h2>
                <ul className="space-y-2.5 text-sm text-ink-muted">
                  {[
                    "Thousands of real customer complaints go unread every day",
                    "Generic messaging doesn't resonate with actual pain",
                    "Ad budgets are wasted on poorly targeted creatives",
                    "No system connects customer voice to campaign strategy",
                  ].map((item) => (
                    <li key={item} className="flex items-start gap-2">
                      <span className="text-pain-high mt-0.5 shrink-0">✗</span>
                      {item}
                    </li>
                  ))}
                </ul>
              </Card>
            </StaggerItem>

            {/* Solution */}
            <StaggerItem>
              <Card className="border-pain-low/30 bg-pain-low-bg/30 dark:bg-pain-low-bg">
                <div className="mb-4 inline-flex items-center gap-2 rounded-full bg-pain-low-bg text-pain-low border border-pain-low/20 px-3 py-1 text-xs font-semibold">
                  ✨ The Solution
                </div>
                <h2 className="text-xl font-bold text-ink mb-3">
                  PainToAd AI bridges the gap.
                </h2>
                <ul className="space-y-2.5 text-sm text-ink-muted">
                  {[
                    "Automatically scrapes and reads thousands of real reviews",
                    "Ranks pain points by urgency, frequency, and business impact",
                    "Generates persona-targeted campaigns from real customer language",
                    "Predicts ROI before you spend a single rupee",
                  ].map((item) => (
                    <li key={item} className="flex items-start gap-2">
                      <CheckCircle2 className="h-4 w-4 text-pain-low mt-0.5 shrink-0" />
                      {item}
                    </li>
                  ))}
                </ul>
              </Card>
            </StaggerItem>
          </StaggerContainer>
        </div>
      </section>

      {/* ══════════ HOW IT WORKS ══════════ */}
      <section className="py-20 px-4 bg-surface-subtle/40" id="how-it-works">
        <div className="mx-auto max-w-5xl">
          <FadeInUp className="text-center mb-12">
            <Badge variant="brand" className="mb-4">
              <Sparkles className="h-3 w-3" /> How it Works
            </Badge>
            <h2 className="text-3xl sm:text-4xl font-bold text-ink tracking-tight">
              From noise to campaign — in minutes
            </h2>
            <p className="mt-4 text-ink-muted max-w-xl mx-auto">
              A multi-agent AI pipeline that does the research, analysis, and
              creative generation so your team can focus on strategy.
            </p>
          </FadeInUp>

          <StaggerContainer className="grid md:grid-cols-3 gap-6 relative">
            {/* Connector line (desktop only) */}
            <div className="hidden md:block absolute top-10 left-[calc(33%+1rem)] right-[calc(33%+1rem)] h-px bg-surface-border" />

            {HOW_IT_WORKS.map((step, i) => {
              const Icon = step.icon;
              return (
                <StaggerItem key={i}>
                  <Card className="relative flex flex-col gap-4 h-full">
                    <div className="flex items-start justify-between">
                      <div className={`inline-flex h-11 w-11 items-center justify-center rounded-xl ${step.color} border ${step.borderColor}`}>
                        <Icon className="h-5 w-5" />
                      </div>
                      <span className="text-3xl font-black text-ink-faint/30 leading-none">{step.step}</span>
                    </div>
                    <div>
                      <h3 className="font-semibold text-ink text-base">{step.title}</h3>
                      <p className="mt-1.5 text-sm text-ink-muted leading-relaxed">{step.description}</p>
                    </div>
                  </Card>
                </StaggerItem>
              );
            })}
          </StaggerContainer>
        </div>
      </section>

      {/* ══════════ FEATURES GRID ══════════ */}
      <section className="py-20 px-4" id="use-cases">
        <div className="mx-auto max-w-5xl">
          <FadeInUp className="text-center mb-12">
            <Badge variant="brand" className="mb-4">All Modules</Badge>
            <h2 className="text-3xl sm:text-4xl font-bold text-ink tracking-tight">
              Everything a marketer needs
            </h2>
            <p className="mt-4 text-ink-muted max-w-xl mx-auto">
              Eight purpose-built modules, each powered by specialized AI agents,
              covering the full campaign lifecycle.
            </p>
          </FadeInUp>

          <StaggerContainer className="grid sm:grid-cols-2 lg:grid-cols-4 gap-4">
            {FEATURES.map((f) => {
              const Icon = f.icon;
              return (
                <StaggerItem key={f.title}>
                  <Card hoverable className="group flex flex-col gap-3 h-full">
                    <div className="h-10 w-10 rounded-xl bg-brand-50 dark:bg-brand-100/10 border border-brand-200 dark:border-brand-600/30 flex items-center justify-center transition-colors group-hover:bg-brand-100 dark:group-hover:bg-brand-100/20">
                      <Icon className="h-5 w-5 text-brand-500 dark:text-brand-400" />
                    </div>
                    <div>
                      <h3 className="font-semibold text-sm text-ink">{f.title}</h3>
                      <p className="mt-1 text-xs text-ink-muted leading-relaxed">{f.desc}</p>
                    </div>
                  </Card>
                </StaggerItem>
              );
            })}
          </StaggerContainer>
        </div>
      </section>

      {/* ══════════ CTA BANNER ══════════ */}
      <section className="py-20 px-4">
        <FadeInUp className="mx-auto max-w-3xl">
          <div
            className="relative overflow-hidden rounded-2xl p-10 text-center border border-brand-200 dark:border-brand-600/30"
            style={{
              background:
                "linear-gradient(135deg, hsl(248 60% 97%), hsl(268 50% 96%))",
            }}
          >
            {/* Dark mode override */}
            <div className="dark:hidden absolute inset-0 rounded-2xl"
              style={{ background: "linear-gradient(135deg, hsl(248 60% 97%), hsl(268 50% 96%))" }} />
            <div className="hidden dark:block absolute inset-0 rounded-2xl"
              style={{ background: "linear-gradient(135deg, hsl(248 30% 14%), hsl(268 25% 16%))" }} />

            <div className="relative z-10">
              <div className="mb-4 inline-flex items-center gap-2 rounded-full bg-brand-100 dark:bg-brand-100/15 border border-brand-200 dark:border-brand-600/40 px-3 py-1 text-xs font-semibold text-brand-600 dark:text-brand-400">
                <Sparkles className="h-3 w-3" /> Free to Try
              </div>
              <h2 className="text-3xl font-bold text-ink tracking-tight">
                Ready to stop guessing?
              </h2>
              <p className="mt-3 text-ink-muted max-w-md mx-auto text-base">
                Enter any business topic and let PainToAd AI show you what your
                customers are really saying — and how to turn it into campaigns
                that convert.
              </p>
              <div className="mt-8 flex flex-wrap items-center justify-center gap-3">
                <Link href="/dashboard">
                  <Button size="lg" rightIcon={<ArrowRight className="h-4 w-4" />}>
                    Launch the App
                  </Button>
                </Link>
                <Link href="/register">
                  <Button variant="secondary" size="lg">
                    Create Free Account
                  </Button>
                </Link>
              </div>
            </div>
          </div>
        </FadeInUp>
      </section>

      <Footer />
    </div>
  );
}
