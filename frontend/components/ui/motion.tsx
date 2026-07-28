"use client";

import React from "react";
import { motion, type HTMLMotionProps } from "framer-motion";

/* ──────────────────────────────────────────────────────────────
   SHARED TRANSITION CONSTANTS & EASINGS
   ────────────────────────────────────────────────────────────── */
export const EASE_SMOOTH = [0.22, 1, 0.36, 1] as const;
export const SPRING_SNAPPY = { type: "spring", stiffness: 450, damping: 25 } as const;
export const SPRING_BOUNCY = { type: "spring", stiffness: 350, damping: 18 } as const;

/* ──────────────────────────────────────────────────────────────
   1. FadeInUp — Visible fade in + translate up on mount / scroll
   ────────────────────────────────────────────────────────────── */
export interface FadeInUpProps extends HTMLMotionProps<"div"> {
  children: React.ReactNode;
  delay?: number;
  duration?: number;
  yOffset?: number;
  once?: boolean;
}

export function FadeInUp({
  children,
  delay = 0,
  duration = 0.45,
  yOffset = 24,
  once = true,
  className,
  ...props
}: FadeInUpProps) {
  return (
    <motion.div
      initial={{ opacity: 0, y: yOffset }}
      whileInView={{ opacity: 1, y: 0 }}
      viewport={{ once, amount: 0.15 }}
      transition={{
        duration,
        delay,
        ease: EASE_SMOOTH,
      }}
      className={className}
      {...props}
    >
      {children}
    </motion.div>
  );
}

/* ──────────────────────────────────────────────────────────────
   2. StaggerContainer + StaggerItem — Cascading card lists
   ────────────────────────────────────────────────────────────── */
export interface StaggerContainerProps extends HTMLMotionProps<"div"> {
  children: React.ReactNode;
  staggerDelay?: number;
  delayChildren?: number;
  once?: boolean;
}

export function StaggerContainer({
  children,
  staggerDelay = 0.09,
  delayChildren = 0.05,
  once = true,
  className,
  ...props
}: StaggerContainerProps) {
  return (
    <motion.div
      initial="hidden"
      whileInView="visible"
      viewport={{ once, amount: 0.1 }}
      variants={{
        hidden: {},
        visible: {
          transition: {
            staggerChildren: staggerDelay,
            delayChildren,
          },
        },
      }}
      className={className}
      {...props}
    >
      {children}
    </motion.div>
  );
}

export interface StaggerItemProps extends HTMLMotionProps<"div"> {
  children: React.ReactNode;
  yOffset?: number;
}

export function StaggerItem({
  children,
  yOffset = 24,
  className,
  ...props
}: StaggerItemProps) {
  return (
    <motion.div
      variants={{
        hidden: { opacity: 0, y: yOffset, scale: 0.97 },
        visible: {
          opacity: 1,
          y: 0,
          scale: 1,
          transition: {
            duration: 0.45,
            ease: EASE_SMOOTH,
          },
        },
      }}
      className={className}
      {...props}
    >
      {children}
    </motion.div>
  );
}

/* ──────────────────────────────────────────────────────────────
   3. HoverLift — Expressive card hover & tactile tap physics
   ────────────────────────────────────────────────────────────── */
export interface HoverLiftProps extends HTMLMotionProps<"div"> {
  children: React.ReactNode;
  liftPx?: number;
  scale?: number;
}

export function HoverLift({
  children,
  liftPx = -6,
  scale = 1.025,
  className,
  ...props
}: HoverLiftProps) {
  return (
    <motion.div
      whileHover={{ y: liftPx, scale }}
      whileTap={{ scale: 0.96 }}
      transition={SPRING_SNAPPY}
      className={className}
      {...props}
    >
      {children}
    </motion.div>
  );
}

/* ──────────────────────────────────────────────────────────────
   4. PageTransition — Smooth & visible route change transition
   ────────────────────────────────────────────────────────────── */
export interface PageTransitionProps extends HTMLMotionProps<"div"> {
  children: React.ReactNode;
}

export function PageTransition({
  children,
  className,
  ...props
}: PageTransitionProps) {
  return (
    <motion.div
      initial={{ opacity: 0, y: 16 }}
      animate={{ opacity: 1, y: 0 }}
      exit={{ opacity: 0, y: -16 }}
      transition={{
        duration: 0.35,
        ease: EASE_SMOOTH,
      }}
      className={className}
      {...props}
    >
      {children}
    </motion.div>
  );
}
