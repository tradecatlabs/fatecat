import { test } from 'node:test';
import assert from 'node:assert/strict';

process.env.NEXT_PUBLIC_SUPABASE_URL = 'http://localhost';
process.env.NEXT_PUBLIC_SUPABASE_ANON_KEY = 'test-anon';

test('annual report generation uses service client for queries', async (t) => {
    const supabaseModule = require('../lib/auth') as any;
    const supabaseServerModule = require('../lib/supabase-server') as any;

    const originalFrom = supabaseModule.supabase.from;
    const originalGetServiceClient = supabaseServerModule.getSystemAdminClient;

    let usedServiceClient = false;
    let cachedReport: Record<string, unknown> | null = null;

    supabaseModule.supabase.from = () => {
        throw new Error('browser client should not be used');
    };

    supabaseServerModule.getSystemAdminClient = () => {
        usedServiceClient = true;
        return {
            from: (table: string) => {
                if (table === 'conversations') {
                    return {
                        select: () => ({
                            eq: () => ({
                                gte: () => ({
                                    lte: async () => ({
                                        data: [
                                            { source_type: 'bazi', created_at: '2024-01-10T00:00:00Z' },
                                            { source_type: 'chat', created_at: '2024-01-11T00:00:00Z' },
                                        ],
                                    }),
                                }),
                            }),
                        }),
                    };
                }
                if (table === 'daily_checkins') {
                    return {
                        select: () => ({
                            eq: () => ({
                                gte: () => ({
                                    lte: async () => ({
                                        data: [{ reward_credits: 1 }],
                                    }),
                                }),
                            }),
                        }),
                    };
                }
                if (table === 'annual_reports') {
                    return {
                        upsert: async (payload: Record<string, unknown>) => {
                            cachedReport = payload.report_data as Record<string, unknown>;
                            return { error: null };
                        },
                    };
                }
                return {};
            },
        };
    };

    t.after(() => {
        supabaseModule.supabase.from = originalFrom;
        supabaseServerModule.getSystemAdminClient = originalGetServiceClient;
    });

    const { generateAnnualReport } = await import('../lib/annual-report');
    const { ANNUAL_REPORT_FEATURE_NAMES } = await import('../lib/annual-report-shared');

    const report = await generateAnnualReport('user-1', 2024);

    assert.equal(usedServiceClient, true);
    assert.ok(report);
    assert.equal(report?.usage.totalAnalyses, 2);
    assert.equal('longestStreak' in (report?.checkin ?? {}), false);
    assert.equal('progress' in (report ?? {}), false);
    assert.equal(ANNUAL_REPORT_FEATURE_NAMES.qimen, '奇门遁甲');
    assert.equal(ANNUAL_REPORT_FEATURE_NAMES.daliuren, '大六壬');
    assert.equal(ANNUAL_REPORT_FEATURE_NAMES.dream, '解梦分析');
    assert.equal(ANNUAL_REPORT_FEATURE_NAMES.chat, 'AI 对话');
    assert.ok(cachedReport);
});

test('annual report summary uses service client when cache is empty', async (t) => {
    const supabaseModule = require('../lib/auth') as any;
    const supabaseServerModule = require('../lib/supabase-server') as any;

    const originalFrom = supabaseModule.supabase.from;
    const originalGetServiceClient = supabaseServerModule.getSystemAdminClient;

    supabaseModule.supabase.from = () => {
        throw new Error('browser client should not be used');
    };

    supabaseServerModule.getSystemAdminClient = () => ({
        from: (table: string) => {
            if (table === 'annual_reports') {
                return {
                    select: () => ({
                        eq: () => ({
                            eq: () => ({
                                maybeSingle: async () => ({ data: null, error: null }),
                            }),
                        }),
                    }),
                };
            }
            if (table === 'conversations') {
                return {
                    select: () => ({
                        eq: () => ({
                            gte: () => ({
                                lte: async () => ({ count: 4 }),
                            }),
                        }),
                    }),
                };
            }
            return {};
        },
    });

    t.after(() => {
        supabaseModule.supabase.from = originalFrom;
        supabaseServerModule.getSystemAdminClient = originalGetServiceClient;
    });

    const { getReportSummary } = await import('../lib/annual-report');

    const summary = await getReportSummary('user-1', 2024);

    assert.deepEqual(summary, {
        hasData: true,
        totalAnalyses: 4,
        topFeature: 'unknown',
    });
});
