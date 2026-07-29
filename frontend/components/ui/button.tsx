"use client";

import * as React from "react";
import { cva, type VariantProps } from "class-variance-authority";
import { motion, type HTMLMotionProps } from "framer-motion";
import { cn } from "@/lib/utils";
import { SPRING_SNAPPY } from "./motion";

/* ──────────────────────────────────────────────────────────────
   Button variant system — uses brand / surface tokens
   ────────────────────────────────────────────────────────────── */
const buttonVariants = cva(
  // base
  [
    "inline-flex items-center justify-center gap-2 whitespace-nowrap",
    "font-medium rounded-lg text-sm leading-none",
    "button-motion",
    "focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-brand-500 focus-visible:ring-offset-2 focus-visible:ring-offset-surface-bg",
    "disabled:pointer-events-none disabled:opacity-40",
    "select-none cursor-pointer",
  ],
  {
    variants: {
      variant: {
        // Primary — filled brand
        primary: [
          "bg-brand-500 text-white",
          "hover:bg-brand-600 active:bg-brand-700",
          "shadow-sm hover:shadow-md",
        ],
        // Secondary — outlined brand
        secondary: [
          "border border-brand-300 text-brand-600 bg-brand-50",
          "hover:bg-brand-100 hover:border-brand-400 active:bg-brand-200",
          "dark:border-brand-600 dark:text-brand-400 dark:bg-brand-100/10",
          "dark:hover:bg-brand-100/20",
        ],
        // Ghost — transparent, minimal
        ghost: [
          "text-ink-muted bg-transparent",
          "hover:bg-surface-subtle hover:text-ink",
          "active:bg-surface-border",
        ],
        // Destructive
        destructive: [
          "bg-pain-high text-white",
          "hover:opacity-90 active:opacity-80",
          "shadow-sm",
        ],
        // Outline — neutral border
        outline: [
          "border border-surface-border text-ink bg-surface-card",
          "hover:bg-surface-subtle active:bg-surface-border",
        ],
        // Link-style
        link: [
          "text-brand-600 underline-offset-4 hover:underline",
          "dark:text-brand-400",
          "p-0 h-auto",
        ],
      },
      size: {
        xs:  "h-7 px-2.5 text-xs rounded-md",
        sm:  "h-8 px-3 text-sm",
        md:  "h-10 px-4 text-sm",
        lg:  "h-11 px-6 text-base",
        xl:  "h-13 px-8 text-base",
        icon: "h-10 w-10 p-0",
        "icon-sm": "h-8 w-8 p-0 rounded-md",
      },
    },
    defaultVariants: {
      variant: "primary",
      size: "md",
    },
  }
);

export interface ButtonProps
  extends Omit<HTMLMotionProps<"button">, "size" | "children">,
    VariantProps<typeof buttonVariants> {
  children?: React.ReactNode;
  /** Show a loading spinner and disable the button */
  loading?: boolean;
  /** Icon rendered before the label */
  leftIcon?: React.ReactNode;
  /** Icon rendered after the label */
  rightIcon?: React.ReactNode;
}

const Button = React.forwardRef<HTMLButtonElement, ButtonProps>(
  (
    {
      className,
      variant,
      size,
      loading = false,
      leftIcon,
      rightIcon,
      disabled,
      children,
      whileHover,
      whileTap,
      ...props
    },
    ref
  ) => {
    const isDisabled = disabled || loading;

    return (
      <motion.button
        ref={ref}
        className={cn(buttonVariants({ variant, size }), className)}
        disabled={isDisabled}
        aria-busy={loading}
        whileHover={isDisabled ? undefined : whileHover ?? { scale: variant === "link" ? 1 : 1.05, y: variant === "link" ? 0 : -2 }}
        whileTap={isDisabled ? undefined : whileTap ?? { scale: variant === "link" ? 1 : 0.95 }}
        transition={SPRING_SNAPPY}
        {...props}
      >
        {loading ? (
          <svg
            className="h-4 w-4 animate-spin"
            xmlns="http://www.w3.org/2000/svg"
            fill="none"
            viewBox="0 0 24 24"
            aria-hidden="true"
          >
            <circle
              className="opacity-25"
              cx="12" cy="12" r="10"
              stroke="currentColor" strokeWidth="4"
            />
            <path
              className="opacity-75"
              fill="currentColor"
              d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4z"
            />
          </svg>
        ) : leftIcon ? (
          <span className="shrink-0">{leftIcon}</span>
        ) : null}

        {children}

        {!loading && rightIcon && (
          <span className="shrink-0">{rightIcon}</span>
        )}
      </motion.button>
    );
  }
);

Button.displayName = "Button";

export { Button, buttonVariants };
