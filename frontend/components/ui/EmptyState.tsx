"use client";

import { Sparkles, ArrowRight } from "lucide-react";
import { Card } from "@/components/ui/card";
import { Button } from "@/components/ui/button";
import { cn } from "@/lib/utils";

interface EmptyStateProps {
  icon?: React.ElementType;
  title: string;
  description: string;
  actionLabel?: string;
  onAction?: () => void;
  exampleInputs?: string[];
  onSelectExample?: (example: string) => void;
  className?: string;
}

export function EmptyState({
  icon: Icon = Sparkles,
  title,
  description,
  actionLabel,
  onAction,
  exampleInputs,
  onSelectExample,
  className,
}: EmptyStateProps) {
  return (
    <Card className={cn("flex flex-col items-center justify-center py-14 px-6 text-center border border-surface-border bg-surface-card", className)}>
      <div className="relative mb-5">
        <div className="h-16 w-16 rounded-2xl bg-brand-50 dark:bg-brand-100/10 border border-brand-200 dark:border-brand-600/30 flex items-center justify-center shadow-sm">
          <Icon className="h-8 w-8 text-brand-500" />
        </div>
        <div className="absolute -bottom-1 -right-1 h-6 w-6 rounded-full bg-surface-card border border-surface-border flex items-center justify-center shadow-xs">
          <Sparkles className="h-3 w-3 text-brand-400" />
        </div>
      </div>

      <h3 className="font-bold text-ink text-lg tracking-tight max-w-sm">{title}</h3>
      <p className="text-sm text-ink-muted mt-1.5 max-w-md leading-relaxed">{description}</p>

      {exampleInputs && exampleInputs.length > 0 && (
        <div className="mt-6 space-y-2">
          <span className="text-xs font-semibold uppercase tracking-wider text-ink-faint block">
            Try these example topics:
          </span>
          <div className="flex flex-wrap justify-center gap-2 max-w-lg">
            {exampleInputs.map((item) => (
              <button
                key={item}
                onClick={() => onSelectExample?.(item)}
                className="rounded-full border border-surface-border bg-surface-subtle/80 px-3.5 py-1.5 text-xs text-ink-muted hover:border-brand-300 hover:text-brand-600 dark:hover:text-brand-400 hover:bg-brand-50/50 dark:hover:bg-brand-100/10 transition-all cursor-pointer font-medium"
              >
                &ldquo;{item}&rdquo;
              </button>
            ))}
          </div>
        </div>
      )}

      {actionLabel && onAction && (
        <div className="mt-6">
          <Button
            onClick={onAction}
            size="md"
            rightIcon={<ArrowRight className="h-4 w-4" />}
          >
            {actionLabel}
          </Button>
        </div>
      )}
    </Card>
  );
}
