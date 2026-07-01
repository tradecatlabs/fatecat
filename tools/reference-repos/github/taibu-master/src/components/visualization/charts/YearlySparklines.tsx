'use client';

import { memo } from 'react';
import type { YearlySparklinesData } from '@/lib/visualization/chart-types';
import { useChartEntrance, CHART_ENTRANCE_BASE, CHART_ENTRANCE_ACTIVE } from '@/components/visualization/shared/useChartEntrance';
import ChartEmpty from '@/components/visualization/shared/ChartEmpty';

interface YearlySparklinesProps {
  data: YearlySparklinesData;
  compact?: boolean;
  className?: string;
}

type YearlySparklineDimension = YearlySparklinesData['data']['dimensions'][number];

function YearlySparklinesInner({ data, compact = false, className = '' }: YearlySparklinesProps) {
  const { ref, entered } = useChartEntrance();
  const { dimensions } = data.data;

  if (dimensions.length === 0) {
    return <ChartEmpty message="暂无年度数据" />;
  }

  const maxScore = Math.max(...dimensions.flatMap((d: YearlySparklineDimension) => d.monthlyScores));
  const minScore = Math.min(...dimensions.flatMap((d: YearlySparklineDimension) => d.monthlyScores));
  const range = maxScore - minScore || 1;

  return (
    <div ref={ref} className={`space-y-3 ${CHART_ENTRANCE_BASE} ${entered ? CHART_ENTRANCE_ACTIVE : ''} ${className}`}>
      {dimensions.map((dim: YearlySparklineDimension) => {
        const points = dim.monthlyScores.map((score: number, idx: number) => {
          const x = (idx / 11) * 100;
          const y = 100 - ((score - minScore) / range) * 100;
          return `${x},${y}`;
        }).join(' ');

        const avg = dim.monthlyScores.reduce((a: number, b: number) => a + b, 0) / 12;
        const color = avg >= 70 ? '#22c55e' : avg >= 50 ? '#f59e0b' : '#ef4444';

        return (
          <div key={dim.key} className="flex items-center gap-3">
            <div className="w-16 text-sm font-medium text-foreground tabular-nums shrink-0">
              {dim.label}
            </div>
            <div className="flex-1 relative h-12 bg-background-secondary/30 rounded-lg overflow-hidden">
              <svg viewBox="0 0 100 100" preserveAspectRatio="none" className="w-full h-full">
                <polyline
                  points={points}
                  fill="none"
                  stroke={color}
                  strokeWidth="3"
                  strokeLinecap="round"
                  strokeLinejoin="round"
                  vectorEffect="non-scaling-stroke"
                />
              </svg>
            </div>
            {!compact && (
              <div className="w-12 text-xs text-foreground-secondary tabular-nums text-right shrink-0">
                {Math.round(avg)}
              </div>
            )}
          </div>
        );
      })}
    </div>
  );
}

export const YearlySparklines = memo(YearlySparklinesInner);
export default YearlySparklines;
