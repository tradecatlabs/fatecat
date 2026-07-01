/**
 * 黄历信息展示组件
 *
 * 显示完整的黄历数据，包括宜忌、吉神凶煞、冲煞、神位等
 * 支持整合日期选择器、命盘选择器和流日/主神信息
 */
'use client';

import { useMemo, useState, useCallback } from 'react'; // Added useState for expand/collapse state, useCallback for memoized functions
import {
    Calendar,
    CheckCircle,
    XCircle,
    MapPin,
    Clock,
    ChevronLeft,
    ChevronRight,
    ChevronDown,
    User,
    Scroll,
} from 'lucide-react';
import Link from 'next/link';
import { SettingsCenterLink } from '@/components/settings/SettingsCenterLink';
import { getCalendarAlmanac, getZhiShenDesc, isBlackDay } from '@/lib/divination/calendar';
import { getBranchElement, getElementColor, getStemElement } from '@/lib/divination/display-helpers';

interface CalendarAlmanacProps {
    date: Date;
    /** 日期变更回调 */
    onDateChange?: (days: number) => void;
    /** 回到今天回调 */
    onGoToday?: () => void;
    /** 是否为今天 */
    isToday?: boolean;
    /** 命盘名称 */
    chartName?: string;
    /** 点击命盘选择器回调 */
    onChartSelect?: () => void;
    /** 是否为个性化模式 */
    isPersonalized?: boolean;
    /** 流日干支 */
    dayStem?: string;
    dayBranch?: string;
    /** 主神（十神） */
    tenGod?: string;
}

export function CalendarAlmanac({
    date,
    onDateChange,
    onGoToday,
    isToday = false,
    chartName,
    onChartSelect,
    isPersonalized = false,
    dayStem,
    dayBranch,
    tenGod,
}: CalendarAlmanacProps) {
    const data = useMemo(() => getCalendarAlmanac(date), [date]);
    
    // State for expanding 宜/忌 lists - needed for user interaction
    const [yiExpanded, setYiExpanded] = useState(false);
    const [jiExpanded, setJiExpanded] = useState(false);

    // 流日干支颜色 - 使用 useMemo 缓存计算结果
    const { dayStemColor, dayBranchColor } = useMemo(() => {
        const stemElement = dayStem ? getStemElement(dayStem) : null;
        const branchElement = dayBranch ? getBranchElement(dayBranch) : null;
        return {
            dayStemColor: stemElement ? getElementColor(stemElement) : undefined,
            dayBranchColor: branchElement ? getElementColor(branchElement) : undefined,
        };
    }, [dayStem, dayBranch]);

    const renderGanZhi = useCallback((value: string) => {
        const stem = value?.[0] || '';
        const branch = value?.[1] || '';
        const stemElement = getStemElement(stem);
        const branchElement = getBranchElement(branch);
        const stemColor = stemElement ? getElementColor(stemElement) : undefined;
        const branchColor = branchElement ? getElementColor(branchElement) : undefined;

        return (
            <span>
                <span style={{ color: stemColor }}>{stem}</span>
                <span style={{ color: branchColor }}>{branch}</span>
            </span>
        );
    }, []);

    return (
        <section className="bg-background rounded-xl border-border overflow-hidden">
            {/* 顶部控制栏：日期切换（含日期信息）+ 流日/主神 + 命盘选择 */}
            {onDateChange && (
                <div className="px-3 py-4 md:py-8 border-b border-border/50 bg-background">
                    {/* 移动端：垂直堆叠布局 */}
                    <div className="md:hidden space-y-3">
                        {/* 第一行：日期切换 */}
                        <div className="flex items-center justify-center gap-2">
                            <button
                                onClick={() => onDateChange(-1)}
                                className="p-1.5 rounded-md hover:bg-background border border-transparent hover:border-border transition-all text-foreground-secondary hover:text-foreground active:scale-95"
                            >
                                <ChevronLeft className="w-5 h-5" />
                            </button>
                            <div className="text-center px-2 min-w-[160px]">
                                {!isToday && onGoToday && (
                                    <button
                                        onClick={onGoToday}
                                        className="mb-1 inline-flex items-center text-[10px] text-foreground-secondary hover:text-foreground transition-colors"
                                    >
                                        返回今日
                                    </button>
                                )}
                                <div className="flex items-baseline justify-center gap-2">
                                    <span className="text-xl font-bold">{data.solarDateChinese}</span>
                                    <span className="text-accent font-medium text-sm">{data.weekday}</span>
                                </div>
                                <p className="text-foreground-secondary text-xs mt-0.5">
                                    农历 {data.lunarDate}
                                </p>
                            </div>
                            <button
                                onClick={() => onDateChange(1)}
                                className="p-1.5 rounded-md hover:bg-background border border-transparent hover:border-border transition-all text-foreground-secondary hover:text-foreground active:scale-95"
                            >
                                <ChevronRight className="w-5 h-5" />
                            </button>
                        </div>

                        {/* 第二行：流日/主神 + 命盘选择 */}
                        <div className="flex items-center justify-between gap-2">
                            {/* 流日/主神（横向紧凑布局） */}
                            {isPersonalized && dayStem && tenGod ? (
                                <div className="flex items-center gap-3 text-xs">
                                    <div className="flex items-center gap-1">
                                        <span className="text-foreground-secondary">流日:</span>
                                        <span className="font-bold">
                                            <span style={{ color: dayStemColor }}>{dayStem}</span>
                                            <span style={{ color: dayBranchColor }}>{dayBranch}</span>
                                        </span>
                                    </div>
                                    <div className="flex items-center gap-1">
                                        <span className="text-foreground-secondary">主神:</span>
                                        <span className="font-bold">{tenGod}</span>
                                    </div>
                                </div>
                            ) : (
                                <div className="flex-1" />
                            )}

                            {/* 命盘选择（简化版） */}
                            {isPersonalized && onChartSelect ? (
                                <button
                                    onClick={onChartSelect}
                                    className="flex items-center gap-1 px-2.5 py-1.5 bg-background hover:bg-background-secondary rounded-lg border border-border/60 hover:border-purple-500/30 transition-all text-xs active:scale-95"
                                >
                                    <span className="text-foreground-secondary">当前命盘:</span>
                                    <span className="font-medium text-purple-600 dark:text-purple-400 max-w-[60px] truncate">
                                        {chartName}
                                    </span>
                                    <ChevronDown className="w-3 h-3 text-foreground-secondary flex-shrink-0" />
                                </button>
                            ) : !isPersonalized && (
                                <SettingsCenterLink
                                    tab="charts"
                                    className="flex items-center gap-1 px-2.5 py-1.5 bg-amber-500/10 border border-amber-500/20 rounded-lg text-xs text-amber-600 hover:bg-amber-500/20 transition-colors active:scale-95"
                                >
                                    <Scroll className="w-3 h-3" />
                                    <span>设置默认八字命盘以获得个性化运势服务</span>
                                </SettingsCenterLink>
                            )}
                        </div>
                    </div>

                    {/* 桌面端：原有横向布局 */}
                    <div className="hidden md:flex items-center justify-between gap-3">
                        {/* 左侧：← 日期信息 → */}
                        <div className="flex items-center gap-1">
                            <button
                                onClick={() => onDateChange(-1)}
                                className="p-1.5 rounded-md hover:bg-background border border-transparent hover:border-border transition-all text-foreground-secondary hover:text-foreground"
                            >
                                <ChevronLeft className="w-5 h-5" />
                            </button>
                            <div className="text-center px-2">
                                {!isToday && onGoToday && (
                                    <div className="mb-1">
                                        <button
                                            onClick={onGoToday}
                                            className="inline-flex items-center text-[10px] text-foreground-secondary hover:text-foreground transition-colors"
                                        >
                                            返回今日
                                        </button>
                                    </div>
                                )}
                                <div className="flex items-baseline justify-center gap-2">
                                    <span className="text-xl font-bold">{data.solarDateChinese}</span>
                                    <span className="text-accent font-medium">{data.weekday}</span>
                                </div>
                                <p className="text-foreground-secondary text-sm">
                                    农历 {data.lunarDate}
                                </p>
                            </div>
                            <button
                                onClick={() => onDateChange(1)}
                                className="p-1.5 rounded-md hover:bg-background border border-transparent hover:border-border transition-all text-foreground-secondary hover:text-foreground"
                            >
                                <ChevronRight className="w-5 h-5" />
                            </button>
                        </div>

                        {/* 中间：流日/主神（竖排） */}
                        {isPersonalized && dayStem && tenGod && (
                            <div className="flex flex-col items-center gap-0.5 text-sm">
                                <div className="flex items-center gap-1">
                                    <span className="text-foreground-secondary">流日: </span>
                                    <span className="font-bold">
                                        <span style={{ color: dayStemColor }}>{dayStem}</span>
                                        <span style={{ color: dayBranchColor }}>{dayBranch}</span>
                                    </span>
                                </div>
                                <div className="flex items-center gap-1">
                                    <span className="text-foreground-secondary">主神: </span>
                                    <span className="font-bold">{tenGod}</span>
                                </div>
                            </div>
                        )}

                        {/* 右侧：命盘选择 */}
                        {isPersonalized && onChartSelect ? (
                            <button
                                onClick={onChartSelect}
                                className="flex items-center gap-1 px-2 py-1 bg-background hover:bg-background-secondary rounded-md border border-border/60 hover:border-purple-500/30 transition-all text-sm"
                            >
                                命主:
                                <span className="font-medium text-purple-600 dark:text-purple-400 max-w-[50px] truncate">
                                    {chartName}
                                </span>
                                <ChevronDown className="w-3 h-3 text-foreground-secondary" />
                            </button>
                        ) : !isPersonalized && (
                            <Link
                                href="/bazi"
                                className="flex items-center gap-1 px-2 py-1 bg-amber-500/10 border border-amber-500/20 rounded-md text-xs text-amber-600 hover:bg-amber-500/20 transition-colors"
                            >
                                <User className="w-3 h-3" />
                                <span>个性化</span>
                            </Link>
                        )}
                    </div>
                </div>
            )}

            {/* 无控制栏时显示日期标题 */}
            {!onDateChange && (
                <div className="p-4 border-b border-border">
                    <div className="flex items-baseline gap-2 mb-0.5">
                        <h2 className="text-xl font-bold">{data.solarDateChinese}</h2>
                        <span className="text-accent font-medium">{data.weekday}</span>
                    </div>
                    <p className="text-foreground-secondary text-sm">
                        农历 {data.lunarDate}
                    </p>
                </div>
            )}

            <div className="p-4 md:p-6 space-y-4 md:space-y-6">
                {/* 生肖 & 干支 */}
                <div className="grid grid-cols-1 md:grid-cols-2 gap-3 md:gap-4 text-xs md:text-sm">
                    <div className="flex flex-wrap items-center gap-x-3 gap-y-1">
                        <span className="text-foreground-secondary whitespace-nowrap">生肖：</span>
                        <span className="whitespace-nowrap">{data.shengXiao.year}年</span>
                        <span className="whitespace-nowrap">{data.shengXiao.month}月</span>
                        <span className="whitespace-nowrap">{data.shengXiao.day}日</span>
                    </div>
                    <div className="flex flex-wrap items-center gap-x-3 gap-y-1">
                        <span className="text-foreground-secondary whitespace-nowrap">干支：</span>
                        <span className="whitespace-nowrap">{renderGanZhi(data.ganZhi.year)}年</span>
                        <span className="whitespace-nowrap">{renderGanZhi(data.ganZhi.month)}月</span>
                        <span className="whitespace-nowrap">{renderGanZhi(data.ganZhi.day)}日</span>
                    </div>
                </div>

                {/* 纳音 */}
                <div className="text-xs md:text-sm">
                    <span className="text-foreground-secondary">纳音：</span>
                    <span>{data.naYin.year} {data.naYin.month} {data.naYin.day}</span>
                </div>

                {/* 节气 */}
                {(data.jieQi.current || data.jieQi.next) && (
                    <div className="p-2.5 md:p-3 rounded-lg border border-border text-xs md:text-sm space-y-1.5 md:space-y-1">
                        <div className="text-foreground-secondary font-medium mb-1.5 md:mb-2">节气：</div>
                        {data.jieQi.current && (
                            <div className="flex items-center gap-1.5 md:gap-2 flex-wrap">
                                <Calendar className="w-3 md:w-3.5 h-3 md:h-3.5 text-accent flex-shrink-0" />
                                <span className="flex-shrink-0">当前节气：{data.jieQi.current.name}</span>
                                <span className="text-foreground-secondary">({data.jieQi.current.date})</span>
                                <div className="flex items-center gap-1">
                                    <Clock className="w-2.5 md:w-3 h-2.5 md:h-3 text-foreground-tertiary" />
                                    <span className="text-foreground-secondary text-[10px] md:text-xs">{data.jieQi.current.time}</span>
                                </div>
                            </div>
                        )}
                        {data.jieQi.next && (
                            <div className="flex items-center gap-1.5 md:gap-2 flex-wrap">
                                <Calendar className="w-3 md:w-3.5 h-3 md:h-3.5 text-foreground-secondary flex-shrink-0" />
                                <span className="text-foreground-secondary flex-shrink-0">下一节气：{data.jieQi.next.name}</span>
                                <span className="text-foreground-secondary">({data.jieQi.next.date})</span>
                                <div className="flex items-center gap-1">
                                    <Clock className="w-2.5 md:w-3 h-2.5 md:h-3 text-foreground-tertiary" />
                                    <span className="text-foreground-tertiary text-[10px] md:text-xs">{data.jieQi.next.time}</span>
                                </div>
                            </div>
                        )}
                    </div>
                )}

                {/* 宜忌 */}
                <div className="grid grid-cols-2 gap-3 md:gap-4">
                    {/* 宜 */}
                    <div>
                        <h3 className="text-xs md:text-sm font-medium text-emerald-500 flex items-center gap-1 mb-2">
                            <CheckCircle className="w-3 md:w-3.5 h-3 md:h-3.5" />
                            宜
                        </h3>
                        <div className="flex flex-wrap gap-1 md:gap-1.5">
                            {data.yi.length > 0 ? (
                                <>
                                    {(yiExpanded ? data.yi : data.yi.slice(0, 4)).map((item, idx) => (
                                        <span
                                            key={idx}
                                            className="px-1.5 md:px-2 py-0.5 text-[10px] md:text-xs rounded bg-emerald-500/10 text-emerald-600 dark:text-emerald-400 border border-emerald-500/20"
                                        >
                                            {item}
                                        </span>
                                    ))}
                                    {data.yi.length > 4 && (
                                        <button
                                            onClick={() => setYiExpanded(!yiExpanded)}
                                            className="px-1.5 md:px-2 py-0.5 text-[10px] md:text-xs text-emerald-600 dark:text-emerald-400 hover:bg-emerald-500/10 rounded transition-colors"
                                        >
                                            {yiExpanded ? '收起' : `+${data.yi.length - 4} ↓`}
                                        </button>
                                    )}
                                </>
                            ) : (
                                <span className="text-[10px] md:text-xs text-foreground-secondary">诸事不宜</span>
                            )}
                        </div>
                    </div>

                    {/* 忌 */}
                    <div>
                        <h3 className="text-xs md:text-sm font-medium text-rose-500 flex items-center gap-1 mb-2">
                            <XCircle className="w-3 md:w-3.5 h-3 md:h-3.5" />
                            忌
                        </h3>
                        <div className="flex flex-wrap gap-1 md:gap-1.5">
                            {data.ji.length > 0 ? (
                                <>
                                    {(jiExpanded ? data.ji : data.ji.slice(0, 4)).map((item, idx) => (
                                        <span
                                            key={idx}
                                            className="px-1.5 md:px-2 py-0.5 text-[10px] md:text-xs rounded bg-rose-500/10 text-rose-600 dark:text-rose-400 border border-rose-500/20"
                                        >
                                            {item}
                                        </span>
                                    ))}
                                    {data.ji.length > 4 && (
                                        <button
                                            onClick={() => setJiExpanded(!jiExpanded)}
                                            className="px-1.5 md:px-2 py-0.5 text-[10px] md:text-xs text-rose-600 dark:text-rose-400 hover:bg-rose-500/10 rounded transition-colors"
                                        >
                                            {jiExpanded ? '收起' : `+${data.ji.length - 4}`}
                                        </button>
                                    )}
                                </>
                            ) : (
                                <span className="text-[10px] md:text-xs text-foreground-secondary">无</span>
                            )}
                        </div>
                    </div>
                </div>

                {/* 吉神凶煞 */}
                <div className="grid grid-cols-2 gap-3 md:gap-4 text-xs md:text-sm">
                    <div>
                        <h3 className="font-medium mb-1">吉神</h3>
                        <p className="text-emerald-600 dark:text-emerald-400 break-words">
                            {data.jiShen.length > 0 ? data.jiShen.join('、') : '无'}
                        </p>
                    </div>
                    <div>
                        <h3 className="font-medium mb-1">凶煞</h3>
                        <p className="text-rose-600 dark:text-rose-400 break-words">
                            {data.xiongSha.length > 0 ? data.xiongSha.join('、') : '无'}
                        </p>
                    </div>
                </div>

                {/* 冲煞 & 空亡 */}
                <div className="grid grid-cols-2 gap-3 md:gap-4 text-xs md:text-sm">
                    <div>
                        <span className="text-foreground-secondary">冲煞：</span>
                        <span>{data.chongSha.chong || '-'}</span>
                    </div>
                    <div>
                        <span className="text-foreground-secondary">空亡：</span>
                        <span>{data.kongWang || '-'}</span>
                    </div>
                </div>

                {/* 胎神 & 天神 */}
                <div className="grid grid-cols-2 gap-3 md:gap-4 text-xs md:text-sm">
                    <div>
                        <span className="text-foreground-secondary">胎神：</span>
                        <span>{data.taiShen || '-'}</span>
                    </div>
                    <div>
                        <span className="text-foreground-secondary">天神：</span>
                        <span className={isBlackDay(data.zhiShen) ? 'text-rose-500' : 'text-emerald-500'}>
                            {getZhiShenDesc(data.zhiShen) || '-'}
                        </span>
                    </div>
                </div>

                {/* 神位 */}
                <div className="grid grid-cols-2 gap-2 md:gap-3 text-xs md:text-sm">
                    <div className="flex items-center gap-1.5 md:gap-2">
                        <MapPin className="w-3 md:w-3.5 h-3 md:h-3.5 text-amber-500 flex-shrink-0" />
                        <span className="text-foreground-secondary whitespace-nowrap">财神位：</span>
                        <span className="truncate">{data.shenWei.caiShen || '-'}</span>
                    </div>
                    <div className="flex items-center gap-1.5 md:gap-2">
                        <MapPin className="w-3 md:w-3.5 h-3 md:h-3.5 text-pink-500 flex-shrink-0" />
                        <span className="text-foreground-secondary whitespace-nowrap">喜神位：</span>
                        <span className="truncate">{data.shenWei.xiShen || '-'}</span>
                    </div>
                    <div className="flex items-center gap-1.5 md:gap-2">
                        <MapPin className="w-3 md:w-3.5 h-3 md:h-3.5 text-emerald-500 flex-shrink-0" />
                        <span className="text-foreground-secondary whitespace-nowrap">福神位：</span>
                        <span className="truncate">{data.shenWei.fuShen || '-'}</span>
                    </div>
                    <div className="flex items-center gap-1.5 md:gap-2">
                        <MapPin className="w-3 md:w-3.5 h-3 md:h-3.5 text-purple-500 flex-shrink-0" />
                        <span className="text-foreground-secondary whitespace-nowrap">阳贵神：</span>
                        <span className="truncate">{data.shenWei.yangGuiShen || '-'}</span>
                    </div>
                </div>

                {/* 扩展信息 */}
                <div className="pt-4 md:pt-8 border-t border-border text-xs md:text-sm space-y-1.5 md:space-y-2 text-foreground-secondary">
                    <div className="flex justify-between">
                        <span>二十八宿：{data.xiu.gong} {data.xiu.name} ({data.xiu.luck})</span>
                        <span>月相：{data.yueXiang}</span>
                    </div>
                    <div className="flex justify-between">
                        <span>六曜：{data.liuYao}</span>
                        <span>九星：{data.jiuXing}</span>
                    </div>
                    <div>
                        <span>物候：{data.wuHou}</span>
                    </div>
                </div>
            </div>
        </section>
    );
}
