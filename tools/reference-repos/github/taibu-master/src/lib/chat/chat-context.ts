import 'server-only';

import { getSystemAdminClient } from '@/lib/api-utils';
import { truncateToTokens } from '@/lib/token-utils';
import { baziProvider } from '@/lib/data-sources/bazi';
import { dailyFortuneProvider } from '@/lib/data-sources/fortune';
import { getBaziCaseProfileByChartId } from '@/lib/server/bazi-case-profile';
import { getUserSettingsSnapshot } from '@/lib/user/settings';

export type DreamContextPayload = {
    baziChartName?: string;
    baziText?: string;
    fortuneText?: string;
};

const MAX_BAZI_TOKENS = 1500;
const MAX_FORTUNE_TOKENS = 500;
const DREAM_CONTEXT_TTL_MS = 30 * 60 * 1000;
const MAX_CACHE_SIZE = 1000;

type DreamContextResult = {
    payload: DreamContextPayload;
    context: { baziChartName?: string; dailyFortune?: string };
};

type DreamContextCacheEntry = {
    expiresAt: number;
    result: DreamContextResult;
};

const dreamContextCache = new Map<string, DreamContextCacheEntry>();

function formatDayKey(date: Date) {
    return `${date.getFullYear()}-${String(date.getMonth() + 1).padStart(2, '0')}-${String(date.getDate()).padStart(2, '0')}`;
}

function pruneDreamContextCache(now = Date.now()) {
    for (const [cacheKey, entry] of dreamContextCache.entries()) {
        if (entry.expiresAt <= now) {
            dreamContextCache.delete(cacheKey);
        }
    }
    if (dreamContextCache.size > MAX_CACHE_SIZE) {
        const entries = Array.from(dreamContextCache.entries());
        entries.sort((a, b) => a[1].expiresAt - b[1].expiresAt);
        const toDelete = entries.slice(0, dreamContextCache.size - MAX_CACHE_SIZE);
        for (const [key] of toDelete) {
            dreamContextCache.delete(key);
        }
    }
}

async function loadPreferredBaziChartMeta(
    supabase: ReturnType<typeof getSystemAdminClient>,
    userId: string,
    defaultBaziId: string | null,
) {
    const baseQuery = supabase
        .from('bazi_charts')
        .select('id, updated_at')
        .eq('user_id', userId);

    if (defaultBaziId) {
        const preferred = await baseQuery.eq('id', defaultBaziId).maybeSingle();
        if (preferred.data) {
            return preferred;
        }
    }

    return await baseQuery
        .order('created_at', { ascending: false })
        .limit(1)
        .maybeSingle();
}

export async function buildDreamContextPayload(userId: string): Promise<DreamContextResult> {
    const supabase = getSystemAdminClient();
    pruneDreamContextCache();

    const userSettingsClient = {
        from(table: 'user_settings') {
            return {
                select(columns: string) {
                    return {
                        eq(column: 'user_id', value: string) {
                            return {
                                maybeSingle() {
                                    return supabase
                                        .from(table)
                                        .select(columns)
                                        .eq(column, value)
                                        .maybeSingle();
                                },
                            };
                        },
                    };
                },
            };
        },
    };

    const [{ settings }, dayKey] = await Promise.all([
        getUserSettingsSnapshot(userSettingsClient, userId),
        Promise.resolve(formatDayKey(new Date())),
    ]);

    const defaultBaziId = settings.defaultBaziChartId;
    const resolvedChartMeta = await loadPreferredBaziChartMeta(supabase, userId, defaultBaziId);

    const resolvedChartId = (resolvedChartMeta.data as { id?: string | null } | null)?.id ?? null;
    const chartUpdatedAt = (resolvedChartMeta.data as { updated_at?: string | null } | null)?.updated_at ?? null;

    const caseProfileMeta = resolvedChartId
        ? await supabase
            .from('bazi_case_profiles')
            .select('updated_at')
            .eq('bazi_chart_id', resolvedChartId)
            .eq('user_id', userId)
            .maybeSingle()
        : { data: null };
    const caseProfileUpdatedAt = (caseProfileMeta.data as { updated_at?: string | null } | null)?.updated_at ?? null;

    const cacheKey = `${userId}:${resolvedChartId ?? 'none'}:${chartUpdatedAt ?? 'none'}:${caseProfileUpdatedAt ?? 'none'}:${dayKey}`;
    const cached = dreamContextCache.get(cacheKey);
    if (cached && cached.expiresAt > Date.now()) {
        return cached.result;
    }

    const [baziChartResult, fortune] = await Promise.all([
        resolvedChartId
            ? supabase
                .from('bazi_charts')
                .select('id, user_id, name, gender, birth_date, birth_time, birth_place, longitude, calendar_type, is_leap_month, created_at, updated_at')
                .eq('user_id', userId)
                .eq('id', resolvedChartId)
                .maybeSingle()
            : Promise.resolve({ data: null }),
        dailyFortuneProvider.get('today', userId, { client: supabase }),
    ]);

    const baziChart = baziChartResult.data;
    const caseProfile = baziChart?.id
        ? await getBaziCaseProfileByChartId(supabase, baziChart.id, userId)
        : null;

    let baziText = baziChart
        ? await baziProvider.formatForAI({
            ...(baziChart as Parameters<typeof baziProvider.formatForAI>[0]),
            caseProfile,
        })
        : '';
    let fortuneText = fortune ? await dailyFortuneProvider.formatForAI(fortune) : '';

    baziText = truncateToTokens(baziText, MAX_BAZI_TOKENS);
    fortuneText = truncateToTokens(fortuneText, MAX_FORTUNE_TOKENS);

    const payload: DreamContextPayload = {
        baziChartName: baziChart?.name,
        baziText: baziText || undefined,
        fortuneText: fortuneText || undefined
    };
    const context = {
        baziChartName: baziChart?.name,
        dailyFortune: fortuneText ? '已参考' : undefined
    };

    const result = { payload, context };
    dreamContextCache.set(cacheKey, {
        expiresAt: Date.now() + DREAM_CONTEXT_TTL_MS,
        result,
    });

    return result;
}
