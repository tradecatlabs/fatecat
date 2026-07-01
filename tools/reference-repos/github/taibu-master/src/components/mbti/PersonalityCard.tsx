/**
 * MBTI 性格类型展示卡片
 */
'use client';

import { useState, useEffect } from 'react';
import { type Dimension, type TestResult, type PersonalityData, PERSONALITY_BASICS, loadPersonalityData, getDimensionDescription } from '@/lib/divination/mbti';
import { ChevronDown, ChevronUp } from 'lucide-react';

interface PersonalityCardProps {
    result: TestResult;
    showDimensions?: boolean;  // 是否显示维度分析（默认 true）
}

function DimensionBar({ left, right, leftPercent, rightPercent }: {
    left: Dimension;
    right: Dimension;
    leftPercent: number;
    rightPercent: number;
}) {
    const leftInfo = getDimensionDescription(left);
    const rightInfo = getDimensionDescription(right);
    const isLeftDominant = leftPercent >= rightPercent;

    return (
        <div className="mb-5 last:mb-0">
            <div className="flex justify-between text-sm mb-2 font-medium">
                <span className={isLeftDominant ? 'text-blue-300 drop-shadow-[0_0_8px_rgba(147,197,253,0.3)]' : 'text-foreground-secondary'}>
                    {leftInfo.name} ({left}) {leftPercent}%
                </span>
                <span className={!isLeftDominant ? 'text-purple-300 drop-shadow-[0_0_8px_rgba(216,180,254,0.3)]' : 'text-foreground-secondary'}>
                    {rightPercent}% ({right}) {rightInfo.name}
                </span>
            </div>
            <div className="h-2.5 bg-background/5 rounded-full overflow-hidden flex ring-1 ring-white/10">
                <div
                    className={`h-full transition-all duration-1000 ease-out ${isLeftDominant ? 'bg-gradient-to-r from-blue-400 to-indigo-500 shadow-[0_0_10px_rgba(59,130,246,0.5)]' : 'bg-transparent'}`}
                    style={{ width: `${leftPercent}%` }}
                />
                <div
                    className={`h-full transition-all duration-1000 ease-out ${!isLeftDominant ? 'bg-gradient-to-l from-purple-400 to-fuchsia-500 shadow-[0_0_10px_rgba(168,85,247,0.5)]' : 'bg-transparent'}`}
                    style={{ width: `${rightPercent}%` }}
                />
            </div>
        </div>
    );
}

export function PersonalityCard({ result, showDimensions = true }: PersonalityCardProps) {
    const [personalityData, setPersonalityData] = useState<PersonalityData | null>(null);
    const [loading, setLoading] = useState(true);
    const [expandedSections, setExpandedSections] = useState<string[]>(['概览']);

    const basic = PERSONALITY_BASICS[result.type];

    useEffect(() => {
        loadPersonalityData(result.type).then((data) => {
            setPersonalityData(data);
            setLoading(false);
        });
    }, [result.type]);

    const toggleSection = (section: string) => {
        setExpandedSections(prev =>
            prev.includes(section)
                ? prev.filter(s => s !== section)
                : [...prev, section]
        );
    };

    return (
        <div className="max-w-3xl mx-auto space-y-8 animate-fade-in">
            {/* 头部：类型标识 */}
            <div className="relative overflow-hidden rounded-[2rem] p-8 md:p-10 text-center group">
                {/* Background Gradient */}
                <div className="absolute inset-0 bg-gradient-to-br from-indigo-500/20 via-purple-500/10 to-pink-500/20 backdrop-blur-xl border border-white/10" />

                {/* Decorative glow */}
                <div className="absolute top-0 left-1/2 -translate-x-1/2 w-32 h-32 bg-purple-500/20 blur-[50px] rounded-full pointer-events-none" />

                <div className="relative z-10">
                    <div className="text-7xl mb-6 transform transition-transform group-hover:scale-110 duration-500 drop-shadow-[0_0_15px_rgba(255,255,255,0.2)]">
                        {basic.emoji}
                    </div>
                    <h1 className="text-5xl font-bold text-transparent bg-clip-text bg-gradient-to-r from-white to-white/70 mb-3 tracking-tight">
                        {result.type}
                    </h1>
                    <h2 className="text-2xl font-semibold text-purple-300 mb-4">{basic.title}</h2>
                    <p className="text-foreground-secondary max-w-lg mx-auto leading-relaxed text-lg">
                        {basic.description}
                    </p>
                </div>
            </div>

            {/* 维度分析 - 可选显示 */}
            {showDimensions && result.percentages && (
                <div className="bg-background/5 backdrop-blur-md rounded-2xl p-6 md:p-8 border border-white/10 shadow-xl">
                    <h3 className="text-lg font-bold text-white mb-6 flex items-center gap-2">
                        <span className="w-1 h-5 bg-blue-500 rounded-full shadow-[0_0_8px_rgba(59,130,246,0.5)]"></span>
                        维度分析
                    </h3>
                    <div className="space-y-6">
                        <DimensionBar
                            left="E" right="I"
                            leftPercent={result.percentages.EI.E}
                            rightPercent={result.percentages.EI.I}
                        />
                        <DimensionBar
                            left="S" right="N"
                            leftPercent={result.percentages.SN.S}
                            rightPercent={result.percentages.SN.N}
                        />
                        <DimensionBar
                            left="T" right="F"
                            leftPercent={result.percentages.TF.T}
                            rightPercent={result.percentages.TF.F}
                        />
                        <DimensionBar
                            left="J" right="P"
                            leftPercent={result.percentages.JP.J}
                            rightPercent={result.percentages.JP.P}
                        />
                    </div>
                </div>
            )}

            {/* 详细描述 */}
            {loading ? (
                <div className="space-y-4">
                    {/* 标题骨架 */}
                    <div className="flex items-center gap-2 px-2">
                        <div className="w-1 h-5 rounded-full bg-purple-500/30 animate-pulse" />
                        <div className="h-5 w-20 rounded bg-background/10 animate-pulse" />
                    </div>
                    {/* 折叠卡片骨架 */}
                    {[1, 2, 3, 4].map(i => (
                        <div key={i} className="bg-background/5 border border-white/5 rounded-2xl p-5">
                            <div className="flex items-center justify-between">
                                <div className="h-5 w-32 rounded bg-background/10 animate-pulse" />
                                <div className="w-5 h-5 rounded bg-background/10 animate-pulse" />
                            </div>
                        </div>
                    ))}
                </div>
            ) : personalityData ? (
                <div className="space-y-4">
                    <h3 className="text-lg font-bold text-white mb-4 px-2 flex items-center gap-2">
                        <span className="w-1 h-5 bg-purple-500 rounded-full shadow-[0_0_8px_rgba(168,85,247,0.5)]"></span>
                        详细解读
                    </h3>
                    {Object.entries(personalityData.sections).map(([title, content]) => (
                        <div
                            key={title}
                            className="bg-background/5 border border-white/5 rounded-2xl overflow-hidden transition-all duration-300 hover:border-white/10 hover:bg-background/[0.07]"
                        >
                            <button
                                onClick={() => toggleSection(title)}
                                className="w-full p-5 flex items-center justify-between text-left group"
                            >
                                <span className="font-semibold text-foreground group-hover:text-purple-300 transition-colors">
                                    {title}
                                </span>
                                {expandedSections.includes(title)
                                    ? <ChevronUp className="w-5 h-5 text-foreground-secondary group-hover:text-purple-300" />
                                    : <ChevronDown className="w-5 h-5 text-foreground-secondary group-hover:text-purple-300" />
                                }
                            </button>
                            {expandedSections.includes(title) && (
                                <div className="px-5 pb-5 pt-0 animate-fade-in">
                                    <div className="h-px w-full bg-background/5 mb-4" />
                                    <p className="text-foreground-secondary text-sm md:text-base whitespace-pre-line leading-relaxed">
                                        {content}
                                    </p>
                                </div>
                            )}
                        </div>
                    ))}
                </div>
            ) : (
                <p className="text-center text-foreground-secondary">加载人格详情失败</p>
            )}
        </div>
    );
}
