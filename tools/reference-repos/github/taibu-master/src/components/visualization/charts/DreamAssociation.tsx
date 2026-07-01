'use client';

import { memo, useState } from 'react';
import type { DreamAssociationData } from '@/lib/visualization/chart-types';
import { useChartEntrance, CHART_ENTRANCE_BASE, CHART_ENTRANCE_ACTIVE } from '@/components/visualization/shared/useChartEntrance';
import ChartEmpty from '@/components/visualization/shared/ChartEmpty';

interface DreamAssociationProps {
  data: DreamAssociationData;
  compact?: boolean;
  className?: string;
}

type DreamSentiment = DreamAssociationData['data']['nodes'][number]['sentiment'];

const TYPE_COLORS: Record<DreamSentiment, string> = {
  positive: '#22c55e',
  negative: '#ef4444',
  neutral: '#9ca3af',
};

const DREAM_SENTIMENT_LABELS: Record<DreamSentiment, string> = {
  positive: '积极',
  negative: '消极',
  neutral: '中性',
};

export function getDreamSentimentLabel(sentiment: DreamSentiment): string {
  return DREAM_SENTIMENT_LABELS[sentiment];
}

function DreamAssociationInner({ data, compact = false, className = '' }: DreamAssociationProps) {
  const { ref, entered } = useChartEntrance();
  const { nodes, edges } = data.data;
  const [activeNode, setActiveNode] = useState<string | null>(null);

  if (nodes.length === 0) {
    return <ChartEmpty message="暂无梦境数据" />;
  }

  const radius = compact ? 80 : 120;
  const centerX = 150;
  const centerY = 150;

  const nodePositions = nodes.map((node, idx) => {
    const angle = (idx / nodes.length) * 2 * Math.PI - Math.PI / 2;
    return {
      ...node,
      x: centerX + radius * Math.cos(angle),
      y: centerY + radius * Math.sin(angle),
    };
  });

  const connectedNodes = activeNode
    ? new Set(edges.filter(e => e.from === activeNode || e.to === activeNode).flatMap(e => [e.from, e.to]))
    : null;

  return (
    <div ref={ref} className={`${CHART_ENTRANCE_BASE} ${entered ? CHART_ENTRANCE_ACTIVE : ''} ${className}`}>
      <svg viewBox="0 0 300 300" className="w-full h-auto">
        {edges.map((edge, idx) => {
          const source = nodePositions.find(n => n.id === edge.from);
          const target = nodePositions.find(n => n.id === edge.to);
          if (!source || !target) return null;

          const isActive = !activeNode || connectedNodes?.has(edge.from) || connectedNodes?.has(edge.to);

          return (
            <g key={idx}>
              <line
                x1={source.x}
                y1={source.y}
                x2={target.x}
                y2={target.y}
                stroke="var(--color-border)"
                strokeWidth="1.5"
                opacity={isActive ? 0.4 : 0.1}
              />
              {edge.label && !compact && (
                <text
                  x={(source.x + target.x) / 2}
                  y={(source.y + target.y) / 2}
                  fill="var(--color-foreground-tertiary)"
                  fontSize="9"
                  textAnchor="middle"
                  opacity={isActive ? 0.8 : 0.3}
                >
                  {edge.label}
                </text>
              )}
            </g>
          );
        })}

        {nodePositions.map((node) => {
          const isActive = !activeNode || activeNode === node.id || connectedNodes?.has(node.id);
          const color = TYPE_COLORS[node.sentiment];

          return (
            <g
              key={node.id}
              onMouseEnter={() => setActiveNode(node.id)}
              onMouseLeave={() => setActiveNode(null)}
              style={{ cursor: 'pointer' }}
            >
              <circle
                cx={node.x}
                cy={node.y}
                r={compact ? 18 : 24}
                fill={color}
                opacity={isActive ? 0.9 : 0.3}
              />
              <text
                x={node.x}
                y={node.y}
                fill="white"
                fontSize={compact ? 10 : 11}
                textAnchor="middle"
                dominantBaseline="middle"
                fontWeight="500"
                opacity={isActive ? 1 : 0.5}
              >
                {node.label}
              </text>
            </g>
          );
        })}
      </svg>

      {!compact && (
        <div className="flex items-center justify-center gap-4 mt-3">
          {(Object.keys(TYPE_COLORS) as DreamSentiment[]).map((type) => (
            <div key={type} className="flex items-center gap-1.5">
              <div className="w-3 h-3 rounded-full" style={{ backgroundColor: TYPE_COLORS[type] }} />
              <span className="text-xs text-foreground-secondary">
                {getDreamSentimentLabel(type)}
              </span>
            </div>
          ))}
        </div>
      )}
    </div>
  );
}

export const DreamAssociation = memo(DreamAssociationInner);
export default DreamAssociation;
