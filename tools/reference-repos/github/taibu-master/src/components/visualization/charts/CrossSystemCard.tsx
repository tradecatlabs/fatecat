'use client';

import { memo } from 'react';
import type { CrossSystemData } from '@/lib/visualization/chart-types';
import { useChartEntrance, CHART_ENTRANCE_BASE, CHART_ENTRANCE_ACTIVE } from '@/components/visualization/shared/useChartEntrance';
import ChartEmpty from '@/components/visualization/shared/ChartEmpty';

interface CrossSystemCardProps {
  data: CrossSystemData;
  compact?: boolean;
  className?: string;
}

function CrossSystemCardInner({ data, compact = false, className = '' }: CrossSystemCardProps) {
  const { ref, entered } = useChartEntrance();
  const { systems, advice } = data.data;

  if (systems.length === 0) {
    return <ChartEmpty message="暂无跨系统数据" />;
  }

  return (
    <div ref={ref} className={`space-y-3 ${CHART_ENTRANCE_BASE} ${entered ? CHART_ENTRANCE_ACTIVE : ''} ${className}`}>
      <div className="grid grid-cols-1 sm:grid-cols-2 gap-3">
        {systems.map((sys, idx: number) => {
          const avgScore = Object.values(sys.scores).reduce((a, b) => (a || 0) + (b || 0), 0) / Object.keys(sys.scores).length;
          const color = avgScore >= 80 ? '#22c55e' : avgScore >= 60 ? '#f59e0b' : '#ef4444';

          return (
            <div
              key={idx}
              className="bg-background-secondary/30 border border-border rounded-xl p-3"
            >
              <div className="flex items-center justify-between mb-2">
                <span className="text-sm font-medium text-foreground">{sys.name}</span>
                <span
                  className="text-xs font-bold px-2 py-0.5 rounded-full"
                  style={{ backgroundColor: `${color}20`, color }}
                >
                  {Math.round(avgScore)}
                </span>
              </div>
            </div>
          );
        })}
      </div>

      {!compact && advice && (
        <div className="bg-accent/10 border border-accent/20 rounded-xl p-3">
          <div className="text-xs font-medium text-foreground-secondary mb-1.5">综合解读</div>
          <div className="text-sm text-foreground leading-relaxed">{advice}</div>
        </div>
      )}
    </div>
  );
}

export const CrossSystemCard = memo(CrossSystemCardInner);
export default CrossSystemCard;
