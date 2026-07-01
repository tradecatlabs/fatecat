/**
 * 紫微运势面板组件
 *
 * 'use client' 标记说明：
 * - 使用 React hooks (useReducer, useMemo, useEffect, useCallback)
 * - 有大限/流年选择交互功能
 */
'use client';

import { useReducer, useMemo, useEffect, useCallback } from 'react';
import { TrendingUp, Calendar } from 'lucide-react';
import type { ZiweiCanonicalJSON, ZiweiOutput as CoreZiweiOutput } from 'taibu-core/ziwei';
import type { ZiweiHoroscopeCanonicalJSON } from 'taibu-core/ziwei-horoscope';
import type { Astrolabe, DecadalInfo } from '@/lib/divination/ziwei';
import { buildZiweiHoroscopeCanonicalJSON } from '@/lib/divination/ziwei';
import { getStemElement, getBranchElement, getElementColor } from '@/lib/divination/display-helpers';

export interface HoroscopeInfo {
    decadal?: DecadalInfo;
    yearly?: { heavenlyStem: string; earthlyBranch: string; palaceIndex: number };
    monthly?: { heavenlyStem: string; earthlyBranch: string; palaceIndex: number };
    daily?: { heavenlyStem: string; earthlyBranch: string; palaceIndex: number };
}

export interface HoroscopeHighlight {
    decadalIndex?: number;
    yearlyIndex?: number;
    monthlyIndex?: number;
    dailyIndex?: number;
}

interface ZiweiHoroscopePanelProps {
    output: CoreZiweiOutput;
    astrolabe: Astrolabe;
    canonicalChart: ZiweiCanonicalJSON;
    onPalaceHighlight?: (highlights: HoroscopeHighlight) => void;
    onHoroscopeChange?: (info: HoroscopeInfo) => void;
}

// Fix 2: useReducer 统一管理选择状态
interface SelectionState {
    selectedDecadalIndex: number | null;
    selectedYear: number | null;
    selectedMonth: number | null;
    selectedDay: number | null;
}

type SelectionAction =
    | { type: 'SELECT_DECADAL'; index: number | null }
    | { type: 'SELECT_YEAR'; year: number | null; decadalIndex?: number }
    | { type: 'SELECT_MONTH'; month: number | null; year?: number }
    | { type: 'SELECT_DAY'; day: number | null; year?: number; month?: number }
    | { type: 'DESELECT_YEAR' }
    | { type: 'DESELECT_MONTH' }
    | { type: 'DESELECT_DAY' };

const initialSelectionState: SelectionState = {
    selectedDecadalIndex: null,
    selectedYear: null,
    selectedMonth: null,
    selectedDay: null,
};

function selectionReducer(state: SelectionState, action: SelectionAction): SelectionState {
    switch (action.type) {
        case 'SELECT_DECADAL': {
            const nextIndex = state.selectedDecadalIndex === action.index ? null : action.index;
            return { ...initialSelectionState, selectedDecadalIndex: nextIndex };
        }
        case 'SELECT_YEAR':
            return {
                ...state,
                selectedDecadalIndex: action.decadalIndex ?? state.selectedDecadalIndex,
                selectedYear: action.year,
                selectedMonth: null,
                selectedDay: null,
            };
        case 'DESELECT_YEAR':
            return { ...state, selectedYear: null, selectedMonth: null, selectedDay: null };
        case 'SELECT_MONTH':
            return {
                ...state,
                selectedYear: action.year ?? state.selectedYear,
                selectedMonth: action.month,
                selectedDay: null,
            };
        case 'DESELECT_MONTH':
            return { ...state, selectedMonth: null, selectedDay: null };
        case 'SELECT_DAY':
            return {
                ...state,
                selectedYear: action.year ?? state.selectedYear,
                selectedMonth: action.month ?? state.selectedMonth,
                selectedDay: action.day,
            };
        case 'DESELECT_DAY':
            return { ...state, selectedDay: null };
        default:
            return state;
    }
}

// Fix 1: 模块级缓存，避免重复排盘计算
const canonicalHoroscopeCacheMap = new WeakMap<object, Map<string, ReturnType<typeof buildZiweiHoroscopeCanonicalJSON>>>();

function getCachedHoroscopeCanonical(output: CoreZiweiOutput, astrolabe: Astrolabe, date: Date) {
    const cacheKey = astrolabe;
    let dateCache = canonicalHoroscopeCacheMap.get(cacheKey);
    if (!dateCache) {
        dateCache = new Map();
        canonicalHoroscopeCacheMap.set(cacheKey, dateCache);
    }
    const dateKey = date.toISOString().split('T')[0];
    if (dateCache.has(dateKey)) {
        return dateCache.get(dateKey)!;
    }
    const result = buildZiweiHoroscopeCanonicalJSON(output, astrolabe, date);
    dateCache.set(dateKey, result);
    return result;
}

export function ZiweiHoroscopePanel({ output, astrolabe, canonicalChart, onPalaceHighlight, onHoroscopeChange }: ZiweiHoroscopePanelProps) {
    const [state, dispatch] = useReducer(selectionReducer, initialSelectionState);
    const { selectedDecadalIndex, selectedYear, selectedMonth, selectedDay } = state;

    // 派生布尔值，无需存储在 state 中
    const decadalSelected = selectedDecadalIndex !== null;
    const yearlySelected = selectedYear !== null;
    const monthlySelected = selectedMonth !== null;
    const dailySelected = selectedDay !== null;

    // 获取大限列表
    const decadalList = useMemo(() => (
        canonicalChart.十二宫位
            .map((palace) => {
                if (typeof palace.宫位索引 !== 'number' || !palace.大限) return null;
                const match = palace.大限.match(/^(\d+)~(\d+)$/u);
                if (!match) return null;
                return {
                    index: palace.宫位索引,
                    startAge: Number(match[1]),
                    endAge: Number(match[2]),
                    palace: {
                        index: palace.宫位索引,
                        name: palace.宫位,
                        heavenlyStem: palace.干支.charAt(0),
                        earthlyBranch: palace.干支.charAt(1),
                    },
                    heavenlyStem: palace.干支.charAt(0),
                };
            })
            .filter((item): item is DecadalInfo => Boolean(item))
            .sort((a, b) => a.startAge - b.startAge)
    ), [canonicalChart.十二宫位]);

    // Fix 3: birthYear 提取为 useMemo 常量
    const birthYear = useMemo(() => parseInt(canonicalChart.基本信息.阳历.split('-')[0]), [canonicalChart.基本信息.阳历]);

    // Fix 4: 去掉 useMemo，直接在 render 中获取当前日期
    const today = new Date();
    const viewYear = selectedYear ?? today.getFullYear();
    const viewMonth = selectedMonth ?? (today.getMonth() + 1);

    const yearlyHoroscope = useMemo<ZiweiHoroscopeCanonicalJSON | null>(() => {
        if (!selectedYear) return null;
        return getCachedHoroscopeCanonical(output, astrolabe, new Date(selectedYear, 5, 15));
    }, [output, astrolabe, selectedYear]);

    const monthlyHoroscope = useMemo<ZiweiHoroscopeCanonicalJSON | null>(() => {
        if (!selectedYear || !selectedMonth) return null;
        return getCachedHoroscopeCanonical(output, astrolabe, new Date(selectedYear, selectedMonth - 1, 15));
    }, [output, astrolabe, selectedYear, selectedMonth]);

    const dailyHoroscope = useMemo<ZiweiHoroscopeCanonicalJSON | null>(() => {
        if (!selectedYear || !selectedMonth || !selectedDay) return null;
        return getCachedHoroscopeCanonical(output, astrolabe, new Date(selectedYear, selectedMonth - 1, selectedDay));
    }, [output, astrolabe, selectedYear, selectedMonth, selectedDay]);

    const yearlyPeriod = yearlyHoroscope?.运限叠宫.find((period) => period.层次 === '流年');
    const monthlyPeriod = monthlyHoroscope?.运限叠宫.find((period) => period.层次 === '流月');
    const dailyPeriod = dailyHoroscope?.运限叠宫.find((period) => period.层次 === '流日');

    // 获取选中的大限
    const selectedDecadal = useMemo(() =>
        decadalList.find(d => d.index === selectedDecadalIndex) ?? null,
        [decadalList, selectedDecadalIndex]);
    const displayDecadal = selectedDecadal ?? decadalList[0] ?? null;

    // 更新高亮宫位和运限信息
    const updateHighlight = useCallback(() => {
        const highlights: HoroscopeHighlight = {};
        const info: HoroscopeInfo = {};

        if (decadalSelected && selectedDecadal) {
            highlights.decadalIndex = selectedDecadal.palace.index;
            info.decadal = selectedDecadal;
        }

        if (yearlySelected && yearlyPeriod) {
            highlights.yearlyIndex = yearlyPeriod.宫位索引;
            info.yearly = {
                heavenlyStem: yearlyPeriod.干支.charAt(0),
                earthlyBranch: yearlyPeriod.干支.charAt(1),
                palaceIndex: yearlyPeriod.宫位索引,
            };
        }
        if (monthlySelected && monthlyPeriod) {
            highlights.monthlyIndex = monthlyPeriod.宫位索引;
            info.monthly = {
                heavenlyStem: monthlyPeriod.干支.charAt(0),
                earthlyBranch: monthlyPeriod.干支.charAt(1),
                palaceIndex: monthlyPeriod.宫位索引,
            };
        }
        if (dailySelected && dailyPeriod) {
            highlights.dailyIndex = dailyPeriod.宫位索引;
            info.daily = {
                heavenlyStem: dailyPeriod.干支.charAt(0),
                earthlyBranch: dailyPeriod.干支.charAt(1),
                palaceIndex: dailyPeriod.宫位索引,
            };
        }

        onPalaceHighlight?.(highlights);
        onHoroscopeChange?.(info);
    }, [
        onPalaceHighlight,
        onHoroscopeChange,
        selectedDecadal,
        yearlyPeriod,
        monthlyPeriod,
        dailyPeriod,
        decadalSelected,
        yearlySelected,
        monthlySelected,
        dailySelected,
    ]);

    // 状态变化时更新高亮
    useEffect(() => {
        updateHighlight();
    }, [updateHighlight]);

    // 计算当前大限内的流年列表
    const yearlyList = useMemo(() => {
        if (!displayDecadal) return [];
            const startYear = birthYear + displayDecadal.startAge;
        const endYear = birthYear + displayDecadal.endAge;
        const years: { year: number; stem: string; branch: string; palace: string }[] = [];

        for (let year = startYear; year <= endYear; year++) {
            const yearDate = new Date(year, 5, 15);
            const yearHoroscope = getCachedHoroscopeCanonical(output, astrolabe, yearDate);
            const yearly = yearHoroscope?.运限叠宫.find((period) => period.层次 === '流年');
            if (yearly) {
                years.push({
                    year,
                    stem: yearly.干支.charAt(0),
                    branch: yearly.干支.charAt(1),
                    palace: yearly.落入本命宫位.replace(/宫$/u, ''),
                });
            }
        }
        return years;
    }, [output, astrolabe, displayDecadal, birthYear]);

    // 计算当前选中年份的12个月（仅在选中流年后才计算）
    const monthlyList = useMemo(() => {
        if (!selectedYear) return [];
        const months: { month: number; stem: string; branch: string; palace: string }[] = [];
        for (let m = 1; m <= 12; m++) {
            const monthDate = new Date(viewYear, m - 1, 15);
            const monthHoroscope = getCachedHoroscopeCanonical(output, astrolabe, monthDate);
            const monthly = monthHoroscope?.运限叠宫.find((period) => period.层次 === '流月');
            if (monthly) {
                months.push({
                    month: m,
                    stem: monthly.干支.charAt(0),
                    branch: monthly.干支.charAt(1),
                    palace: monthly.落入本命宫位.replace(/宫$/u, ''),
                });
            }
        }
        return months;
    }, [output, astrolabe, viewYear, selectedYear]);

    // 计算当前选中月份的日期列表（仅在选中流月后才计算）
    const dailyList = useMemo(() => {
        if (!selectedMonth) return [];
        const year = viewYear;
        const month = viewMonth - 1;
        const daysInMonth = new Date(year, month + 1, 0).getDate();
        const days: { day: number; stem: string; branch: string; palace: string }[] = [];

        for (let d = 1; d <= daysInMonth; d++) {
            const dayDate = new Date(year, month, d);
            const dayHoroscope = getCachedHoroscopeCanonical(output, astrolabe, dayDate);
            const daily = dayHoroscope?.运限叠宫.find((period) => period.层次 === '流日');
            if (daily) {
                days.push({
                    day: d,
                    stem: daily.干支.charAt(0),
                    branch: daily.干支.charAt(1),
                    palace: daily.落入本命宫位.replace(/宫$/u, ''),
                });
            }
        }
        return days;
    }, [output, astrolabe, viewYear, viewMonth, selectedMonth]);

    // 大限选择 - 支持取消，切换大限时清除流年/流月/流日
    const handleDecadalSelect = (d: DecadalInfo) => {
        dispatch({ type: 'SELECT_DECADAL', index: d.index });
    };

    // 获取天干或地支的五行颜色样式
    const getCharColorStyle = (char: string) => {
        const stemElement = getStemElement(char);
        if (stemElement) return { color: getElementColor(stemElement) };
        const branchElement = getBranchElement(char);
        if (branchElement) return { color: getElementColor(branchElement) };
        return {};
    };

    return (
        <div className="sm:space-y-4 space-y-1">
            {/* 大限 */}
            <section className="bg-background rounded-xl md:p-4 p-1 max-w-[390px] mx-auto sm:max-w-none">
                <h2 className="text-base font-semibold sm:mb-3 mb-1 flex items-center gap-2">
                    <TrendingUp className="w-4 h-4 text-accent" />
                    大限（每运10年）
                </h2>
                <div className="overflow-x-auto sm:-mx-4 sm:px-4 scrollbar-hide">
                    <div className="flex sm:gap-2 gap-1 min-w-max sm:pb-2">
                        {decadalList.map(d => {
                            const isSelected = decadalSelected && selectedDecadalIndex === d.index;
                            return (
                                <button
                                    key={d.index}
                                    onClick={() => handleDecadalSelect(d)}
                                    className={`
                                        flex-shrink-0 w-9.5 sm:w-16 text-center sm:p-2 rounded-lg border-2 transition-all
                                        ${isSelected
                                            ? 'border-accent bg-accent/10'
                                            : 'border-transparent bg-background hover:bg-background'
                                        }
                                    `}
                                >
                                    <div className="text-xs text-foreground-secondary">{d.palace.name}</div>
                                    <div className="text-xs text-foreground-secondary">{d.startAge}岁</div>
                                    <div className="flex flex-col items-center mt-1">
                                        <span
                                            className="text-base sm:text-lg font-bold"
                                            style={getCharColorStyle(d.heavenlyStem)}
                                        >
                                            {d.heavenlyStem}
                                        </span>
                                        <span
                                            className="text-base sm:text-lg font-bold"
                                            style={getCharColorStyle(d.palace.earthlyBranch)}
                                        >
                                            {d.palace.earthlyBranch}
                                        </span>
                                    </div>
                                </button>
                            );
                        })}
                    </div>
                </div>
            </section>

            {/* 流年 */}
            {displayDecadal && yearlyList.length > 0 && (
                <section className="bg-background rounded-xl md:p-4 p-1 max-w-[390px] mx-auto sm:max-w-none">
                    <h2 className="text-base font-semibold sm:mb-3 mb-1 flex items-center gap-2">
                        <Calendar className="w-4 h-4 text-accent" />
                        流年
                    </h2>
                    <div className="overflow-x-auto sm:-mx-4 sm:px-4 scrollbar-hide">
                        <div className="flex sm:gap-2 gap-1 min-w-max sm:pb-2">
                            {yearlyList.map(yearInfo => {
                                const isSelected = yearlySelected && selectedYear === yearInfo.year;
                                const age = yearInfo.year - birthYear;
                                return (
                                    <button
                                        key={yearInfo.year}
                                        onClick={() => {
                                            if (isSelected) {
                                                dispatch({ type: 'DESELECT_YEAR' });
                                                return;
                                            }
                                            dispatch({
                                                type: 'SELECT_YEAR',
                                                year: yearInfo.year,
                                                decadalIndex: displayDecadal?.index,
                                            });
                                        }}
                                        className={`
                                            flex-shrink-0 w-9.5 sm:w-14 text-center sm:p-2 rounded-lg border-2 transition-all
                                            ${isSelected
                                                ? 'border-accent bg-accent/10'
                                                : 'border-transparent bg-background hover:bg-background'
                                            }
                                        `}
                                    >
                                        <div className="text-xs text-foreground-secondary">{yearInfo.year}</div>
                                        <div className="flex flex-col items-center mt-1">
                                            <span
                                                className="text-sm sm:text-base font-bold"
                                                style={getCharColorStyle(yearInfo.stem)}
                                            >
                                                {yearInfo.stem}
                                            </span>
                                            <span
                                                className="text-sm sm:text-base font-bold"
                                                style={getCharColorStyle(yearInfo.branch)}
                                            >
                                                {yearInfo.branch}
                                            </span>
                                        </div>
                                        <div className="text-xs text-foreground-secondary">{age}岁</div>
                                    </button>
                                );
                            })}
                        </div>
                    </div>
                </section>
            )}

            {/* 流月 */}
            {selectedYear && monthlyList.length > 0 && (
                <section className="bg-background rounded-xl md:p-4 p-1 max-w-[390px] mx-auto sm:max-w-none">
                    <h2 className="text-base font-semibold sm:mb-3 mb-1 flex items-center gap-2">
                        <Calendar className="w-4 h-4 text-accent" />
                        {viewYear}年流月
                    </h2>
                    <div className="overflow-x-auto sm:-mx-4 sm:px-4 scrollbar-hide">
                        <div className="flex sm:gap-1.5 gap-1 min-w-max sm:pb-2">
                            {monthlyList.map(monthInfo => {
                                const isSelected = monthlySelected && selectedMonth === monthInfo.month && selectedYear === viewYear;
                                return (
                                    <button
                                        key={monthInfo.month}
                                        type="button"
                                        onClick={() => {
                                            if (isSelected) {
                                                dispatch({ type: 'DESELECT_MONTH' });
                                                return;
                                            }
                                            dispatch({
                                                type: 'SELECT_MONTH',
                                                month: monthInfo.month,
                                                year: selectedYear === null ? viewYear : undefined,
                                            });
                                        }}
                                        className={`
                                            flex-shrink-0 w-9 sm:w-12 text-center sm:p-1.5 rounded-lg border-2 transition-all
                                            ${isSelected
                                                ? 'border-accent bg-accent/10'
                                                : 'border-transparent bg-background hover:bg-background-secondary'
                                            }
                                        `}
                                    >
                                        <div className="text-xs text-foreground-secondary">{monthInfo.month}月</div>
                                        <div className="flex flex-col items-center mt-0.5">
                                            <span
                                                className="text-sm font-bold"
                                                style={getCharColorStyle(monthInfo.stem)}
                                            >
                                                {monthInfo.stem}
                                            </span>
                                            <span
                                                className="text-sm font-bold"
                                                style={getCharColorStyle(monthInfo.branch)}
                                            >
                                                {monthInfo.branch}
                                            </span>
                                        </div>
                                    </button>
                                );
                            })}
                        </div>
                    </div>
                    <p className="mt-2 text-xs text-foreground-secondary">
                        点击流月可查看对应的流日
                    </p>
                </section>
            )}

            {/* 流日 */}
            {selectedMonth && dailyList.length > 0 && (
                <section className="bg-background rounded-xl md:p-4 p-1 max-w-[390px] mx-auto sm:max-w-none">
                    <h2 className="text-base font-semibold sm:mb-3 mb-1 flex items-center gap-2">
                        <Calendar className="w-4 h-4 text-accent" />
                        {viewYear}年{viewMonth}月流日
                    </h2>
                    <div className="overflow-x-auto sm:-mx-4 sm:px-4 scrollbar-hide">
                        <div className="flex sm:gap-1.5 gap-1 min-w-max sm:pb-2">
                            {dailyList.map(dayInfo => {
                                const isSelected = dailySelected && selectedDay === dayInfo.day && selectedMonth === viewMonth && selectedYear === viewYear;
                                return (
                                    <button
                                        key={dayInfo.day}
                                        type="button"
                                        onClick={() => {
                                            if (isSelected) {
                                                dispatch({ type: 'DESELECT_DAY' });
                                                return;
                                            }
                                            dispatch({
                                                type: 'SELECT_DAY',
                                                day: dayInfo.day,
                                                year: selectedYear === null ? viewYear : undefined,
                                                month: selectedMonth === null ? viewMonth : undefined,
                                            });
                                        }}
                                        className={`
                                            flex-shrink-0 w-10.5 sm:w-13 text-center sm:p-1.5 rounded-lg border-2 transition-all
                                            ${isSelected
                                                ? 'border-accent bg-accent/10'
                                                : 'border-transparent bg-background hover:bg-background-secondary'
                                            }
                                        `}
                                    >
                                        <div className="text-xs text-foreground-secondary">{dayInfo.day}日</div>
                                        <div className="flex flex-col items-center gap-0.5 text-xs mt-0.5">
                                            <span
                                                className="font-semibold"
                                                style={getCharColorStyle(dayInfo.stem)}
                                            >
                                                {dayInfo.stem}
                                            </span>
                                            <span
                                                className="font-semibold"
                                                style={getCharColorStyle(dayInfo.branch)}
                                            >
                                                {dayInfo.branch}
                                            </span>
                                        </div>
                                    </button>
                                );
                            })}
                        </div>
                    </div>
                </section>
            )}

        </div>
    );
}
