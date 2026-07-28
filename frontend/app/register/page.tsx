"use client";

import Link from "next/link";
import { useForm } from "react-hook-form";
import { zodResolver } from "@hookform/resolvers/zod";
import { z } from "zod";
import { Sparkles, Mail, Lock, Eye, EyeOff, User, ArrowRight, CheckCircle2 } from "lucide-react";
import { useState } from "react";
import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";
import { Card } from "@/components/ui/card";
import { ThemeToggle } from "@/components/ui/theme-toggle";

const registerSchema = z.object({
  name: z.string().min(2, "Name must be at least 2 characters"),
  email: z.string().min(1, "Email is required").email("Enter a valid email"),
  password: z
    .string()
    .min(8, "Password must be at least 8 characters")
    .regex(/[A-Z]/, "Include at least one uppercase letter")
    .regex(/[0-9]/, "Include at least one number"),
  confirmPassword: z.string().min(1, "Please confirm your password"),
}).refine((d) => d.password === d.confirmPassword, {
  message: "Passwords do not match",
  path: ["confirmPassword"],
});

type RegisterForm = z.infer<typeof registerSchema>;

const PERKS = [
  "Scrape 7 platforms instantly",
  "Unlimited pain point analysis",
  "AI campaign generation",
  "ROI predictions before you spend",
];

export default function RegisterPage() {
  const [showPassword, setShowPassword] = useState(false);
  const [showConfirm, setShowConfirm] = useState(false);
  const [isLoading, setIsLoading] = useState(false);
  const [serverError, setServerError] = useState<string | null>(null);
  const [success, setSuccess] = useState(false);

  const {
    register,
    handleSubmit,
    watch,
    formState: { errors },
  } = useForm<RegisterForm>({
    resolver: zodResolver(registerSchema),
  });

  const passwordValue = watch("password", "");

  const strengthChecks = [
    { label: "8+ characters", pass: passwordValue.length >= 8 },
    { label: "Uppercase letter", pass: /[A-Z]/.test(passwordValue) },
    { label: "Number", pass: /[0-9]/.test(passwordValue) },
  ];
  const strengthScore = strengthChecks.filter((c) => c.pass).length;
  const strengthLabel = ["", "Weak", "Fair", "Strong"][strengthScore];
  const strengthColor = ["", "text-pain-high", "text-pain-medium", "text-pain-low"][strengthScore];
  const strengthBarColor = ["", "bg-pain-high", "bg-pain-medium", "bg-pain-low"][strengthScore];

  const onSubmit = async (data: RegisterForm) => {
    setIsLoading(true);
    setServerError(null);
    // TODO: wire to services/auth.ts when backend is ready
    await new Promise((r) => setTimeout(r, 1400));
    setIsLoading(false);
    setSuccess(true);
  };

  if (success) {
    return (
      <div className="min-h-dvh bg-surface-bg flex flex-col items-center justify-center px-4">
        <Card className="w-full max-w-sm text-center py-10 shadow-card-hover">
          <div className="mx-auto mb-5 h-16 w-16 rounded-2xl bg-pain-low-bg border border-pain-low/30 flex items-center justify-center">
            <CheckCircle2 className="h-8 w-8 text-pain-low" />
          </div>
          <h1 className="text-xl font-bold text-ink mb-2">Account created!</h1>
          <p className="text-sm text-ink-muted mb-6">
            Welcome to PainToAd AI. You&apos;re ready to start turning pain into
            campaigns.
          </p>
          <Link href="/dashboard">
            <Button className="w-full" rightIcon={<ArrowRight className="h-4 w-4" />}>
              Go to Dashboard
            </Button>
          </Link>
        </Card>
      </div>
    );
  }

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

      <div className="flex flex-1 items-center justify-center px-4 py-10">
        <div className="w-full max-w-[780px] grid md:grid-cols-2 gap-8 items-start">

          {/* Left — Perks */}
          <div className="hidden md:flex flex-col gap-6 pt-3">
            <div>
              <div className="h-12 w-12 rounded-2xl bg-brand-500 text-white flex items-center justify-center mb-4 shadow-sm">
                <Sparkles className="h-6 w-6" />
              </div>
              <h1 className="text-2xl font-bold text-ink tracking-tight leading-tight">
                Start turning pain into campaigns today
              </h1>
              <p className="mt-3 text-sm text-ink-muted leading-relaxed">
                Join Compass Crew&apos;s PainToAd AI — the platform that reads
                what your customers actually say, and writes your best ads for you.
              </p>
            </div>

            <ul className="space-y-3">
              {PERKS.map((perk) => (
                <li key={perk} className="flex items-center gap-3 text-sm text-ink-muted">
                  <CheckCircle2 className="h-4 w-4 text-pain-low shrink-0" />
                  {perk}
                </li>
              ))}
            </ul>

            <div className="mt-2 rounded-xl border border-surface-border bg-surface-subtle p-4">
              <p className="text-xs text-ink-faint italic leading-relaxed">
                &ldquo;We finally know exactly which pain points to address in our ads.
                Our CTR went up because we&apos;re speaking our customers&apos; own language.&rdquo;
              </p>
              <p className="mt-2 text-xs font-medium text-ink-muted">
                — Demo User, SaaS Marketing
              </p>
            </div>
          </div>

          {/* Right — Form */}
          <div>
            <div className="text-center md:text-left mb-6">
              <h2 className="text-2xl font-bold text-ink tracking-tight">Create account</h2>
              <p className="mt-1.5 text-sm text-ink-muted">Free forever. No credit card needed.</p>
            </div>

            <Card className="shadow-card-hover">
              <form onSubmit={handleSubmit(onSubmit)} noValidate className="space-y-4">
                {serverError && (
                  <div
                    role="alert"
                    className="rounded-lg border border-pain-high/30 bg-pain-high-bg p-3 text-sm text-pain-high"
                  >
                    {serverError}
                  </div>
                )}

                {/* Name */}
                <Input
                  label="Full name"
                  type="text"
                  autoComplete="name"
                  placeholder="Muskan Yeshminali"
                  fullWidth
                  leftAdornment={<User className="h-4 w-4" />}
                  error={errors.name?.message}
                  {...register("name")}
                />

                {/* Email */}
                <Input
                  label="Work email"
                  type="email"
                  autoComplete="email"
                  placeholder="you@company.com"
                  fullWidth
                  leftAdornment={<Mail className="h-4 w-4" />}
                  error={errors.email?.message}
                  {...register("email")}
                />

                {/* Password */}
                <div className="space-y-1.5">
                  <Input
                    label="Password"
                    type={showPassword ? "text" : "password"}
                    autoComplete="new-password"
                    placeholder="Min. 8 characters"
                    fullWidth
                    leftAdornment={<Lock className="h-4 w-4" />}
                    rightAdornment={
                      <button
                        type="button"
                        onClick={() => setShowPassword((v) => !v)}
                        aria-label={showPassword ? "Hide password" : "Show password"}
                        className="hover:text-ink transition-colors"
                      >
                        {showPassword ? <EyeOff className="h-4 w-4" /> : <Eye className="h-4 w-4" />}
                      </button>
                    }
                    error={errors.password?.message}
                    {...register("password")}
                  />

                  {/* Strength meter */}
                  {passwordValue && (
                    <div className="space-y-1.5">
                      <div className="flex gap-1">
                        {[1, 2, 3].map((n) => (
                          <div
                            key={n}
                            className={`h-1 flex-1 rounded-full transition-all duration-300 ${
                              n <= strengthScore ? strengthBarColor : "bg-surface-border"
                            }`}
                          />
                        ))}
                      </div>
                      <div className="flex items-center justify-between">
                        <span className={`text-xs font-medium ${strengthColor}`}>
                          {strengthLabel}
                        </span>
                        <div className="flex gap-2">
                          {strengthChecks.map((c) => (
                            <span
                              key={c.label}
                              className={`text-[10px] ${c.pass ? "text-pain-low" : "text-ink-faint"}`}
                            >
                              {c.label}
                            </span>
                          ))}
                        </div>
                      </div>
                    </div>
                  )}
                </div>

                {/* Confirm password */}
                <Input
                  label="Confirm password"
                  type={showConfirm ? "text" : "password"}
                  autoComplete="new-password"
                  placeholder="Repeat your password"
                  fullWidth
                  leftAdornment={<Lock className="h-4 w-4" />}
                  rightAdornment={
                    <button
                      type="button"
                      onClick={() => setShowConfirm((v) => !v)}
                      aria-label={showConfirm ? "Hide confirm password" : "Show confirm password"}
                      className="hover:text-ink transition-colors"
                    >
                      {showConfirm ? <EyeOff className="h-4 w-4" /> : <Eye className="h-4 w-4" />}
                    </button>
                  }
                  error={errors.confirmPassword?.message}
                  {...register("confirmPassword")}
                />

                <Button
                  type="submit"
                  variant="primary"
                  size="md"
                  loading={isLoading}
                  className="w-full"
                  rightIcon={!isLoading ? <ArrowRight className="h-4 w-4" /> : undefined}
                >
                  Create Account
                </Button>

                <p className="text-xs text-ink-faint text-center leading-relaxed">
                  By creating an account you agree to our{" "}
                  <button type="button" className="underline hover:text-ink-muted">Terms</button> and{" "}
                  <button type="button" className="underline hover:text-ink-muted">Privacy Policy</button>.
                </p>
              </form>
            </Card>

            <p className="mt-5 text-center text-sm text-ink-muted">
              Already have an account?{" "}
              <Link
                href="/login"
                className="font-medium text-brand-600 dark:text-brand-400 hover:underline"
              >
                Sign in
              </Link>
            </p>
          </div>
        </div>
      </div>
    </div>
  );
}
