/**
 * 四柱反推时间工具
 * 根据完整的四柱（年月日时）反推出可能的出生日期时间
 */

import { Solar } from 'lunar-javascript';
import type { EarthlyBranch, HeavenlyStem } from '@/types';

// 完整的柱数据（不包含空字符串）
interface CompletePillarData {
    stem: HeavenlyStem;
    branch: EarthlyBranch;
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

interface FourPillars {
    year: CompletePillarData;
    month: CompletePillarData;
    day: CompletePillarData;
    hour: CompletePillarData;
}

/**
 * 根据年柱反推可能的公历年份（1900-2100年）
 * 注意：干支年以立春为界，一个公历年可能包含两个干支年
 * 所以需要同时检查1月（可能是上一个干支年）和6月（当年干支年）
 */
export function reverseYear(yearPillar: CompletePillarData): number[] {
    const years: number[] = [];
    const startYear = 1900;
    const endYear = 2100;

    for (let year = startYear; year <= endYear; year++) {
        try {
            // 检查1月15日（可能是上一个干支年，立春前）
            const solar1 = Solar.fromYmd(year, 1, 15);
            const ec1 = solar1.getLunar().getEightChar();
            if (ec1.getYearGan() === yearPillar.stem && ec1.getYearZhi() === yearPillar.branch) {
                if (!years.includes(year)) years.push(year);
            }

            // 检查6月15日（当年干支年，立春后）
            const solar6 = Solar.fromYmd(year, 6, 15);
            const ec6 = solar6.getLunar().getEightChar();
            if (ec6.getYearGan() === yearPillar.stem && ec6.getYearZhi() === yearPillar.branch) {
                if (!years.includes(year)) years.push(year);
            }
        } catch {
            // 忽略无效日期
        }
    }

    return years;
}

/**
 * 根据年柱和月柱反推可能的月份（1-12）
 * 需要同时验证年柱，因为同一公历年可能跨越两个干支年
 * 月柱以节气为界，需要检查月初和月中来覆盖节气变化
 */
export function reverseMonth(
    year: number,
    yearPillar: CompletePillarData,
    monthPillar: CompletePillarData
): number[] {
    const months: number[] = [];

    for (let month = 1; month <= 12; month++) {
        // 检查月初（1日）和月中（15日），覆盖节气变化
        const checkDays = [1, 15];
        for (const checkDay of checkDays) {
            try {
                const solar = Solar.fromYmd(year, month, checkDay);
                const eightChar = solar.getLunar().getEightChar();

                if (eightChar.getYearGan() === yearPillar.stem &&
                    eightChar.getYearZhi() === yearPillar.branch &&
                    eightChar.getMonthGan() === monthPillar.stem &&
                    eightChar.getMonthZhi() === monthPillar.branch) {
                    if (!months.includes(month)) {
                        months.push(month);
                    }
                }
            } catch {
                // 忽略无效日期
            }
        }
    }

    return months;
}

/**
 * 根据日柱反推可能的日期
 */
export function reverseDay(
    year: number,
    month: number,
    dayPillar: CompletePillarData
): number[] {
    const days: number[] = [];
    const daysInMonth = new Date(year, month, 0).getDate();

    for (let day = 1; day <= daysInMonth; day++) {
        try {
            const solar = Solar.fromYmd(year, month, day);
            const lunar = solar.getLunar();
            const eightChar = lunar.getEightChar();

            const dayGan = eightChar.getDayGan();
            const dayZhi = eightChar.getDayZhi();

            if (dayGan === dayPillar.stem && dayZhi === dayPillar.branch) {
                days.push(day);
            }
        } catch {
            // 忽略无效日期
        }
    }

    return days;
}

/**
 * 根据时柱反推可能的时辰（0-23小时）
 */
export function reverseHour(hourPillar: CompletePillarData): number[] {
    const branchToHours: Record<EarthlyBranch, number[]> = {
        '子': [23, 0],
        '丑': [1, 2],
        '寅': [3, 4],
        '卯': [5, 6],
        '辰': [7, 8],
        '巳': [9, 10],
        '午': [11, 12],
        '未': [13, 14],
        '申': [15, 16],
        '酉': [17, 18],
        '戌': [19, 20],
        '亥': [21, 22],
    };

    return branchToHours[hourPillar.branch] || [];
}

/**
 * 根据完整的四柱反推可能的出生日期时间
 * 返回所有匹配的日期时间组合（按农历时间去重）
 */
export function reversePillars(pillars: FourPillars): ReversedDateTime[] {
    const results: ReversedDateTime[] = [];
    const seenLunarDates = new Set<string>();

    // 1. 反推年份
    const possibleYears = reverseYear(pillars.year);

    for (const year of possibleYears) {
        // 2. 反推月份（需要同时传入年柱进行验证）
        const possibleMonths = reverseMonth(year, pillars.year, pillars.month);

        for (const month of possibleMonths) {
            // 3. 反推日期
            const possibleDays = reverseDay(year, month, pillars.day);

            for (const day of possibleDays) {
                // 4. 反推时辰
                const possibleHours = reverseHour(pillars.hour);

                for (const hour of possibleHours) {
                    try {
                        // 验证这个日期时间的四柱是否完全匹配
                        const solar = Solar.fromYmdHms(year, month, day, hour, 0, 0);
                        const lunar = solar.getLunar();
                        const eightChar = lunar.getEightChar();

                        const yearGan = eightChar.getYearGan();
                        const yearZhi = eightChar.getYearZhi();
                        const monthGan = eightChar.getMonthGan();
                        const monthZhi = eightChar.getMonthZhi();
                        const dayGan = eightChar.getDayGan();
                        const dayZhi = eightChar.getDayZhi();

                        // 验证四柱是否完全匹配
                        if (
                            yearGan === pillars.year.stem && yearZhi === pillars.year.branch &&
                            monthGan === pillars.month.stem && monthZhi === pillars.month.branch &&
                            dayGan === pillars.day.stem && dayZhi === pillars.day.branch
                        ) {
                            // 生成农历时间的唯一标识（用于去重）
                            const lunarKey = `${lunar.getYearInChinese()}年${lunar.getMonthInChinese()}月${lunar.getDayInChinese()}${pillars.hour.branch}时`;

                            // 按农历时间去重，同一个时辰只保留一个结果
                            if (!seenLunarDates.has(lunarKey)) {
                                seenLunarDates.add(lunarKey);
                                results.push({
                                    year,
                                    month,
                                    day,
                                    hour,
                                    minute: 0,
                                    solarDate: `${year}年${month}月${day}日 ${String(hour).padStart(2, '0')}:00`,
                                    lunarDate: `农历${lunar.getYearInChinese()}年${lunar.getMonthInChinese()}月${lunar.getDayInChinese()} ${pillars.hour.branch}时`,
                                });
                            }
                        }
                    } catch {
                        // 忽略无效日期
                    }
                }
            }
        }
    }

    return results;
}
