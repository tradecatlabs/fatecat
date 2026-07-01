/**
 * 智能四柱输入组件
 * 年柱、日柱：分开选择天干和地支（符合六十甲子规则）
 * 月柱：根据年柱计算，选择完整组合
 * 时柱：根据日柱计算，选择完整组合
 * 最后反推出具体时间
 */
'use client';

import { useState, useMemo } from 'react';
import { X, Calendar, Trash2 } from 'lucide-react';
import type { HeavenlyStem, EarthlyBranch, PillarData } from '@/types';
import { reversePillars } from '@/lib/divination/pillars-reverse';
import {
    calculateMonthPillars,
    calculateHourPillars,
    getAvailableBranches,
} from '@/lib/divination/pillars-calculator';
import { useToast } from '@/components/ui/Toast';

// 天干选项
const HEAVENLY_STEMS: HeavenlyStem[] = ['甲', '乙', '丙', '丁', '戊', '己', '庚', '辛', '壬', '癸'];

// 五行颜色映射（与结果页面一致）
// 木-绿色, 火-红色, 土-黄色, 金-金色, 水-蓝色
const ELEMENT_BG_COLORS: Record<string, string> = {
    // 天干
    '甲': 'bg-emerald-50 text-emerald-700', '乙': 'bg-emerald-50 text-emerald-700',  // 木
    '丙': 'bg-red-50 text-red-600', '丁': 'bg-red-50 text-red-600',                  // 火
    '戊': 'bg-gray-50 text-[#8B4513]', '己': 'bg-gray-50 text-[#8B4513]',          // 土
    '庚': 'bg-yellow-50 text-yellow-600', '辛': 'bg-yellow-50 text-yellow-600',      // 金
    '壬': 'bg-blue-50 text-blue-600', '癸': 'bg-blue-50 text-blue-600',              // 水
    // 地支
    '寅': 'bg-emerald-50 text-emerald-700', '卯': 'bg-emerald-50 text-emerald-700',  // 木
    '巳': 'bg-red-50 text-red-600', '午': 'bg-red-50 text-red-600',                  // 火
    '辰': 'bg-gray-50 text-[#8B4513]', '戌': 'bg-gray-50 text-[#8B4513]',          // 土
    '丑': 'bg-gray-50 text-[#8B4513]', '未': 'bg-gray-50 text-[#8B4513]',          // 土
    '申': 'bg-yellow-50 text-yellow-600', '酉': 'bg-yellow-50 text-yellow-600',      // 金
    '亥': 'bg-blue-50 text-blue-600', '子': 'bg-blue-50 text-blue-600',              // 水
};

type PillarType = 'year' | 'month' | 'day' | 'hour';
// 选择步骤：年天干 -> 年地支 -> 月柱 -> 日天干 -> 日地支 -> 时柱
type SelectionStep = 'year_stem' | 'year_branch' | 'month' | 'day_stem' | 'day_branch' | 'hour' | 'complete';

interface SmartPillarsInputProps {
    value?: {
        year: PillarData;
        month: PillarData;
        day: PillarData;
        hour: PillarData;
    };
    onChange: (pillars: {
        year: PillarData;
        month: PillarData;
        day: PillarData;
        hour: PillarData;
    }, dateTime?: {
        year: number;
        month: number;
        day: number;
        hour: number;
        minute: number;
    }) => void;
}

interface ReversedDateTime {
    year: number;
    month: number;
    day: number;
    hour: number;
    minute: number;
    solarDate: string;
    lunarDate: string;
}

// 选择步骤的标签
const STEP_LABELS: Record<SelectionStep, string> = {
    'year_stem': '年柱天干',
    'year_branch': '年柱地支',
    'month': '月柱',
    'day_stem': '日柱天干',
    'day_branch': '日柱地支',
    'hour': '时柱',
    'complete': '完成',
};

const EMPTY_PILLARS: {
    year: PillarData;
    month: PillarData;
    day: PillarData;
    hour: PillarData;
} = {
    year: { stem: '', branch: '' },
    month: { stem: '', branch: '' },
    day: { stem: '', branch: '' },
    hour: { stem: '', branch: '' },
};

export function SmartPillarsInput({ value, onChange }: SmartPillarsInputProps) {
    const [possibleDates, setPossibleDates] = useState<ReversedDateTime[]>([]);
    const [showDateSelector, setShowDateSelector] = useState(false);
    const { showToast } = useToast();

    // 初始化为空的四柱
    const pillars = value || EMPTY_PILLARS;

    // 判断柱是否完整
    const isPillarComplete = (p: PillarData) => p.stem !== '' && p.branch !== '';

    // 获取当前选择步骤
    const currentStep = useMemo((): SelectionStep => {
        // 年柱：先天干后地支
        if (pillars.year.stem === '') return 'year_stem';
        if (pillars.year.branch === '') return 'year_branch';
        // 月柱：完整选择
        if (!isPillarComplete(pillars.month)) return 'month';
        // 日柱：先天干后地支
        if (pillars.day.stem === '') return 'day_stem';
        if (pillars.day.branch === '') return 'day_branch';
        // 时柱：完整选择
        if (!isPillarComplete(pillars.hour)) return 'hour';
        return 'complete';
    }, [pillars]);

    // 计算年柱可选地支（根据已选天干）
    const yearBranchOptions = useMemo(() => {
        if (pillars.year.stem === '') return [];
        return getAvailableBranches(pillars.year.stem as HeavenlyStem);
    }, [pillars.year.stem]);

    // 计算月柱选项（根据年柱）
    const monthOptions = useMemo(() => {
        if (!isPillarComplete(pillars.year)) return [];
        return calculateMonthPillars(pillars.year as { stem: HeavenlyStem; branch: EarthlyBranch });
    }, [pillars.year]);

    // 计算日柱可选地支（根据已选天干）
    const dayBranchOptions = useMemo(() => {
        if (pillars.day.stem === '') return [];
        return getAvailableBranches(pillars.day.stem as HeavenlyStem);
    }, [pillars.day.stem]);

    // 计算时柱选项（根据日柱）
    const hourOptions = useMemo(() => {
        if (!isPillarComplete(pillars.day)) return [];
        return calculateHourPillars(pillars.day as { stem: HeavenlyStem; branch: EarthlyBranch });
    }, [pillars.day]);

    // 选择年柱天干（清空年地支及后续所有柱）
    const handleSelectYearStem = (stem: HeavenlyStem) => {
        onChange({
            year: { stem, branch: '' },
            month: { stem: '', branch: '' },
            day: { stem: '', branch: '' },
            hour: { stem: '', branch: '' },
        });
    };

    // 选择年柱地支（清空月柱及后续所有柱）
    const handleSelectYearBranch = (branch: EarthlyBranch) => {
        onChange({
            ...pillars,
            year: { ...pillars.year, branch },
            month: { stem: '', branch: '' },
            day: { stem: '', branch: '' },
            hour: { stem: '', branch: '' },
        });
    };

    // 选择月柱（清空日柱及时柱）
    const handleSelectMonth = (month: { stem: HeavenlyStem; branch: EarthlyBranch }) => {
        onChange({
            ...pillars,
            month,
            day: { stem: '', branch: '' },
            hour: { stem: '', branch: '' },
        });
    };

    // 选择日柱天干（清空日地支及时柱）
    const handleSelectDayStem = (stem: HeavenlyStem) => {
        onChange({
            ...pillars,
            day: { stem, branch: '' },
            hour: { stem: '', branch: '' },
        });
    };

    // 选择日柱地支（清空时柱）
    const handleSelectDayBranch = (branch: EarthlyBranch) => {
        onChange({
            ...pillars,
            day: { ...pillars.day, branch },
            hour: { stem: '', branch: '' },
        });
    };

    // 选择时柱并尝试反推时间
    const handleSelectHour = (hour: { stem: HeavenlyStem; branch: EarthlyBranch }) => {
        const newPillars = { ...pillars, hour };

        // 所有四柱都选择完整，进行反推时间
        const completePillars = {
            year: newPillars.year as { stem: HeavenlyStem; branch: EarthlyBranch },
            month: newPillars.month as { stem: HeavenlyStem; branch: EarthlyBranch },
            day: newPillars.day as { stem: HeavenlyStem; branch: EarthlyBranch },
            hour: newPillars.hour as { stem: HeavenlyStem; branch: EarthlyBranch },
        };
        const dates = reversePillars(completePillars);

        if (dates.length === 0) {
            // 没有找到匹配时间，但仍然保存四柱
            onChange(newPillars);
            showToast('warning', '在1900-2100年范围内未找到匹配的时间，四柱已保存');
        } else if (dates.length === 1) {
            onChange(newPillars, {
                year: dates[0].year,
                month: dates[0].month,
                day: dates[0].day,
                hour: dates[0].hour,
                minute: dates[0].minute,
            });
        } else {
            onChange(newPillars);
            setPossibleDates(dates);
            setShowDateSelector(true);
        }
    };

    // 清除所有选择
    const handleClear = () => {
        onChange({
            year: { stem: '', branch: '' },
            month: { stem: '', branch: '' },
            day: { stem: '', branch: '' },
            hour: { stem: '', branch: '' },
        });
        setPossibleDates([]);
        setShowDateSelector(false);
    };

    // 选择日期
    const handleDateSelect = (date: ReversedDateTime) => {
        onChange(pillars, {
            year: date.year,
            month: date.month,
            day: date.day,
            hour: date.hour,
            minute: date.minute,
        });
        setShowDateSelector(false);
        setPossibleDates([]);
    };

    const pillarLabels = { year: '年柱', month: '月柱', day: '日柱', hour: '时柱' };

    // 处理点击已选择的天干/地支进行清空
    const handleClickToEdit = (pillarType: PillarType, part: 'stem' | 'branch') => {
        // 根据点击的位置清空该位置及后续所有柱
        if (pillarType === 'year') {
            if (part === 'stem') {
                // 清空年柱天干及后续所有
                onChange({
                    year: { stem: '', branch: '' },
                    month: { stem: '', branch: '' },
                    day: { stem: '', branch: '' },
                    hour: { stem: '', branch: '' },
                });
            } else {
                // 清空年柱地支及后续所有
                onChange({
                    ...pillars,
                    year: { ...pillars.year, branch: '' },
                    month: { stem: '', branch: '' },
                    day: { stem: '', branch: '' },
                    hour: { stem: '', branch: '' },
                });
            }
        } else if (pillarType === 'month') {
            // 清空月柱及后续所有
            onChange({
                ...pillars,
                month: { stem: '', branch: '' },
                day: { stem: '', branch: '' },
                hour: { stem: '', branch: '' },
            });
        } else if (pillarType === 'day') {
            if (part === 'stem') {
                // 清空日柱天干及后续所有
                onChange({
                    ...pillars,
                    day: { stem: '', branch: '' },
                    hour: { stem: '', branch: '' },
                });
            } else {
                // 清空日柱地支及后续所有
                onChange({
                    ...pillars,
                    day: { ...pillars.day, branch: '' },
                    hour: { stem: '', branch: '' },
                });
            }
        } else if (pillarType === 'hour') {
            // 清空时柱
            onChange({
                ...pillars,
                hour: { stem: '', branch: '' },
            });
        }
    };

    // 渲染天干选择按钮
    const renderStemButtons = (onSelect: (stem: HeavenlyStem) => void) => (
        <div className="grid grid-cols-5 gap-2">
            {HEAVENLY_STEMS.map((stem) => (
                <button
                    key={stem}
                    type="button"
                    onClick={() => onSelect(stem)}
                    className={`
                        py-2.5 rounded-full text-base font-bold
                        transition-all duration-200 hover:scale-105
                        ${ELEMENT_BG_COLORS[stem]}
                        border border-transparent hover:border-accent/50
                    `}
                >
                    {stem}
                </button>
            ))}
        </div>
    );

    // 渲染地支选择按钮
    const renderBranchButtons = (branches: EarthlyBranch[], onSelect: (branch: EarthlyBranch) => void) => (
        <div className="grid grid-cols-6 gap-2">
            {branches.map((branch) => (
                <button
                    key={branch}
                    type="button"
                    onClick={() => onSelect(branch)}
                    className={`
                        py-2.5 rounded-full text-base font-bold
                        transition-all duration-200 hover:scale-105
                        ${ELEMENT_BG_COLORS[branch]}
                        border border-transparent hover:border-accent/50
                    `}
                >
                    {branch}
                </button>
            ))}
        </div>
    );

    // 渲染完整柱选择按钮
    const renderPillarButtons = (
        options: { stem: HeavenlyStem; branch: EarthlyBranch }[],
        onSelect: (p: { stem: HeavenlyStem; branch: EarthlyBranch }) => void
    ) => (
        <div className="grid grid-cols-4 gap-2">
            {options.map((p, index) => (
                <button
                    key={`${p.stem}${p.branch}-${index}`}
                    type="button"
                    onClick={() => onSelect(p)}
                    className={`
                        py-2 px-1 rounded-lg text-sm font-bold
                        transition-all duration-200 hover:scale-105
                        ${ELEMENT_BG_COLORS[p.stem]}
                        border border-transparent hover:border-accent/50
                    `}
                >
                    {p.stem}{p.branch}
                </button>
            ))}
        </div>
    );

    return (
        <>
            <div className="space-y-4">
                {/* 四柱显示区域 */}
                <div className="grid grid-cols-4 gap-2">
                    {(['year', 'month', 'day', 'hour'] as PillarType[]).map((pillarType) => {
                        const pillar = pillars[pillarType];
                        const isComplete = isPillarComplete(pillar);
                        const hasStem = pillar.stem !== '';
                        const hasBranch = pillar.branch !== '';
                        const isCurrent = (
                            (pillarType === 'year' && (currentStep === 'year_stem' || currentStep === 'year_branch')) ||
                            (pillarType === 'month' && currentStep === 'month') ||
                            (pillarType === 'day' && (currentStep === 'day_stem' || currentStep === 'day_branch')) ||
                            (pillarType === 'hour' && currentStep === 'hour')
                        );

                        // 判断天干/地支是否可点击（已有值才可点击重新编辑）
                        const canClickStem = hasStem;
                        const canClickBranch = hasBranch;

                        return (
                            <div key={pillarType} className="text-center">
                                <div className="text-xs text-foreground-secondary mb-2">
                                    {pillarLabels[pillarType]}
                                </div>
                                <div className="space-y-1">
                                    {/* 天干 */}
                                    <button
                                        type="button"
                                        onClick={() => canClickStem && handleClickToEdit(pillarType, 'stem')}
                                        disabled={!canClickStem}
                                        className={`
                                            w-12 h-12 rounded-full flex items-center justify-center
                                            text-base font-bold transition-all mx-auto
                                            ${hasStem
                                                ? `${ELEMENT_BG_COLORS[pillar.stem]} ${canClickStem ? 'cursor-pointer hover:ring-2 hover:ring-accent/50' : ''}`
                                                : isCurrent
                                                    ? 'bg-accent/10 border-2 border-dashed border-accent'
                                                    : 'bg-background-secondary border-2 border-transparent'
                                            }
                                            disabled:cursor-default
                                        `}
                                    >
                                        {pillar.stem || ''}
                                    </button>
                                    {/* 地支 */}
                                    <button
                                        type="button"
                                        onClick={() => canClickBranch && handleClickToEdit(pillarType, 'branch')}
                                        disabled={!canClickBranch}
                                        className={`
                                            w-12 h-12 rounded-full flex items-center justify-center
                                            text-base font-bold transition-all mx-auto
                                            ${isComplete
                                                ? `${ELEMENT_BG_COLORS[pillar.branch]} ${canClickBranch ? 'cursor-pointer hover:ring-2 hover:ring-accent/50' : ''}`
                                                : isCurrent && hasStem
                                                    ? 'bg-accent/10 border-2 border-dashed border-accent'
                                                    : 'bg-background-secondary border-2 border-transparent'
                                            }
                                            disabled:cursor-default
                                        `}
                                    >
                                        {pillar.branch || ''}
                                    </button>
                                </div>
                            </div>
                        );
                    })}
                </div>

                {/* 查找范围和清除按钮 */}
                <div className="flex items-center justify-between text-xs text-foreground-secondary">
                    <span>查找范围：1900-2100年</span>
                    <button
                        type="button"
                        onClick={handleClear}
                        className="flex items-center gap-1 text-foreground-secondary hover:text-red-500 transition-colors"
                    >
                        <Trash2 className="w-3.5 h-3.5" />
                        清除
                    </button>
                </div>

                {/* 选择区域 */}
                {currentStep !== 'complete' && (
                    <div className="space-y-2">
                        <div className="text-xs text-foreground-secondary">
                            请选择{STEP_LABELS[currentStep]}：
                        </div>

                        {/* 年柱天干选择 */}
                        {currentStep === 'year_stem' && renderStemButtons(handleSelectYearStem)}

                        {/* 年柱地支选择 */}
                        {currentStep === 'year_branch' && renderBranchButtons(yearBranchOptions, handleSelectYearBranch)}

                        {/* 月柱选择 */}
                        {currentStep === 'month' && renderPillarButtons(monthOptions, handleSelectMonth)}

                        {/* 日柱天干选择 */}
                        {currentStep === 'day_stem' && renderStemButtons(handleSelectDayStem)}

                        {/* 日柱地支选择 */}
                        {currentStep === 'day_branch' && renderBranchButtons(dayBranchOptions, handleSelectDayBranch)}

                        {/* 时柱选择 */}
                        {currentStep === 'hour' && renderPillarButtons(hourOptions, handleSelectHour)}
                    </div>
                )}

                {/* 全部完成提示 */}
                {currentStep === 'complete' && (
                    <div className="text-center text-sm text-green-600 py-2">
                        四柱选择完成
                    </div>
                )}
            </div>

            {/* 时间选择模态框 */}
            {showDateSelector && possibleDates.length > 0 && (
                <div className="fixed inset-0 z-50 flex items-center justify-center p-4 animate-fade-in">
                    <div className="absolute inset-0 bg-black/50" onClick={() => setShowDateSelector(false)} />

                    <div className="relative bg-background rounded-xl shadow-xl max-w-2xl w-full max-h-[80vh] overflow-y-auto">
                        <div className="sticky top-0 bg-background border-b border-border px-6 py-4 flex items-center justify-between">
                            <h2 className="text-lg font-semibold flex items-center gap-2">
                                <Calendar className="w-5 h-5 text-accent" />
                                选择具体时间
                            </h2>
                            <button
                                type="button"
                                onClick={() => setShowDateSelector(false)}
                                className="text-foreground-secondary hover:text-foreground transition-colors"
                            >
                                <X className="w-5 h-5" />
                            </button>
                        </div>

                        <div className="p-6 space-y-3">
                            <p className="text-sm text-foreground-secondary mb-4">
                                找到 {possibleDates.length} 个可能的时间，请选择您的出生时间：
                            </p>
                            {possibleDates.map((date, index) => (
                                <button
                                    key={index}
                                    type="button"
                                    onClick={() => handleDateSelect(date)}
                                    className="w-full p-4 border border-border rounded-lg hover:border-accent/50 hover:bg-background-secondary transition-all text-left"
                                >
                                    <div className="font-medium">{date.solarDate}</div>
                                    <div className="text-sm text-foreground-secondary mt-1">{date.lunarDate}</div>
                                </button>
                            ))}
                        </div>
                    </div>
                </div>
            )}
        </>
    );
}
