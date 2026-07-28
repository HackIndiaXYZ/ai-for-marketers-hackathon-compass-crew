"use client";

import * as React from "react";
import { cn } from "@/lib/utils";

/* ──────────────────────────────────────────────────────────────
   Input — text field with label, helper text, error state
   ────────────────────────────────────────────────────────────── */

export interface InputProps
  extends React.InputHTMLAttributes<HTMLInputElement> {
  label?: string;
  helperText?: string;
  error?: string;
  leftAdornment?: React.ReactNode;
  rightAdornment?: React.ReactNode;
  /** Full-width layout */
  fullWidth?: boolean;
}

const Input = React.forwardRef<HTMLInputElement, InputProps>(
  (
    {
      className,
      label,
      helperText,
      error,
      leftAdornment,
      rightAdornment,
      fullWidth = false,
      id,
      disabled,
      ...props
    },
    ref
  ) => {
    const generatedId = React.useId();
    const inputId = id ?? generatedId;
    const hasError = Boolean(error);

    return (
      <div className={cn("flex flex-col gap-1.5", fullWidth && "w-full")}>
        {label && (
          <label
            htmlFor={inputId}
            className="text-sm font-medium text-ink leading-none"
          >
            {label}
          </label>
        )}

        <div className="relative flex items-center">
          {leftAdornment && (
            <span className="absolute left-3 flex items-center text-ink-faint pointer-events-none">
              {leftAdornment}
            </span>
          )}

          <input
            ref={ref}
            id={inputId}
            disabled={disabled}
            aria-invalid={hasError}
            aria-describedby={
              hasError
                ? `${inputId}-error`
                : helperText
                ? `${inputId}-helper`
                : undefined
            }
            className={cn(
              // base
              "w-full rounded-lg border bg-surface-card text-ink text-sm placeholder:text-ink-faint",
              "h-10 px-3 py-2",
              "transition-all duration-150",
              // border states
              "border-surface-border",
              "focus:outline-none focus:ring-2 focus:ring-brand-500 focus:border-brand-400 focus:ring-offset-0",
              // error
              hasError && "border-pain-high focus:ring-pain-high",
              // disabled
              "disabled:opacity-50 disabled:cursor-not-allowed disabled:bg-surface-subtle",
              // adornment padding
              leftAdornment && "pl-9",
              rightAdornment && "pr-9",
              className
            )}
            {...props}
          />

          {rightAdornment && (
            <span className="absolute right-3 flex items-center text-ink-faint">
              {rightAdornment}
            </span>
          )}
        </div>

        {hasError && (
          <p
            id={`${inputId}-error`}
            role="alert"
            className="text-xs text-pain-high"
          >
            {error}
          </p>
        )}
        {!hasError && helperText && (
          <p id={`${inputId}-helper`} className="text-xs text-ink-faint">
            {helperText}
          </p>
        )}
      </div>
    );
  }
);

Input.displayName = "Input";

export { Input };
