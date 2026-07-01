'use client';

import type { MBTISpectrumData } from '@/lib/visualization/chart-types';
import { useChartEntrance, CHART_ENTRANCE_BASE, CHART_ENTRANCE_ACTIVE } from '@/components/visualization/shared/useChartEntrance';
import ChartEmpty from '@/components/visualization/shared/ChartEmpty';

interface MBTISpectrumProps {
  data: MBTISpectrumData;
  compact?: boolean;
  className?: string;
}

export default function MBTISpectrum({ data, className = '' }: MBTISpectrumProps) {
  const { ref, entered } = useChartEntrance();
  const { dimensions, type } = data.data;

  if (!dimensions || !type) {
    return <ChartEmpty message="暂无 MBTI 数据" />;
  }

  const dimensionArray = Object.entries(dimensions).map(([axis, value]) => ({
    axis: axis as 'EI' | 'SN' | 'TF' | 'JP',
    ...value,
  }));

  return (
    <div ref={ref} className={`space-y-4 ${CHART_ENTRANCE_BASE} ${entered ? CHART_ENTRANCE_ACTIVE : ''} ${className}`}>
      {/* MBTI Type Badge */}
      <div className="flex justify-center">
        <div className="px-6 py-3 rounded-xl bg-[var(--color-accent)] text-[var(--color-background)] text-2xl font-bold tracking-wider">
          {type}
        </div>
      </div>

      {/* Spectrum Bars */}
      <div className="space-y-4">
        {dimensionArray.map((dim) => {
          const percentage = ((dim.score + 50) / 100) * 100;
          const isLeft = dim.score < 0;

          return (
            <div key={dim.axis} className="space-y-1.5">
              {/* Labels */}
              <div className="flex justify-between text-xs font-medium">
                <span className={isLeft ? 'text-[var(--color-accent)]' : 'text-[var(--color-foreground-secondary)]'}>
                  {dim.axis[0]}
                </span>
                <span className={!isLeft ? 'text-[var(--color-accent)]' : 'text-[var(--color-foreground-secondary)]'}>
                  {dim.axis[1]}
                </span>
              </div>

              {/* Bar */}
              <div className="relative h-8 bg-[var(--color-background-secondary)] rounded-full overflow-hidden">
                <div className="absolute inset-0 flex">
                  <div className="flex-1 border-r border-[var(--color-border)]" />
                  <div className="flex-1" />
                </div>
                <div
                  className="absolute top-0 h-full bg-[var(--color-accent)] transition-all duration-700"
                  style={{
                    left: `${Math.min(percentage, 50)}%`,
                    width: `${Math.abs(percentage - 50)}%`,
                  }}
                />
                <div
                  className="absolute top-1/2 -translate-y-1/2 w-3 h-3 rounded-full bg-[var(--color-foreground)] border-2 border-[var(--color-background)] transition-all duration-700"
                  style={{ left: `calc(${percentage}% - 6px)` }}
                />
              </div>

              {/* Score */}
              <div className="text-center text-xs text-[var(--color-foreground-secondary)] tabular-nums">
                {dim.score > 0 ? '+' : ''}{dim.score}
              </div>
            </div>
          );
        })}
      </div>
    </div>
  );
}
