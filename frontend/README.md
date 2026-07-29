# 🐸 PainToAd AI — Frontend Application

> **Turn Customer Pain Points into High-ROI Ad Campaigns**  
> Built for AI for Marketers Hackathon by **Team Compass Crew**.

PainToAd AI is a modern SaaS frontend that scrapes real customer complaints from 7 channels (Reddit, Quora, Google Reviews, MouthShut, Twitter/X, Justdial, IndiaMART), analyzes pain intensity & emotional frequency, synthesizes target buyer personas, and automatically generates multi-channel ad copy (Google Search, Facebook, Instagram, WhatsApp, Email, SEO) with pre-launch ROI predictions.

---

## 🎨 Key Features & Architecture

### 1. 🎯 Modern Light/Dark Pastel Theme & Design System
- **Curated Color Tokens**: Primary Lavender-Violet (`#7C6FCD`), Deep Slate Ink (`#0F0F1A` / `#413E55`) for maximum legibility and contrast.
- **Pain Severity System**:
  - 🔴 **High Impact**: Coral Red (`#E11D48`)
  - 🟡 **Medium Impact**: Amber Gold (`#D97706`)
  - 🟢 **Low Impact**: Emerald Green (`#10B981`)
- **Theme Toggle**: Real-time dark mode toggle with smooth animated icon transitions.

### 2. ⚡ Smooth Motion & Micro-Interactions (Framer Motion + CSS)
- **Viewport Entrance Animations**: Cards and lists stagger and slide up on mount and scroll.
- **Interactive Micro-Lifts**: Cards and action tiles elevate (`translateY(-6px)`, `scale: 1.018`) with hardware-accelerated spring physics on hover and press.
- **Tactile Button Bounces**: Buttons compress on click (`scale: 0.96`) with instant spring feedback.
- **Page Transitions**: Seamless route change transitions using Next.js `app/template.tsx`.

### 3. 🚀 8 Purpose-Built SaaS Modules
1. **Landing Page (`/`)**: Dynamic SaaS landing page with floating hero card, platform ticker, problem/solution breakdown, feature cards, and bottom CTA.
2. **One-Click Demo Auth (`/login` & `/register`)**: Instant hackathon demo access prefilling credentials and redirecting to the dashboard.
3. **Dashboard (`/dashboard`)**: Central hub displaying scraped stats, platform distribution bar charts, emotional severity pie chart, activity graphs, recent pain points, and quick action shortcuts.
4. **Pain Analyzer (`/analyze`)**: Topic-based complaint scraping with intensity sliders, platform filters, sentiment tags, and supporting quotes.
5. **Persona Intelligence (`/personas`)**: AI-generated target customer profiles with purchasing power metrics, core drivers, and channel preferences.
6. **Campaign Generator (`/campaigns`)**: Multi-channel ad copy generator with tone controls (Professional, Urgent, Conversational, Empathetic), multi-language options (English, Hinglish, Hindi, Bengali), and instant copy buttons.
7. **Market Insights (`/insights`)**: Plain-language AI market intelligence briefs with expandable key findings and strategic recommendations.
8. **Campaign Optimizer (`/optimizer`)**: A/B variant side-by-side comparison with CTR prediction, cost-per-click forecasts, quality radar charts, and recommended budget splits.
9. **ROI Simulator (`/simulator`)**: Interactive pre-spend budget & reach trajectory model with projected revenue and return-on-ad-spend (ROAS).
10. **Settings (`/settings`)**: Brand voice persistence, target platform selections, team management, and theme preferences.

---

## 🛠️ Tech Stack

- **Framework**: Next.js 15 (App Router, React 19)
- **Language**: TypeScript
- **Styling**: Tailwind CSS v3 + CSS Design Tokens (`globals.css`)
- **Animations**: Framer Motion 12 + Custom CSS Micro-Interactions
- **Icons**: Lucide React
- **Data Visualization**: Recharts

---

## 🚀 Getting Started

### Prerequisites
- Node.js `>= 18.0.0`
- `npm` or `yarn`

### Installation & Run

1. Navigate to the frontend directory:
   ```bash
   cd frontend
   ```

2. Install dependencies:
   ```bash
   npm install
   ```

3. Run the development server:
   ```bash
   npm run dev
   ```

4. Open your browser:
   ```text
   http://localhost:3000
   ```

### Production Build
To verify type safety and static page prerendering:
```bash
npm run build
```

---

## 👥 Authors
- **Team**: Compass Crew
- **UI/UX Lead & Frontend Engineer**: Muskan (`muskan/frontend`)
