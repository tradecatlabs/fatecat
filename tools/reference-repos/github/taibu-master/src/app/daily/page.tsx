/**
 * 每日运势页面
 * 
 * 支持个性化运势（基于用户八字命盘）和通用运势
 */
'use client';

import { useState, useMemo, useEffect, Suspense } from 'react';
import { useSearchParams } from 'next/navigation';
import { FeatureGate } from '@/components/layout/FeatureGate';

import {
    Briefcase,
    Heart,
    Wallet,
    Activity,
    Star,
    Sparkles,
    User,
    X,
    Share2,
} from 'lucide-react';

import { ChartPickerModal, type ChartItem } from '@/components/common/ChartPickerModal';
import { CalendarAlmanac } from '@/components/daily/CalendarAlmanac';
import { DailyAIChat } from '@/components/daily/DailyAIChat';
import { ShareCard } from '@/components/fortune/ShareCard';
import { FortuneTrendChart, type FortuneTrendDataPoint } from '@/components/fortune/FortuneTrendChart';
import { InterpretationModeToggle, type InterpretationMode } from '@/components/fortune/InterpretationModeToggle';
import { calculateDailyFortune, calculateGenericDailyFortune, calculateWeeklyTrend, fortuneLevelToChartValue, isLevelFavorable, type DailyFortune } from '@/lib/divination/fortune';
import { generateFortuneInterpretation } from '@/lib/divination/fortune-interpretations';
import { getCalendarAlmanac } from '@/lib/divination/calendar';

import type { FortuneLevel } from '@/types';
import { AuthModal } from '@/components/auth/AuthModal';
import { useToast } from '@/components/ui/Toast';
import { loadPrimarySavedBaziChart, loadSavedBaziChart, type SavedBaziChart } from '@/lib/user/charts-client';
import { useFeatureToggles } from '@/lib/hooks/useFeatureToggles';
import { useSessionSafe } from '@/components/providers/ClientProviders';

const scoreItems = [
    { key: 'overall', label: '综合运势', icon: Star, color: 'text-amber-500' },
    { key: 'career', label: '事业运', icon: Briefcase, color: 'text-blue-500' },
    { key: 'love', label: '感情运', icon: Heart, color: 'text-pink-500' },
    { key: 'wealth', label: '财运', icon: Wallet, color: 'text-green-500' },
    { key: 'health', label: '健康运', icon: Activity, color: 'text-red-500' },
    { key: 'social', label: '人际运', icon: User, color: 'text-purple-500' },
];

// 解析日期字符串
function parseDateParam(dateStr: string | null): Date {
    if (!dateStr) return new Date();

    const parts = dateStr.split('-');
    if (parts.length === 3) {
        const year = parseInt(parts[0]);
        const month = parseInt(parts[1]) - 1;
        const day = parseInt(parts[2]);
        if (!isNaN(year) && !isNaN(month) && !isNaN(day)) {
            return new Date(year, month, day);
        }
    }
    return new Date();
}

function DailyPageContent() {
    const searchParams = useSearchParams();
    const { isFeatureEnabled, isLoading: featureToggleLoading } = useFeatureToggles();
    const { user, loading: sessionLoading } = useSessionSafe();
    const baziFeatureEnabled = !featureToggleLoading && isFeatureEnabled('bazi');
    const [selectedDate, setSelectedDate] = useState(() => parseDateParam(searchParams.get('date')));
    const [baziChart, setBaziChart] = useState<SavedBaziChart | null>(null);
    const [loading, setLoading] = useState(true);
    const [chartLoadError, setChartLoadError] = useState<string | null>(null);
    const [showChartSelector, setShowChartSelector] = useState(false);
    const [showShareCard, setShowShareCard] = useState(false);
    const [interpretationMode, setInterpretationMode] = useState<InterpretationMode>('colloquial');
    const [reloadToken, setReloadToken] = useState(0);

    const [showAuthModal, setShowAuthModal] = useState(false);
    const { showToast } = useToast();

    // 初始化
    useEffect(() => {
        let cancelled = false;

        const init = async () => {
            if (sessionLoading) return;
            if (!user || !baziFeatureEnabled) {
                if (!cancelled) {
                    setBaziChart(null);
                    setChartLoadError(null);
                    setLoading(false);
                }
                return;
            }

            setLoading(true);
            setChartLoadError(null);
            try {
                const nextChart = await loadPrimarySavedBaziChart();
                if (!cancelled) {
                    setBaziChart(nextChart);
                }
            } catch (err) {
                if (!cancelled) {
                    setBaziChart(null);
                    setChartLoadError(err instanceof Error ? err.message : '加载命盘失败');
                }
            } finally {
                if (!cancelled) {
                    setLoading(false);
                }
            }
        };

        void init();
        return () => {
            cancelled = true;
        };
    }, [baziFeatureEnabled, reloadToken, sessionLoading, user]);

    // 当 URL 参数变化时同步日期
    useEffect(() => {
        const dateParam = searchParams.get('date');
        if (dateParam) {
            setSelectedDate(parseDateParam(dateParam));
        } else {
            setSelectedDate(new Date());
        }
    }, [searchParams]);

    // 计算运势
    const fortune = useMemo(() => {
        if (baziChart) {
            return calculateDailyFortune(baziChart.output, selectedDate);
        }
        const generic = calculateGenericDailyFortune(selectedDate);
        return {
            ...generic,
            date: `${selectedDate.getFullYear()}-${String(selectedDate.getMonth() + 1).padStart(2, '0')}-${String(selectedDate.getDate()).padStart(2, '0')}`,
            dayStem: undefined as unknown,
            dayBranch: '',
            tenGod: '',
            luckyColor: '',
            luckyDirection: '',
        } as DailyFortune;
    }, [baziChart, selectedDate]);

    const changeDate = (days: number) => {
        const newDate = new Date(selectedDate);
        newDate.setDate(newDate.getDate() + days);
        setSelectedDate(newDate);
    };

    const goToToday = () => {
        setSelectedDate(new Date());
    };

    const handleSelectChart = async (chart: ChartItem) => {
        try {
            const fullChart = await loadSavedBaziChart(chart.id);
            if (!fullChart) {
                throw new Error('未找到所选命盘');
            }
            setBaziChart(fullChart);
            setChartLoadError(null);
        } catch (error) {
            const message = error instanceof Error ? error.message : '加载命盘失败';
            setChartLoadError(message);
            showToast('error', message);
        }
        setShowChartSelector(false);
    };

    const isToday = selectedDate.toDateString() === new Date().toDateString();
    const isPersonalized = !!baziChart;

    // 计算周趋势数据（用于趋势图）
    const trendData = useMemo((): FortuneTrendDataPoint[] => {
        if (!baziChart) return [];
        const weekData = calculateWeeklyTrend(baziChart.output, selectedDate);
        return weekData.map(d => ({
            date: d.date,
            fullDate: d.fullDate,
            dayOfMonth: d.dayOfMonth,
            scores: d.scores,
        }));
    }, [baziChart, selectedDate]);

    // 根据解读模式生成建议
    const interpretedAdvice = useMemo(() => {
        if (!baziChart || !fortune.tenGod) return fortune.advice;
        return generateFortuneInterpretation(
            fortune.tenGod,
            {
                overall: fortune.overall,
                career: fortune.career,
                love: fortune.love,
                wealth: fortune.wealth,
                health: fortune.health,
                social: fortune.social,
            },
            interpretationMode
        );
    }, [baziChart, fortune, interpretationMode]);

    // 获取黄历数据用于分享卡片
    const almanacData = useMemo(() => {
        const data = getCalendarAlmanac(selectedDate);
        return {
            yi: data.yi,
            ji: data.ji,
        };
    }, [selectedDate]);

    if (loading) {
        return (
            <div className="min-h-screen bg-background">
                <div className="max-w-5xl mx-auto px-4 py-8 space-y-8">
                    <div className="grid grid-cols-1 lg:grid-cols-2 gap-8">
                        {/* 左侧黄历骨架 */}
                        <div className="bg-background border border-border rounded-md p-6 space-y-4">
                            <div className="flex items-center justify-between">
                                <div className="h-6 w-6 rounded bg-foreground/5 animate-pulse" />
                                <div className="h-8 w-32 rounded bg-foreground/10 animate-pulse" />
                                <div className="h-6 w-6 rounded bg-foreground/5 animate-pulse" />
                            </div>
                            <div className="h-32 w-full rounded bg-foreground/5 animate-pulse" />
                        </div>
                        {/* 右侧运势骨架 */}
                        <div className="space-y-6">
                            <div className="bg-background border border-border rounded-md p-6 space-y-4">
                                <div className="h-5 w-24 rounded bg-foreground/10 animate-pulse" />
                                <div className="space-y-3">
                                    {[1, 2, 3, 4].map(i => (
                                        <div key={i} className="h-4 w-full rounded bg-foreground/5 animate-pulse" />
                                    ))}
                                </div>
                            </div>
                        </div>
                    </div>
                </div>
            </div>
        );
    }

    return (
        <div className="min-h-screen bg-background text-foreground pb-20 lg:pb-8">
            <div className="max-w-5xl mx-auto px-4 py-8 animate-fade-in space-y-8">
                {chartLoadError ? (
                    <section className="rounded-md border border-[#f5c2c7] bg-[#fff5f5] px-4 py-4">
                        <div className="flex flex-col gap-3 sm:flex-row sm:items-center sm:justify-between">
                            <div className="space-y-1">
                                <h2 className="text-sm font-semibold text-[#b42318]">命盘加载失败</h2>
                                <p className="text-sm text-[#7a271a]">
                                    {chartLoadError}。当前不会伪装成个性化结果，你可以重试或重新选择命盘。
                                </p>
                            </div>
                            <div className="flex items-center gap-2">
                                <button
                                    type="button"
                                    onClick={() => setReloadToken((value) => value + 1)}
                                    className="rounded-md border border-[#f0d5dd] bg-white px-3 py-2 text-sm font-medium text-[#7a271a] transition-colors hover:bg-[#fff1f3]"
                                >
                                    重试
                                </button>
                                <button
                                    type="button"
                                    onClick={() => setShowChartSelector(true)}
                                    className="rounded-md bg-[#2383e2] px-3 py-2 text-sm font-medium text-white transition-colors hover:bg-[#1d70c7]"
                                >
                                    重新选择命盘
                                </button>
                            </div>
                        </div>
                    </section>
                ) : null}

                {baziFeatureEnabled && user && (
                    <ChartPickerModal
                        isOpen={showChartSelector}
                        onClose={() => setShowChartSelector(false)}
                        onSelect={handleSelectChart}
                        userId={user.id}
                        title="选择八字命盘"
                        filterType="bazi"
                    />
                )}

                {/* 分享卡片弹窗 - 采用 Notion 风格弹窗 */}
                {showShareCard && (
                    <div className="fixed inset-0 bg-black/20 z-50 flex items-center justify-center p-4">
                        <div className="bg-background border border-border rounded-lg p-6 max-w-md w-full shadow-md">
                            <div className="flex items-center justify-between mb-6">
                                <h2 className="text-sm font-semibold flex items-center gap-2">
                                    <Share2 className="w-4 h-4 text-[#2eaadc]" />
                                    分享运势
                                </h2>
                                <button
                                    onClick={() => setShowShareCard(false)}
                                    className="p-1.5 rounded-md hover:bg-background-secondary transition-colors"
                                >
                                    <X className="w-4 h-4" />
                                </button>
                            </div>
                            <ShareCard
                                fortune={fortune}
                                date={selectedDate}
                                userName={baziChart?.name}
                                isPersonalized={isPersonalized}
                                almanac={almanacData}
                            />
                        </div>
                    </div>
                )}

                {/* 主要内容网格区域 */}
                <div className="grid grid-cols-1 lg:grid-cols-[minmax(0,1.08fr)_minmax(0,0.92fr)] gap-8 items-start">

                    {/* 左侧：黄历信息 - 纯白/米色卡片，细边框 */}
                    <div className="bg-background border border-border rounded-md overflow-hidden">
                        <CalendarAlmanac
                            date={selectedDate}
                            onDateChange={changeDate}
                            onGoToday={goToToday}
                            isToday={isToday}
                            chartName={baziChart?.name}
                            onChartSelect={baziFeatureEnabled ? () => setShowChartSelector(true) : undefined}
                            isPersonalized={isPersonalized}
                            dayStem={fortune.dayStem}
                            dayBranch={fortune.dayBranch}
                            tenGod={fortune.tenGod}
                        />
                    </div>

                    {/* 右侧：趋势图 + 运势分析 */}
                    <div className="space-y-6">
                        {/* 1. 7日运势趋势 (仅个性化模式显示) */}
                        {isPersonalized && trendData.length > 0 && (
                            <section className="bg-background border border-border rounded-md p-6">
                                <div className="w-full">
                                    <FortuneTrendChart
                                        data={trendData}
                                        selectedDate={fortune.date}
                                        height={200}
                                        multiDimension={false}
                                        title={
                                            <div className="flex items-center gap-2 text-sm font-semibold">
                                                <Activity className="w-4 h-4 text-[#2eaadc]" />
                                                7日运势趋势
                                            </div>
                                        }
                                    />
                                </div>
                            </section>
                        )}

                        {/* 2. 详细运势评分与分析 */}
                        <section className="bg-background border border-border rounded-md p-6 flex flex-col">
                            <div className="flex items-center justify-between mb-6">
                                <div className="flex items-center gap-3">
                                    <h2 className="text-sm font-semibold flex items-center gap-2">
                                        运势分析
                                    </h2>
                                    {fortune.dayStem && fortune.dayBranch && (
                                        <span className="text-[11px] text-foreground/40 uppercase tracking-wider">
                                            日干支：{fortune.dayStem}{fortune.dayBranch}
                                        </span>
                                    )}
                                </div>
                                <button
                                    onClick={() => setShowShareCard(true)}
                                    className="flex items-center gap-1.5 px-2.5 py-1 text-xs font-medium rounded-md border border-border hover:bg-background-secondary active:bg-background-tertiary transition-colors"
                                >
                                    <Share2 className="w-3.5 h-3.5" />
                                    分享
                                </button>
                            </div>

                            {/* 评分条 - 移除渐变，使用 Notion 强调色 */}
                            <div className="grid grid-cols-2 gap-x-8 gap-y-4 mb-2">
                                {scoreItems.map(item => {
                                    const level = fortune[item.key as keyof typeof fortune] as FortuneLevel;
                                    const chartValue = fortuneLevelToChartValue(level);
                                    const Icon = item.icon;
                                    const isFavorable = isLevelFavorable(level);
                                    const isNeutral = level === '平';

                                    return (
                                        <div key={item.key} className="group">
                                            <div className="flex items-center justify-between mb-1.5">
                                                <div className="flex items-center gap-2">
                                                    <Icon className={`w-3.5 h-3.5 ${item.color}`} />
                                                    <span className="text-xs font-medium text-foreground/80">{item.label}</span>
                                                </div>
                                                <span className={`text-xs font-semibold ${isFavorable ? 'text-[#0f7b6c]' : isNeutral ? 'text-[#dfab01]' : 'text-[#eb5757]'}`}>
                                                    {level}
                                                </span>
                                            </div>
                                            <div className="h-1 bg-background-secondary rounded-full overflow-hidden">
                                                <div
                                                    className={`h-full transition-all duration-1000 ease-out rounded-full ${isFavorable ? 'bg-[#0f7b6c]' :
                                                        isNeutral ? 'bg-[#dfab01]' :
                                                            'bg-[#eb5757]'
                                                        }`}
                                                    style={{ width: `${chartValue}%` }}
                                                />
                                            </div>
                                        </div>
                                    );
                                })}
                            </div>

                            <div className="space-y-6">
                                {/* 幸运信息 - 列表样式 */}
                                {isPersonalized && fortune.luckyColor && (
                                    <div className="grid grid-cols-2 gap-4 pt-2 border-t border-border/60">
                                        <div className="flex flex-col gap-1">
                                            <span className="text-[10px] uppercase tracking-wider text-foreground/40 font-semibold">幸运色</span>
                                            <span className="text-sm font-medium">{fortune.luckyColor}</span>
                                        </div>
                                        <div className="flex flex-col gap-1">
                                            <span className="text-[10px] uppercase tracking-wider text-foreground/40 font-semibold">吉方位</span>
                                            <span className="text-sm font-medium">{fortune.luckyDirection}</span>
                                        </div>
                                    </div>
                                )}

                                {/* 指引区域 - 纯文本/列表风格 */}
                                <div className="pt-1 border-t border-border/60">
                                    <div className="flex items-center justify-between mb-4">
                                        <h3 className="text-sm font-semibold flex items-center gap-2">
                                            运势指引
                                        </h3>
                                        {isPersonalized && (
                                            <InterpretationModeToggle
                                                mode={interpretationMode}
                                                onModeChange={setInterpretationMode}
                                                compact
                                            />
                                        )}
                                    </div>
                                    <ul className="space-y-3">
                                        {interpretedAdvice.map((advice, index) => (
                                            <li key={index} className="flex gap-3 text-sm text-foreground/80 leading-relaxed group">
                                                <span className="flex-shrink-0 w-5 h-5 rounded bg-background-secondary text-[10px] font-bold flex items-center justify-center mt-0.5">
                                                    {index + 1}
                                                </span>
                                                <span>{advice}</span>
                                            </li>
                                        ))}
                                    </ul>
                                </div>
                            </div>
                        </section>
                    </div>
                </div>

                {/* AI Chat 模块 - 嵌入式极简设计 */}
                <section className="bg-background border border-border rounded-md overflow-hidden">
                    {user ? (
                        <div className="p-1">
                            <DailyAIChat date={selectedDate} userId={user.id} />
                        </div>
                    ) : (
                        <div className="p-12 text-center">
                            <div className="w-12 h-12 bg-background-secondary rounded-md flex items-center justify-center mx-auto mb-4">
                                <Sparkles className="w-6 h-6 text-[#a083ff]" />
                            </div>
                            <h3 className="text-base font-semibold mb-2">AI 命理师在线解读</h3>
                            <p className="text-sm text-foreground/60 mb-6 max-w-sm mx-auto">
                                登录即可解锁 AI 智能对话，针对您的命盘进行深度的一对一分析。
                            </p>
                            <button
                                onClick={() => setShowAuthModal(true)}
                                className="px-6 py-2 bg-[#2383e2] text-white text-sm font-medium rounded-md hover:bg-[#2383e2]/90 active:bg-[#1a65b0] transition-colors"
                            >
                                立即登录
                            </button>
                        </div>
                    )}
                </section>
            </div>

            <AuthModal
                isOpen={showAuthModal}
                onClose={() => setShowAuthModal(false)}
            />
        </div>
    );
}
// 底部导出保持不变
export default function DailyPage() {
    return (
        <FeatureGate featureId="daily">
        <Suspense fallback={
            <div className="min-h-screen bg-background">
                <div className="max-w-7xl mx-auto md:px-4 px-2 md:py-8 py-2 space-y-6">
                    <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
                        <div className="bg-background/60 rounded-xl shadow-sm p-4 space-y-4">
                            <div className="flex items-center justify-between">
                                <div className="h-8 w-8 rounded-lg bg-foreground/5 animate-pulse" />
                                <div className="h-10 w-32 rounded bg-foreground/10 animate-pulse" />
                                <div className="h-8 w-8 rounded-lg bg-foreground/5 animate-pulse" />
                            </div>
                            <div className="h-24 w-full rounded-xl bg-foreground/5 animate-pulse" />
                        </div>
                        <div className="bg-background/60 rounded-2xl p-4 space-y-4">
                            <div className="h-6 w-32 rounded bg-foreground/10 animate-pulse" />
                            <div className="grid grid-cols-2 gap-3">
                                {[1, 2, 3, 4].map(i => (
                                    <div key={i} className="h-12 rounded bg-foreground/5 animate-pulse" />
                                ))}
                            </div>
                        </div>
                    </div>
                </div>
            </div>
        }>
            <DailyPageContent />
        </Suspense>
        </FeatureGate>
    );
}
