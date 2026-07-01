'use client';

import { useMemo } from 'react';
import { RadialBarChart, RadialBar, ResponsiveContainer, PolarAngleAxis } from 'recharts';
import type { CompatibilityGaugeData } from '@/lib/visualization/chart-types';
import { getScoreColor } from '@/lib/visualization/chart-theme';
import { AnimatedNumber } from '@/components/visualization/shared/AnimatedNumber';
import { ScoreBar } from '@/components/visualization/shared/ScoreBar';
import { useChartEntrance, CHART_ENTRANCE_BASE, CHART_ENTRANCE_ACTIVE } from '@/components/visualization/shared/useChartEntrance';
import ChartEmpty from '@/components/visualization/shared/ChartEmpty';

interface CompatibilityGaugeProps {
  data: CompatibilityGaugeData;
  compact?: boolean;
  className?: string;
}

export default function CompatibilityGauge({ data, compact = false, className = '' }: CompatibilityGaugeProps) {
  const { ref, entered } = useChartEntrance();
  const { overallScore, dimensions } = data.data;

  const gaugeData = useMemo(() => [{ value: overallScore ?? 0, fill: getScoreColor(overallScore ?? 0) }], [overallScore]);

  if (overallScore == null || !dimensions) {
    return <ChartEmpty message="暂无兼容度数据" />;
  }


  return (
    <div ref={ref} className={`space-y-4 ${CHART_ENTRANCE_BASE} ${entered ? CHART_ENTRANCE_ACTIVE : ''} ${className}`}>
      {/* Radial Gauge */}
      <div className="relative">
        <ResponsiveContainer width="100%" height={compact ? 180 : 220}>
          <RadialBarChart
            cx="50%"
            cy="50%"
            innerRadius="70%"
            outerRadius="100%"
            data={gaugeData}
            startAngle={180}
            endAngle={0}
          >
            <PolarAngleAxis type="number" domain={[0, 100]} angleAxisId={0} tick={false} />
            <RadialBar
              background={{ fill: 'var(--color-background-secondary)' }}
              dataKey="value"
              cornerRadius={8}
              animationDuration={1200}
            />
          </RadialBarChart>
        </ResponsiveContainer>

        {/* Center Score */}
        <div className="absolute inset-0 flex items-center justify-center pointer-events-none">
          <div className="text-center" style={{ marginTop: compact ? '-20px' : '-30px' }}>
            <div className="text-4xl font-bold" style={{ color: getScoreColor(overallScore) }}>
              <AnimatedNumber value={overallScore} />
            </div>
            <div className="text-xs text-[var(--color-foreground-secondary)] mt-1">匹配度</div>
          </div>
        </div>
      </div>

      {/* Dimensions */}
      {!compact && dimensions && dimensions.length > 0 && (
        <div className="space-y-2.5">
          {dimensions.map((dim) => (
            <div key={dim.key} className="space-y-1">
              <div className="flex items-center justify-between text-xs">
                <span className="text-[var(--color-foreground)]">{dim.label}</span>
                <span className="font-bold tabular-nums" style={{ color: getScoreColor(dim.score) }}>
                  {dim.score}
                </span>
              </div>
              <ScoreBar score={dim.score} color={getScoreColor(dim.score)} height={6} showLabel={false} />
              {dim.detail && (
                <p className="text-[10px] text-[var(--color-foreground-secondary)] leading-relaxed">
                  {dim.detail}
                </p>
              )}
            </div>
          ))}
        </div>
      )}
    </div>
  );
}
