"use client";

import Link from "next/link";
import { useRouter } from "next/navigation";
import { useForm } from "react-hook-form";
import { zodResolver } from "@hookform/resolvers/zod";
import { z } from "zod";
import { Sparkles, Mail, Lock, Eye, EyeOff, ArrowRight, Zap } from "lucide-react";
import { useState } from "react";
import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";
import { Card } from "@/components/ui/card";
import { ThemeToggle } from "@/components/ui/theme-toggle";

const loginSchema = z.object({
  email: z.string().min(1, "Email is required").email("Enter a valid email"),
  password: z.string().min(6, "Password must be at least 6 characters"),
});

type LoginForm = z.infer<typeof loginSchema>;

export default function LoginPage() {
  const router = useRouter();
  const [showPassword, setShowPassword] = useState(false);
  const [isLoading, setIsLoading] = useState(false);

  const {
    register,
    handleSubmit,
    formState: { errors },
  } = useForm<LoginForm>({
    resolver: zodResolver(loginSchema),
    defaultValues: {
      email: "muskan@compasscrew.ai",
      password: "demoPassword123",
    },
  });

  const handleDemoLogin = async () => {
    setIsLoading(true);
    await new Promise((r) => setTimeout(r, 600));
    router.push("/dashboard");
  };

  const onSubmit = async (_data: LoginForm) => {
    setIsLoading(true);
    await new Promise((r) => setTimeout(r, 600));
    router.push("/dashboard");
  };

  return (
    <div className="min-h-dvh bg-surface-bg flex flex-col">
      {/* Top bar */}
      <div className="flex items-center justify-between px-6 py-4">
        <Link href="/" className="flex items-center gap-2 group">
          <div className="flex h-8 w-8 items-center justify-center rounded-lg bg-brand-500 text-white shadow-sm transition-transform group-hover:scale-105">
            <Sparkles className="h-4 w-4" />
          </div>
          <span className="font-semibold text-base tracking-tight text-ink">
            PainToAd<span className="text-brand-500">AI</span>
          </span>
        </Link>
        <ThemeToggle />
      </div>

      {/* Centered card */}
      <div className="flex flex-1 items-center justify-center px-4 py-10">
        <div className="w-full max-w-sm">
          {/* Header */}
          <div className="text-center mb-6">
            <h1 className="text-2xl font-bold text-ink tracking-tight">
              Welcome back
            </h1>
            <p className="mt-2 text-sm text-ink-muted">
              Sign in to explore PainToAd AI features
            </p>
          </div>

          <Card className="shadow-card-hover space-y-4">
            {/* Quick Demo Login Banner */}
            <div className="rounded-xl border border-brand-200 dark:border-brand-600/30 bg-brand-50 dark:bg-brand-100/10 p-3.5 text-center">
              <p className="text-xs font-semibold text-brand-700 dark:text-brand-300">
                🚀 Hackathon Demo Mode
              </p>
              <p className="text-[11px] text-ink-muted mt-0.5 mb-2.5">
                Explore all platform features with demo access
              </p>
              <Button
                type="button"
                variant="primary"
                size="sm"
                className="w-full"
                loading={isLoading}
                onClick={handleDemoLogin}
                leftIcon={!isLoading ? <Zap className="h-3.5 w-3.5" /> : undefined}
              >
                One-Click Demo Access
              </Button>
            </div>

            <div className="flex items-center gap-3">
              <div className="flex-1 h-px bg-surface-border" />
              <span className="text-xs text-ink-faint">or sign in with email</span>
              <div className="flex-1 h-px bg-surface-border" />
            </div>

            <form onSubmit={handleSubmit(onSubmit)} noValidate className="space-y-4">
              {/* Email */}
              <Input
                label="Email address"
                type="email"
                autoComplete="email"
                placeholder="muskan@compasscrew.ai"
                fullWidth
                leftAdornment={<Mail className="h-4 w-4" />}
                error={errors.email?.message}
                {...register("email")}
              />

              {/* Password */}
              <Input
                label="Password"
                type={showPassword ? "text" : "password"}
                autoComplete="current-password"
                placeholder="••••••••"
                fullWidth
                leftAdornment={<Lock className="h-4 w-4" />}
                rightAdornment={
                  <button
                    type="button"
                    onClick={() => setShowPassword((v) => !v)}
                    aria-label={showPassword ? "Hide password" : "Show password"}
                    className="hover:text-ink transition-colors"
                  >
                    {showPassword ? (
                      <EyeOff className="h-4 w-4" />
                    ) : (
                      <Eye className="h-4 w-4" />
                    )}
                  </button>
                }
                error={errors.password?.message}
                {...register("password")}
              />

              {/* Forgot password */}
              <div className="text-right">
                <button
                  type="button"
                  className="text-xs text-brand-600 dark:text-brand-400 hover:underline"
                >
                  Forgot password?
                </button>
              </div>

              {/* Submit */}
              <Button
                type="submit"
                variant="primary"
                size="md"
                loading={isLoading}
                className="w-full"
                rightIcon={!isLoading ? <ArrowRight className="h-4 w-4" /> : undefined}
              >
                Sign In
              </Button>
            </form>

            {/* Divider */}
            <div className="my-5 flex items-center gap-3">
              <div className="flex-1 h-px bg-surface-border" />
              <span className="text-xs text-ink-faint">or continue with</span>
              <div className="flex-1 h-px bg-surface-border" />
            </div>

            {/* Social auth */}
            <Button
              variant="outline"
              size="md"
              className="w-full"
              type="button"
              onClick={handleDemoLogin}
              leftIcon={
                <svg className="h-4 w-4" viewBox="0 0 24 24" aria-hidden="true">
                  <path
                    d="M22.56 12.25c0-.78-.07-1.53-.2-2.25H12v4.26h5.92c-.26 1.37-1.04 2.53-2.21 3.31v2.77h3.57c2.08-1.92 3.28-4.74 3.28-8.09z"
                    fill="#4285F4"
                  />
                  <path
                    d="M12 23c2.97 0 5.46-.98 7.28-2.66l-3.57-2.77c-.98.66-2.23 1.06-3.71 1.06-2.86 0-5.29-1.93-6.16-4.53H2.18v2.84C3.99 20.53 7.7 23 12 23z"
                    fill="#34A853"
                  />
                  <path
                    d="M5.84 14.09c-.22-.66-.35-1.36-.35-2.09s.13-1.43.35-2.09V7.07H2.18C1.43 8.55 1 10.22 1 12s.43 3.45 1.18 4.93l2.85-2.22.81-.62z"
                    fill="#FBBC05"
                  />
                  <path
                    d="M12 5.38c1.62 0 3.06.56 4.21 1.64l3.15-3.15C17.45 2.09 14.97 1 12 1 7.7 1 3.99 3.47 2.18 7.07l3.66 2.84c.87-2.6 3.3-4.53 6.16-4.53z"
                    fill="#EA4335"
                  />
                </svg>
              }
            >
              Continue with Google
            </Button>
          </Card>

          {/* Register link */}
          <p className="mt-6 text-center text-sm text-ink-muted">
            Don&apos;t have an account?{" "}
            <Link
              href="/register"
              className="font-medium text-brand-600 dark:text-brand-400 hover:underline"
            >
              Create one free
            </Link>
          </p>
        </div>
      </div>
    </div>
  );
}
