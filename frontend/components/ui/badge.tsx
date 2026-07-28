import * as React from "react";
import { cva, type VariantProps } from "class-variance-authority";
import { cn } from "@/lib/utils";

const badgeVariants = cva(
  "inline-flex items-center gap-1 rounded-full text-xs font-medium px-2 py-0.5 border leading-none whitespace-nowrap",
  {
    variants: {
      variant: {
        default:    "bg-surface-subtle text-ink border-surface-border",
        brand:      "bg-brand-100 text-brand-600 border-brand-200 dark:bg-brand-100/15 dark:text-brand-400 dark:border-brand-600/40",
        high:       "badge-high",
        medium:     "badge-medium",
        low:        "badge-low",
        outline:    "bg-transparent text-ink border-surface-border",
      },
    },
    defaultVariants: { variant: "default" },
  }
);

export interface BadgeProps
  extends React.HTMLAttributes<HTMLSpanElement>,
    VariantProps<typeof badgeVariants> {}

function Badge({ className, variant, ...props }: BadgeProps) {
  return (
    <span className={cn(badgeVariants({ variant }), className)} {...props} />
  );
}

export { Badge, badgeVariants };
