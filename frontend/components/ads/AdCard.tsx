"use client";

import { useState } from "react";
import { motion } from "framer-motion";
import { Copy, Check, RefreshCw, ExternalLink } from "lucide-react";
import { cn } from "@/lib/utils";
import { Badge } from "@/components/ui/badge";
import { Button } from "@/components/ui/button";
import { SPRING_SNAPPY } from "@/components/ui/motion";

/* ──────────────────────────────────────────────────────────────
   AdCard — displays a single generated campaign asset
   ────────────────────────────────────────────────────────────── */
export type AdType =
  | "google-search"
  | "google-display"
  | "facebook"
  | "instagram"
  | "whatsapp"
  | "email"
  | "seo"
  | "landing";

export interface AdCardProps {
  id: string;
  type: AdType;
  headline: string;
  body: string;
  cta?: string;
  persona?: string;
  language: string;
  tone: string;
  onRegenerate?: (id: string) => void;
  regenerating?: boolean;
}

const typeConfig: Record<AdType, { label: string; color: string; bg: string }> = {
  "google-search":  { label: "Google Search",   color: "text-blue-600 dark:text-blue-400",  bg: "bg-blue-50 border-blue-200 dark:bg-blue-900/20 dark:border-blue-700/40" },
  "google-display": { label: "Google Display",  color: "text-blue-600 dark:text-blue-400",  bg: "bg-blue-50 border-blue-200 dark:bg-blue-900/20 dark:border-blue-700/40" },
  facebook:         { label: "Facebook Ad",     color: "text-indigo-600 dark:text-indigo-400", bg: "bg-indigo-50 border-indigo-200 dark:bg-indigo-900/20 dark:border-indigo-700/40" },
  instagram:        { label: "Instagram",       color: "text-pink-600 dark:text-pink-400",  bg: "bg-pink-50 border-pink-200 dark:bg-pink-900/20 dark:border-pink-700/40" },
  whatsapp:         { label: "WhatsApp",        color: "text-green-600 dark:text-green-400", bg: "bg-green-50 border-green-200 dark:bg-green-900/20 dark:border-green-700/40" },
  email:            { label: "Email Campaign",  color: "text-amber-600 dark:text-amber-400", bg: "bg-amber-50 border-amber-200 dark:bg-amber-900/20 dark:border-amber-700/40" },
  seo:              { label: "SEO Content",     color: "text-teal-600 dark:text-teal-400",  bg: "bg-teal-50 border-teal-200 dark:bg-teal-900/20 dark:border-teal-700/40" },
  landing:          { label: "Landing Page",    color: "text-violet-600 dark:text-violet-400", bg: "bg-violet-50 border-violet-200 dark:bg-violet-900/20 dark:border-violet-700/40" },
};

export function AdCard({
  id,
  type,
  headline,
  body,
  cta,
  persona,
  language,
  tone,
  onRegenerate,
  regenerating = false,
}: AdCardProps) {
  const [copiedField, setCopiedField] = useState<"headline" | "body" | "cta" | null>(null);
  const config = typeConfig[type];

  const handleCopy = async (text: string, field: "headline" | "body" | "cta") => {
    await navigator.clipboard.writeText(text);
    setCopiedField(field);
    setTimeout(() => setCopiedField(null), 1800);
  };

  const CopyBtn = ({ text, field }: { text: string; field: "headline" | "body" | "cta" }) => (
    <button
      onClick={() => handleCopy(text, field)}
      title={`Copy ${field}`}
      className="ml-1.5 shrink-0 rounded p-0.5 text-ink-faint hover:text-ink transition-colors cursor-pointer"
    >
      {copiedField === field ? (
        <Check className="h-3.5 w-3.5 text-pain-low" />
      ) : (
        <Copy className="h-3.5 w-3.5" />
      )}
    </button>
  );

  return (
    <motion.div
      whileHover={{ y: -6, scale: 1.015 }}
      whileTap={{ scale: 0.98 }}
      transition={SPRING_SNAPPY}
      className="hover-lift rounded-card border border-surface-border bg-surface-card shadow-card hover:shadow-card-hover cursor-pointer flex flex-col overflow-hidden h-full"
    >
      {/* Header */}
      <div className={cn("px-4 py-3 border-b border-surface-border flex items-center justify-between gap-3", config.bg)}>
        <span className={cn("text-xs font-semibold", config.color)}>{config.label}</span>
        <div className="flex items-center gap-2">
          {persona && (
            <Badge variant="default" className="text-[10px]">👤 {persona}</Badge>
          )}
          <Badge variant="default" className="text-[10px]">{language}</Badge>
          <Badge variant="default" className="text-[10px]">{tone}</Badge>
        </div>
      </div>

      {/* Body */}
      <div className="p-5 flex-1 space-y-4">
        {/* Headline */}
        <div>
          <div className="flex items-center justify-between text-[10px] font-semibold uppercase tracking-wider text-ink-faint mb-1">
            <span>Headline</span>
            <CopyBtn text={headline} field="headline" />
          </div>
          <p className="font-bold text-ink text-base leading-snug">{headline}</p>
        </div>

        {/* Ad Body */}
        <div>
          <div className="flex items-center justify-between text-[10px] font-semibold uppercase tracking-wider text-ink-faint mb-1">
            <span>Primary Text / Body</span>
            <CopyBtn text={body} field="body" />
          </div>
          <p className="text-sm text-ink-muted leading-relaxed whitespace-pre-line">{body}</p>
        </div>

        {/* Call to Action */}
        {cta && (
          <div>
            <div className="flex items-center justify-between text-[10px] font-semibold uppercase tracking-wider text-ink-faint mb-1">
              <span>CTA Button / Link</span>
              <CopyBtn text={cta} field="cta" />
            </div>
            <div className="inline-flex items-center gap-1.5 rounded-lg bg-surface-subtle border border-surface-border px-3 py-1.5 text-xs font-semibold text-brand-600 dark:text-brand-400">
              {cta}
            </div>
          </div>
        )}
      </div>

      {/* Card Footer */}
      <div className="px-5 py-3 border-t border-surface-border bg-surface-subtle/50 flex items-center justify-between">
        <span className="text-xs text-ink-faint">Pain-Aligned Copy</span>

        {onRegenerate && (
          <Button
            variant="ghost"
            size="xs"
            loading={regenerating}
            leftIcon={!regenerating ? <RefreshCw className="h-3 w-3" /> : undefined}
            onClick={(e) => {
              e.stopPropagation();
              onRegenerate(id);
            }}
          >
            Regenerate
          </Button>
        )}
      </div>
    </motion.div>
  );
}
