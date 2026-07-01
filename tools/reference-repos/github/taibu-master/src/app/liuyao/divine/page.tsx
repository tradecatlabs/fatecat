/**
 * 六爻起卦页面
 *
 * 铜钱起卦交互
 */
'use client';

import { useState } from 'react';
import { useRouter } from 'next/navigation';
import { ArrowLeft, AlertCircle } from 'lucide-react';
import { SoundWaveLoader } from '@/components/ui/SoundWaveLoader';
import Link from 'next/link';
import { CoinToss } from '@/components/liuyao/CoinToss';
import { YongShenTargetPicker } from '@/components/liuyao/YongShenTargetPicker';
import { useToast } from '@/components/ui/Toast';
import { type Yao, type CoinTossResult, findHexagram, yaosTpCode, calculateChangedHexagram, type LiuQin } from '@/lib/divination/liuyao';
import { supabase } from '@/lib/auth';
import { readSessionJSON, writeSessionJSON } from '@/lib/cache/session-storage';
import { saveDivinationAction } from '@/lib/divination/save-client';

type LiuyaoQuestionSession = {
    question: string;
    yongShenTargets: LiuQin[];
};

export default function DivinePage() {
    const router = useRouter();
    const { showToast } = useToast();
    const [question] = useState(() => {
        if (typeof window === 'undefined') return '';
        const payload = readSessionJSON<LiuyaoQuestionSession | string>('liuyao_question');
        if (!payload) return '';
        if (typeof payload === 'string') return payload;
        return payload.question || '';
    });
    const [yongShenTargets, setYongShenTargets] = useState<LiuQin[]>(() => {
        if (typeof window === 'undefined') return [];
        const payload = readSessionJSON<LiuyaoQuestionSession | string>('liuyao_question');
        if (!payload || typeof payload === 'string') return [];
        return Array.isArray(payload.yongShenTargets) ? payload.yongShenTargets : [];
    });
    const [isComplete, setIsComplete] = useState(false);
    const requiresYongShenTargets = question.trim().length > 0;

    const handleYongShenTargetsChange = (targets: LiuQin[]) => {
        setYongShenTargets(targets);
        writeSessionJSON('liuyao_question', { question, yongShenTargets: targets });
    };

    const handleComplete = async (yaos: Yao[], results: CoinTossResult[]) => {
        if (requiresYongShenTargets && yongShenTargets.length === 0) {
            showToast('error', '请至少选择一个分析目标');
            return;
        }
        setIsComplete(true);

        // 计算卦象
        const hexagramCode = yaosTpCode(yaos);
        const hexagram = findHexagram(hexagramCode);
        const { changedCode, changedLines } = calculateChangedHexagram(yaos);
        const changedHexagram = changedLines.length > 0 ? findHexagram(changedCode) : undefined;

        // 保存起卦记录到数据库
        let divinationId: string | null = null;
        try {
            const { data: { session } } = await supabase.auth.getSession();
            if (session?.user) {
                const saveResult = await saveDivinationAction({
                    endpoint: '/api/liuyao',
                    body: {
                        question,
                        yongShenTargets,
                        yaos,
                        changedHexagram,
                        changedLines,
                    },
                    idKey: 'divinationId',
                    fallbackMessage: '保存起卦记录失败',
                });
                if (!saveResult.ok) {
                    throw new Error(saveResult.error.message || '保存起卦记录失败');
                }
                if (saveResult.id) {
                    divinationId = saveResult.id;
                }
            }
        } catch (error) {
            console.error('保存起卦记录失败:', error);
        }

        // 存储结果到 sessionStorage
        const result = {
            question,
            yongShenTargets,
            yaos,
            results,
            hexagram,
            changedHexagram,
            changedLines,
            divinationId,
            createdAt: new Date().toISOString(),
        };
        writeSessionJSON('liuyao_result', result);

        // 延迟跳转结果页
        setTimeout(() => {
            router.push('/liuyao/result');
        }, 1500);
    };



    return (
        <div className="md:min-h-screen bg-background">
            <div className="max-w-2xl mx-auto px-4 py-4 md:py-8">
                {/* 返回 - 仅桌面端显示 */}
                <Link
                    href="/liuyao"
                    className="hidden md:inline-flex items-center gap-2 text-foreground-secondary hover:text-foreground mb-4 md:mb-6"
                >
                    <ArrowLeft className="w-4 h-4" />
                    返回
                </Link>

                {/* 标题 */}
                <div className="text-center mb-4 md:mb-8">
                    <h1 className="hidden md:block text-xl md:text-2xl font-bold text-foreground">铜钱起卦</h1>
                    <p className="text-foreground-secondary md:mt-1 md:mt-2 text-sm md:text-base">
                        静心凝神，点击按钮抛掷铜钱
                    </p>
                </div>

                {/* 问题显示 */}
                {question && (
                    <div className="bg-accent/10 border border-accent/30 rounded-xl p-3 md:p-4 mb-4 md:mb-8">
                        <div className="text-center">
                            <span className="inline-flex items-center gap-1 text-xs md:text-sm text-accent font-medium">
                                <AlertCircle className="w-3 h-3 md:w-4 md:h-4" />
                                所问之事
                            </span>
                            <p className="text-foreground font-semibold text-base md:text-lg mt-1 md:mt-2">{question}</p>
                        </div>
                    </div>
                )}

                {requiresYongShenTargets && yongShenTargets.length === 0 && (
                    <div className="mb-4 md:mb-8">
                        <div className="text-sm text-red-500 mb-2">必须先选择分析目标</div>
                        <YongShenTargetPicker
                            value={yongShenTargets}
                            onChange={handleYongShenTargetsChange}
                            variant="block"
                        />
                    </div>
                )}

                {/* 铜钱起卦 */}
                <div className="bg-background rounded-xl p-0 md:p-8">
                    <CoinToss
                        onComplete={handleComplete}
                        disabled={isComplete || (requiresYongShenTargets && yongShenTargets.length === 0)}
                    />
                </div>

                {/* 完成提示 */}
                {isComplete && (
                    <div className="text-center mt-4 md:mt-8">
                        <SoundWaveLoader variant="inline" />
                        <p className="text-accent text-sm md:text-base font-medium mt-2">卦象已成，正在跳转...</p>
                    </div>
                )}
            </div>
        </div>
    );
}
