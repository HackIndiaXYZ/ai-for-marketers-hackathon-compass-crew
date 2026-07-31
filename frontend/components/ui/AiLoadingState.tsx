"use client";

import { Sparkles, Loader2, CheckCircle2 } from "lucide-react";
import { Card } from "@/components/ui/card";
import { cn } from "@/lib/utils";

export interface LoadingStep {
  label: string;
  sublabel?: string;
}

interface AiLoadingStateProps {
  title?: string;
  subtitle?: string;
  steps: (string | LoadingStep)[];
  currentStepIndex: number;
  progressPercent?: number;
  className?: string;
}

export function AiLoadingState({
  title = "AI Engine Active",
  subtitle,
  steps,
  currentStepIndex,
  progressPercent,
  className,
}: AiLoadingStateProps) {
  const calculatedProgress =
    progressPercent !== undefined
      ? progressPercent
      : Math.min(100, Math.round(((currentStepIndex + 1) / steps.length) * 100));

  return (
    <Card className={cn("overflow-hidden border border-brand-200 dark:border-brand-600/30 bg-surface-card shadow-card", className)}>
      <div className="flex flex-col items-center py-8 px-6 gap-6 text-center">
        {/* Animated AI Thinking Badge & Pulse rings */}
        <div className="relative h-20 w-20 flex items-center justify-center">
          <div className="absolute inset-0 rounded-3xl bg-brand-500/10 dark:bg-brand-500/20 animate-ping" />
          <div className="absolute -inset-2 rounded-full border-2 border-dashed border-brand-400/50 animate-[spin_8s_linear_infinite]" />
          <div className="relative h-16 w-16 rounded-2xl bg-gradient-to-br from-brand-500 to-brand-700 text-white flex items-center justify-center shadow-lg shadow-brand-500/25">
            <Sparkles className="h-8 w-8 animate-pulse" />
          </div>
        </div>

        {/* Header Text */}
        <div className="space-y-1 max-w-md">
          <h3 className="font-bold text-ink text-lg tracking-tight">{title}</h3>
          {subtitle && <p className="text-sm text-ink-muted leading-relaxed">{subtitle}</p>}
        </div>

        {/* Progress bar */}
        <div className="w-full max-w-md space-y-1.5">
          <div className="flex justify-between items-center text-xs font-semibold text-ink-muted">
            <span>Processing intelligence</span>
            <span className="text-brand-600 dark:text-brand-400 font-bold">{calculatedProgress}%</span>
          </div>
          <div className="h-2 w-full rounded-full bg-surface-subtle overflow-hidden border border-surface-border">
            <div
              className="h-full rounded-full bg-gradient-to-r from-brand-500 via-brand-400 to-pain-low transition-all duration-500 ease-out"
              style={{ width: `${calculatedProgress}%` }}
            />
          </div>
        </div>

        {/* Step checklist */}
        <div className="w-full max-w-md space-y-2.5 bg-surface-subtle/50 rounded-xl p-4 border border-surface-border text-left">
          {steps.map((stepItem, idx) => {
            const stepLabel = typeof stepItem === "string" ? stepItem : stepItem.label;
            const stepSub = typeof stepItem === "object" ? stepItem.sublabel : undefined;
            const isDone = idx < currentStepIndex;
            const isCurrent = idx === currentStepIndex;

            return (
              <div key={idx} className="flex items-start gap-3 transition-colors">
                <div className="mt-0.5 shrink-0">
                  {isDone ? (
                    <CheckCircle2 className="h-4.5 w-4.5 text-pain-low" />
                  ) : isCurrent ? (
                    <div className="h-4.5 w-4.5 rounded-full bg-brand-500/20 text-brand-600 dark:text-brand-400 flex items-center justify-center">
                      <Loader2 className="h-3.5 w-3.5 animate-spin" />
                    </div>
                  ) : (
                    <div className="h-4.5 w-4.5 rounded-full border-2 border-surface-border bg-surface-card" />
                  )}
                </div>
                <div className="min-w-0 flex-1">
                  <p
                    className={cn(
                      "text-xs font-medium transition-colors leading-tight",
                      isDone
                        ? "text-ink-muted"
                        : isCurrent
                        ? "text-ink font-bold"
                        : "text-ink-faint"
                    )}
                  >
                    {stepLabel}
                  </p>
                  {stepSub && isCurrent && (
                    <p className="text-[11px] text-brand-600 dark:text-brand-400 mt-0.5 animate-pulse">
                      {stepSub}
                    </p>
                  )}
                </div>
              </div>
            );
          })}
        </div>
      </div>
    </Card>
  );
}

export function SkeletonCard({ className }: { className?: string }) {
  return (
    <Card className={cn("p-5 space-y-4 animate-pulse", className)}>
      <div className="flex items-center gap-3">
        <div className="h-10 w-10 rounded-xl bg-surface-subtle" />
        <div className="space-y-2 flex-1">
          <div className="h-4 w-1/3 rounded bg-surface-subtle" />
          <div className="h-3 w-1/4 rounded bg-surface-subtle" />
        </div>
      </div>
      <div className="space-y-2">
        <div className="h-3 w-full rounded bg-surface-subtle" />
        <div className="h-3 w-5/6 rounded bg-surface-subtle" />
        <div className="h-3 w-4/6 rounded bg-surface-subtle" />
      </div>
      <div className="flex gap-2 pt-2">
        <div className="h-6 w-16 rounded-full bg-surface-subtle" />
        <div className="h-6 w-20 rounded-full bg-surface-subtle" />
      </div>
    </Card>
  );
}
