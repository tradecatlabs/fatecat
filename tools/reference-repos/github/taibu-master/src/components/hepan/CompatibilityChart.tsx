/**
 * 兼容性雷达图组件
 */
'use client';

import { type CompatibilityDimension, getCompatibilityLevel } from '@/lib/divination/hepan';

interface CompatibilityChartProps {
    dimensions: CompatibilityDimension[];
    overallScore: number;
}

export function CompatibilityChart({ dimensions, overallScore }: CompatibilityChartProps) {
    const { level, color } = getCompatibilityLevel(overallScore);

    return (
        <div className="bg-background/5 backdrop-blur-md border border-white/10 rounded-3xl p-6 sm:p-8">
            {/* 总分 */}
            <div className="text-center mb-8 relative">
                <div className="relative inline-flex items-center justify-center">
                    {/* 背景光晕 */}
                    <div className="absolute inset-0 bg-rose-500/20 blur-3xl rounded-full" />

                    <svg className="w-40 h-40 transform -rotate-90 relative z-10">
                        {/* 轨道 */}
                        <circle
                            cx="80"
                            cy="80"
                            r="70"
                            fill="none"
                            stroke="currentColor"
                            strokeWidth="8"
                            className="text-white/5"
                        />
                        {/* 进度条 */}
                        <circle
                            cx="80"
                            cy="80"
                            r="70"
                            fill="none"
                            stroke="currentColor"
                            strokeWidth="8"
                            strokeDasharray={`${overallScore * 4.4} 440`}
                            strokeLinecap="round"
                            className="text-rose-500 drop-shadow-[0_0_10px_rgba(244,63,94,0.5)] transition-all duration-1000 ease-out"
                        />
                    </svg>
                    <div className="absolute inset-0 flex flex-col items-center justify-center z-10">
                        <span className="text-4xl font-bold text-foreground tracking-tight">{overallScore}</span>
                        <span className={`text-base font-medium mt-1 px-3 py-0.5 rounded-full bg-background/5 border border-white/10 ${color}`}>
                            {level}
                        </span>
                    </div>
                </div>
                <p className="text-sm font-medium text-foreground-secondary mt-4 uppercase tracking-wider">综合契合度</p>
            </div>

            {/* 维度列表 */}
            <div className="space-y-6">
                {dimensions.map((dim, index) => {
                    const { color: dimColor } = getCompatibilityLevel(dim.score);
                    return (
                        <div key={index} className="relative">
                            <div className="flex justify-between items-center mb-2">
                                <span className="text-base font-medium text-foreground flex items-center gap-2">
                                    {dim.name}
                                </span>
                                <span className={`text-sm font-bold ${dimColor}`}>{dim.score}分</span>
                            </div>

                            {/* 进度条轨道 */}
                            <div className="h-2.5 bg-background/5 rounded-full overflow-hidden border border-white/5">
                                <div
                                    className="h-full bg-indigo-500 shadow-[0_0_10px_rgba(99,102,241,0.5)] rounded-full transition-all duration-1000 ease-out relative overflow-hidden"
                                    style={{ width: `${dim.score}%` }}
                                >
                                    <div className="absolute inset-0 bg-background/20" />
                                </div>
                            </div>

                            <p className="text-xs text-foreground-secondary/70 mt-1.5 leading-relaxed">
                                {dim.description}
                            </p>
                        </div>
                    );
                })}
            </div>
        </div>
    );
}
