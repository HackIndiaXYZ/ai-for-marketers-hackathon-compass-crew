"use client";

import * as React from "react";
import { X } from "lucide-react";
import { motion, AnimatePresence } from "framer-motion";
import { cn } from "@/lib/utils";
import { Button } from "./button";
import { SPRING_SNAPPY } from "./motion";

/* ──────────────────────────────────────────────────────────────
   Modal — accessible dialog using Framer Motion AnimatePresence
   ────────────────────────────────────────────────────────────── */

export interface ModalProps {
  open: boolean;
  onClose: () => void;
  title?: string;
  description?: string;
  /** Max width variant */
  size?: "sm" | "md" | "lg" | "xl" | "full";
  children: React.ReactNode;
  /** Render custom footer instead of default close */
  footer?: React.ReactNode;
  className?: string;
}

const sizeClasses = {
  sm:   "max-w-sm",
  md:   "max-w-md",
  lg:   "max-w-lg",
  xl:   "max-w-2xl",
  full: "max-w-[95vw] max-h-[95vh]",
};

export function Modal({
  open,
  onClose,
  title,
  description,
  size = "md",
  children,
  footer,
  className,
}: ModalProps) {
  // Close on Escape
  React.useEffect(() => {
    const handleKey = (e: KeyboardEvent) => {
      if (e.key === "Escape" && open) onClose();
    };
    document.addEventListener("keydown", handleKey);
    return () => document.removeEventListener("keydown", handleKey);
  }, [open, onClose]);

  // Lock body scroll while open
  React.useEffect(() => {
    if (open) {
      document.body.style.overflow = "hidden";
    } else {
      document.body.style.overflow = "";
    }
    return () => { document.body.style.overflow = ""; };
  }, [open]);

  return (
    <AnimatePresence>
      {open && (
        <div className="fixed inset-0 z-50 flex items-center justify-center p-4">
          {/* Backdrop */}
          <motion.div
            initial={{ opacity: 0 }}
            animate={{ opacity: 1 }}
            exit={{ opacity: 0 }}
            transition={{ duration: 0.2 }}
            className="absolute inset-0 bg-ink/40 backdrop-blur-sm"
            onClick={onClose}
            aria-hidden="true"
          />

          {/* Panel */}
          <motion.div
            role="dialog"
            aria-modal="true"
            aria-labelledby={title ? "modal-title" : undefined}
            aria-describedby={description ? "modal-desc" : undefined}
            initial={{ opacity: 0, scale: 0.95, y: 10 }}
            animate={{ opacity: 1, scale: 1, y: 0 }}
            exit={{ opacity: 0, scale: 0.95, y: 10 }}
            transition={SPRING_SNAPPY}
            className={cn(
              "relative z-10 w-full",
              "bg-surface-card rounded-xl shadow-card-hover border border-surface-border",
              "flex flex-col overflow-hidden",
              sizeClasses[size],
              className
            )}
          >
            {/* Header */}
            {(title || description) && (
              <div className="flex items-start justify-between gap-4 p-5 border-b border-surface-border">
                <div className="flex-1 min-w-0">
                  {title && (
                    <h2
                      id="modal-title"
                      className="text-base font-semibold text-ink leading-snug"
                    >
                      {title}
                    </h2>
                  )}
                  {description && (
                    <p id="modal-desc" className="text-sm text-ink-muted mt-0.5">
                      {description}
                    </p>
                  )}
                </div>
                <Button
                  variant="ghost"
                  size="icon-sm"
                  onClick={onClose}
                  aria-label="Close modal"
                  className="shrink-0 -mr-1 -mt-1"
                >
                  <X className="h-4 w-4" />
                </Button>
              </div>
            )}

            {/* Body */}
            <div className="flex-1 overflow-y-auto p-5 scrollbar-thin">
              {children}
            </div>

            {/* Footer */}
            {footer && (
              <div className="flex items-center justify-end gap-2 p-4 border-t border-surface-border bg-surface-subtle">
                {footer}
              </div>
            )}
          </motion.div>
        </div>
      )}
    </AnimatePresence>
  );
}
