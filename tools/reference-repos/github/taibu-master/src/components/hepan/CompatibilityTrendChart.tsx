/**
 * 合盘兼容性趋势图组件
 *
 * 显示半年/一年的兼容性走势曲线
 */
'use client';

import {
    XAxis,
    YAxis,
    CartesianGrid,
    Tooltip,
    ResponsiveContainer,
    ReferenceLine,
    Area,
    AreaChart,
} from 'recharts';
import { TrendingUp, CalendarDays } from 'lucide-react';

export interface CompatibilityTrendPoint {
    month: string;           // 月份标签 (e.g., "1月", "2月")
    fullMonth: string;       // 完整日期 (e.g., "2024-01")
    score: number;           // 兼容性分数 (0-100)
    dimension?: {
        wuxing: number;      // 五行配合
        communication: number; // 沟通契合
        emotion: number;     // 情感共鸣
    };
    event?: string;          // 特殊事件提示
}

type CompatibilityTooltipProps = {
    active?: boolean;
    payload?: { payload: CompatibilityTrendPoint }[];
};

function CompatibilityTrendTooltip({ active, payload }: CompatibilityTooltipProps) {
    if (!active || !payload || !payload.length) return null;

    const point = payload[0].payload;
    return (
        <div className="bg-background/95 backdrop-blur-xl border border-border rounded-xl p-4 shadow-xl ring-1 ring-white/10">
            <div className="flex items-center gap-2 mb-2 pb-2 border-b border-border/50">
                <CalendarDays className="w-4 h-4 text-foreground-secondary" />
                <span className="font-medium text-foreground">{point.fullMonth}</span>
            </div>

            <div className="flex items-baseline gap-2 mb-3">
                <span className="text-2xl font-bold text-indigo-500">{point.score}</span>
                <span className="text-sm text-foreground-secondary">分</span>
            </div>

            {point.dimension && (
                <div className="space-y-1.5 text-xs text-foreground-secondary">
                    <div className="flex justify-between gap-4">
                        <span>五行配合</span>
                        <span className="font-medium text-foreground">{point.dimension.wuxing}</span>
                    </div>
                    <div className="flex justify-between gap-4">
                        <span>沟通契合</span>
                        <span className="font-medium text-foreground">{point.dimension.communication}</span>
                    </div>
                    <div className="flex justify-between gap-4">
                        <span>情感共鸣</span>
                        <span className="font-medium text-foreground">{point.dimension.emotion}</span>
                    </div>
                </div>
            )}
            {point.event && (
                <div className="mt-3 pt-2 border-t border-border/50 text-xs font-medium text-amber-500 flex items-start gap-1">
                    <span>⚡</span>
                    {point.event}
                </div>
            )}
        </div>
    );
}

interface CompatibilityTrendChartProps {
    data: CompatibilityTrendPoint[];
    period: 6 | 12;
    onPeriodChange?: (period: 6 | 12) => void;
    height?: number;
}

export function CompatibilityTrendChart({
    data,
    period,
    onPeriodChange,
    height = 320,
}: CompatibilityTrendChartProps) {
    // 计算平均分
    const averageScore = Math.round(
        data.reduce((sum, d) => sum + d.score, 0) / data.length
    );

    // 找出最高和最低点
    const maxPoint = data.reduce((max, d) => (d.score > max.score ? d : max), data[0]);
    const minPoint = data.reduce((min, d) => (d.score < min.score ? d : min), data[0]);

    // 计算趋势（正向、负向、平稳）
    const firstHalf = data.slice(0, Math.floor(data.length / 2));
    const secondHalf = data.slice(Math.floor(data.length / 2));
    const firstAvg = firstHalf.reduce((sum, d) => sum + d.score, 0) / firstHalf.length;
    const secondAvg = secondHalf.reduce((sum, d) => sum + d.score, 0) / secondHalf.length;
    const trend = secondAvg - firstAvg > 3 ? 'up' : secondAvg - firstAvg < -3 ? 'down' : 'stable';

    const trendText = trend === 'up' ? '整体呈上升趋势' : trend === 'down' ? '整体呈下降趋势' : '整体较为平稳';
    const trendColor = trend === 'up' ? 'text-emerald-500' : trend === 'down' ? 'text-rose-500' : 'text-amber-500';

    return (
        <div className="bg-background/5 backdrop-blur-md rounded-3xl p-6 border border-white/10">
            {/* 标题和时间选择 */}
            <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-4 mb-8">
                <div>
                    <h3 className="text-lg font-bold text-foreground flex items-center gap-2">
                        <div className="p-1.5 rounded-lg bg-indigo-500/10 text-indigo-500">
                            <TrendingUp className="w-5 h-5" />
                        </div>
                        兼容性走势
                    </h3>
                    <p className="text-sm text-foreground-secondary mt-1 ml-9">
                        未来{period}个月的感情能量波动预测
                    </p>
                </div>

                {onPeriodChange && (
                    <div className="flex items-center bg-background/5 rounded-xl p-1 border border-white/5 self-start sm:self-auto">
                        <button
                            onClick={() => onPeriodChange(6)}
                            className={`px-4 py-1.5 text-sm font-medium rounded-lg transition-all ${period === 6
                                ? 'bg-indigo-500 text-white shadow-lg shadow-indigo-500/20'
                                : 'text-foreground-secondary hover:text-foreground'
                                }`}
                        >
                            半年
                        </button>
                        <button
                            onClick={() => onPeriodChange(12)}
                            className={`px-4 py-1.5 text-sm font-medium rounded-lg transition-all ${period === 12
                                ? 'bg-indigo-500 text-white shadow-lg shadow-indigo-500/20'
                                : 'text-foreground-secondary hover:text-foreground'
                                }`}
                        >
                            一年
                        </button>
                    </div>
                )}
            </div>

            {/* 趋势概要 */}
            <div className="grid grid-cols-3 gap-4 mb-8">
                <div className="bg-background/5 rounded-2xl p-4 border border-white/5 flex flex-col items-center justify-center text-center group hover:bg-background/10 transition-colors">
                    <span className="text-xs font-medium text-foreground-secondary mb-1">平均分</span>
                    <span className="text-2xl font-bold text-indigo-500 group-hover:scale-110 transition-transform">{averageScore}</span>
                </div>
                <div className="bg-background/5 rounded-2xl p-4 border border-white/5 flex flex-col items-center justify-center text-center group hover:bg-background/10 transition-colors">
                    <span className="text-xs font-medium text-foreground-secondary mb-1">最高点</span>
                    <span className="text-2xl font-bold text-emerald-500 group-hover:scale-110 transition-transform">{maxPoint?.score}</span>
                    <span className="text-[10px] text-foreground-secondary mt-1 bg-background/5 px-2 py-0.5 rounded-full">{maxPoint?.month}</span>
                </div>
                <div className="bg-background/5 rounded-2xl p-4 border border-white/5 flex flex-col items-center justify-center text-center group hover:bg-background/10 transition-colors">
                    <span className="text-xs font-medium text-foreground-secondary mb-1">最低点</span>
                    <span className="text-2xl font-bold text-rose-500 group-hover:scale-110 transition-transform">{minPoint?.score}</span>
                    <span className="text-[10px] text-foreground-secondary mt-1 bg-background/5 px-2 py-0.5 rounded-full">{minPoint?.month}</span>
                </div>
            </div>

            {/* 图表 */}
            <div className="w-full" style={{ height }}>
                <ResponsiveContainer width="100%" height="100%">
                    <AreaChart
                        data={data}
                        margin={{ top: 10, right: 10, left: -20, bottom: 0 }}
                    >
                        <defs>
                            <linearGradient id="colorScore" x1="0" y1="0" x2="0" y2="1">
                                <stop offset="5%" stopColor="#6366f1" stopOpacity={0.3} />
                                <stop offset="95%" stopColor="#6366f1" stopOpacity={0} />
                            </linearGradient>
                        </defs>
                        <CartesianGrid
                            strokeDasharray="3 3"
                            vertical={false}
                            stroke="rgba(255,255,255,0.05)"
                        />
                        <XAxis
                            dataKey="month"
                            axisLine={false}
                            tickLine={false}
                            tick={{ fontSize: 12, fill: 'var(--foreground-secondary)' }}
                            interval={period === 12 ? 1 : 0}
                            dy={10}
                        />
                        <YAxis
                            domain={[30, 100]}
                            axisLine={false}
                            tickLine={false}
                            tick={{ fontSize: 12, fill: 'var(--foreground-secondary)' }}
                            ticks={[40, 60, 80, 100]}
                        />
                        <Tooltip
                            content={<CompatibilityTrendTooltip />}
                            cursor={{ stroke: 'rgba(255,255,255,0.2)', strokeWidth: 1, strokeDasharray: '5 5' }}
                        />
                        <ReferenceLine
                            y={averageScore}
                            stroke="#6366f1"
                            strokeDasharray="3 3"
                            strokeOpacity={0.4}
                            label={{
                                value: '平均线',
                                position: 'right',
                                fill: '#6366f1',
                                fontSize: 10,
                                opacity: 0.8
                            }}
                        />
                        <Area
                            type="monotone"
                            dataKey="score"
                            stroke="#6366f1"
                            strokeWidth={3}
                            fill="url(#colorScore)"
                            activeDot={{
                                r: 6,
                                stroke: '#6366f1',
                                strokeWidth: 4,
                                fill: '#fff',
                            }}
                            animationDuration={1500}
                        />
                    </AreaChart>
                </ResponsiveContainer>
            </div>

            {/* 底部说明 */}
            <div className="mt-6 flex items-center justify-between text-xs text-foreground-secondary border-t border-white/5 pt-4">
                <div className="flex items-center gap-4">
                    <div className="flex items-center gap-1.5">
                        <div className="w-2.5 h-2.5 rounded-full bg-emerald-500" />
                        <span>波峰</span>
                    </div>
                    <div className="flex items-center gap-1.5">
                        <div className="w-2.5 h-2.5 rounded-full bg-rose-500" />
                        <span>波谷</span>
                    </div>
                </div>
                <div className="font-medium">
                    趋势预测：<span className={trendColor}>{trendText}</span>
                </div>
            </div>
        </div>
    );
}
