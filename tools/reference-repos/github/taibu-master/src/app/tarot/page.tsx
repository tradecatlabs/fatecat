/**
 * 塔罗牌占卜页面
 *
 * 选择牌阵并跳转到结果页
 */
'use client';

import { useEffect, useState } from 'react';
import { useRouter } from 'next/navigation';
import dynamic from 'next/dynamic';
import { Calendar, Layers, ChevronRight } from 'lucide-react';
import Image from 'next/image';

import { TAROT_SPREADS, getDailyCard, type DrawnCard, type TarotSpread } from '@/lib/divination/tarot';

const HistoryDrawer = dynamic(
    () => import('@/components/layout/HistoryDrawer').then(mod => mod.HistoryDrawer),
    { ssr: false }
);

export default function TarotPage() {
    const router = useRouter();
    const [question, setQuestion] = useState('');
    const [birthDate, setBirthDate] = useState('');
    const [dailyCard, setDailyCard] = useState<DrawnCard | null>(null);

    useEffect(() => {
        let cancelled = false;

        void getDailyCard().then((card) => {
            if (!cancelled) {
                setDailyCard(card);
            }
        }).catch(() => {
            if (!cancelled) {
                setDailyCard(null);
            }
        });

        return () => {
            cancelled = true;
        };
    }, []);

    const handleSelectSpread = (spread: TarotSpread) => {
        const params = new URLSearchParams();
        params.set('spreadId', spread.id);
        if (question.trim()) {
            params.set('question', question.trim());
        }
        if (birthDate) {
            params.set('birthDate', birthDate);
        }
        router.push(`/tarot/result?${params.toString()}`);
    };

    return (
        <>
            <div className="md:min-h-screen bg-background md:pb-12 text-foreground">
                {/* 页面标题 - 移动端隐藏（顶栏已显示） */}
                <div className="hidden md:block text-center py-8">
                    <h1 className="text-2xl lg:text-3xl font-bold">塔罗占卜</h1>
                    <p className="text-foreground/60 mt-2">聆听内心的声音，探索命运的指引</p>
                </div>

                <div className="max-w-4xl mx-auto px-4 mt-4">
                    {/* 每日一牌 - 卡片样式增强 */}
                    {dailyCard && (
                        <div className="bg-background rounded-lg p-4 md:p-6 shadow-sm border border-border md:mb-10 mb-6 overflow-hidden relative group">
                            <div className="flex flex-row items-center gap-4 md:gap-6 relative z-10">
                                <div className="relative w-24 h-36 md:w-32 md:h-48 flex-shrink-0 rounded-md overflow-hidden shadow-md transition-all duration-150">
                                    <Image
                                        src={dailyCard.card.image}
                                        alt={dailyCard.card.nameChinese}
                                        fill
                                        className={`object-cover ${dailyCard.orientation === 'reversed' ? 'rotate-180' : ''}`}
                                    />
                                    <div className="absolute inset-0 ring-1 ring-black/5 rounded-md" />
                                </div>

                                <div className="flex-1 text-left">
                                    <div className="inline-flex items-center gap-1.5 md:gap-2 px-2.5 md:px-3 py-0.5 md:py-1 rounded-md bg-purple-50 text-purple-600 text-[10px] md:text-xs font-bold uppercase tracking-wider mb-2 md:mb-3">
                                        <Calendar className="w-3 h-3 md:w-3.5 md:h-3.5" />
                                        今日指引
                                    </div>

                                    <h3 className="text-lg md:text-2xl font-bold mb-1 md:mb-2 flex items-center justify-start gap-2 md:gap-3">
                                        {dailyCard.card.nameChinese}
                                        <span className={`px-1.5 md:px-2 py-0.5 rounded-md text-[10px] md:text-xs font-bold border ${dailyCard.orientation === 'reversed'
                                            ? 'bg-orange-50 text-orange-600 border-orange-100'
                                            : 'bg-green-50 text-green-600 border-green-100'
                                            }`}>
                                            {dailyCard.orientation === 'reversed' ? '逆位' : '正位'}
                                        </span>
                                    </h3>

                                    <p className="text-sm md:text-base text-foreground/70 leading-relaxed mb-2 md:mb-4 line-clamp-3 md:line-clamp-none">
                                        {dailyCard.orientation === 'reversed'
                                            ? dailyCard.card.reversedMeaning
                                            : dailyCard.card.uprightMeaning}
                                    </p>

                                    <div className="text-[10px] md:text-xs text-foreground/40">
                                        * 每日自动抽取，为您提供当天的运势指引
                                    </div>
                                </div>
                            </div>
                        </div>
                    )}

                    {/* 问题输入 */}
                    <div className="mb-6 md:mb-10 text-center max-w-2xl mx-auto">
                        <label className="block text-sm font-medium text-foreground/60 mb-3 uppercase tracking-wider">
                            心中默念您的问题（选填）
                        </label>
                        <div className="relative group">
                            <input
                                type="text"
                                value={question}
                                onChange={(e) => setQuestion(e.target.value)}
                                placeholder="例如：我的事业发展会如何？"
                                className="relative w-full px-4 md:px-6 py-3 md:py-4 bg-background rounded-lg border border-border shadow-sm 
                                    focus:border-[#2383e2] focus:ring-2 focus:ring-[#2383e2]/10 focus:outline-none 
                                    text-center text-base md:text-lg text-foreground placeholder:text-foreground/30
                                    transition-all duration-150"
                            />
                        </div>

                        <div className="mt-4">
                            <label className="block text-sm font-medium text-foreground/60 mb-3 uppercase tracking-wider">
                                出生日期（选填，用于塔罗数秘术）
                            </label>
                            <div className="relative group">
                                <input
                                    type="date"
                                    value={birthDate}
                                    onChange={(e) => setBirthDate(e.target.value)}
                                    className="relative w-full px-4 md:px-6 py-3 md:py-4 bg-background rounded-lg border border-border shadow-sm focus:border-[#2383e2] focus:ring-2 focus:ring-[#2383e2]/10 focus:outline-none text-center text-base md:text-lg text-foreground transition-all duration-150"
                                />
                            </div>
                        </div>
                    </div>

                    {/* 牌阵选择 - 网格布局 */}
                    <div>
                        <div className="flex items-center justify-between mb-4 md:mb-6">
                            <h2 className="text-lg md:text-xl font-bold flex items-center gap-2">
                                <Layers className="w-5 h-5 text-[#2383e2]" />
                                选择牌阵开始占卜
                            </h2>
                        </div>

                        <div className="grid grid-cols-2 md:grid-cols-2 gap-3 md:gap-4">
                            {TAROT_SPREADS.map(spread => (
                                <button
                                    key={spread.id}
                                    onClick={() => handleSelectSpread(spread)}
                                    className="relative flex flex-col p-4 md:p-6 bg-background rounded-lg border border-border hover:bg-background-secondary active:bg-background-tertiary text-left transition-all duration-150 group shadow-sm overflow-hidden"
                                >
                                    <div className="relative z-10 w-full">
                                        <div className="flex items-center justify-between mb-2 md:mb-3">
                                            <span className="inline-flex items-center justify-center w-8 h-8 md:w-10 md:h-10 rounded-md bg-background text-foreground/70 group-hover:bg-[#2383e2] group-hover:text-white transition-colors duration-150">
                                                <Layers className="w-4 h-4 md:w-5 md:h-5" />
                                            </span>
                                            <span className="text-[10px] md:text-xs font-bold text-foreground/50 bg-background px-2 md:px-2.5 py-0.5 md:py-1 rounded-md uppercase tracking-wider group-hover:bg-background group-hover:text-[#2383e2] transition-colors">
                                                {spread.cardCount} 张牌
                                            </span>
                                        </div>

                                        <h3 className="text-base md:text-lg font-bold mb-1 md:mb-2 group-hover:text-[#2383e2] transition-colors line-clamp-1">
                                            {spread.name}
                                        </h3>

                                        <p className="text-xs md:text-sm text-foreground/60 leading-relaxed line-clamp-2 mb-2 md:mb-4 h-8 md:h-10">
                                            {spread.description}
                                        </p>

                                        <div className="flex items-center text-[10px] md:text-xs font-bold text-[#2383e2] mt-auto">
                                            开始占卜 <ChevronRight className="w-3 h-3 ml-1" />
                                        </div>
                                    </div>
                                </button>
                            ))}
                        </div>
                    </div>
                </div>
            </div>
            <HistoryDrawer type="tarot" />
        </>
    );
}
