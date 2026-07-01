'use client';

import { useMemo } from 'react';
import { getScoreColor } from '@/lib/visualization/chart-theme';

interface ScoreBarProps {
  score?: number;
  value?: number;
  max?: number;
  label?: string;
  color?: string;
  size?: 'sm' | 'md' | 'lg';
  height?: number;
  showLabel?: boolean;
  animated?: boolean;
  className?: string;
}

const SIZE_HEIGHT: Record<string, number> = { sm: 4, md: 8, lg: 12 };

export function ScoreBar({
  score,
  value,
  max = 100,
  label,
  color,
  size = 'md',
  height,
  showLabel = true,
  animated = true,
  className = '',
}: ScoreBarProps) {
  const raw = score ?? value ?? 0;
  const pct = useMemo(() => Math.min(100, Math.max(0, (raw / max) * 100)), [raw, max]);
  const barColor = color ?? getScoreColor(raw);
  const barHeight = height ?? SIZE_HEIGHT[size];

  return (
    <div className={`flex items-center gap-2 w-full ${className}`}>
      {label && showLabel && (
        <span className="text-xs text-[var(--color-foreground-secondary)] shrink-0 min-w-[3rem]">
          {label}
        </span>
      )}
      <div
        className="flex-1 rounded-full overflow-hidden"
        style={{ height: barHeight, backgroundColor: 'var(--color-background-secondary)' }}
      >
        <div
          className={`h-full rounded-full ${animated ? 'transition-all duration-700 ease-out' : ''}`}
          style={{ width: `${pct}%`, backgroundColor: barColor }}
        />
      </div>
      {showLabel && (
        <span className="text-xs font-medium tabular-nums shrink-0 min-w-[2rem] text-right" style={{ color: barColor }}>
          {Math.round(raw)}
        </span>
      )}
    </div>
  );
}

export default ScoreBar;
