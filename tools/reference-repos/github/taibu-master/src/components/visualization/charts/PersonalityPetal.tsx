'use client';

import { useMemo } from 'react';
import type { PersonalityPetalData } from '@/lib/visualization/chart-types';
import { useChartEntrance, CHART_ENTRANCE_BASE, CHART_ENTRANCE_ACTIVE } from '@/components/visualization/shared/useChartEntrance';
import ChartEmpty from '@/components/visualization/shared/ChartEmpty';

interface PersonalityPetalProps {
  data: PersonalityPetalData;
  compact?: boolean;
  className?: string;
}

const PETAL_COLORS = ['#3b82f6', '#22c55e', '#f59e0b', '#ef4444', '#8b5cf6', '#ec4899'];

function polarToCartesian(cx: number, cy: number, r: number, angleDeg: number) {
  const rad = ((angleDeg - 90) * Math.PI) / 180;
  return { x: cx + r * Math.cos(rad), y: cy + r * Math.sin(rad) };
}

export default function PersonalityPetal({ data, compact = false, className = '' }: PersonalityPetalProps) {
  const { ref, entered } = useChartEntrance();
  const { traits } = data.data;

  const petalData = useMemo(() => {
    if (!traits || traits.length === 0) return [];
    const cx = 150;
    const cy = 150;
    const maxR = 100;
    const angleStep = 360 / traits.length;

    return traits.map((trait, i) => {
      const angle = i * angleStep;
      const r = (trait.score / 100) * maxR;
      const pos = polarToCartesian(cx, cy, r, angle);
      const labelPos = polarToCartesian(cx, cy, maxR + 25, angle);
      return { ...trait, color: PETAL_COLORS[i % PETAL_COLORS.length], angle, r, x: pos.x, y: pos.y, labelX: labelPos.x, labelY: labelPos.y };
    });
  }, [traits]);

  const pathD = useMemo(() => {
    if (petalData.length === 0) return '';
    const points = petalData.map((p) => `${p.x},${p.y}`).join(' L ');
    return `M ${points} Z`;
  }, [petalData]);

  if (!traits || traits.length === 0) {
    return <ChartEmpty message="暂无性格特质数据" />;
  }

  return (
    <div ref={ref} className={`space-y-4 ${CHART_ENTRANCE_BASE} ${entered ? CHART_ENTRANCE_ACTIVE : ''} ${className}`}>
      <svg viewBox="0 0 300 300" className="w-full max-w-[280px] mx-auto">
        {/* Grid circles */}
        {[20, 40, 60, 80, 100].map((r) => (
          <circle
            key={r}
            cx={150}
            cy={150}
            r={r}
            fill="none"
            stroke="var(--color-border)"
            strokeWidth={0.5}
            opacity={0.3}
          />
        ))}

        {/* Grid lines */}
        {petalData.map((p) => (
          <line
            key={p.label}
            x1={150}
            y1={150}
            x2={p.labelX}
            y2={p.labelY}
            stroke="var(--color-border)"
            strokeWidth={0.5}
            opacity={0.3}
          />
        ))}

        {/* Petal shape */}
        <path
          d={pathD}
          fill="var(--color-accent)"
          fillOpacity={0.25}
          stroke="var(--color-accent)"
          strokeWidth={2}
        />

        {/* Data points */}
        {petalData.map((p) => (
          <circle
            key={p.label}
            cx={p.x}
            cy={p.y}
            r={4}
            fill={p.color || 'var(--color-accent)'}
            stroke="var(--color-background)"
            strokeWidth={2}
          />
        ))}

        {/* Labels */}
        {petalData.map((p) => (
          <text
            key={p.label}
            x={p.labelX}
            y={p.labelY}
            textAnchor="middle"
            dominantBaseline="central"
            className="text-[10px] font-medium"
            fill="var(--color-foreground)"
          >
            {p.label}
          </text>
        ))}
      </svg>

      {/* Trait scores */}
      {!compact && (
        <div className="grid grid-cols-1 sm:grid-cols-2 gap-2">
          {petalData.map((trait) => (
            <div
              key={trait.label}
              className="flex items-center justify-between px-2.5 py-1.5 rounded-lg bg-[var(--color-background-secondary)]/40"
            >
              <span className="text-xs text-[var(--color-foreground)]">{trait.label}</span>
              <span
                className="text-xs font-bold tabular-nums"
                style={{ color: trait.color }}
              >
                {trait.score}
              </span>
            </div>
          ))}
        </div>
      )}
    </div>
  );
}
