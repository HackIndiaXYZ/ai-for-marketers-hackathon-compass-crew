"use client";

import { motion } from "framer-motion";
import { Zap, Globe2, ShoppingBag, CheckCircle2 } from "lucide-react";
import { cn } from "@/lib/utils";
import { Badge } from "@/components/ui/badge";
import { SPRING_SNAPPY } from "@/components/ui/motion";

/* ──────────────────────────────────────────────────────────────
   PersonaCard
   ────────────────────────────────────────────────────────────── */
export type PurchasingPower = "low" | "medium" | "high" | "premium";

export interface PersonaCardProps {
  emoji: string;
  name: string;
  ageRange: string;
  description: string;
  needs: string[];
  purchasingPower: PurchasingPower;
  channels: string[];
  topPains: string[];
  color?: "brand" | "high" | "medium" | "low";
}

const powerConfig: Record<PurchasingPower, { label: string; bars: number; color: string }> = {
  low:     { label: "Budget Conscious",  bars: 1, color: "bg-pain-high" },
  medium:  { label: "Mid-Range Spender", bars: 2, color: "bg-pain-medium" },
  high:    { label: "High Spender",      bars: 3, color: "bg-pain-low" },
  premium: { label: "Premium Buyer",     bars: 4, color: "bg-brand-500" },
};

const colorAccent = {
  brand:  "bg-brand-50 border-brand-200 dark:bg-brand-100/10 dark:border-brand-600/30",
  high:   "bg-pain-high-bg border-pain-high/20",
  medium: "bg-pain-medium-bg border-pain-medium/20",
  low:    "bg-pain-low-bg border-pain-low/20",
};

export function PersonaCard({
  emoji,
  name,
  ageRange,
  description,
  needs,
  purchasingPower,
  channels,
  topPains,
  color = "brand",
}: PersonaCardProps) {
  const power = powerConfig[purchasingPower];

  return (
    <motion.div
      whileHover={{ y: -6, scale: 1.015 }}
      whileTap={{ scale: 0.98 }}
      transition={SPRING_SNAPPY}
      className="hover-lift rounded-card border border-surface-border bg-surface-card shadow-card hover:shadow-card-hover cursor-pointer flex flex-col overflow-hidden h-full"
    >
      {/* Header with avatar + name */}
      <div className={cn("p-5 border-b border-surface-border", colorAccent[color])}>
        <div className="flex items-start gap-4">
          <div className="h-14 w-14 rounded-2xl bg-surface-card border border-surface-border flex items-center justify-center text-3xl shrink-0 shadow-md">
            {emoji}
          </div>
          <div className="min-w-0 flex-1">
            <h3 className="font-extrabold text-ink text-lg leading-tight tracking-tight">{name}</h3>
            <p className="text-xs text-ink-muted mt-0.5 font-medium">{ageRange}</p>
            <div className="mt-2.5 flex items-center gap-2 text-xs text-ink font-semibold">
              <ShoppingBag className="h-3.5 w-3.5 text-brand-500 shrink-0" />
              <span>{power.label}</span>
              <div className="flex gap-1 ml-auto">
                {[1, 2, 3, 4].map((bar) => (
                  <div
                    key={bar}
                    className={cn(
                      "h-3.5 w-1.5 rounded-sm transition-colors",
                      bar <= power.bars ? power.color : "bg-surface-border"
                    )}
                  />
                ))}
              </div>
            </div>
          </div>
        </div>
      </div>

      {/* Content */}
      <div className="p-5 flex-1 space-y-5 text-xs">
        {/* Description */}
        <p className="text-ink-muted leading-relaxed text-sm font-normal">{description}</p>

        {/* Core Needs & Drivers */}
        <div className="space-y-2 bg-surface-subtle/70 rounded-xl p-3 border border-surface-border">
          <p className="font-bold uppercase tracking-wider text-ink text-[10px] flex items-center gap-1.5">
            <Zap className="h-3.5 w-3.5 text-brand-500" /> Core Needs & Drivers
          </p>
          <ul className="space-y-1.5">
            {needs.map((need) => (
              <li key={need} className="flex items-start gap-2 text-ink text-xs font-medium">
                <CheckCircle2 className="h-4 w-4 text-pain-low shrink-0 mt-0.5" />
                <span>{need}</span>
              </li>
            ))}
          </ul>
        </div>

        {/* Top Pains Targeted */}
        <div className="space-y-2">
          <p className="font-bold uppercase tracking-wider text-pain-high text-[10px] flex items-center gap-1.5">
            🔥 Top Pain Points Triggered
          </p>
          <div className="space-y-1.5">
            {topPains.map((pain) => (
              <div
                key={pain}
                className="rounded-lg bg-pain-high-bg/40 border border-pain-high/20 border-l-3 border-l-pain-high px-3 py-2 text-xs text-ink font-medium leading-snug italic"
              >
                &ldquo;{pain}&rdquo;
              </div>
            ))}
          </div>
        </div>

        {/* Channels */}
        <div className="space-y-2">
          <p className="font-bold uppercase tracking-wider text-ink text-[10px] flex items-center gap-1.5">
            <Globe2 className="h-3.5 w-3.5 text-brand-500" /> Preferred Channels
          </p>
          <div className="flex flex-wrap gap-1.5">
            {channels.map((ch) => (
              <Badge key={ch} variant="brand" className="text-xs px-2.5 py-0.5 font-semibold">
                {ch}
              </Badge>
            ))}
          </div>
        </div>
      </div>

      {/* Footer CTA */}
      <div className="px-5 py-3 border-t border-surface-border bg-surface-subtle/80 text-xs text-ink-faint flex items-center justify-between font-medium">
        <span>AI-Generated Persona</span>
        <span className="font-bold text-brand-600 dark:text-brand-400 flex items-center gap-1">
          Target in Campaigns →
        </span>
      </div>
    </motion.div>
  );
}
