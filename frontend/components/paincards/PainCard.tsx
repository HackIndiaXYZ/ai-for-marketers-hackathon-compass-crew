"use client";

import { useState } from "react";
import { motion } from "framer-motion";
import {
  AlertTriangle,
  TrendingUp,
  MessageSquare,
  BarChart2,
  Copy,
  Check,
  ChevronDown,
  ChevronUp,
} from "lucide-react";
import { cn } from "@/lib/utils";
import { Badge } from "@/components/ui/badge";
import { Button } from "@/components/ui/button";
import { SPRING_SNAPPY } from "@/components/ui/motion";

/* ──────────────────────────────────────────────────────────────
   PainCard — displays a single customer pain point
   ────────────────────────────────────────────────────────────── */
export type Intensity = "high" | "medium" | "low";

export interface PainCardProps {
  id: string;
  quote: string;
  topic: string;
  platform: string;
  mentions: number;
  intensity: Intensity;
  impactScore: number;       // 0–100
  emotionTags?: string[];
  supportingQuotes?: string[];
}

const intensityConfig = {
  high: {
    label: "High Impact",
    icon: AlertTriangle,
    bar: "bg-pain-high",
    badge: "high" as const,
    ring: "ring-pain-high/20",
    bg: "bg-pain-high-bg/60 dark:bg-pain-high-bg",
  },
  medium: {
    label: "Medium Impact",
    icon: TrendingUp,
    bar: "bg-pain-medium",
    badge: "medium" as const,
    ring: "ring-pain-medium/20",
    bg: "bg-pain-medium-bg/60 dark:bg-pain-medium-bg",
  },
  low: {
    label: "Low Impact",
    icon: BarChart2,
    bar: "bg-pain-low",
    badge: "low" as const,
    ring: "ring-pain-low/20",
    bg: "bg-pain-low-bg/60 dark:bg-pain-low-bg",
  },
};

export function PainCard({
  quote,
  topic,
  platform,
  mentions,
  intensity,
  impactScore,
  emotionTags = [],
  supportingQuotes = [],
}: PainCardProps) {
  const [expanded, setExpanded] = useState(false);
  const [copied, setCopied] = useState(false);
  const config = intensityConfig[intensity];
  const Icon = config.icon;

  const handleCopy = async () => {
    await navigator.clipboard.writeText(quote);
    setCopied(true);
    setTimeout(() => setCopied(false), 1800);
  };

  return (
    <motion.div
      whileHover={{ y: -6, scale: 1.015 }}
      whileTap={{ scale: 0.98 }}
      transition={SPRING_SNAPPY}
      className={cn(
        "hover-lift rounded-card border bg-surface-card shadow-card hover:shadow-card-hover cursor-pointer",
        "ring-1",
        config.ring
      )}
    >
      {/* Card Header — Severity banner + topic tag */}
      <div
        className={cn(
          "flex items-center justify-between gap-3 px-5 py-3 rounded-t-card border-b border-surface-border",
          config.bg
        )}
      >
        <div className="flex items-center gap-2">
          <Badge variant={config.badge}>
            <Icon className="h-3 w-3" />
            {config.label}
          </Badge>
          <span className="text-xs font-semibold text-ink-faint">
            Score: {impactScore}/100
          </span>
        </div>
        <Badge variant="default">{topic}</Badge>
      </div>

      {/* Main Content */}
      <div className="p-5 space-y-4">
        {/* Scraped Quote */}
        <blockquote className="text-sm font-medium text-ink leading-relaxed italic border-l-2 border-brand-300 pl-3">
          &ldquo;{quote}&rdquo;
        </blockquote>

        {/* Impact Bar */}
        <div className="space-y-1">
          <div className="flex justify-between text-xs text-ink-muted font-medium">
            <span>Emotional Intensity</span>
            <span>{impactScore}%</span>
          </div>
          <div className="h-2 w-full rounded-full bg-surface-subtle overflow-hidden">
            <div
              className={cn("h-full rounded-full transition-all duration-500", config.bar)}
              style={{ width: `${impactScore}%` }}
            />
          </div>
        </div>

        {/* Meta tags: Platform & Mention Count */}
        <div className="flex flex-wrap items-center justify-between gap-2 pt-1 border-t border-surface-border text-xs text-ink-faint">
          <div className="flex items-center gap-3">
            <span className="flex items-center gap-1 font-medium text-ink-muted">
              <MessageSquare className="h-3.5 w-3.5 text-brand-500" />
              {platform}
            </span>
            <span>·</span>
            <span>{mentions} mentions</span>
          </div>

          <button
            onClick={handleCopy}
            className="flex items-center gap-1 text-xs font-medium text-ink-faint hover:text-brand-600 transition-colors"
          >
            {copied ? (
              <>
                <Check className="h-3.5 w-3.5 text-pain-low" /> Copied
              </>
            ) : (
              <>
                <Copy className="h-3.5 w-3.5" /> Copy quote
              </>
            )}
          </button>
        </div>

        {/* Emotion tags if present */}
        {emotionTags.length > 0 && (
          <div className="flex flex-wrap gap-1.5 pt-1">
            {emotionTags.map((tag) => (
              <span
                key={tag}
                className="rounded-md bg-surface-subtle border border-surface-border px-2 py-0.5 text-[11px] text-ink-muted font-medium"
              >
                #{tag}
              </span>
            ))}
          </div>
        )}

        {/* Expandable Supporting Quotes */}
        {supportingQuotes.length > 0 && (
          <div className="pt-2 border-t border-surface-border">
            <button
              onClick={() => setExpanded((v) => !v)}
              className="flex items-center gap-1.5 text-xs font-medium text-brand-600 hover:underline"
            >
              {expanded ? (
                <>
                  <ChevronUp className="h-3.5 w-3.5" /> Hide supporting quotes
                </>
              ) : (
                <>
                  <ChevronDown className="h-3.5 w-3.5" /> View {supportingQuotes.length} more quotes
                </>
              )}
            </button>

            {expanded && (
              <ul className="mt-3 space-y-2 text-xs text-ink-muted pl-2 border-l border-surface-border">
                {supportingQuotes.map((q, i) => (
                  <li key={i} className="italic">&ldquo;{q}&rdquo;</li>
                ))}
              </ul>
            )}
          </div>
        )}
      </div>

      {/* Action Footer */}
      <div className="px-5 py-3 bg-surface-subtle/50 border-t border-surface-border rounded-b-card flex items-center justify-between">
        <span className="text-xs text-ink-faint">AI-verified pain signal</span>
        <Button variant="ghost" size="xs">
          Generate Ad for Pain →
        </Button>
      </div>
    </motion.div>
  );
}
