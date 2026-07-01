/**
 * MBTI 性格测试主页面
 *
 * 提供测试介绍与进入入口
 */
'use client'; // Uses client-side state for modal and question count.

import { useState, useEffect } from 'react';
import { useRouter } from 'next/navigation';
import { Play, Eye } from 'lucide-react';
import { SoundWaveLoader } from '@/components/ui/SoundWaveLoader';

import { loadQuestions, type MBTIQuestion, PERSONALITY_BASICS } from '@/lib/divination/mbti';

function MBTIPageContent() {
    const router = useRouter();
    // Tracks question count to enable start button after load.
    const [questions, setQuestions] = useState<MBTIQuestion[]>([]);

    // 加载全部题目
    useEffect(() => {
        loadQuestions().then((allQuestions) => {
            setQuestions(allQuestions);
        });
    }, []);

    return (
        <div className="min-h-screen bg-background md:pb-12 text-foreground">
            {/* 页面标题 */}
            <div className="text-center pt-8 md:pt-12 pb-6">
                <h1 className="text-2xl lg:text-3xl font-bold">
                    MBTI 性格测试
                </h1>
                <p className="text-foreground/60 mt-2 max-w-md mx-auto">
                    探索你的性格类型，发现你与生俱来的天赋与倾向
                </p>

                    {/* 开始按钮 */}
                    <div className="mt-6">
                        <button
                            onClick={() => router.push('/mbti/test')}
                            disabled={questions.length === 0}
                            className="group relative inline-flex items-center gap-2 px-8 py-4 bg-[#2383e2] text-white rounded-md
                                text-lg font-bold shadow-sm hover:bg-[#2383e2]/90 active:bg-[#1a65b0]
                                disabled:opacity-50 disabled:cursor-not-allowed
                                transition-all duration-150 overflow-hidden"
                        >
                            {questions.length === 0 ? (
                                <>
                                    <SoundWaveLoader variant="inline" />
                                    <span>准备试题中...</span>
                                </>
                            ) : (
                                <>
                                    <Play className="w-5 h-5 fill-current" />
                                    <span>开始测试</span>
                                </>
                            )}
                        </button>
                        <p className="mt-3 text-sm text-foreground/40 font-medium">
                            共 {questions.length || 93} 道题目 · 约需 10-15 分钟
                        </p>
                    </div>
            </div>

            <div className="max-w-5xl mx-auto px-4 py-12">
                {/* 16种人格预览 */}
                <div className="mb-8 flex items-center justify-between">
                    <h2 className="text-xl font-bold flex items-center gap-2">
                        <span className="w-1 h-6 bg-[#37352f] rounded-full" />
                        16型人格图鉴
                    </h2>
                    <span className="text-sm font-medium text-foreground/50">
                        点击查看详细解读
                    </span>
                </div>

                <div className="grid grid-cols-2 sm:grid-cols-4 lg:grid-cols-4 gap-4">
                    {Object.entries(PERSONALITY_BASICS).map(([type, info]) => (
                        <button
                            key={type}
                            onClick={() => router.push(`/mbti/personality/${type}`)}
                            className="bg-background border border-border rounded-lg p-4 text-center
                                hover:bg-background-secondary active:bg-background-tertiary shadow-sm
                                transition-all duration-150 cursor-pointer group relative overflow-hidden"
                        >
                            <div className="absolute top-0 right-0 p-2 opacity-0 group-hover:opacity-100 transition-opacity duration-150">
                                <Eye className="w-4 h-4 text-[#2383e2]" />
                            </div>

                            <div className="text-4xl mb-3">
                                {info.emoji}
                            </div>
                            <div className="text-lg font-bold font-mono tracking-wide mb-1">
                                {type}
                            </div>
                            <div className="text-sm font-bold text-[#2383e2] mb-1">
                                {info.title}
                            </div>
                            <div className="text-xs text-foreground/60 line-clamp-1">
                                {info.description}
                            </div>
                        </button>
                    ))}
                </div>
            </div>
        </div>
    );
}

export default function MBTIPage() {
    return <MBTIPageContent />;
}
