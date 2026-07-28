"use client";

import Link from "next/link";
import { usePathname } from "next/navigation";
import { motion, AnimatePresence } from "framer-motion";
import {
  LayoutDashboard,
  Search,
  Users,
  Megaphone,
  Lightbulb,
  TrendingUp,
  Gauge,
  Settings,
  Sparkles,
  X,
  LogOut,
} from "lucide-react";
import { cn } from "@/lib/utils";
import { Button } from "@/components/ui/button";
import { SPRING_SNAPPY } from "@/components/ui/motion";

const NAV_ITEMS = [
  { label: "Dashboard", href: "/dashboard", icon: LayoutDashboard },
  { label: "Analyze Pains", href: "/analyze", icon: Search },
  { label: "Personas", href: "/personas", icon: Users },
  { label: "Campaigns", href: "/campaigns", icon: Megaphone },
  { label: "Insights", href: "/insights", icon: Lightbulb },
  { label: "Optimizer", href: "/optimizer", icon: TrendingUp },
  { label: "Simulator", href: "/simulator", icon: Gauge },
  { label: "Settings", href: "/settings", icon: Settings },
];

interface SidebarProps {
  isOpen?: boolean;
  onClose?: () => void;
}

export function Sidebar({ isOpen, onClose }: SidebarProps) {
  const pathname = usePathname();

  const sidebarContent = (
    <div className="flex h-full w-64 flex-col bg-surface-card border-r border-surface-border transition-colors">
      {/* Header / Logo */}
      <div className="flex h-16 items-center justify-between px-6 border-b border-surface-border">
        <Link href="/dashboard" className="flex items-center gap-2.5 group">
          <div className="flex h-8 w-8 items-center justify-center rounded-lg bg-brand-500 text-white shadow-sm transition-transform group-hover:scale-105">
            <Sparkles className="h-4 w-4" />
          </div>
          <span className="font-semibold text-base tracking-tight text-ink">
            PainToAd<span className="text-brand-500">AI</span>
          </span>
        </Link>
        {onClose && (
          <Button
            variant="ghost"
            size="icon-sm"
            onClick={onClose}
            className="lg:hidden"
            aria-label="Close sidebar"
          >
            <X className="h-4 w-4" />
          </Button>
        )}
      </div>

      {/* Navigation Items */}
      <div className="flex-1 overflow-y-auto px-4 py-6 scrollbar-thin">
        <div className="text-xs font-semibold uppercase tracking-wider text-ink-faint px-3 mb-3">
          Modules
        </div>
        <nav className="space-y-1">
          {NAV_ITEMS.map((item) => {
            const Icon = item.icon;
            const isActive = pathname === item.href || pathname?.startsWith(`${item.href}/`);

            return (
              <Link
                key={item.href}
                href={item.href}
                onClick={onClose}
                className={cn(
                  "flex items-center gap-3 px-3 py-2.5 rounded-lg text-sm font-medium transition-all duration-150 group relative z-10",
                  isActive
                    ? "text-brand-600 dark:text-brand-400 font-semibold"
                    : "text-ink-muted hover:bg-surface-subtle hover:text-ink"
                )}
              >
                {isActive && (
                  <motion.div
                    layoutId="activeNavBg"
                    className="absolute inset-0 rounded-lg bg-brand-50 dark:bg-brand-100/10 z-0"
                    transition={SPRING_SNAPPY}
                  />
                )}
                <Icon
                  className={cn(
                    "h-4 w-4 shrink-0 transition-colors z-10",
                    isActive
                      ? "text-brand-500 dark:text-brand-400"
                      : "text-ink-faint group-hover:text-ink"
                  )}
                />
                <span className="flex-1 z-10">{item.label}</span>
                {isActive && (
                  <motion.div
                    layoutId="activeNavDot"
                    className="h-1.5 w-1.5 rounded-full bg-brand-500 dark:bg-brand-400 z-10"
                    transition={SPRING_SNAPPY}
                  />
                )}
              </Link>
            );
          })}
        </nav>
      </div>

      {/* Footer / User Profile & Team Info */}
      <div className="p-4 border-t border-surface-border bg-surface-subtle/50">
        <div className="flex items-center justify-between">
          <div className="flex items-center gap-2.5 min-w-0">
            <div className="h-8 w-8 rounded-full bg-brand-200 text-brand-700 dark:bg-brand-600/30 dark:text-brand-300 font-semibold text-xs flex items-center justify-center shrink-0">
              CC
            </div>
            <div className="min-w-0">
              <p className="text-xs font-medium text-ink truncate">Compass Crew</p>
              <p className="text-[11px] text-ink-faint truncate">Muskan (UI/UX)</p>
            </div>
          </div>
          <Link href="/">
            <Button variant="ghost" size="icon-sm" title="Log out">
              <LogOut className="h-3.5 w-3.5 text-ink-faint" />
            </Button>
          </Link>
        </div>
      </div>
    </div>
  );

  return (
    <>
      {/* Desktop Sidebar */}
      <aside className="hidden lg:block fixed inset-y-0 left-0 z-30">
        {sidebarContent}
      </aside>

      {/* Mobile Drawer */}
      <AnimatePresence>
        {isOpen && (
          <div className="fixed inset-0 z-50 lg:hidden">
            <motion.div
              initial={{ opacity: 0 }}
              animate={{ opacity: 1 }}
              exit={{ opacity: 0 }}
              transition={{ duration: 0.2 }}
              className="fixed inset-0 bg-ink/40 backdrop-blur-sm"
              onClick={onClose}
            />
            <motion.div
              initial={{ x: "-100%" }}
              animate={{ x: 0 }}
              exit={{ x: "-100%" }}
              transition={SPRING_SNAPPY}
              className="fixed inset-y-0 left-0 z-50 w-64"
            >
              {sidebarContent}
            </motion.div>
          </div>
        )}
      </AnimatePresence>
    </>
  );
}
