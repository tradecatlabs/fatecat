/**
 * 冲突点展示组件
 *
 * 包含冲突触发因素和沟通建议模板
 */
'use client';

import { useState } from 'react';
import { AlertTriangle, AlertCircle, Info, ChevronDown, MessageCircle, Shield, Lightbulb, CheckCircle2 } from 'lucide-react';
import { type ConflictPoint, type HepanType } from '@/lib/divination/hepan';
import { getCommunicationTemplate, getSeverityAdvice, type CommunicationTemplate } from '@/lib/communication-templates';

interface ConflictPointsProps {
    conflicts: ConflictPoint[];
    hepanType: HepanType;
}

export function ConflictPoints({ conflicts, hepanType }: ConflictPointsProps) {
    const [expandedIndex, setExpandedIndex] = useState<number | null>(null);
    const [showTemplate, setShowTemplate] = useState<number | null>(null);

    if (conflicts.length === 0) {
        return (
            <div className="bg-emerald-500/5 backdrop-blur-md border border-emerald-500/10 rounded-3xl p-8 text-center">
                <div className="w-16 h-16 rounded-full bg-emerald-500/10 flex items-center justify-center mx-auto mb-4">
                    <CheckCircle2 className="w-8 h-8 text-emerald-500" />
                </div>
                <h3 className="text-lg font-bold text-foreground mb-2">暂未发现明显冲突点</h3>
                <p className="text-foreground-secondary max-w-sm mx-auto">
                    双方八字配合良好，能量场和谐互补，关系发展将会比较顺利。
                </p>
            </div>
        );
    }

    const severityConfig = {
        high: {
            icon: AlertTriangle,
            bgColor: 'bg-rose-500/10',
            borderColor: 'border-rose-500/20',
            iconColor: 'text-rose-500',
            label: '高度关注',
            bgSolid: 'bg-rose-500',
        },
        medium: {
            icon: AlertCircle,
            bgColor: 'bg-amber-500/10',
            borderColor: 'border-amber-500/20',
            iconColor: 'text-amber-500',
            label: '中度关注',
            bgSolid: 'bg-amber-500',
        },
        low: {
            icon: Info,
            bgColor: 'bg-blue-500/10',
            borderColor: 'border-blue-500/20',
            iconColor: 'text-blue-500',
            label: '轻度留意',
            bgSolid: 'bg-blue-500',
        },
    };

    const toggleExpand = (index: number) => {
        setExpandedIndex(expandedIndex === index ? null : index);
        if (expandedIndex !== index) {
            setShowTemplate(null);
        }
    };

    return (
        <div className="space-y-6">
            <h3 className="text-xl font-bold text-foreground flex items-center gap-2">
                <span className="w-1.5 h-6 bg-rose-500 rounded-full" />
                需要关注的问题
            </h3>

            {conflicts.map((conflict, index) => {
                const config = severityConfig[conflict.severity];
                const Icon = config.icon;
                const isExpanded = expandedIndex === index;
                const template = getCommunicationTemplate(hepanType, conflict.title);
                const severityAdvice = getSeverityAdvice(conflict.severity);

                return (
                    <div
                        key={index}
                        className={`bg-background/5 backdrop-blur-md border border-white/10 rounded-2xl overflow-hidden transition-all duration-300 hover:border-white/20 hover:shadow-lg`}
                    >
                        {/* Summary Section */}
                        <div
                            className="p-5 cursor-pointer"
                            onClick={() => toggleExpand(index)}
                        >
                            <div className="flex items-start gap-4">
                                <div className={`p-2.5 rounded-xl ${config.bgColor} ${config.iconColor} shrink-0`}>
                                    <Icon className="w-6 h-6" />
                                </div>

                                <div className="flex-1 min-w-0">
                                    <div className="flex items-center flex-wrap gap-2 mb-2">
                                        <h4 className="text-lg font-bold text-foreground">{conflict.title}</h4>
                                        <span className={`text-xs px-2.5 py-0.5 rounded-full font-medium ${config.bgColor} ${config.iconColor} border ${config.borderColor}`}>
                                            {config.label}
                                        </span>
                                    </div>

                                    <p className="text-foreground-secondary text-sm leading-relaxed mb-3">
                                        {conflict.description}
                                    </p>

                                    <div className="flex items-start gap-2 text-sm bg-background/5 p-3 rounded-lg border border-white/5">
                                        <Lightbulb className="w-4 h-4 text-amber-500 mt-0.5 shrink-0" />
                                        <span className="text-foreground-secondary/90">{conflict.suggestion}</span>
                                    </div>
                                </div>

                                {conflict.triggerFactors && conflict.triggerFactors.length > 0 && (
                                    <button className="text-foreground-secondary hover:text-foreground transition-colors p-1">
                                        <ChevronDown className={`w-5 h-5 transition-transform duration-300 ${isExpanded ? 'rotate-180' : ''}`} />
                                    </button>
                                )}
                            </div>
                        </div>

                        {/* Expanded Details */}
                        {isExpanded && conflict.triggerFactors && (
                            <div className="border-t border-white/10 bg-background/5 p-5 space-y-6 animate-fade-in">
                                {/* Trigger Factors */}
                                <div>
                                    <h5 className="font-semibold text-foreground mb-4 flex items-center gap-2">
                                        <Shield className="w-4 h-4 text-emerald-500" />
                                        常见触发情境与应对
                                    </h5>
                                    <div className="grid gap-3">
                                        {conflict.triggerFactors.map((trigger, tIdx) => (
                                            <div
                                                key={tIdx}
                                                className="bg-background/5 rounded-xl p-4 border border-white/5 hover:bg-background/10 transition-colors"
                                            >
                                                <div className="text-sm font-semibold text-foreground mb-2">
                                                    {trigger.scenario}
                                                </div>
                                                <div className="space-y-2 text-xs md:text-sm">
                                                    <div className="flex items-start gap-2 text-foreground-secondary">
                                                        <span className="text-rose-500 font-medium shrink-0">触发行为：</span>
                                                        {trigger.trigger}
                                                    </div>
                                                    <div className="flex items-start gap-2 text-foreground-secondary">
                                                        <span className="text-amber-500 font-medium shrink-0">警示：</span>
                                                        {trigger.warning}
                                                    </div>
                                                    <div className="flex items-start gap-2 text-foreground-secondary">
                                                        <span className="text-emerald-500 font-medium shrink-0">预防：</span>
                                                        {trigger.prevention}
                                                    </div>
                                                </div>
                                            </div>
                                        ))}
                                    </div>
                                </div>

                                {/* Communication Template */}
                                <div>
                                    <button
                                        onClick={(e) => {
                                            e.stopPropagation();
                                            setShowTemplate(showTemplate === index ? null : index);
                                        }}
                                        className={`w-full flex items-center justify-between p-4 rounded-xl border transition-all ${showTemplate === index
                                                ? 'bg-indigo-500/10 border-indigo-500/30'
                                                : 'bg-background/5 border-white/10 hover:bg-background/10'
                                            }`}
                                    >
                                        <span className="font-semibold text-foreground flex items-center gap-2">
                                            <MessageCircle className="w-4 h-4 text-indigo-500" />
                                            沟通建议与话术模板
                                        </span>
                                        <ChevronDown className={`w-4 h-4 text-foreground-secondary transition-transform duration-300 ${showTemplate === index ? 'rotate-180' : ''}`} />
                                    </button>

                                    {showTemplate === index && (
                                        <div className="mt-3 animate-fade-in">
                                            <CommunicationTemplateCard template={template} />
                                        </div>
                                    )}
                                </div>

                                {/* General Advice */}
                                <div className="bg-amber-500/5 rounded-xl p-4 border border-amber-500/10">
                                    <h5 className="text-sm font-semibold text-foreground mb-3 flex items-center gap-2">
                                        <Lightbulb className="w-4 h-4 text-amber-500" />
                                        通用建议
                                    </h5>
                                    <ul className="space-y-2">
                                        {severityAdvice.map((advice, aIdx) => (
                                            <li key={aIdx} className="text-sm text-foreground-secondary flex items-start gap-2.5">
                                                <div className="w-1.5 h-1.5 rounded-full bg-amber-500 mt-1.5 shrink-0" />
                                                {advice}
                                            </li>
                                        ))}
                                    </ul>
                                </div>
                            </div>
                        )}
                    </div>
                );
            })}
        </div>
    );
}

function CommunicationTemplateCard({ template }: { template: CommunicationTemplate }) {
    return (
        <div className="bg-indigo-500/5 rounded-xl p-5 border border-indigo-500/10 space-y-5">
            <div>
                <h5 className="text-sm font-bold text-foreground mb-1">{template.title}</h5>
                <p className="text-xs text-foreground-secondary">适用情境：{template.context}</p>
            </div>

            <div>
                <div className="text-xs font-semibold text-indigo-400 mb-2 uppercase tracking-wide">参考话术</div>
                <div className="bg-background/5 rounded-xl p-4 text-sm text-foreground leading-relaxed italic border border-white/10 relative">
                    <span className="absolute top-2 left-2 text-white/10 text-2xl font-serif">&quot;</span>
                    <span className="relative z-10 px-2 block">{template.script}</span>
                    <span className="absolute bottom-2 right-2 text-white/10 text-2xl font-serif">&quot;</span>
                </div>
            </div>

            <div className="grid md:grid-cols-2 gap-4">
                <div>
                    <div className="text-xs font-semibold text-emerald-500 mb-2 uppercase tracking-wide">沟通技巧</div>
                    <ul className="space-y-2">
                        {template.tips.map((tip, idx) => (
                            <li key={idx} className="text-xs text-foreground-secondary flex items-start gap-2">
                                <CheckCircle2 className="w-3.5 h-3.5 text-emerald-500 shrink-0 mt-0.5" />
                                {tip}
                            </li>
                        ))}
                    </ul>
                </div>

                <div>
                    <div className="text-xs font-semibold text-rose-500 mb-2 uppercase tracking-wide">避免用语</div>
                    <div className="flex flex-wrap gap-2">
                        {template.avoidPhrases.map((phrase, idx) => (
                            <span
                                key={idx}
                                className="text-xs px-2.5 py-1 bg-rose-500/10 text-rose-400 rounded-lg border border-rose-500/10"
                            >
                                {phrase}
                            </span>
                        ))}
                    </div>
                </div>
            </div>
        </div>
    );
}
