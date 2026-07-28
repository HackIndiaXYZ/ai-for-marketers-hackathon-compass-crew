"use client";

import * as React from "react";
import { motion, type HTMLMotionProps } from "framer-motion";
import { cn } from "@/lib/utils";
import { SPRING_SNAPPY } from "./motion";

/* ──────────────────────────────────────────────────────────────
   Card — surface container with soft shadow + border & motion support
   ────────────────────────────────────────────────────────────── */

export interface CardProps extends HTMLMotionProps<"div"> {
  /** Adds hover lift animation */
  hoverable?: boolean;
  /** Remove padding */
  noPadding?: boolean;
}

const Card = React.forwardRef<HTMLDivElement, CardProps>(
  ({ className, hoverable = false, noPadding = false, whileHover, whileTap, ...props }, ref) => (
    <motion.div
      ref={ref}
      whileHover={hoverable ? whileHover ?? { y: -6, scale: 1.02 } : undefined}
      whileTap={hoverable ? whileTap ?? { scale: 0.98 } : undefined}
      transition={SPRING_SNAPPY}
      className={cn(
        "rounded-card bg-surface-card border border-surface-border shadow-card",
        !noPadding && "p-5",
        hoverable && "hover-lift hover:shadow-card-hover cursor-pointer",
        className
      )}
      {...props}
    />
  )
);
Card.displayName = "Card";

/* Header ───────────────────────────────────────────────────── */
const CardHeader = React.forwardRef<
  HTMLDivElement,
  React.HTMLAttributes<HTMLDivElement>
>(({ className, ...props }, ref) => (
  <div
    ref={ref}
    className={cn("flex flex-col gap-1 mb-4", className)}
    {...props}
  />
));
CardHeader.displayName = "CardHeader";

/* Title ────────────────────────────────────────────────────── */
const CardTitle = React.forwardRef<
  HTMLHeadingElement,
  React.HTMLAttributes<HTMLHeadingElement>
>(({ className, ...props }, ref) => (
  <h3
    ref={ref}
    className={cn("font-semibold text-ink leading-snug text-base", className)}
    {...props}
  />
));
CardTitle.displayName = "CardTitle";

/* Description ──────────────────────────────────────────────── */
const CardDescription = React.forwardRef<
  HTMLParagraphElement,
  React.HTMLAttributes<HTMLParagraphElement>
>(({ className, ...props }, ref) => (
  <p
    ref={ref}
    className={cn("text-sm text-ink-muted leading-relaxed", className)}
    {...props}
  />
));
CardDescription.displayName = "CardDescription";

/* Content ──────────────────────────────────────────────────── */
const CardContent = React.forwardRef<
  HTMLDivElement,
  React.HTMLAttributes<HTMLDivElement> & { noPadding?: boolean }
>(({ className, noPadding = false, ...props }, ref) => (
  <div ref={ref} className={cn(!noPadding && "", className)} {...props} />
));
CardContent.displayName = "CardContent";

/* Footer ───────────────────────────────────────────────────── */
const CardFooter = React.forwardRef<
  HTMLDivElement,
  React.HTMLAttributes<HTMLDivElement>
>(({ className, ...props }, ref) => (
  <div
    ref={ref}
    className={cn(
      "flex items-center mt-4 pt-4 border-t border-surface-border",
      className
    )}
    {...props}
  />
));
CardFooter.displayName = "CardFooter";

export { Card, CardHeader, CardTitle, CardDescription, CardContent, CardFooter };
