import { calculateZiweiChartBundle, generateZiweiChartText, type ZiweiFormData } from '@/lib/divination/ziwei';
import { resolveChartTextDetailLevel, type ChartTextDetailLevel } from '@/lib/divination/detail-level';

export type ZiweiPromptInput = {
    id?: string;
    name?: string;
    gender?: ZiweiFormData['gender'] | string;
    birthDate?: string;
    birthTime?: string;
    longitude?: number;
    birthPlace?: string;
    calendarType?: ZiweiFormData['calendarType'];
    isLeapMonth?: boolean;
};

type ResolvedZiweiPromptData = ReturnType<typeof calculateZiweiChartBundle>;

function rebuildZiweiChart(chart: ZiweiPromptInput): ResolvedZiweiPromptData | null {
    const birthDate = chart.birthDate;
    const birthTime = chart.birthTime;
    if (!birthDate || !birthTime) return null;

    const [birthYear, birthMonth, birthDay] = birthDate.split('-').map(Number);
    const [birthHour, birthMinute] = birthTime.split(':').map(Number);
    if (
        !Number.isFinite(birthYear)
        || !Number.isFinite(birthMonth)
        || !Number.isFinite(birthDay)
        || !Number.isFinite(birthHour)
        || !Number.isFinite(birthMinute)
    ) {
        return null;
    }

    try {
        return calculateZiweiChartBundle({
            name: chart.name || '未命名',
            gender: chart.gender === 'female' ? 'female' : 'male',
            birthYear,
            birthMonth,
            birthDay,
            birthHour,
            birthMinute,
            birthPlace: chart.birthPlace,
            longitude: chart.longitude,
            calendarType: chart.calendarType === 'lunar' ? 'lunar' : 'solar',
            isLeapMonth: chart.isLeapMonth ?? false,
        });
    } catch {
        return null;
    }
}

export function resolveZiweiPromptData(chart?: ZiweiPromptInput): ResolvedZiweiPromptData | null {
    if (!chart) return null;
    return rebuildZiweiChart(chart);
}

export function formatZiweiPromptText(chart?: ZiweiPromptInput, detailLevel?: ChartTextDetailLevel): string {
    const resolved = resolveZiweiPromptData(chart);
    if (!resolved) return '';
    return generateZiweiChartText(resolved.output, {
        detailLevel: resolveChartTextDetailLevel('ziwei', detailLevel),
    });
}
