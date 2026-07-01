/**
 * Fortune Radar Chart
 *
 * Multi-dimensional radar chart showing current fortune scores.
 * Features primary radar with solid fill, optional comparison overlay,
 * center overall score display, score bars grid, and advice card.
 */
'use client';

import { useMemo } from 'react';
import { useChartEntrance, CHART_ENTRANCE_BASE, CHART_ENTRANCE_ACTIVE } from '@/components/visualization/shared/useChartEntrance';
import ChartEmpty from '@/components/visualization/shared/ChartEmpty';
import {
  RadarChart,
  Radar,
  PolarGrid,
  PolarAngleAxis,
  PolarRadiusAxis,
  ResponsiveContainer,
} from 'recharts';
import type { FortuneDimensionKey } from '@/lib/visualization/dimensions';
import {
  getDimensionConfig,
  getDimensionsByKeys,
  DEFAULT_DIMENSIONS,
} from '@/lib/visualization/dimensions';
import {
  getDimensionColor,
  getScoreColor,
} from '@/lib/visualization/chart-theme';
import type { FortuneRadarData } from '@/lib/visualization/chart-types';
import { ScoreBar } from '@/components/visualization/shared/ScoreBar';
import TrendIndicator from '@/components/visualization/shared/TrendIndicator';
import { AnimatedNumber } from '@/components/visualization/shared/AnimatedNumber';

// ===== Types =====

interface FortuneRadarProps {
  data: FortuneRadarData;
  compact?: boolean;
  selectedDimensions?: FortuneDimensionKey[];
}

// Data point for Recharts RadarChart
interface RadarDataPoint {
  dimension: string;
  label: string;
  score: number;
  previousScore?: number;
  fullMark: number;
}

// ===== Constants =====

const RADAR_HEIGHT_DESKTOP = 300;
const RADAR_HEIGHT_COMPACT = 220;

// ===== Custom Angle Axis Tick =====

function CustomAngleAxisTick({
  x,
  y,
  payload,
  dimensionColors,
}: {
  x?: number;
  y?: number;
  payload?: { value: string };
  dimensionColors: Record<string, string>;
}) {
  if (!x || !y || !payload) return null;

  const dimKey = payload.value;
  const config = getDimensionConfig(dimKey as FortuneDimensionKey);
  const label = config?.label ?? dimKey;
  const color = dimensionColors[dimKey] ?? 'var(--color-foreground-secondary)';

  return (
    <g transform={`translate(${x},${y})`}>
      <text
        x={0}
        y={0}
        textAnchor="middle"
        dominantBaseline="central"
        fill={color}
        fontSize={11}
        fontWeight={500}
      >
        {label}
      </text>
    </g>
  );
}

// ===== Main Component =====

function FortuneRadarInner({
  data,
  compact = false,
  selectedDimensions,
}: FortuneRadarProps) {
  const { ref, entered } = useChartEntrance();
  const { scores, previousScores, overallScore, overallLabel, topAdvice, period } = data.data;

  // Determine which dimensions to show
  const dimensionKeys = useMemo(() => {
    if (selectedDimensions && selectedDimensions.length > 0) {
      return selectedDimensions.filter((k) => k in scores);
    }
    const scoreKeys = Object.keys(scores) as FortuneDimensionKey[];
    if (scoreKeys.length > 0) return scoreKeys;
    return DEFAULT_DIMENSIONS;
  }, [selectedDimensions, scores]);

  // Build radar data points
  const radarData = useMemo((): RadarDataPoint[] => {
    return dimensionKeys.map((key) => {
      const scoreEntry = scores[key];
      return {
        dimension: key,
        label: scoreEntry?.label ?? getDimensionConfig(key)?.label ?? key,
        score: scoreEntry?.score ?? 0,
        previousScore: previousScores?.[key],
        fullMark: 100,
      };
    });
  }, [dimensionKeys, scores, previousScores]);

  // Map dimension keys to their colors for axis labels
  const dimensionColors = useMemo(() => {
    const map: Record<string, string> = {};
    for (const key of dimensionKeys) {
      map[key] = getDimensionColor(key);
    }
    return map;
  }, [dimensionKeys]);

  const hasPreviousScores = previousScores && Object.keys(previousScores).length > 0;

  const radarHeight = compact ? RADAR_HEIGHT_COMPACT : RADAR_HEIGHT_DESKTOP;

  if (dimensionKeys.length === 0) {
    return <ChartEmpty message="暂无运势评分数据" />;
  }

  return (
    <div ref={ref} className={`space-y-4 ${CHART_ENTRANCE_BASE} ${entered ? CHART_ENTRANCE_ACTIVE : ''}`}>
      {/* Title */}
      {!compact && (data.title || data.subtitle) && (
        <div>
          {data.title && (
            <h3 className="text-base font-bold text-[var(--color-foreground)]">{data.title}</h3>
          )}
          {data.subtitle && (
            <p className="text-xs text-[var(--color-foreground-secondary)] mt-0.5">
              {data.subtitle}
            </p>
          )}
        </div>
      )}

      {/* Radar Chart with Center Score */}
      <div className="relative">
        <ResponsiveContainer width="100%" height={radarHeight}>
          <RadarChart
            data={radarData}
            cx="50%"
            cy="50%"
            outerRadius={compact ? '65%' : '70%'}
          >
            <PolarGrid
              stroke="var(--color-border)"
              strokeOpacity={0.4}
              gridType="polygon"
            />

            <PolarAngleAxis
              dataKey="dimension"
              tick={<CustomAngleAxisTick dimensionColors={dimensionColors} />}
              tickLine={false}
            />

            <PolarRadiusAxis
              angle={90}
              domain={[0, 100]}
              tick={{ fontSize: 9, fill: 'var(--color-foreground-tertiary)' }}
              tickCount={5}
              axisLine={false}
            />

            {/* Previous scores (comparison, dashed outline) */}
            {hasPreviousScores && (
              <Radar
                name="上期"
                dataKey="previousScore"
                stroke="var(--color-foreground-tertiary)"
                strokeWidth={1.5}
                strokeDasharray="4 3"
                fill="var(--color-foreground-tertiary)"
                fillOpacity={0.08}
                isAnimationActive={true}
                animationDuration={800}
              />
            )}

            {/* Current scores (primary radar) */}
            <Radar
              name="当前"
              dataKey="score"
              stroke="var(--color-accent, #D4AF37)"
              strokeWidth={2}
              fill="var(--color-accent, #D4AF37)"
              fillOpacity={0.2}
              dot={{
                r: 3,
                fill: 'var(--color-accent, #D4AF37)',
                stroke: 'var(--color-background)',
                strokeWidth: 1.5,
              }}
              isAnimationActive={true}
              animationDuration={1200}
              animationEasing="ease-out"
            />
          </RadarChart>
        </ResponsiveContainer>

        {/* Center overall score overlay */}
        <div className="absolute inset-0 flex items-center justify-center pointer-events-none">
          <div className="text-center">
            <div className="text-3xl font-bold" style={{ color: getScoreColor(overallScore) }}>
              <AnimatedNumber value={overallScore} />
            </div>
            <div className="text-xs text-[var(--color-foreground-secondary)] mt-0.5">
              {overallLabel}
            </div>
            {period && (
              <div className="text-[10px] text-[var(--color-foreground-tertiary)] mt-0.5">
                {period}
              </div>
            )}
          </div>
        </div>
      </div>

      {/* Score Bars Grid */}
      <div className={`grid gap-2.5 ${compact ? 'grid-cols-1' : 'grid-cols-1 sm:grid-cols-2'}`}>
        {getDimensionsByKeys(dimensionKeys).map((dimConfig) => {
          const scoreEntry = scores[dimConfig.key];
          if (!scoreEntry) return null;

          return (
            <div
              key={dimConfig.key}
              className="flex items-center gap-2 bg-[var(--color-background-secondary)]/40 rounded-lg px-2.5 py-2"
            >
              {/* Dimension icon + label */}
              <div className="flex items-center gap-1.5 min-w-[80px] shrink-0">
                <span className="text-sm">{dimConfig.icon}</span>
                <span className="text-xs font-medium text-[var(--color-foreground)]">
                  {dimConfig.label}
                </span>
              </div>

              {/* Score bar */}
              <div className="flex-1">
                <ScoreBar
                  score={scoreEntry.score}
                  color={getDimensionColor(dimConfig.key)}
                  height={6}
                  showLabel={false}
                />
              </div>

              {/* Score value + trend */}
              <div className="flex items-center gap-1 shrink-0">
                <span
                  className="text-xs font-bold tabular-nums"
                  style={{ color: getDimensionColor(dimConfig.key) }}
                >
                  {scoreEntry.score}
                </span>
                <TrendIndicator trend={scoreEntry.trend} size="sm" />
              </div>
            </div>
          );
        })}
      </div>

      {/* Legend for comparison mode */}
      {hasPreviousScores && !compact && (
        <div className="flex items-center gap-4 text-xs text-[var(--color-foreground-secondary)]">
          <div className="flex items-center gap-1.5">
            <div className="w-4 h-0.5 bg-[var(--color-accent,#D4AF37)]" />
            <span>当前</span>
          </div>
          <div className="flex items-center gap-1.5">
            <div className="w-4 h-0.5 border-t border-dashed border-[var(--color-foreground-tertiary)]" />
            <span>上期</span>
          </div>
        </div>
      )}

      {/* Top Advice */}
      {topAdvice && !compact && (
        <div className="bg-[var(--color-background-secondary)]/50 border border-[var(--color-border)]/50 rounded-xl p-3">
          <div className="text-xs text-[var(--color-foreground-secondary)] leading-relaxed">
            {topAdvice}
          </div>
        </div>
      )}
    </div>
  );
}

export const FortuneRadar = FortuneRadarInner;
export default FortuneRadar;
