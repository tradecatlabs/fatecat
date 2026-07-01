/**
 * 每月运势页面
 * 
 * 支持个性化运势（基于用户八字命盘）和通用运势
 */
'use client';

import { useState, useMemo, useEffect } from 'react';
import {
    CalendarRange as CalendarIcon,
    ChevronLeft,
    ChevronRight,
    TrendingUp,
    User,
    ChevronDown,
} from 'lucide-react';
import Link from 'next/link';
import { SettingsCenterLink } from '@/components/settings/SettingsCenterLink';
import { FeatureGate } from '@/components/layout/FeatureGate';
import { useToast } from '@/components/ui/Toast';

import { ChartPickerModal, type ChartItem } from '@/components/common/ChartPickerModal';
import { FortuneTrendChart, type FortuneTrendDataPoint } from '@/components/fortune/FortuneTrendChart';
import { calculateMonthlyFortune, calculateDailyFortune, calculateGenericDailyFortune, calculateMonthlyTrend, isLevelFavorable, compareLevels, type MonthlyFortune } from '@/lib/divination/fortune';
import { getBranchElement, getElementColor, getStemElement } from '@/lib/divination/display-helpers';
import type { FortuneLevel } from '@/types';
import { loadPrimarySavedBaziChart, loadSavedBaziChart, type SavedBaziChart } from '@/lib/user/charts-client';
import { useFeatureToggles } from '@/lib/hooks/useFeatureToggles';
import { useSessionSafe } from '@/components/providers/ClientProviders';

const monthNames = ['一月', '二月', '三月', '四月', '五月', '六月', '七月', '八月', '九月', '十月', '十一月', '十二月'];

function MonthlyPageContent() {
    const { isFeatureEnabled, isLoading: featureToggleLoading } = useFeatureToggles();
    const { user, loading: sessionLoading } = useSessionSafe();
    const baziFeatureEnabled = !featureToggleLoading && isFeatureEnabled('bazi');
    const today = new Date();
    const [year, setYear] = useState(today.getFullYear());
    const [month, setMonth] = useState(today.getMonth() + 1);
    const [baziChart, setBaziChart] = useState<SavedBaziChart | null>(null);
    const [loading, setLoading] = useState(true);
    const [chartLoadError, setChartLoadError] = useState<string | null>(null);
    const [showChartSelector, setShowChartSelector] = useState(false);
    const [showTrendChart, setShowTrendChart] = useState(true);
    const [reloadToken, setReloadToken] = useState(0);
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

    // 计算月度运势
    const fortune = useMemo((): MonthlyFortune | null => {
        if (baziChart) {
            return calculateMonthlyFortune(baziChart.output, year, month);
        }
        return null;
    }, [baziChart, year, month]);

    // 计算日历数据
    const calendarData = useMemo(() => {
        const daysInMonth = new Date(year, month, 0).getDate();
        const days = [];

        for (let day = 1; day <= daysInMonth; day++) {
            const date = new Date(year, month - 1, day);
            let level: FortuneLevel;

            if (baziChart) {
                const dayFortune = calculateDailyFortune(baziChart.output, date);
                level = dayFortune.overall;
            } else {
                const generic = calculateGenericDailyFortune(date);
                level = generic.overall;
            }

            days.push({
                day,
                level,
                trend: isLevelFavorable(level) ? 'up' : compareLevels(level, '平') < 0 ? 'down' : 'neutral',
            });
        }

        return days;
    }, [baziChart, year, month]);

    // 计算月度趋势数据（用于趋势图）
    const trendData = useMemo((): FortuneTrendDataPoint[] => {
        if (!baziChart) return [];
        const monthData = calculateMonthlyTrend(baziChart.output, year, month);
        return monthData.map(d => ({
            date: d.date,
            fullDate: d.fullDate,
            dayOfMonth: d.dayOfMonth,
            scores: d.scores,
            isKeyDate: d.isKeyDate,
            keyDateType: d.keyDateType as 'lucky' | 'warning' | 'turning' | 'peak' | 'valley' | undefined,
            keyDateDesc: d.keyDateDesc,
        }));
    }, [baziChart, year, month]);

    const changeMonth = (delta: number) => {
        let newMonth = month + delta;
        let newYear = year;

        if (newMonth > 12) {
            newMonth = 1;
            newYear++;
        } else if (newMonth < 1) {
            newMonth = 12;
            newYear--;
        }

        setMonth(newMonth);
        setYear(newYear);
    };

    const goToCurrentMonth = () => {
        setYear(today.getFullYear());
        setMonth(today.getMonth() + 1);
    };

    const isCurrentMonth = year === today.getFullYear() && month === today.getMonth() + 1;
    const isPersonalized = !!baziChart;

    const getLevelDotColor = (level: FortuneLevel) => {
        if (isLevelFavorable(level)) return 'bg-green-500';
        if (level === '平') return 'bg-gray-400';
        return 'bg-red-500';
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

    const monthStemElement = fortune?.monthStem ? getStemElement(fortune.monthStem) : null;
    const monthBranchElement = fortune?.monthBranch ? getBranchElement(fortune.monthBranch) : null;
    const monthStemColor = monthStemElement ? getElementColor(monthStemElement) : undefined;
    const monthBranchColor = monthBranchElement ? getElementColor(monthBranchElement) : undefined;

    if (loading) {
        return (
            <div className="min-h-screen bg-background">
                <div className="max-w-4xl mx-auto px-4 py-4 md:py-8 space-y-6">
                    {/* 月度总结卡片骨架 */}
                    <div className="bg-background border border-border rounded-3xl overflow-hidden">
                        <div className="p-4 border-b border-border/50 bg-background-secondary/30">
                            <div className="flex items-center justify-between">
                                <div className="flex items-center gap-2">
                                    <div className="w-8 h-8 rounded-lg bg-foreground/5 animate-pulse" />
                                    <div className="h-6 w-32 rounded bg-foreground/10 animate-pulse" />
                                    <div className="w-8 h-8 rounded-lg bg-foreground/5 animate-pulse" />
                                </div>
                                <div className="h-8 w-40 rounded-full bg-foreground/5 animate-pulse" />
                            </div>
                        </div>
                        <div className="p-6">
                            <div className="flex flex-col sm:flex-row gap-6">
                                <div className="sm:w-1/3 space-y-3">
                                    <div className="h-4 w-20 rounded bg-foreground/5 animate-pulse" />
                                    <div className="h-10 w-24 rounded bg-foreground/10 animate-pulse" />
                                    <div className="h-8 w-28 rounded-lg bg-foreground/5 animate-pulse" />
                                </div>
                                <div className="sm:w-2/3 space-y-3">
                                    <div className="h-6 w-24 rounded bg-foreground/10 animate-pulse" />
                                    <div className="h-4 w-full rounded bg-foreground/5 animate-pulse" />
                                    <div className="h-4 w-full rounded bg-foreground/5 animate-pulse" />
                                    <div className="h-4 w-3/4 rounded bg-foreground/5 animate-pulse" />
                                </div>
                            </div>
                        </div>
                    </div>
                    {/* 日历骨架 */}
                    <div className="bg-background rounded-3xl border border-border overflow-hidden">
                        <div className="p-5 border-b border-border/50 bg-background-secondary/30">
                            <div className="h-6 w-28 rounded bg-foreground/10 animate-pulse" />
                        </div>
                        <div className="p-6">
                            <div className="grid grid-cols-7 gap-2 sm:gap-4">
                                {Array.from({ length: 35 }).map((_, i) => (
                                    <div key={i} className="h-14 sm:h-16 rounded-2xl bg-foreground/5 animate-pulse" />
                                ))}
                            </div>
                        </div>
                    </div>
                </div>
            </div>
        );
    }

    return (
        <div className="min-h-screen bg-background">
            {/* 顶部 Hero 区域 - 仅显示标题 */}
            <div className="hidden md:block relative overflow-hidden border-border/50 pb-4 pt-12">
                <div className="absolute inset-0 bg-grid-pattern opacity-[0.03] pointer-events-none" />
                <div className="max-w-4xl mx-auto px-4 relative z-10">
                    <div className="text-center">
                        <h1 className="text-4xl font-bold bg-clip-text text-transparent bg-gradient-to-r from-indigo-600 to-purple-600 dark:from-indigo-400 dark:to-purple-400 mb-4 tracking-tight flex items-center justify-center gap-3">
                            月度运势
                        </h1>
                        <p className="text-lg text-foreground-secondary/80 max-w-lg mx-auto">
                            把握流月气场，洞悉机遇与挑战，规划最佳行动时机。
                        </p>
                    </div>
                </div>
            </div>

            <div className="max-w-4xl mx-auto px-4 py-4 md:py-8 space-y-6 relative z-20">
                {chartLoadError ? (
                    <div className="rounded-2xl border border-[#f5c2c7] bg-[#fff5f5] px-4 py-4 shadow-sm">
                        <div className="flex flex-col gap-3 sm:flex-row sm:items-center sm:justify-between">
                            <div className="space-y-1">
                                <h2 className="text-sm font-semibold text-[#b42318]">命盘加载失败</h2>
                                <p className="text-sm text-[#7a271a]">
                                    {chartLoadError}。当前不会伪装成个性化月运结果，你可以重试或重新选择命盘。
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
                    </div>
                ) : null}

                {/* 非个性化时的提示卡片 */}
                {!isPersonalized && baziFeatureEnabled && !chartLoadError && (
                    <div className="bg-gradient-to-r from-amber-500/10 to-orange-500/5 border border-amber-500/20 rounded-2xl p-4 flex items-center justify-between shadow-sm">
                        <div className="flex items-center gap-3">
                            <div className="p-2 bg-amber-500/10 rounded-lg">
                                <User className="w-5 h-5 text-amber-600 dark:text-amber-400" />
                            </div>
                            <div>
                                <h3 className="font-medium text-amber-900 dark:text-amber-100">当前为通用运势</h3>
                                <p className="text-xs text-amber-700/70 dark:text-amber-300/70">关联八字命盘，获取专属精准分析</p>
                            </div>
                        </div>
                        <SettingsCenterLink
                            tab="charts"
                            className="px-4 py-2 bg-amber-500 text-white rounded-lg text-sm font-medium hover:bg-amber-600 transition-colors shadow-md hover:shadow-lg hover:shadow-amber-500/20"
                        >
                            去排盘
                        </SettingsCenterLink>
                    </div>
                )}

                {/* 月度总结卡片 - 整合月份选择器和命盘选择器 */}
                {isPersonalized && fortune && (
                    <div className="bg-background border border-border rounded-3xl shadow-sm relative overflow-hidden">
                        <div className="absolute top-0 right-0 w-64 h-64 bg-gradient-to-bl from-indigo-500/5 to-transparent pointer-events-none" />

                        {/* 顶部控制栏：月份选择器 + 命盘选择器 */}
                        <div className="p-4 border-b border-border/50 bg-background-secondary/30 relative z-10">
                            <div className="flex flex-col sm:flex-row items-center justify-between gap-3">
                                {/* 月份选择器 */}
                                <div className="flex items-center gap-2">
                                    <button
                                        onClick={() => changeMonth(-1)}
                                        className="p-2 rounded-lg hover:bg-background border border-transparent hover:border-border transition-all text-foreground-secondary hover:text-foreground"
                                    >
                                        <ChevronLeft className="w-5 h-5" />
                                    </button>
                                    <div className="text-center min-w-[120px]">
                                        <div className="text-lg font-bold text-foreground tabular-nums">
                                            {year}年 {monthNames[month - 1]}
                                        </div>
                                        {isCurrentMonth ? (
                                            <div className="text-xs font-medium text-indigo-500 bg-indigo-50 dark:bg-indigo-500/10 px-2 py-0.5 rounded-full inline-block">
                                                本月
                                            </div>
                                        ) : (
                                            <button
                                                onClick={goToCurrentMonth}
                                                className="text-xs text-foreground-secondary hover:text-indigo-500 transition-colors"
                                            >
                                                回到本月
                                            </button>
                                        )}
                                    </div>
                                    <button
                                        onClick={() => changeMonth(1)}
                                        className="p-2 rounded-lg hover:bg-background border border-transparent hover:border-border transition-all text-foreground-secondary hover:text-foreground"
                                    >
                                        <ChevronRight className="w-5 h-5" />
                                    </button>
                                </div>

                                {/* 命盘选择器 */}
                                <button
                                    onClick={() => setShowChartSelector(true)}
                                    className="group flex items-center gap-2 px-4 py-2 bg-background hover:bg-background-secondary rounded-full border border-border/60 hover:border-indigo-500/30 shadow-sm hover:shadow-md transition-all duration-300"
                                >
                                    <span className="text-sm font-medium text-foreground-secondary group-hover:text-foreground">
                                        命主: <span className="text-indigo-600 dark:text-indigo-400">{baziChart.name}</span>
                                    </span>
                                    <ChevronDown className="w-4 h-4 text-foreground-secondary group-hover:text-foreground transition-transform group-hover:rotate-180" />
                                </button>
                            </div>
                        </div>

                        {/* 月度总结内容 */}
                        <div className="p-6">
                            <div className="flex flex-col sm:flex-row gap-6 relative z-10">
                                <div className="sm:w-1/3 flex flex-col justify-center items-center sm:items-start border-b sm:border-b-0 sm:border-r border-border/50 pb-4 sm:pb-0 sm:pr-6">
                                    <div className="text-sm font-medium text-foreground-secondary mb-1">本月能量</div>
                                    <div className="flex items-baseline gap-2 mb-2">
                                        <span className="text-3xl font-bold font-serif text-indigo-900 dark:text-indigo-100">
                                            <span style={{ color: monthStemColor }}>{fortune.monthStem}</span>
                                            <span style={{ color: monthBranchColor }}>{fortune.monthBranch}</span>
                                        </span>
                                        <span className="text-sm text-foreground-secondary">月</span>
                                    </div>
                                    <div className="flex items-center gap-2 bg-background-secondary px-3 py-1.5 rounded-lg border border-border/50">
                                        <span className="text-xs text-foreground-secondary">主运十神</span>
                                        <span className="text-sm font-bold">{fortune.tenGod}</span>
                                    </div>
                                    {fortune && (
                                        <div className="mt-4 flex flex-col items-center sm:items-start w-full">
                                            <div className="flex justify-between w-full text-xs text-foreground-secondary mb-1">
                                                <span>综合运势</span>
                                                <span className="font-bold">{fortune.overall}</span>
                                            </div>
                                            <div className="h-2 w-full bg-background-secondary rounded-full overflow-hidden">
                                                <div
                                                    className={`h-full rounded-full ${getLevelDotColor(fortune.overall)} transition-all duration-1000`}
                                                    style={{ width: `${fortune._chart.overall}%` }}
                                                />
                                            </div>
                                        </div>
                                    )}
                                </div>
                                <div className="sm:w-2/3 flex flex-col justify-center">
                                    <h3 className="text-lg font-bold text-foreground mb-3 flex items-center gap-2">
                                        运势批语
                                    </h3>
                                    <p className="text-foreground leading-relaxed text-justify">
                                        {fortune.summary}
                                    </p>
                                </div>
                            </div>
                        </div>
                    </div>
                )}

                {/* 非个性化时的月份选择器 */}
                {!isPersonalized && (
                    <div className="flex items-center justify-center gap-4 bg-background/50 backdrop-blur-md rounded-xl border border-border/50 p-3">
                        <button
                            onClick={() => changeMonth(-1)}
                            className="p-2 rounded-lg hover:bg-background-secondary transition-all text-foreground-secondary"
                        >
                            <ChevronLeft className="w-5 h-5" />
                        </button>
                        <div className="text-center min-w-[120px]">
                            <div className="text-lg font-bold text-foreground">
                                {year}年 {monthNames[month - 1]}
                            </div>
                            {isCurrentMonth ? (
                                <div className="text-xs font-medium text-indigo-500 bg-indigo-50 dark:bg-indigo-500/10 px-2 py-0.5 rounded-full inline-block">
                                    本月
                                </div>
                            ) : (
                                <button
                                    onClick={goToCurrentMonth}
                                    className="text-xs text-foreground-secondary hover:text-indigo-500 transition-colors"
                                >
                                    回到本月
                                </button>
                            )}
                        </div>
                        <button
                            onClick={() => changeMonth(1)}
                            className="p-2 rounded-lg hover:bg-background-secondary transition-all text-foreground-secondary"
                        >
                            <ChevronRight className="w-5 h-5" />
                        </button>
                    </div>
                )}

                {/* 趋势图 */}
                {isPersonalized && trendData.length > 0 && (
                    <div className="bg-background rounded-3xl p-1 border border-border shadow-sm">
                        <div className="p-5 border-b border-border/50 flex items-center justify-between">
                            <h2 className="font-bold text-lg flex items-center gap-2">
                                <TrendingUp className="w-5 h-5 text-indigo-500" />
                                运势起伏
                            </h2>
                            <button
                                onClick={() => setShowTrendChart(!showTrendChart)}
                                className="p-2 hover:bg-background-secondary rounded-full transition-colors"
                            >
                                <ChevronDown className={`w-5 h-5 text-foreground-secondary transition-transform duration-300 ${showTrendChart ? 'rotate-180' : ''}`} />
                            </button>
                        </div>
                        {showTrendChart && (
                            <div className="p-4 sm:p-6 bg-background-secondary/30 rounded-b-[1.4rem]">
                                <FortuneTrendChart
                                    data={trendData}
                                    height={300}
                                    simplifiedMode={true}
                                    hideKeyDateLegend={true}
                                    defaultOverallOnly={true}
                                />
                            </div>
                        )}
                    </div>
                )}

                {/* 运势日历 */}
                <div className="bg-background rounded-3xl border border-border shadow-sm overflow-hidden">
                    <div className="p-5 border-b border-border/50 flex items-center justify-between bg-background-secondary/30">
                        <h2 className="font-bold text-lg flex items-center gap-2">
                            <CalendarIcon className="w-5 h-5 text-indigo-500" />
                            每日运程
                        </h2>

                        {/* 图例 */}
                        <div className="flex items-center gap-3 sm:gap-4 text-[10px] sm:text-xs text-foreground-secondary">
                            <div className="flex items-center gap-1.5">
                                <div className="w-2.5 h-2.5 rounded-full bg-green-500 shadow-sm shadow-green-500/20" />
                                <span>吉</span>
                            </div>
                            <div className="flex items-center gap-1.5">
                                <div className="w-2.5 h-2.5 rounded-full bg-gray-400 shadow-sm shadow-gray-400/20" />
                                <span>平</span>
                            </div>
                            <div className="flex items-center gap-1.5">
                                <div className="w-2.5 h-2.5 rounded-full bg-red-500 shadow-sm shadow-red-500/20" />
                                <span>凶</span>
                            </div>
                        </div>
                    </div>

                    <div className="p-6">
                        <div className="grid grid-cols-7 gap-2 sm:gap-4 mb-2">
                            {['日', '一', '二', '三', '四', '五', '六'].map(d => (
                                <div key={d} className="text-center text-foreground-secondary/60 text-xs font-medium py-2">
                                    {d}
                                </div>
                            ))}
                        </div>

                        <div className="grid grid-cols-7 gap-2 sm:gap-4">
                            {/* 填充月初空白 */}
                            {Array.from({ length: new Date(year, month - 1, 1).getDay() }).map((_, i) => (
                                <div key={`empty-${i}`} />
                            ))}

                            {calendarData.map(day => {
                                const isToday = year === today.getFullYear() &&
                                    month === today.getMonth() + 1 &&
                                    day.day === today.getDate();

                                return (
                                    <Link
                                        key={day.day}
                                        href={`/daily?date=${year}-${String(month).padStart(2, '0')}-${String(day.day).padStart(2, '0')}`}
                                        className={`
                                            group relative p-2 sm:p-3 rounded-2xl text-center cursor-pointer
                                            border transition-all duration-300
                                            hover:shadow-md hover:-translate-y-1
                                            ${isToday
                                                ? 'bg-indigo-50 dark:bg-indigo-500/20 border-indigo-200 dark:border-indigo-500/30 ring-1 ring-indigo-500/20'
                                                : 'bg-background-secondary/30 hover:bg-background-secondary border-transparent hover:border-border'
                                            }
                                        `}
                                    >
                                        <div className={`text-xs sm:text-sm font-medium mb-1 ${isToday ? 'text-indigo-600 dark:text-indigo-400' : 'text-foreground-secondary'}`}>
                                            {day.day}
                                        </div>
                                        <div className="flex flex-col items-center gap-1">
                                            <div className={`w-1.5 h-1.5 sm:w-2 sm:h-2 rounded-full ${getLevelDotColor(day.level)}`} />
                                            <div className={`text-[10px] sm:text-xs font-medium ${
                                                isLevelFavorable(day.level) ? 'text-green-600 dark:text-green-400' :
                                                day.level === '平' ? 'text-gray-500 dark:text-gray-400' :
                                                'text-red-600 dark:text-red-400'
                                            }`}>
                                                {day.level}
                                            </div>
                                        </div>
                                    </Link>
                                );
                            })}
                        </div>
                    </div>
                </div>

                {/* 底部提示 */}
                {!isPersonalized && (
                    <div className="text-center py-8">
                        <Link
                            href="/bazi"
                            className="inline-flex items-center gap-2 px-6 py-3 rounded-full bg-background border border-border shadow-sm hover:shadow-md hover:border-indigo-500/30 transition-all group"
                        >
                            <span className="text-sm text-foreground-secondary group-hover:text-foreground">完成八字排盘，获取更精准的分析</span>
                            <ChevronRight className="w-4 h-4 text-foreground-secondary group-hover:text-indigo-500" />
                        </Link>
                    </div>
                )}
            </div>

            {/* 命盘选择器弹窗 */}
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
        </div>
    );
}

export default function MonthlyPage() {
    return (
        <FeatureGate featureId="monthly">
            <MonthlyPageContent />
        </FeatureGate>
    );
}
