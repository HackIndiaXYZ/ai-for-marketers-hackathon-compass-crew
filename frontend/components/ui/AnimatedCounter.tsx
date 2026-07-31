"use client";

import { useEffect, useState } from "react";

interface AnimatedCounterProps {
  value: string | number;
  duration?: number;
  className?: string;
  prefix?: string;
  suffix?: string;
}

export function AnimatedCounter({
  value,
  duration = 1000,
  className = "",
  prefix = "",
  suffix = "",
}: AnimatedCounterProps) {
  // Extract number from string like "529", "340%", "₹20,000"
  const rawStr = String(value);
  const numericVal = parseFloat(rawStr.replace(/[^0-9.]/g, ""));
  const isPercent = rawStr.includes("%");
  const isCurrency = rawStr.includes("₹");
  const hasSub = rawStr.includes("+");

  const [displayCount, setDisplayCount] = useState<number>(isNaN(numericVal) ? 0 : 0);

  useEffect(() => {
    if (isNaN(numericVal)) return;

    let startTimestamp: number | null = null;
    const startValue = 0;
    const endValue = numericVal;

    const step = (timestamp: number) => {
      if (!startTimestamp) startTimestamp = timestamp;
      const progress = Math.min((timestamp - startTimestamp) / duration, 1);
      // Ease out cubic function
      const easeOut = 1 - Math.pow(1 - progress, 3);
      const current = Math.floor(startValue + (endValue - startValue) * easeOut);
      
      setDisplayCount(current);

      if (progress < 1) {
        window.requestAnimationFrame(step);
      } else {
        setDisplayCount(endValue);
      }
    };

    const animId = window.requestAnimationFrame(step);
    return () => window.cancelAnimationFrame(animId);
  }, [numericVal, duration]);

  if (isNaN(numericVal)) {
    return <span className={className}>{rawStr}</span>;
  }

  const formattedNum = isCurrency
    ? `₹${displayCount.toLocaleString("en-IN")}`
    : displayCount.toLocaleString("en-IN");

  const finalPrefix = prefix || (hasSub && !isCurrency ? "+" : "");
  const finalSuffix = suffix || (isPercent ? "%" : "");

  return (
    <span className={className}>
      {finalPrefix}
      {formattedNum}
      {finalSuffix}
    </span>
  );
}
