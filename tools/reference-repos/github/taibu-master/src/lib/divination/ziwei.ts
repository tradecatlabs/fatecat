/**
 * 紫微斗数排盘核心逻辑
 *
 * web 侧保留展示/交互辅助，但主排盘真源来自 core。
 */

import {
    calculateZiweiDataWithAstrolabe,
    createAstrolabeWithTrueSolar,
    toZiweiJson,
    toZiweiText,
    type ZiweiCanonicalJSON,
    type ZiweiOutput as CoreZiweiOutput,
} from 'taibu-core/ziwei';
import {
    calculateZiweiHoroscopeDataWithAstrolabe,
    toZiweiHoroscopeJson,
    type ZiweiHoroscopeCanonicalJSON,
    type ZiweiHoroscopeOutput as CoreZiweiHoroscopeOutput,
} from 'taibu-core/ziwei-horoscope';
import type { Gender, CalendarType } from '@/types';
import { resolveChartTextDetailLevel, type ChartTextDetailLevel } from '@/lib/divination/detail-level';

export type Astrolabe = ReturnType<typeof createAstrolabeWithTrueSolar>['astrolabe'];

function toCoreZiweiInput(formData: ZiweiFormData) {
    return {
        gender: formData.gender,
        birthYear: formData.birthYear,
        birthMonth: formData.birthMonth,
        birthDay: formData.birthDay,
        birthHour: formData.birthHour,
        birthMinute: formData.birthMinute,
        calendarType: formData.calendarType === 'lunar' ? 'lunar' as const : 'solar' as const,
        isLeapMonth: formData.isLeapMonth,
        longitude: formData.longitude,
    };
}

// ===== 类型定义 =====

/** 紫微斗数表单数据 */
export interface ZiweiFormData {
    name: string;
    gender: Gender;
    birthYear: number;
    birthMonth: number;
    birthDay: number;
    birthHour: number;
    birthMinute: number;
    calendarType: CalendarType;
    isLeapMonth?: boolean; // 是否闰月
    birthPlace?: string; // 出生地点（不参与排盘，仅用于存储）
    longitude?: number;
    isUnknownTime?: boolean; // 是否未知时辰
}

// ===== 常量 =====

const EARTHLY_BRANCHES = ['子', '丑', '寅', '卯', '辰', '巳', '午', '未', '申', '酉', '戌', '亥'];

const PALACE_LAYOUT_ORDER = [
    5, 6, 7, 8,    // 巳午未申 (第一行)
    4, -1, -1, 9,  // 辰-中空-酉 (第二行)
    3, -1, -1, 10, // 卯-中空-戌 (第三行)
    2, 1, 0, 11,   // 寅丑子亥 (第四行)
];

const PALACE_TEXT_ORDER = ['命宫', '兄弟', '夫妻', '子女', '财帛', '疾厄', '迁移', '交友', '官禄', '田宅', '福德', '父母'];

// ===== 主要导出函数 =====

export function calculateZiweiChartBundle(formData: ZiweiFormData): {
    output: CoreZiweiOutput;
    astrolabe: Astrolabe;
} {
    const { output, astrolabe } = calculateZiweiDataWithAstrolabe(toCoreZiweiInput(formData));
    return {
        output,
        astrolabe,
    };
}

/**
 * 获取宫位的传统排列顺序（用于 4x3 布局）
 * 返回索引数组，按照：
 *   [巳] [午] [未] [申]
 *   [辰]         [酉]
 *   [卯]         [戌]
 *   [寅] [丑] [子] [亥]
 */
export function getPalaceLayoutOrder(): number[] {
    return PALACE_LAYOUT_ORDER;
}

/**
 * 根据地支获取宫位索引
 */
export function getBranchIndex(branch: string): number {
    return EARTHLY_BRANCHES.indexOf(branch);
}

// ===== 运限类型定义 =====

/** 运限宫位信息 */
export interface HoroscopePalaceInfo {
    index: number;
    name: string;
    heavenlyStem: string;
    earthlyBranch: string;
    mutagen?: string[];
}

/** 大限信息 */
export interface DecadalInfo {
    index: number;
    startAge: number;
    endAge: number;
    palace: HoroscopePalaceInfo;
    heavenlyStem: string;
}

/** 流年/流月/流日信息 */
export interface FlowPeriodInfo {
    period: string;  // year/month/day value
    palace: HoroscopePalaceInfo;
    heavenlyStem: string;
    earthlyBranch: string;
}

/** 完整运限数据 */
export interface ZiweiHoroscope {
    decadal: DecadalInfo;
    yearly: FlowPeriodInfo;
    monthly: FlowPeriodInfo;
    daily: FlowPeriodInfo;
}

// ===== 运限计算函数 =====

/**
 * 获取指定日期的运限信息（复用 core shared horoscope helper）
 */
export function getHoroscope(output: CoreZiweiOutput, astrolabe: Astrolabe, date: Date = new Date()): ZiweiHoroscope | null {
    try {
        const horoscope = calculateZiweiHoroscopeDataWithAstrolabe(astrolabe, {
            targetDate: date,
        });
        const decadalRange = getDecadalList(output).find((item) => item.index === horoscope.decadal.index);
        const decadal: DecadalInfo = {
            index: horoscope.decadal.index,
            startAge: decadalRange?.startAge ?? 0,
            endAge: decadalRange?.endAge ?? 0,
            palace: {
                index: horoscope.decadal.index,
                name: horoscope.decadal.name,
                heavenlyStem: horoscope.decadal.heavenlyStem,
                earthlyBranch: horoscope.decadal.earthlyBranch,
                mutagen: horoscope.decadal.mutagen,
            },
            heavenlyStem: horoscope.decadal.heavenlyStem,
        };

        const yearly: FlowPeriodInfo = {
            period: String(date.getFullYear()),
            palace: {
                index: horoscope.yearly.index,
                name: horoscope.yearly.name,
                heavenlyStem: horoscope.yearly.heavenlyStem,
                earthlyBranch: horoscope.yearly.earthlyBranch,
                mutagen: horoscope.yearly.mutagen,
            },
            heavenlyStem: horoscope.yearly.heavenlyStem,
            earthlyBranch: horoscope.yearly.earthlyBranch,
        };

        const monthly: FlowPeriodInfo = {
            period: String(date.getMonth() + 1),
            palace: {
                index: horoscope.monthly.index,
                name: horoscope.monthly.name,
                heavenlyStem: horoscope.monthly.heavenlyStem,
                earthlyBranch: horoscope.monthly.earthlyBranch,
                mutagen: horoscope.monthly.mutagen,
            },
            heavenlyStem: horoscope.monthly.heavenlyStem,
            earthlyBranch: horoscope.monthly.earthlyBranch,
        };

        const daily: FlowPeriodInfo = {
            period: horoscope.targetDate,
            palace: {
                index: horoscope.daily.index,
                name: horoscope.daily.name,
                heavenlyStem: horoscope.daily.heavenlyStem,
                earthlyBranch: horoscope.daily.earthlyBranch,
                mutagen: horoscope.daily.mutagen,
            },
            heavenlyStem: horoscope.daily.heavenlyStem,
            earthlyBranch: horoscope.daily.earthlyBranch,
        };

        return { decadal, yearly, monthly, daily };
    } catch (error) {
        console.error('获取运限信息失败:', error);
        return null;
    }
}

export function buildZiweiHoroscopeCanonicalJSON(_output: CoreZiweiOutput, astrolabe: Astrolabe, date: Date = new Date()) {
    try {
        const result = calculateZiweiHoroscopeDataWithAstrolabe(astrolabe, {
            targetDate: date,
        }) as CoreZiweiHoroscopeOutput;
        return toZiweiHoroscopeJson(result) as ZiweiHoroscopeCanonicalJSON;
    } catch (error) {
        console.error('构建紫微运限 JSON 失败:', error);
        return null;
    }
}

/**
 * 获取大限列表
 */
export function getDecadalList(output: CoreZiweiOutput): DecadalInfo[] {
    return output.decadalList
        .map((item, index) => {
            const palaceIndex = output.palaces.findIndex((palace) =>
                palace.name === item.palace.name && palace.earthlyBranch === item.palace.earthlyBranch
            );
            const resolvedIndex = palaceIndex >= 0 ? palaceIndex : index;
            return {
                index: resolvedIndex,
                startAge: item.startAge,
                endAge: item.endAge,
                palace: {
                    index: resolvedIndex,
                    name: item.palace.name,
                    heavenlyStem: item.heavenlyStem,
                    earthlyBranch: item.palace.earthlyBranch,
                },
                heavenlyStem: item.heavenlyStem,
            };
        })
        .sort((a, b) => a.startAge - b.startAge);
}

// ===== 三方四正 =====

/**
 * 获取宫位的三方四正索引
 */
export function getTriangleSquare(palaceIndex: number): {
    self: number;
    opposite: number;
    triangle: number[];
    square: number[];
} {
    const normalize = (i: number) => ((i % 12) + 12) % 12;
    const self = normalize(palaceIndex);
    const opposite = normalize(palaceIndex + 6);
    const left = normalize(palaceIndex + 4);
    const right = normalize(palaceIndex - 4);

    return {
        self,
        opposite,
        triangle: [self, left, right],
        square: [self, opposite, left, right],
    };
}

/**
 * 获取宫位名称对应的索引
 */
export function getPalaceIndexByName(output: CoreZiweiOutput, name: string): number {
    return output.palaces.findIndex((palace) => palace.name === name);
}

function getTraditionalTextPalaces(output: CoreZiweiOutput) {
    return [...output.palaces].sort((leftPalace, rightPalace) => {
        const left = PALACE_TEXT_ORDER.indexOf(leftPalace.name);
        const right = PALACE_TEXT_ORDER.indexOf(rightPalace.name);
        const leftOrder = left >= 0 ? left : Number.MAX_SAFE_INTEGER;
        const rightOrder = right >= 0 ? right : Number.MAX_SAFE_INTEGER;
        if (leftOrder !== rightOrder) return leftOrder - rightOrder;
        return (leftPalace.index ?? 0) - (rightPalace.index ?? 0);
    });
}

export function buildZiweiCanonicalJSON(output: CoreZiweiOutput) {
    return toZiweiJson({
        ...output,
        palaces: getTraditionalTextPalaces(output),
    }, { detailLevel: 'full' }) as ZiweiCanonicalJSON;
}

/**
 * 生成紫微命盘文字版本（用于AI分析和复制）
 */
export function generateZiweiChartText(
    output: CoreZiweiOutput,
    options: { includeHoroscope?: boolean; detailLevel?: ChartTextDetailLevel; astrolabe?: Astrolabe } = {},
): string {
    const detailLevel = resolveChartTextDetailLevel('ziwei', options.detailLevel);
    const orderedOutput: CoreZiweiOutput = {
        ...output,
        palaces: getTraditionalTextPalaces(output),
    };

    if (!options.includeHoroscope || !options.astrolabe) {
        return toZiweiText(orderedOutput, { detailLevel });
    }

    const horoscope = getHoroscope(output, options.astrolabe, new Date());
    if (!horoscope) {
        return toZiweiText(orderedOutput, { detailLevel });
    }

    return toZiweiText(orderedOutput, {
        detailLevel,
        horoscope: {
            decadal: { palaceName: horoscope.decadal.palace.name, ageRange: `${horoscope.decadal.startAge}-${horoscope.decadal.endAge}岁` },
            yearly: { palaceName: horoscope.yearly.palace.name, period: horoscope.yearly.period },
            monthly: { palaceName: horoscope.monthly.palace.name, period: horoscope.monthly.period },
            daily: { palaceName: horoscope.daily.palace.name, period: horoscope.daily.period },
        },
    });
}
