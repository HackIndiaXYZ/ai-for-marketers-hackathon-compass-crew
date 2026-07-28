"use client";

import { useState } from "react";
import {
  User,
  Lock,
  Bell,
  Mic,
  Save,
  Check,
  Globe2,
  X,
  Plus,
  Shield,
  Palette,
} from "lucide-react";
import { Sidebar } from "@/components/sidebar/Sidebar";
import { Navbar } from "@/components/navbar/Navbar";
import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";
import { Badge } from "@/components/ui/badge";
import { Card, CardHeader, CardTitle, CardDescription, CardContent } from "@/components/ui/card";
import { cn } from "@/lib/utils";

/* ── Tab config ─────────────────────────────────────────────── */
const TABS = [
  { id: "account",     label: "Account",       icon: User    },
  { id: "brand-voice", label: "Brand Voice",   icon: Mic     },
  { id: "appearance",  label: "Appearance",    icon: Palette },
  { id: "notifications",label: "Notifications",icon: Bell    },
  { id: "security",    label: "Security",      icon: Shield  },
] as const;
type Tab = typeof TABS[number]["id"];

/* ── Toggle switch ──────────────────────────────────────────── */
function Toggle({ checked, onChange, id }: { checked: boolean; onChange: () => void; id: string }) {
  return (
    <button
      id={id}
      role="switch"
      aria-checked={checked}
      onClick={onChange}
      className={cn(
        "relative inline-flex h-6 w-11 shrink-0 cursor-pointer rounded-full border-2 border-transparent transition-colors duration-200",
        checked ? "bg-brand-500" : "bg-surface-border"
      )}
    >
      <span
        className={cn(
          "pointer-events-none inline-block h-5 w-5 rounded-full bg-white shadow-md ring-0 transition-transform duration-200",
          checked ? "translate-x-5" : "translate-x-0"
        )}
      />
    </button>
  );
}

/* ── Section wrapper ────────────────────────────────────────── */
function Section({ title, desc, children }: { title: string; desc?: string; children: React.ReactNode }) {
  return (
    <Card>
      <CardHeader>
        <CardTitle>{title}</CardTitle>
        {desc && <CardDescription>{desc}</CardDescription>}
      </CardHeader>
      <CardContent className="space-y-5">{children}</CardContent>
    </Card>
  );
}

/* ── Save feedback ──────────────────────────────────────────── */
function useSave() {
  const [saving, setSaving] = useState(false);
  const [saved, setSaved] = useState(false);
  const save = async () => {
    setSaving(true);
    await new Promise((r) => setTimeout(r, 900));
    setSaving(false);
    setSaved(true);
    setTimeout(() => setSaved(false), 2000);
  };
  return { saving, saved, save };
}

/* ── Keyword chip ───────────────────────────────────────────── */
function KeywordChip({ label, onRemove }: { label: string; onRemove: () => void }) {
  return (
    <span className="inline-flex items-center gap-1 rounded-full border border-surface-border bg-surface-subtle px-2.5 py-1 text-xs font-medium text-ink-muted">
      {label}
      <button onClick={onRemove} className="ml-0.5 hover:text-pain-high transition-colors">
        <X className="h-3 w-3" />
      </button>
    </span>
  );
}

/* ── Page ──────────────────────────────────────────────────── */
export default function SettingsPage() {
  const [sidebarOpen, setSidebarOpen] = useState(false);
  const [activeTab, setActiveTab] = useState<Tab>("account");
  const { saving, saved, save } = useSave();

  /* Account fields */
  const [name,  setName]  = useState("Muskan Yeshminali");
  const [email, setEmail] = useState("muskan@compasscrew.ai");
  const [company, setCompany] = useState("Compass Crew");
  const [role, setRole] = useState("Marketing Lead");

  /* Brand voice */
  const [brandName, setBrandName]  = useState("PainToAd AI");
  const [industry, setIndustry]    = useState("SaaS / Marketing Tech");
  const [toneVal, setToneVal]      = useState(60);
  const [formalVal, setFormalVal]  = useState(45);
  const [lang, setLang]            = useState("English");
  const [useWords, setUseWords]    = useState(["data-driven", "ROI", "customer insight", "pain points"]);
  const [avoidWords, setAvoidWords]= useState(["cheap", "free trial spam", "guaranteed"]);
  const [newUse, setNewUse]        = useState("");
  const [newAvoid, setNewAvoid]    = useState("");

  /* Notifications */
  const [notifs, setNotifs] = useState({
    analysisComplete: true,
    campaignReady: true,
    weeklyReport: false,
    insightBriefs: true,
    productUpdates: false,
    tips: true,
  });
  const toggleNotif = (key: keyof typeof notifs) => setNotifs((n) => ({ ...n, [key]: !n[key] }));

  return (
    <div className="flex min-h-dvh bg-surface-bg">
      <Sidebar isOpen={sidebarOpen} onClose={() => setSidebarOpen(false)} />
      <div className="flex flex-1 flex-col lg:pl-64">
        <Navbar onMobileMenuToggle={() => setSidebarOpen(true)} />

        <main className="flex-1 p-5 lg:p-8 space-y-6">
          {/* Header */}
          <div className="flex flex-col sm:flex-row sm:items-center sm:justify-between gap-4">
            <div>
              <h1 className="text-2xl font-bold text-ink tracking-tight">Settings</h1>
              <p className="text-sm text-ink-muted mt-0.5">
                Manage your account, brand voice, and preferences.
              </p>
            </div>
            <Button
              size="sm"
              loading={saving}
              leftIcon={saved ? <Check className="h-3.5 w-3.5" /> : !saving ? <Save className="h-3.5 w-3.5" /> : undefined}
              onClick={save}
              className={saved ? "bg-pain-low hover:bg-pain-low/90" : ""}
            >
              {saved ? "Saved!" : "Save Changes"}
            </Button>
          </div>

          {/* Tabs */}
          <div className="flex items-center gap-1.5 overflow-x-auto pb-1 scrollbar-thin border-b border-surface-border">
            {TABS.map(({ id, label, icon: Icon }) => (
              <button
                key={id}
                onClick={() => setActiveTab(id)}
                className={cn(
                  "flex items-center gap-1.5 whitespace-nowrap px-4 py-2.5 text-sm font-medium transition-all border-b-2 -mb-px shrink-0",
                  activeTab === id
                    ? "border-brand-500 text-brand-600 dark:text-brand-400"
                    : "border-transparent text-ink-muted hover:text-ink hover:border-surface-border"
                )}
              >
                <Icon className="h-4 w-4" />
                {label}
              </button>
            ))}
          </div>

          {/* ── Account ── */}
          {activeTab === "account" && (
            <div className="max-w-xl space-y-5">
              <Section title="Personal Information" desc="Your name and contact details.">
                <Input label="Full Name"    value={name}    onChange={(e) => setName(e.target.value)}    fullWidth leftAdornment={<User className="h-4 w-4" />} />
                <Input label="Email Address"value={email}   onChange={(e) => setEmail(e.target.value)}   fullWidth type="email" />
                <Input label="Company"      value={company} onChange={(e) => setCompany(e.target.value)} fullWidth leftAdornment={<Globe2 className="h-4 w-4" />} />
                <Input label="Role"         value={role}    onChange={(e) => setRole(e.target.value)}    fullWidth />
              </Section>

              <Section title="Danger Zone" desc="Irreversible actions — proceed with care.">
                <div className="flex items-center justify-between">
                  <div>
                    <p className="text-sm font-medium text-ink">Delete Account</p>
                    <p className="text-xs text-ink-faint mt-0.5">All data will be permanently removed.</p>
                  </div>
                  <Button variant="outline" size="sm" className="border-pain-high/40 text-pain-high hover:bg-pain-high-bg">
                    Delete Account
                  </Button>
                </div>
              </Section>
            </div>
          )}

          {/* ── Brand Voice ── */}
          {activeTab === "brand-voice" && (
            <div className="max-w-xl space-y-5">
              <Section title="Brand Identity" desc="Help AI write in your brand's voice.">
                <Input label="Brand / Product Name" value={brandName} onChange={(e) => setBrandName(e.target.value)} fullWidth />
                <Input label="Industry / Category"  value={industry}  onChange={(e) => setIndustry(e.target.value)}  fullWidth />

                {/* Tone sliders */}
                <div className="space-y-4">
                  <div className="space-y-2">
                    <div className="flex justify-between">
                      <span className="text-sm font-medium text-ink">Tone</span>
                      <span className="text-xs text-brand-600 dark:text-brand-400 font-semibold">
                        {toneVal < 33 ? "Serious" : toneVal < 66 ? "Balanced" : "Playful"}
                      </span>
                    </div>
                    <input type="range" min={0} max={100} value={toneVal} onChange={(e) => setToneVal(+e.target.value)} className="w-full accent-brand-500" />
                    <div className="flex justify-between text-xs text-ink-faint">
                      <span>Serious</span><span>Playful</span>
                    </div>
                  </div>
                  <div className="space-y-2">
                    <div className="flex justify-between">
                      <span className="text-sm font-medium text-ink">Formality</span>
                      <span className="text-xs text-brand-600 dark:text-brand-400 font-semibold">
                        {formalVal < 33 ? "Casual" : formalVal < 66 ? "Professional" : "Formal"}
                      </span>
                    </div>
                    <input type="range" min={0} max={100} value={formalVal} onChange={(e) => setFormalVal(+e.target.value)} className="w-full accent-brand-500" />
                    <div className="flex justify-between text-xs text-ink-faint">
                      <span>Casual</span><span>Formal</span>
                    </div>
                  </div>
                </div>

                {/* Default language */}
                <div className="space-y-2">
                  <span className="text-sm font-medium text-ink">Default Campaign Language</span>
                  <div className="flex flex-wrap gap-2">
                    {["English", "Hinglish", "Hindi", "Bengali"].map((l) => (
                      <button
                        key={l}
                        onClick={() => setLang(l)}
                        className={cn(
                          "rounded-lg border px-3 py-1.5 text-xs font-medium transition-all",
                          lang === l
                            ? "bg-brand-500 text-white border-brand-500"
                            : "bg-surface-card border-surface-border text-ink-muted hover:border-brand-300"
                        )}
                      >
                        {l}
                      </button>
                    ))}
                  </div>
                </div>
              </Section>

              <Section title="Keyword Memory" desc="Words the AI will prefer or avoid in campaigns.">
                <div>
                  <p className="text-xs font-semibold uppercase tracking-wider text-pain-low mb-2">✅ Always use</p>
                  <div className="flex flex-wrap gap-2 mb-3">
                    {useWords.map((w) => (
                      <KeywordChip key={w} label={w} onRemove={() => setUseWords((prev) => prev.filter((x) => x !== w))} />
                    ))}
                  </div>
                  <div className="flex gap-2">
                    <Input
                      value={newUse}
                      onChange={(e) => setNewUse(e.target.value)}
                      placeholder="Add keyword..."
                      onKeyDown={(e) => { if (e.key === "Enter" && newUse.trim()) { setUseWords((p) => [...p, newUse.trim()]); setNewUse(""); }}}
                      fullWidth leftAdornment={<Plus className="h-3.5 w-3.5" />}
                    />
                    <Button
                      size="sm"
                      variant="secondary"
                      onClick={() => { if (newUse.trim()) { setUseWords((p) => [...p, newUse.trim()]); setNewUse(""); }}}
                    >
                      Add
                    </Button>
                  </div>
                </div>
                <div>
                  <p className="text-xs font-semibold uppercase tracking-wider text-pain-high mb-2">🚫 Never use</p>
                  <div className="flex flex-wrap gap-2 mb-3">
                    {avoidWords.map((w) => (
                      <KeywordChip key={w} label={w} onRemove={() => setAvoidWords((prev) => prev.filter((x) => x !== w))} />
                    ))}
                  </div>
                  <div className="flex gap-2">
                    <Input
                      value={newAvoid}
                      onChange={(e) => setNewAvoid(e.target.value)}
                      placeholder="Add keyword to avoid..."
                      onKeyDown={(e) => { if (e.key === "Enter" && newAvoid.trim()) { setAvoidWords((p) => [...p, newAvoid.trim()]); setNewAvoid(""); }}}
                      fullWidth leftAdornment={<X className="h-3.5 w-3.5" />}
                    />
                    <Button
                      size="sm"
                      variant="secondary"
                      onClick={() => { if (newAvoid.trim()) { setAvoidWords((p) => [...p, newAvoid.trim()]); setNewAvoid(""); }}}
                    >
                      Add
                    </Button>
                  </div>
                </div>
              </Section>
            </div>
          )}

          {/* ── Appearance ── */}
          {activeTab === "appearance" && (
            <div className="max-w-xl">
              <Section title="Theme" desc="Choose how PainToAd AI looks.">
                <div className="grid grid-cols-3 gap-3">
                  {[
                    { id: "light", label: "Light",  preview: "bg-white border border-surface-border" },
                    { id: "dark",  label: "Dark",   preview: "bg-[#16143B]" },
                    { id: "system",label: "System", preview: "bg-gradient-to-br from-white to-[#16143B]" },
                  ].map((t) => (
                    <button
                      key={t.id}
                      className="flex flex-col items-center gap-2 rounded-xl border border-surface-border p-3 hover:border-brand-300 transition-all hover:shadow-card"
                    >
                      <div className={cn("h-12 w-full rounded-lg", t.preview)} />
                      <span className="text-xs font-medium text-ink-muted">{t.label}</span>
                    </button>
                  ))}
                </div>
              </Section>
            </div>
          )}

          {/* ── Notifications ── */}
          {activeTab === "notifications" && (
            <div className="max-w-xl">
              <Section title="Email Notifications" desc="Choose what we send to your inbox.">
                {[
                  { key: "analysisComplete", label: "Analysis Complete",    desc: "When a pain point analysis finishes"       },
                  { key: "campaignReady",    label: "Campaigns Ready",      desc: "When new campaign assets are generated"    },
                  { key: "weeklyReport",     label: "Weekly Performance Report", desc: "Every Monday with last week's metrics"  },
                  { key: "insightBriefs",    label: "New Insight Briefs",   desc: "When new market intelligence is available" },
                  { key: "productUpdates",   label: "Product Updates",      desc: "New features and platform improvements"    },
                  { key: "tips",             label: "Tips & Best Practices",desc: "Occasional tips to get more from the platform" },
                ].map(({ key, label, desc }) => (
                  <div key={key} className="flex items-center justify-between gap-4 py-2 border-b border-surface-border last:border-0">
                    <div>
                      <p className="text-sm font-medium text-ink">{label}</p>
                      <p className="text-xs text-ink-faint mt-0.5">{desc}</p>
                    </div>
                    <Toggle
                      id={key}
                      checked={notifs[key as keyof typeof notifs]}
                      onChange={() => toggleNotif(key as keyof typeof notifs)}
                    />
                  </div>
                ))}
              </Section>
            </div>
          )}

          {/* ── Security ── */}
          {activeTab === "security" && (
            <div className="max-w-xl space-y-5">
              <Section title="Change Password" desc="Use a strong, unique password.">
                <Input label="Current Password"  type="password" fullWidth leftAdornment={<Lock className="h-4 w-4" />} placeholder="••••••••" />
                <Input label="New Password"       type="password" fullWidth leftAdornment={<Lock className="h-4 w-4" />} placeholder="Min. 8 characters" />
                <Input label="Confirm New Password" type="password" fullWidth leftAdornment={<Lock className="h-4 w-4" />} placeholder="Repeat new password" />
                <Button variant="secondary" size="sm">Update Password</Button>
              </Section>

              <Section title="Active Sessions" desc="Devices currently signed in to your account.">
                {[
                  { device: "MacBook Pro · Chrome", location: "Mumbai, IN", current: true,  time: "Active now" },
                  { device: "iPhone 15 · Safari",    location: "Mumbai, IN", current: false, time: "3 hours ago" },
                ].map((s, i) => (
                  <div key={i} className="flex items-center justify-between gap-4 py-2 border-b border-surface-border last:border-0">
                    <div>
                      <div className="flex items-center gap-2">
                        <p className="text-sm font-medium text-ink">{s.device}</p>
                        {s.current && <Badge variant="low" className="text-[10px]">Current</Badge>}
                      </div>
                      <p className="text-xs text-ink-faint mt-0.5">{s.location} · {s.time}</p>
                    </div>
                    {!s.current && (
                      <Button variant="ghost" size="xs" className="text-pain-high hover:text-pain-high hover:bg-pain-high-bg">
                        Revoke
                      </Button>
                    )}
                  </div>
                ))}
              </Section>
            </div>
          )}

        </main>
      </div>
    </div>
  );
}
