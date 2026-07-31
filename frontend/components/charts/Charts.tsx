"use client";

import {
  BarChart,
  Bar,
  XAxis,
  YAxis,
  CartesianGrid,
  Tooltip,
  ResponsiveContainer,
  PieChart,
  Pie,
  Cell,
  Legend,
  AreaChart,
  Area,
} from "recharts";

/* ──────────────────────────────────────────────────────────────
   Shared chart color palette — resolved from design tokens
   (recharts needs real color strings, not CSS vars)
   ────────────────────────────────────────────────────────────── */
export const CHART_COLORS = {
  brand:  "#7C6FCD",
  high:   "#F04444",
  medium: "#E8920A",
  low:    "#2D9E6A",
  faint:  "#9B96AF",
  border: "#E2DFF0",
  bg:     "#F8F8FB",
};

/* ──────────────────────────────────────────────────────────────
   Shared Tooltip style
   ────────────────────────────────────────────────────────────── */
const tooltipStyle = {
  backgroundColor: "#ffffff",
  border: "1px solid #E2DFF0",
  borderRadius: 10,
  fontSize: 12,
  boxShadow: "0 4px 16px rgba(0,0,0,0.08)",
  color: "#16143B",
};

/* ──────────────────────────────────────────────────────────────
   PainByPlatformBar — horizontal bar chart with draw-in animation
   ────────────────────────────────────────────────────────────── */
interface BarData {
  platform: string;
  count: number;
  high: number;
  medium: number;
  low: number;
}

export function PainByPlatformBar({ data }: { data: BarData[] }) {
  return (
    <ResponsiveContainer width="100%" height={240}>
      <BarChart
        data={data}
        layout="vertical"
        margin={{ top: 0, right: 16, left: 0, bottom: 0 }}
        barSize={10}
        barGap={2}
      >
        <CartesianGrid strokeDasharray="3 3" stroke={CHART_COLORS.border} horizontal={false} />
        <XAxis type="number" tick={{ fontSize: 11, fill: CHART_COLORS.faint }} axisLine={false} tickLine={false} />
        <YAxis
          type="category"
          dataKey="platform"
          tick={{ fontSize: 11, fill: CHART_COLORS.faint }}
          axisLine={false}
          tickLine={false}
          width={90}
        />
        <Tooltip contentStyle={tooltipStyle} cursor={{ fill: "rgba(124,111,205,0.06)" }} />
        <Bar
          dataKey="high"
          name="High"
          fill={CHART_COLORS.high}
          radius={[0, 4, 4, 0]}
          stackId="a"
          isAnimationActive={true}
          animationDuration={800}
          animationEasing="ease-out"
        />
        <Bar
          dataKey="medium"
          name="Medium"
          fill={CHART_COLORS.medium}
          radius={[0, 0, 0, 0]}
          stackId="a"
          isAnimationActive={true}
          animationDuration={800}
          animationEasing="ease-out"
        />
        <Bar
          dataKey="low"
          name="Low"
          fill={CHART_COLORS.low}
          radius={[0, 4, 4, 0]}
          stackId="a"
          isAnimationActive={true}
          animationDuration={800}
          animationEasing="ease-out"
        />
      </BarChart>
    </ResponsiveContainer>
  );
}

/* ──────────────────────────────────────────────────────────────
   CampaignActivityArea — area/line chart for daily activity with animation
   ────────────────────────────────────────────────────────────── */
interface ActivityData {
  day: string;
  campaigns: number;
  insights: number;
}

export function CampaignActivityArea({ data }: { data: ActivityData[] }) {
  return (
    <ResponsiveContainer width="100%" height={180}>
      <AreaChart data={data} margin={{ top: 4, right: 8, left: -20, bottom: 0 }}>
        <defs>
          <linearGradient id="brandGrad" x1="0" y1="0" x2="0" y2="1">
            <stop offset="5%" stopColor={CHART_COLORS.brand} stopOpacity={0.18} />
            <stop offset="95%" stopColor={CHART_COLORS.brand} stopOpacity={0} />
          </linearGradient>
          <linearGradient id="lowGrad" x1="0" y1="0" x2="0" y2="1">
            <stop offset="5%" stopColor={CHART_COLORS.low} stopOpacity={0.15} />
            <stop offset="95%" stopColor={CHART_COLORS.low} stopOpacity={0} />
          </linearGradient>
        </defs>
        <CartesianGrid strokeDasharray="3 3" stroke={CHART_COLORS.border} vertical={false} />
        <XAxis dataKey="day" tick={{ fontSize: 11, fill: CHART_COLORS.faint }} axisLine={false} tickLine={false} />
        <YAxis tick={{ fontSize: 11, fill: CHART_COLORS.faint }} axisLine={false} tickLine={false} />
        <Tooltip contentStyle={tooltipStyle} />
        <Area
          type="monotone"
          dataKey="campaigns"
          name="Campaigns"
          stroke={CHART_COLORS.brand}
          strokeWidth={2}
          fill="url(#brandGrad)"
          dot={{ fill: CHART_COLORS.brand, r: 3, strokeWidth: 0 }}
          activeDot={{ r: 5 }}
          isAnimationActive={true}
          animationDuration={800}
          animationEasing="ease-out"
        />
        <Area
          type="monotone"
          dataKey="insights"
          name="Insights"
          stroke={CHART_COLORS.low}
          strokeWidth={2}
          fill="url(#lowGrad)"
          dot={{ fill: CHART_COLORS.low, r: 3, strokeWidth: 0 }}
          activeDot={{ r: 5 }}
          isAnimationActive={true}
          animationDuration={800}
          animationEasing="ease-out"
        />
      </AreaChart>
    </ResponsiveContainer>
  );
}

/* ──────────────────────────────────────────────────────────────
   PainSeverityPie — donut chart with draw-in animation
   ────────────────────────────────────────────────────────────── */
interface PieData {
  name: string;
  value: number;
  color: string;
}

export function PainSeverityPie({ data }: { data: PieData[] }) {
  return (
    <ResponsiveContainer width="100%" height={210}>
      <PieChart>
        <Pie
          data={data}
          cx="50%"
          cy="45%"
          innerRadius={50}
          outerRadius={74}
          paddingAngle={4}
          dataKey="value"
          isAnimationActive={true}
          animationDuration={900}
          animationEasing="ease-out"
        >
          {data.map((entry, index) => (
            <Cell key={`cell-${index}`} fill={entry.color} stroke="none" />
          ))}
        </Pie>
        <Tooltip
          contentStyle={tooltipStyle}
          formatter={(value, name) => [`${value ?? ""}`, `${name}`]}
        />
        <Legend
          iconType="circle"
          iconSize={9}
          wrapperStyle={{ fontSize: 11, color: CHART_COLORS.faint, paddingTop: 10 }}
        />
      </PieChart>
    </ResponsiveContainer>
  );
}
