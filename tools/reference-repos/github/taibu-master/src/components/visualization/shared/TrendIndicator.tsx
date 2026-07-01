'use client';

import { TrendingUp, TrendingDown, Minus } from 'lucide-react';

interface TrendIndicatorProps {
  trend: 'up' | 'down' | 'stable';
  label?: string;
  percentage?: number;
  size?: 'sm' | 'md';
}

const TREND_CONFIG = {
  up:     { Icon: TrendingUp,   color: '#22c55e', prefix: '+' },
  down:   { Icon: TrendingDown, color: '#ef4444', prefix: '' },
  stable: { Icon: Minus,        color: '#9ca3af', prefix: '' },
} as const;

const ICON_SIZE = { sm: 14, md: 18 } as const;

export default function TrendIndicator({ trend, label, percentage, size = 'md' }: TrendIndicatorProps) {
  const config = TREND_CONFIG[trend] ?? TREND_CONFIG.stable;
  const { Icon, color, prefix } = config;
  const iconSize = ICON_SIZE[size];
  const textClass = size === 'sm' ? 'text-xs' : 'text-sm';

  return (
    <span className={`inline-flex items-center gap-1 ${textClass}`} style={{ color }}>
      <Icon size={iconSize} />
      {percentage != null && (
        <span className="font-medium tabular-nums">
          {prefix}{percentage}%
        </span>
      )}
      {label && <span>{label}</span>}
    </span>
  );
}
