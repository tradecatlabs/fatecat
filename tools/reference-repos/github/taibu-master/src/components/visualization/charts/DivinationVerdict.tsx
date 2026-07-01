'use client';

import type { DivinationVerdictData } from '@/lib/visualization/chart-types';
import { useChartEntrance, CHART_ENTRANCE_BASE, CHART_ENTRANCE_ACTIVE } from '@/components/visualization/shared/useChartEntrance';
import ChartEmpty from '@/components/visualization/shared/ChartEmpty';

interface DivinationVerdictProps {
  data: DivinationVerdictData;
  compact?: boolean;
  className?: string;
}

const VERDICT_CONFIG = {
  auspicious: { icon: '✨', color: '#22c55e', bg: 'rgba(34,197,94,0.1)', label: '吉' },
  neutral: { icon: '⚖️', color: '#eab308', bg: 'rgba(234,179,8,0.1)', label: '平' },
  inauspicious: { icon: '⚠️', color: '#ef4444', bg: 'rgba(239,68,68,0.1)', label: '凶' },
};

export default function DivinationVerdict({ data, compact = false, className = '' }: DivinationVerdictProps) {
  const { ref, entered } = useChartEntrance();
  const { verdictScore, confidence, question, keyFactors } = data.data;

  if (verdictScore == null) {
    return <ChartEmpty message="暂无吉凶判断数据" />;
  }

  // Map verdict string to config key
  const verdictKey = verdictScore >= 70 ? 'auspicious' : verdictScore >= 40 ? 'neutral' : 'inauspicious';
  const config = VERDICT_CONFIG[verdictKey];

  // Map confidence to percentage
  const confidenceMap = { high: 90, medium: 70, low: 50 };
  const confidencePercent = confidenceMap[confidence];

  return (
    <div ref={ref} className={`space-y-4 ${CHART_ENTRANCE_BASE} ${entered ? CHART_ENTRANCE_ACTIVE : ''} ${className}`}>
      {/* Verdict Badge */}
      <div className="flex items-center justify-center">
        <div
          className="inline-flex flex-col items-center gap-2 px-8 py-6 rounded-2xl border-2"
          style={{ borderColor: config.color, backgroundColor: config.bg }}
        >
          <div className="text-5xl">{config.icon}</div>
          <div className="text-3xl font-bold" style={{ color: config.color }}>
            {config.label}
          </div>
          {confidencePercent !== undefined && (
            <div className="text-xs text-[var(--color-foreground-secondary)]">
              置信度 {confidencePercent}%
            </div>
          )}
        </div>
      </div>

      {/* Title */}
      {question && (
        <div className="text-center text-base font-bold text-[var(--color-foreground)]">
          {question}
        </div>
      )}

      {/* Keywords */}
      {!compact && keyFactors && keyFactors.length > 0 && (
        <div className="flex flex-wrap justify-center gap-2">
          {keyFactors.slice(0, 5).map((kf, i) => (
            <span
              key={i}
              className="px-2.5 py-1 text-xs rounded-full border"
              style={{ borderColor: config.color, color: config.color, backgroundColor: config.bg }}
            >
              {kf.factor}
            </span>
          ))}
        </div>
      )}
    </div>
  );
}
