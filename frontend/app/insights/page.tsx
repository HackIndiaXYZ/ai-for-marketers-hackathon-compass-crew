"use client";

import {
  Lightbulb,
  Sparkles,
  TrendingUp,
  Users,
  Target,
  Globe2,
  BarChart2,
  RefreshCw,
  ChevronDown,
  BookOpen,
  Zap,
  ArrowRight,
  Copy,
  Download,
  Share2,
  Check,
} from "lucide-react";
import Link from "next/link";
import { Sidebar } from "@/components/sidebar/Sidebar";
import { Navbar } from "@/components/navbar/Navbar";
import { Button } from "@/components/ui/button";
import { Badge } from "@/components/ui/badge";
import { Card } from "@/components/ui/card";
import { Modal } from "@/components/ui/modal";
import { StaggerContainer, StaggerItem } from "@/components/ui/motion";
import { cn } from "@/lib/utils";

/* ── Types ─────────────────────────────────────────────────── */
type InsightCategory = "Market Trends" | "Customer Behavior" | "Competitor Gap" | "Channel Strategy" | "Pricing Intelligence";

interface InsightBrief {
  id: string;
  category: InsightCategory;
  title: string;
  summary: string;
  keyFindings: string[];
  recommendations: string[];
  stat: { value: string; label: string };
  date: string;
  readTime: string;
}

const CATEGORIES: ("All" | InsightCategory)[] = [
  "All",
  "Market Trends",
  "Customer Behavior",
  "Competitor Gap",
  "Channel Strategy",
  "Pricing Intelligence",
];

const categoryConfig: Record<InsightCategory, { icon: typeof Lightbulb; color: string }> = {
  "Market Trends":        { icon: TrendingUp,  color: "text-brand-500 bg-brand-50 border-brand-200 dark:bg-brand-100/10 dark:border-brand-600/30" },
  "Customer Behavior":   { icon: Users,       color: "text-pain-medium bg-pain-medium-bg border-pain-medium/20" },
  "Competitor Gap":      { icon: Target,      color: "text-pain-high bg-pain-high-bg border-pain-high/20" },
  "Channel Strategy":    { icon: Globe2,      color: "text-pain-low bg-pain-low-bg border-pain-low/20" },
  "Pricing Intelligence": { icon: BarChart2,   color: "text-brand-600 bg-brand-50 border-brand-200 dark:bg-brand-100/10 dark:border-brand-600/30" },
};

type CategoryFilter = typeof CATEGORIES[number];

const BRIEFS: InsightBrief[] = [
  {
    id: "b1",
    category: "Customer Behavior",
    title: "Onboarding Friction Is the #1 Driver of Early Churn in SaaS",
    summary:
      "Across 247 Reddit & Quora discussions, buyers report abandoning SaaS products within 48 hours when onboarding requires manual config without interactive guidance.",
    keyFindings: [
      "68% of complaints mention lack of clear 'next steps' right after signup",
      "Users expect a working result within 5 minutes of first login",
      "Support tickets spike by 3x for products lacking self-serve walkthroughs",
    ],
    recommendations: [
      "Run ads highlighting 'Instant 2-minute setup' instead of feature laundry lists",
      "Create WhatsApp onboarding nudges for users who drop off after signup",
      "Highlight 24/7 live chat support as a primary USP in ad copy",
    ],
    stat: { value: "68%", label: "churn caused by onboarding friction" },
    date: "Today",
    readTime: "2 min read",
  },
  {
    id: "b2",
    category: "Pricing Intelligence",
    title: "Hidden Fees Create Severe Trust Deficits in Tier-2 Indian Cities",
    summary:
      "Scraped MouthShut & Google Reviews show buyers in Tier-2/3 cities reject SaaS & edtech subscriptions when final invoice pricing differs from advertised pricing.",
    keyFindings: [
      "GST & processing fee surprises cause 42% cart abandonment at checkout",
      "Buyers actively search for 'all-inclusive pricing' reviews before purchasing",
      "Regional language reviews express 2x higher frustration with billing opacity",
    ],
    recommendations: [
      "State 'GST included · No hidden charges' explicitly in all ad creatives",
      "Use Hinglish ad variants for Facebook & Instagram targeting Tier-2 demographics",
      "Offer transparent monthly pricing breakdowns on checkout landing pages",
    ],
    stat: { value: "42%", label: "cart drop-off from unexpected tax/fees" },
    date: "Yesterday",
    readTime: "3 min read",
  },
  {
    id: "b3",
    category: "Competitor Gap",
    title: "Support Delay Complaints Surging Across Legacy Competitors",
    summary:
      "Twitter/X & Google Reviews analysis reveals major incumbents averaging 3-5 day support response times, opening a prime positioning window.",
    keyFindings: [
      "189 mentions of 'unresponsive support' targeting top 3 category leaders",
      "Buyers willing to pay 15-20% premium for guaranteed < 1 hour support SLAs",
      "Negative support reviews receive 4x more helpful votes on review sites",
    ],
    recommendations: [
      "Position your product with 'Human support in under 15 minutes' as main headline",
      "Target competitor brand keywords on Google Search with support SLA copy",
      "Deploy comparison landing pages focusing on support response speed",
    ],
    stat: { value: "3-5 days", label: "avg. competitor support delay" },
    date: "2 days ago",
    readTime: "2 min read",
  },
  {
    id: "b4",
    category: "Channel Strategy",
    title: "WhatsApp Outperforms Email 4:1 for High-Intent Lead Conversion in India",
    summary:
      "Conversion tracking across 24 campaigns indicates WhatsApp messaging yields 4x higher open rates and 2.8x higher CTR compared to traditional email sequences.",
    keyFindings: [
      "WhatsApp messages achieve 88% open rate within 1 hour of delivery",
      "Voice note previews & short video clips increase click rates by 35%",
      "Users prefer WhatsApp for quick Q&A before booking a demo",
    ],
    recommendations: [
      "Make WhatsApp the primary CTA on mobile Google Search & Facebook ads",
      "Automate instant WhatsApp welcome messages containing pain-point solutions",
      "Include interactive button options (Book Demo / View Pricing) in WhatsApp flows",
    ],
    stat: { value: "88%", label: "WhatsApp open rate within 1 hour" },
    date: "3 days ago",
    readTime: "3 min read",
  },
];

function BriefCard({ brief }: { brief: InsightBrief }) {
  const [modalOpen, setModalOpen] = useState(false);
  const [copied, setCopied] = useState(false);
  const [shared, setShared] = useState(false);

  const cfg = categoryConfig[brief.category];
  const Icon = cfg.icon;

  const getBriefText = () => {
    return `# ${brief.title}\nCategory: ${brief.category} | ${brief.date}\n\n## Summary\n${brief.summary}\n\n## Key Findings\n${brief.keyFindings.map((f) => `- ${f}`).join("\n")}\n\n## Recommendations\n${brief.recommendations.map((r) => `- ${r}`).join("\n")}\n\nStat: ${brief.stat.value} ${brief.stat.label}`;
  };

  const handleCopy = () => {
    navigator.clipboard.writeText(getBriefText());
    setCopied(true);
    setTimeout(() => setCopied(false), 2000);
  };

  const handleShare = () => {
    navigator.clipboard.writeText(`https://paintoad.ai/insights#${brief.id}`);
    setShared(true);
    setTimeout(() => setShared(false), 2000);
  };

  const handleExport = () => {
    const element = document.createElement("a");
    const file = new Blob([getBriefText()], { type: "text/markdown" });
    element.href = URL.createObjectURL(file);
    element.download = `${brief.id}-${brief.title.toLowerCase().replace(/[^a-z0-9]/g, "-")}.md`;
    document.body.appendChild(element);
    element.click();
    document.body.removeChild(element);
  };

  return (
    <>
      <Card className="flex flex-col justify-between hover:shadow-card-hover transition-all">
        <div className="p-5">
          {/* Header tags */}
          <div className="flex items-center justify-between gap-2 mb-3">
            <div className="flex items-center gap-2">
              <span className={cn("inline-flex items-center gap-1.5 rounded-lg px-2.5 py-1 text-xs font-semibold border", cfg.color)}>
                <Icon className="h-3.5 w-3.5" />
                {brief.category}
              </span>
            </div>
            <div className="flex items-center gap-2 text-xs text-ink-faint">
              <span>{brief.readTime}</span>
              <span>·</span>
              <span>{brief.date}</span>
            </div>
          </div>

          {/* Title & Summary */}
          <h3 className="font-bold text-ink text-base leading-snug">{brief.title}</h3>
          <p className="text-sm text-ink-muted mt-2 leading-relaxed">{brief.summary}</p>

          {/* Key stat */}
          <div className={cn("mt-4 rounded-xl p-3 border flex items-center gap-3", cfg.color)}>
            <Zap className="h-5 w-5 shrink-0" />
            <div>
              <span className="text-2xl font-black leading-none">{brief.stat.value}</span>
              <span className="text-xs ml-2 leading-snug">{brief.stat.label}</span>
            </div>
          </div>
        </div>

        {/* Footer actions */}
        <div className="px-5 py-3.5 flex items-center justify-between border-t border-surface-border bg-surface-subtle/50">
          <Button
            variant="ghost"
            size="xs"
            onClick={() => setModalOpen(true)}
            leftIcon={<BookOpen className="h-3.5 w-3.5" />}
            className="text-brand-600 dark:text-brand-400 font-semibold"
          >
            Read Full Brief
          </Button>
          <div className="flex items-center gap-1">
            <Button variant="ghost" size="icon-sm" onClick={handleCopy} title="Copy Brief">
              {copied ? <Check className="h-3.5 w-3.5 text-pain-low" /> : <Copy className="h-3.5 w-3.5 text-ink-muted" />}
            </Button>
            <Button variant="ghost" size="icon-sm" onClick={handleExport} title="Export Markdown">
              <Download className="h-3.5 w-3.5 text-ink-muted" />
            </Button>
            <Button variant="ghost" size="icon-sm" onClick={handleShare} title="Share Brief Link">
              {shared ? <Check className="h-3.5 w-3.5 text-pain-low" /> : <Share2 className="h-3.5 w-3.5 text-ink-muted" />}
            </Button>
          </div>
        </div>
      </Card>

      {/* Modal Dialog for Full Brief */}
      <Modal
        open={modalOpen}
        onClose={() => setModalOpen(false)}
        title={brief.title}
        size="lg"
        footer={
          <div className="flex items-center justify-between w-full">
            <div className="flex items-center gap-2">
              <Button
                variant="secondary"
                size="sm"
                onClick={handleCopy}
                leftIcon={copied ? <Check className="h-3.5 w-3.5 text-pain-low" /> : <Copy className="h-3.5 w-3.5" />}
              >
                {copied ? "Copied!" : "Copy Brief"}
              </Button>
              <Button
                variant="secondary"
                size="sm"
                onClick={handleExport}
                leftIcon={<Download className="h-3.5 w-3.5" />}
              >
                Export MD
              </Button>
              <Button
                variant="secondary"
                size="sm"
                onClick={handleShare}
                leftIcon={shared ? <Check className="h-3.5 w-3.5 text-pain-low" /> : <Share2 className="h-3.5 w-3.5" />}
              >
                {shared ? "Link Copied" : "Share"}
              </Button>
            </div>
            <Link href="/campaigns">
              <Button size="sm" rightIcon={<ArrowRight className="h-3.5 w-3.5" />}>
                Apply to Campaigns
              </Button>
            </Link>
          </div>
        }
      >
        <div className="space-y-6">
          <div className="flex items-center justify-between border-b border-surface-border pb-3">
            <span className={cn("inline-flex items-center gap-1.5 rounded-lg px-2.5 py-1 text-xs font-semibold border", cfg.color)}>
              <Icon className="h-3.5 w-3.5" />
              {brief.category}
            </span>
            <span className="text-xs text-ink-faint">{brief.readTime} · Published {brief.date}</span>
          </div>

          <div className="space-y-2">
            <h4 className="text-xs font-bold uppercase tracking-wider text-ink-faint">Executive Summary</h4>
            <p className="text-sm text-ink leading-relaxed">{brief.summary}</p>
          </div>

          <div className={cn("rounded-xl p-4 border flex items-center gap-4", cfg.color)}>
            <Zap className="h-6 w-6 shrink-0" />
            <div>
              <p className="text-3xl font-black leading-none">{brief.stat.value}</p>
              <p className="text-xs font-medium mt-1">{brief.stat.label}</p>
            </div>
          </div>

          <div className="grid md:grid-cols-2 gap-5 pt-2">
            <div className="space-y-3 bg-surface-subtle/60 rounded-xl p-4 border border-surface-border">
              <p className="text-xs font-bold uppercase tracking-wider text-ink">🔍 Key Research Findings</p>
              <ul className="space-y-2">
                {brief.keyFindings.map((f, i) => (
                  <li key={i} className="flex items-start gap-2 text-xs text-ink-muted leading-snug">
                    <span className="text-pain-high font-bold shrink-0">●</span>
                    {f}
                  </li>
                ))}
              </ul>
            </div>
            <div className="space-y-3 bg-surface-subtle/60 rounded-xl p-4 border border-surface-border">
              <p className="text-xs font-bold uppercase tracking-wider text-ink">✅ Strategic Recommendations</p>
              <ul className="space-y-2">
                {brief.recommendations.map((r, i) => (
                  <li key={i} className="flex items-start gap-2 text-xs text-ink-muted leading-snug">
                    <span className="text-pain-low font-bold shrink-0">→</span>
                    {r}
                  </li>
                ))}
              </ul>
            </div>
          </div>
        </div>
      </Modal>
    </>
  );
}

/* ── Page ──────────────────────────────────────────────────── */
export default function InsightsPage() {
  const [sidebarOpen, setSidebarOpen] = useState(false);
  const [filter, setFilter] = useState<CategoryFilter>("All");
  const [generating, setGenerating] = useState(false);

  const filtered = filter === "All" ? BRIEFS : BRIEFS.filter((b) => b.category === filter);

  const handleGenerate = async () => {
    setGenerating(true);
    await new Promise((r) => setTimeout(r, 1400));
    setGenerating(false);
  };

  return (
    <div className="flex min-h-dvh bg-surface-bg">
      <Sidebar isOpen={sidebarOpen} onClose={() => setSidebarOpen(false)} />
      <div className="flex flex-1 flex-col lg:pl-64">
        <Navbar onMobileMenuToggle={() => setSidebarOpen(true)} />

        <main className="flex-1 p-5 lg:p-8 space-y-6">
          {/* Header */}
          <div className="flex flex-col sm:flex-row sm:items-center sm:justify-between gap-4">
            <div>
              <h1 className="text-2xl font-bold text-ink tracking-tight">Market Insights</h1>
              <p className="text-sm text-ink-muted mt-0.5">
                AI-written intelligence briefs in plain language — strategy you can act on today.
              </p>
            </div>
            <div className="flex items-center gap-2">
              <Badge variant="brand" className="hidden sm:flex">
                <BookOpen className="h-3 w-3" />
                {BRIEFS.length} briefs generated
              </Badge>
              <Button
                size="sm"
                loading={generating}
                leftIcon={!generating ? <Sparkles className="h-3.5 w-3.5" /> : undefined}
                onClick={handleGenerate}
              >
                Generate New Brief
              </Button>
            </div>
          </div>

          {/* Category filter */}
          <div className="flex items-center gap-2 overflow-x-auto pb-1 scrollbar-thin">
            {CATEGORIES.map((cat) => {
              const isActive = filter === cat;
              const cfg = cat !== "All" ? categoryConfig[cat as InsightCategory] : null;
              const Icon = cfg?.icon;
              return (
                <button
                  key={cat}
                  onClick={() => setFilter(cat)}
                  className={cn(
                    "flex items-center gap-1.5 whitespace-nowrap rounded-xl border px-3.5 py-1.5 text-xs font-medium transition-all shrink-0",
                    isActive
                      ? "bg-brand-500 text-white border-brand-500"
                      : "bg-surface-card border-surface-border text-ink-muted hover:border-brand-300 hover:text-ink"
                  )}
                >
                  {Icon && <Icon className="h-3.5 w-3.5" />}
                  {cat}
                </button>
              );
            })}
          </div>

          {/* Briefs */}
          <StaggerContainer className="grid grid-cols-1 xl:grid-cols-2 gap-5">
            {filtered.map((brief) => (
              <StaggerItem key={brief.id}>
                <BriefCard brief={brief} />
              </StaggerItem>
            ))}
          </StaggerContainer>

          {filtered.length === 0 && (
            <Card className="text-center py-12">
              <Lightbulb className="h-8 w-8 text-ink-faint mx-auto mb-3" />
              <p className="text-ink-muted text-sm">No briefs in this category yet.</p>
              <Button variant="ghost" size="sm" className="mt-3" onClick={() => setFilter("All")}>
                Show all
              </Button>
            </Card>
          )}
        </main>
      </div>
    </div>
  );
}
