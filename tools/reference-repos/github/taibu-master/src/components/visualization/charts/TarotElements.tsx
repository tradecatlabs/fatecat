'use client';

import { useMemo } from 'react';
import { PieChart, Pie, Cell, ResponsiveContainer, Legend } from 'recharts';
import type { TarotElementsData } from '@/lib/visualization/chart-types';
import { useChartEntrance, CHART_ENTRANCE_BASE, CHART_ENTRANCE_ACTIVE } from '@/components/visualization/shared/useChartEntrance';
import ChartEmpty from '@/components/visualization/shared/ChartEmpty';

interface TarotElementsProps {
  data: TarotElementsData;
  compact?: boolean;
  className?: string;
}

const ELEMENT_CONFIG = {
  fire: { color: '#ef4444', icon: '🔥', label: '火' },
  water: { color: '#3b82f6', icon: '💧', label: '水' },
  air: { color: '#a855f7', icon: '💨', label: '风' },
  earth: { color: '#22c55e', icon: '🌍', label: '土' },
};

type TarotElementKey = keyof typeof ELEMENT_CONFIG;

function renderLegendLabel(value: string | number, entry: unknown) {
  const payload = (
    entry
    && typeof entry === 'object'
    && 'payload' in entry
    ? (entry as { payload?: { element?: string; value?: number } }).payload
    : undefined
  );

  const elementKey = payload?.element;
  const count = payload?.value;
  if (!elementKey || !(elementKey in ELEMENT_CONFIG) || typeof count !== 'number') {
    return <span className="text-xs text-[var(--color-foreground)]">{String(value)}</span>;
  }

  return (
    <span className="text-xs text-[var(--color-foreground)]">
      {ELEMENT_CONFIG[elementKey as TarotElementKey].icon} {String(value)} ({count})
    </span>
  );
}

export default function TarotElements({ data, compact = false, className = '' }: TarotElementsProps) {
  const { ref, entered } = useChartEntrance();
  const { elements } = data.data;

  const chartData = useMemo(
    () => elements ? Object.entries(elements).map(([key, value]) => ({
      name: ELEMENT_CONFIG[key as keyof typeof ELEMENT_CONFIG]?.label ?? key,
      value: value.count,
      element: key,
      percentage: value.percentage,
    })) : [],
    [elements]
  );

  if (!elements || Object.keys(elements).length === 0) {
    return <ChartEmpty message="暂无塔罗元素数据" />;
  }

  return (
    <div ref={ref} className={`space-y-4 ${CHART_ENTRANCE_BASE} ${entered ? CHART_ENTRANCE_ACTIVE : ''} ${className}`}>
      <ResponsiveContainer width="100%" height={compact ? 200 : 240}>
        <PieChart>
          <Pie
            data={chartData}
            cx="50%"
            cy="50%"
            innerRadius={compact ? 50 : 60}
            outerRadius={compact ? 80 : 95}
            paddingAngle={3}
            dataKey="value"
            animationDuration={1000}
          >
            {chartData.map((entry) => (
              <Cell
                key={entry.element}
                fill={ELEMENT_CONFIG[entry.element as keyof typeof ELEMENT_CONFIG].color}
                stroke="var(--color-background)"
                strokeWidth={2}
              />
            ))}
          </Pie>
          <Legend
            verticalAlign="bottom"
            height={36}
            formatter={renderLegendLabel}
          />
        </PieChart>
      </ResponsiveContainer>
    </div>
  );
}
