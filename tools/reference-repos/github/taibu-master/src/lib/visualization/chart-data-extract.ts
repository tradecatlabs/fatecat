/**
 * 从 Markdown 文本中提取 ```chart 代码块的 JSON 数据
 *
 * AI 回复中的图表数据以 ```chart ... ``` 格式嵌入。
 * 此工具函数提取并解析这些 JSON 块，用于图表数据复用。
 */

import type {
    ChartData,
    ChartType,
    FortuneRadarData,
    LifeFortuneTrendData,
} from '@/lib/visualization/chart-types';
import { getDimensionConfig, normalizeDimensionKey } from '@/lib/visualization/dimensions';

const CHART_BLOCK_REGEX = /```chart\s*\n([\s\S]*?)```/g;

type FortuneRadarPayload = FortuneRadarData['data'];
type FortuneRadarScores = FortuneRadarPayload['scores'];
type LifeFortuneTrendPayload = LifeFortuneTrendData['data'];
type LifeFortuneTrendPeriod = LifeFortuneTrendPayload['periods'][number];
type LifeFortuneTrendYearlyScore = NonNullable<LifeFortuneTrendPeriod['yearlyScores']>[number];
type LifeFortuneTrendTurningDirection = LifeFortuneTrendPayload['lifeHighlight']['nextTurningPoint']['direction'];

export interface ExtractedChart {
    chartType: ChartType;
    title: string;
    raw: ChartData;
}

/**
 * 从 markdown 文本中提取所有 chart 块并解析为 ChartData。
 * 无效 JSON 会被静默跳过。
 */
export function extractChartBlocks(markdown: string): ExtractedChart[] {
    const results: ExtractedChart[] = [];
    let match: RegExpExecArray | null;

    // Reset regex state
    CHART_BLOCK_REGEX.lastIndex = 0;

    while ((match = CHART_BLOCK_REGEX.exec(markdown)) !== null) {
        const jsonStr = match[1]?.trim();
        if (!jsonStr) continue;

        try {
            const parsed = JSON.parse(jsonStr) as ChartData;
            if (parsed && typeof parsed.chartType === 'string' && typeof parsed.title === 'string') {
                const normalized = normalizeChartData(parsed);
                results.push({
                    chartType: normalized.chartType,
                    title: normalized.title,
                    raw: normalized,
                });
            }
        } catch {
            // Skip malformed chart blocks
        }
    }

    return results;
}

/**
 * 从对话 messages 数组中提取所有 AI 回复里的 chart 数据。
 * 返回去重后的图表列表（按 chartType + title 去重，保留最新的）。
 */
export function extractChartsFromMessages(
    messages: Array<{ role: string; content: string }>,
): ExtractedChart[] {
    const seen = new Map<string, ExtractedChart>();

    for (const msg of messages) {
        if (msg.role !== 'assistant') continue;
        const charts = extractChartBlocks(msg.content);
        for (const chart of charts) {
            // Later messages override earlier ones for the same chart type + title
            seen.set(`${chart.chartType}:${chart.title}`, chart);
        }
    }

    return Array.from(seen.values());
}

/**
 * 将提取的图表数据格式化为可注入 AI prompt 的参考文本。
 * 用于在对话中引用之前生成的图表，避免 AI 重复生成。
 */
export function formatPreviousChartsForPrompt(charts: ExtractedChart[], maxCharts = 3): string {
    if (charts.length === 0) return '';

    const selected = charts.slice(-maxCharts);
    const lines = selected.map((chart) => {
        return `- ${chart.title} (${chart.chartType})`;
    });

    return [
        '用户之前的分析中已生成以下图表，如果与当前问题相关，可以参考或更新其中的数据，而不必从头生成：',
        ...lines,
    ].join('\n');
}

export function normalizeChartData(chart: ChartData): ChartData {
    const data = asRecord(chart.data);
    if (!data) return chart;

    if (chart.chartType === 'fortune_radar') {
        return {
            ...chart,
            data: normalizeFortuneRadarData(data),
        };
    }

    if (chart.chartType === 'life_fortune_trend') {
        return {
            ...chart,
            data: normalizeLifeFortuneTrendData(data),
        };
    }

    return chart;
}

function normalizeFortuneRadarData(data: Record<string, unknown>): FortuneRadarPayload {
    const scores = normalizeRadarScores(data.scores);
    const previousScores = normalizeNumericDimensionScores(data.previousScores);
    const computedOverall = average(Object.values(scores).map((entry) => entry.score));

    return {
        ...data,
        period: normalizeString(data.period),
        scores,
        previousScores,
        overallScore: normalizeScore(data.overallScore) ?? computedOverall ?? 0,
        overallLabel: normalizeString(data.overallLabel),
        topAdvice: normalizeString(data.topAdvice),
    };
}

function normalizeLifeFortuneTrendData(data: Record<string, unknown>): LifeFortuneTrendPayload {
    const currentAge = toFiniteNumber(data.currentAge);
    const currentYear = toFiniteNumber(data.currentYear);
    const rawPeriods = Array.isArray(data.periods) ? data.periods : [];

    const periods = rawPeriods
        .map((period, index) => normalizeLifeFortuneTrendPeriod(asRecord(period), index, currentAge, currentYear))
        .filter((period): period is NonNullable<typeof period> => period !== null);

    const rawLifeHighlight = asRecord(data.lifeHighlight);
    const rawBestPeriod = asRecord(rawLifeHighlight?.bestPeriod);
    const rawTurningPoint = asRecord(rawLifeHighlight?.nextTurningPoint);
    const normalizedTurningAge = toFiniteNumber(rawTurningPoint?.age);
    const normalizedDirection: LifeFortuneTrendTurningDirection | undefined =
        rawTurningPoint?.direction === 'up' || rawTurningPoint?.direction === 'down'
        ? rawTurningPoint.direction
        : undefined;

    return {
        ...data,
        currentAge: currentAge ?? Number.NaN,
        currentYear: currentYear ?? Number.NaN,
        periods,
        lifeHighlight: {
            bestPeriod: {
                label: normalizeString(rawBestPeriod?.label),
                ages: normalizeString(rawBestPeriod?.ages),
                reason: normalizeString(rawBestPeriod?.reason),
            },
            currentStatus: normalizeString(rawLifeHighlight?.currentStatus),
            nextTurningPoint: {
                age: normalizedTurningAge ?? Number.NaN,
                direction: normalizedDirection ?? 'up',
                reason: normalizeString(rawTurningPoint?.reason),
            },
        },
    };
}

function normalizeLifeFortuneTrendPeriod(
    period: Record<string, unknown> | undefined,
    index: number,
    currentAge: number | undefined,
    currentYear: number | undefined,
): LifeFortuneTrendPeriod | null {
    if (!period) return null;

    const scores = normalizeNumericDimensionScores(period.scores);
    if (Object.keys(scores).length === 0) {
        return null;
    }

    const yearlyScores = normalizeYearlyScores(period.yearlyScores);
    const inferredStartAge = yearlyScores[0]?.age;
    const inferredEndAge = yearlyScores[yearlyScores.length - 1]?.age;
    const normalizedAgeRange = normalizeAscendingPair(
        toFiniteNumber(period.startAge) ?? inferredStartAge,
        toFiniteNumber(period.endAge) ?? inferredEndAge,
    );

    if (!normalizedAgeRange && yearlyScores.length === 0) {
        return null;
    }

    const inferredStartYear = yearlyScores[0]?.year;
    const inferredEndYear = yearlyScores[yearlyScores.length - 1]?.year;
    const normalizedYearRange = normalizeAscendingPair(
        toFiniteNumber(period.startYear) ?? inferredStartYear,
        toFiniteNumber(period.endYear) ?? inferredEndYear,
    );

    const startAge = normalizedAgeRange?.[0] ?? inferredStartAge ?? Number.NaN;
    const endAge = normalizedAgeRange?.[1] ?? inferredEndAge ?? Number.NaN;
    const startYear = normalizedYearRange?.[0]
        ?? inferYearFromAge(startAge, currentAge, currentYear)
        ?? Number.NaN;
    const endYear = normalizedYearRange?.[1]
        ?? inferYearFromAge(endAge, currentAge, currentYear)
        ?? Number.NaN;

    return {
        label: normalizeString(period.label, `阶段${index + 1}`),
        startAge,
        endAge,
        startYear,
        endYear,
        scores,
        summary: normalizeString(period.summary),
        highlights: normalizeStringArray(period.highlights),
        warnings: normalizeStringArray(period.warnings),
        yearlyScores,
    };
}

function normalizeRadarScores(input: unknown): FortuneRadarScores {
    const rawScores = asRecord(input);
    if (!rawScores) return {};

    const result: FortuneRadarScores = {};
    for (const [rawKey, rawValue] of Object.entries(rawScores)) {
        const key = normalizeDimensionKey(rawKey);
        if (!key) continue;

        const score = normalizeScore(asRecord(rawValue)?.score ?? rawValue);
        if (score == null) continue;

        result[key] = {
            score,
            label: normalizeString(asRecord(rawValue)?.label, getDimensionConfig(key).label),
            trend: normalizeTrend(asRecord(rawValue)?.trend),
        };
    }

    return result;
}

function normalizeNumericDimensionScores(input: unknown): LifeFortuneTrendPeriod['scores'] {
    const rawScores = asRecord(input);
    if (!rawScores) return {};

    const result: LifeFortuneTrendPeriod['scores'] = {};
    for (const [rawKey, rawValue] of Object.entries(rawScores)) {
        const key = normalizeDimensionKey(rawKey);
        if (!key) continue;

        const score = normalizeScore(rawValue);
        if (score == null) continue;
        result[key] = score;
    }

    return result;
}

function normalizeYearlyScores(input: unknown): LifeFortuneTrendYearlyScore[] {
    if (!Array.isArray(input)) return [];

    return input
        .map((item) => {
            const record = asRecord(item);
            if (!record) return null;

            const age = toFiniteNumber(record.age);
            const year = toFiniteNumber(record.year);
            const overall = normalizeScore(record.overall);
            if (age == null || year == null || overall == null) return null;

            return { age, year, overall };
        })
        .filter((item): item is LifeFortuneTrendYearlyScore => item !== null)
        .sort((a, b) => a.age - b.age || a.year - b.year);
}

function normalizeTrend(value: unknown): 'up' | 'down' | 'stable' {
    return value === 'up' || value === 'down' || value === 'stable' ? value : 'stable';
}

function normalizeString(value: unknown, fallback = ''): string {
    if (typeof value !== 'string') return fallback;
    const trimmed = value.trim();
    return trimmed || fallback;
}

function normalizeStringArray(value: unknown): string[] {
    if (Array.isArray(value)) {
        return value
            .filter((entry): entry is string => typeof entry === 'string')
            .map((entry) => entry.trim())
            .filter(Boolean);
    }

    if (typeof value === 'string') {
        const trimmed = value.trim();
        return trimmed ? [trimmed] : [];
    }

    return [];
}

function normalizeScore(value: unknown): number | undefined {
    const parsed = toFiniteNumber(value);
    if (parsed == null) return undefined;
    return Math.max(0, Math.min(100, Math.round(parsed)));
}

function toFiniteNumber(value: unknown): number | undefined {
    if (typeof value === 'number') {
        return Number.isFinite(value) ? value : undefined;
    }

    if (typeof value === 'string') {
        const trimmed = value.trim();
        if (!trimmed) return undefined;
        const parsed = Number.parseFloat(trimmed.replace(/,/g, ''));
        return Number.isFinite(parsed) ? parsed : undefined;
    }

    return undefined;
}

function normalizeAscendingPair(first: number | undefined, second: number | undefined) {
    if (first == null || second == null) return undefined;
    return first <= second ? [first, second] as const : [second, first] as const;
}

function inferYearFromAge(age: number, currentAge: number | undefined, currentYear: number | undefined) {
    if (!Number.isFinite(age) || currentAge == null || currentYear == null) {
        return undefined;
    }

    return currentYear - currentAge + age;
}

function average(values: number[]) {
    if (values.length === 0) return undefined;
    return Math.round(values.reduce((sum, value) => sum + value, 0) / values.length);
}

function asRecord(value: unknown): Record<string, unknown> | undefined {
    if (!value || typeof value !== 'object' || Array.isArray(value)) return undefined;
    return value as Record<string, unknown>;
}
