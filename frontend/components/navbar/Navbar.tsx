"use client";

import Link from "next/link";
import { usePathname } from "next/navigation";
import { Sparkles, Menu, LogOut } from "lucide-react";
import { ThemeToggle } from "@/components/ui/theme-toggle";
import { Button } from "@/components/ui/button";

export function Navbar({ onMobileMenuToggle }: { onMobileMenuToggle?: () => void }) {
  const pathname = usePathname();
  const isLandingPage = pathname === "/";

  return (
    <header className="sticky top-0 z-40 w-full border-b border-surface-border bg-surface-card/80 backdrop-blur-md transition-colors">
      <div className="mx-auto flex h-16 max-w-7xl items-center justify-between px-4 sm:px-6 lg:px-8">
        {/* Brand / Logo */}
        <div className="flex items-center gap-3">
          {onMobileMenuToggle && (
            <Button
              variant="ghost"
              size="icon-sm"
              onClick={onMobileMenuToggle}
              className="lg:hidden"
              aria-label="Toggle mobile menu"
            >
              <Menu className="h-5 w-5" />
            </Button>
          )}
          {isLandingPage && (
            <Link href="/" className="flex items-center gap-2.5 group">
              <div className="flex h-9 w-9 items-center justify-center rounded-xl bg-brand-500 text-white shadow-sm transition-transform group-hover:scale-105">
                <Sparkles className="h-5 w-5" />
              </div>
              <span className="font-semibold text-lg tracking-tight text-ink">
                PainToAd<span className="text-brand-500 ml-0.5">AI</span>
              </span>
            </Link>
          )}
        </div>

        {/* Center Nav Links (Visible on Landing Page) */}
        {isLandingPage && (
          <nav className="hidden md:flex items-center gap-8 text-sm font-medium text-ink-muted">
            <a href="#how-it-works" className="transition-colors hover:text-ink">
              How it Works
            </a>
            <a href="#features" className="transition-colors hover:text-ink">
              Features
            </a>
            <a href="#use-cases" className="transition-colors hover:text-ink">
              Use Cases
            </a>
          </nav>
        )}

        {/* Right Action Items */}
        <div className="flex items-center gap-3">
          <ThemeToggle />
          {isLandingPage ? (
            <Link href="/login">
              <Button variant="primary" size="sm">
                Sign In
              </Button>
            </Link>
          ) : (
            <Link href="/">
              <Button
                variant="outline"
                size="sm"
                leftIcon={<LogOut className="h-4 w-4" />}
                className="text-ink-muted hover:text-ink hover:border-brand-300 transition-colors"
              >
                Log Out
              </Button>
            </Link>
          )}
        </div>
      </div>
    </header>
  );
}
