"use client";

import { AlertTriangle, RefreshCw, WifiOff, ServerOff, Sparkles, HelpCircle } from "lucide-react";
import { Card } from "@/components/ui/card";
import { Button } from "@/components/ui/button";
import { cn } from "@/lib/utils";

export type ErrorType = "timeout" | "network" | "backend" | "gemini" | "empty" | "generic";

interface ErrorCardProps {
  type?: ErrorType;
  title?: string;
  description?: string;
  onRetry?: () => void;
  onUseFallback?: () => void;
  className?: string;
}

const errorConfig: Record<
  ErrorType,
  { icon: React.ElementType; title: string; desc: string; badge: string }
> = {
  timeout: {
    icon: AlertTriangle,
    title: "Request Timed Out",
    desc: "The AI model is taking longer than expected to process your request. Please try again.",
    badge: "Timeout",
  },
  network: {
    icon: WifiOff,
    title: "Connection Lost",
    desc: "Unable to reach the server. Please check your network connection and try again.",
    badge: "Network Error",
  },
  backend: {
    icon: ServerOff,
    title: "Service Temporarily Unavailable",
    desc: "Our backend server is currently starting up or undergoing maintenance. Try again in a moment.",
    badge: "Backend Offline",
  },
  gemini: {
    icon: Sparkles,
    title: "AI Synthesis Paused",
    desc: "Gemini API experienced a temporary rate limit or quota delay. Click retry to rerun synthesis.",
    badge: "AI Engine",
  },
  empty: {
    icon: HelpCircle,
    title: "No Results Discovered",
    desc: "We couldn't find matching customer complaints for this topic. Try expanding your search terms.",
    badge: "No Data",
  },
  generic: {
    icon: AlertTriangle,
    title: "Something Went Wrong",
    desc: "An unexpected error occurred while generating intelligence. Please try again.",
    badge: "Notice",
  },
};

export function ErrorCard({
  type = "generic",
  title,
  description,
  onRetry,
  onUseFallback,
  className,
}: ErrorCardProps) {
  const cfg = errorConfig[type];
  const Icon = cfg.icon;

  return (
    <Card className={cn("border border-pain-high/30 bg-pain-high-bg/50 p-6 text-center shadow-card", className)}>
      <div className="flex flex-col items-center gap-4 max-w-md mx-auto">
        <div className="h-12 w-12 rounded-2xl bg-pain-high/10 border border-pain-high/30 flex items-center justify-center text-pain-high shrink-0 shadow-sm">
          <Icon className="h-6 w-6" />
        </div>

        <div className="space-y-1">
          <span className="inline-block rounded-full bg-pain-high/15 border border-pain-high/30 px-2.5 py-0.5 text-[10px] font-bold uppercase tracking-wider text-pain-high">
            {cfg.badge}
          </span>
          <h3 className="font-bold text-ink text-base tracking-tight">{title || cfg.title}</h3>
          <p className="text-xs text-ink-muted leading-relaxed">{description || cfg.desc}</p>
        </div>

        <div className="flex items-center gap-3 pt-2 flex-wrap justify-center">
          {onRetry && (
            <Button
              size="sm"
              onClick={onRetry}
              leftIcon={<RefreshCw className="h-3.5 w-3.5" />}
              className="bg-pain-high text-white hover:bg-pain-high/90 border-transparent"
            >
              Try Again
            </Button>
          )}
          {onUseFallback && (
            <Button variant="secondary" size="sm" onClick={onUseFallback}>
              Load Sample Data
            </Button>
          )}
        </div>
      </div>
    </Card>
  );
}
