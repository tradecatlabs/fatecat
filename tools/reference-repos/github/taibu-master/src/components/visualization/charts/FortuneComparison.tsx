'use client';

import { memo } from 'react';
import { RadarChart, PolarGrid, PolarAngleAxis, PolarRadiusAxis, Radar, ResponsiveContainer, Legend } from 'recharts';
import type { FortuneComparisonData } from '@/lib/visualization/chart-types';
import { useChartEntrance, CHART_ENTRANCE_BASE, CHART_ENTRANCE_ACTIVE } from '@/components/visualization/shared/useChartEntrance';
import ChartEmpty from '@/components/visualization/shared/ChartEmpty';

interface FortuneComparisonProps {
  data: FortuneComparisonData;
  compact?: boolean;
  className?: string;
}

const COLORS = ['#3b82f6', '#ef4444', '#22c55e', '#f59e0b', '#8b5cf6'];

function FortuneComparisonInner({ data, compact = false, className = '' }: FortuneComparisonProps) {
  const { ref, entered } = useChartEntrance();
  const { periodA, periodB, dimensions } = data.data;

  if (dimensions.length === 0) {
    return <ChartEmpty message="暂无对比数据" />;
  }

  const chartData = dimensions.map(dim => ({
    dimension: dim.label,
    [periodA.label]: dim.scoreA,
    [periodB.label]: dim.scoreB,
  }));

  const periods = [periodA, periodB];

  return (
    <div ref={ref} className={`${CHART_ENTRANCE_BASE} ${entered ? CHART_ENTRANCE_ACTIVE : ''} ${className}`}>
      <ResponsiveContainer width="100%" height={compact ? 240 : 320}>
        <RadarChart data={chartData}>
          <PolarGrid stroke="var(--color-border)" opacity={0.3} />
          <PolarAngleAxis
            dataKey="dimension"
            tick={{ fill: 'var(--color-foreground-secondary)', fontSize: 11 }}
          />
          <PolarRadiusAxis
            angle={90}
            domain={[0, 100]}
            tick={{ fill: 'var(--color-foreground-tertiary)', fontSize: 10 }}
          />
          {periods.map((period, idx) => (
            <Radar
              key={period.label}
              name={period.label}
              dataKey={period.label}
              stroke={COLORS[idx % COLORS.length]}
              fill={COLORS[idx % COLORS.length]}
              fillOpacity={0.2}
              strokeWidth={2}
            />
          ))}
          <Legend
            wrapperStyle={{ fontSize: 12 }}
            iconType="circle"
          />
        </RadarChart>
      </ResponsiveContainer>
    </div>
  );
}

export const FortuneComparison = memo(FortuneComparisonInner);
export default FortuneComparison;
