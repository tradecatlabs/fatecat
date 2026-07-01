import { test, type TestContext } from 'node:test';
import assert from 'node:assert/strict';
import { NextRequest } from 'next/server';
import { ensureRouteTestEnv } from './helpers/route-mock';

ensureRouteTestEnv();

function mockUserContext(
    t: TestContext,
    routeModulePath: string,
    client: Record<string, unknown> = {},
) {
    const apiUtilsModule = require('../lib/api-utils') as typeof import('../lib/api-utils');
    const routePath = require.resolve(routeModulePath);
    const pipelinePath = require.resolve('../lib/api/divination-pipeline');
    const originalRequireUserContext = apiUtilsModule.requireUserContext;

    apiUtilsModule.requireUserContext = async () => ({
        user: { id: 'user-1' },
        db: client,
        supabase: client,
        accessToken: 'test-token',
    }) as Awaited<ReturnType<typeof import('../lib/api-utils').requireUserContext>>;

    delete require.cache[routePath];
    delete require.cache[pipelinePath];

    t.after(() => {
        apiUtilsModule.requireUserContext = originalRequireUserContext;
        delete require.cache[routePath];
        delete require.cache[pipelinePath];
    });
}

test('mbti save action persists reading through shared save helper', async (t) => {
    let insertedPayload: Record<string, unknown> | null = null;
    const mockDb = {
        from: (table: string) => {
            assert.equal(table, 'mbti_readings');
            return {
                insert: (payload: Record<string, unknown>) => {
                    insertedPayload = payload;
                    return {
                        select: () => ({
                            single: async () => ({
                                data: { id: 'reading-1' },
                                error: null,
                            }),
                        }),
                    };
                },
            };
        },
    };

    mockUserContext(t, '../app/api/mbti/route', mockDb);

    const { POST } = await import('../app/api/mbti/route');
    const response = await POST(new NextRequest('http://localhost/api/mbti', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
            'Authorization': 'Bearer test-token',
        },
        body: JSON.stringify({
            action: 'save',
            type: 'INTJ',
            scores: { E: 20, I: 80, S: 40, N: 60, T: 70, F: 30, J: 55, P: 45 },
            percentages: {
                EI: { E: 20, I: 80 },
                SN: { S: 40, N: 60 },
                TF: { T: 70, F: 30 },
                JP: { J: 55, P: 45 },
            },
        }),
    }));
    const data = await response.json();

    assert.equal(response.status, 200);
    assert.equal(data.success, true);
    assert.equal(data.data.readingId, 'reading-1');
    assert.equal(insertedPayload?.user_id, 'user-1');
    assert.equal(insertedPayload?.mbti_type, 'INTJ');
});

test('daliuren save action persists reading through shared save helper', async (t) => {
    const { calculateDaliuren } = require('taibu-core') as typeof import('taibu-core');

    let insertedPayload: Record<string, unknown> | null = null;
    const mockDb = {
        from: (table: string) => {
            assert.equal(table, 'daliuren_divinations');
            return {
                insert: (payload: Record<string, unknown>) => {
                    insertedPayload = payload;
                    return {
                        select: () => ({
                            single: async () => ({
                                data: { id: 'divination-1' },
                                error: null,
                            }),
                        }),
                    };
                },
            };
        },
    };

    mockUserContext(t, '../app/api/daliuren/route', mockDb);

    const resultData = calculateDaliuren({
        date: '2025-01-15',
        hour: 10,
        minute: 30,
        timezone: 'Asia/Shanghai',
        question: '测试问题',
    });

    const { POST } = await import('../app/api/daliuren/route');
    const response = await POST(new NextRequest('http://localhost/api/daliuren', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
            'Authorization': 'Bearer test-token',
        },
        body: JSON.stringify({
            action: 'save',
            date: '2025-01-15',
            hour: 10,
            minute: 30,
            timezone: 'Asia/Shanghai',
            question: '测试问题',
            resultData,
        }),
    }));
    const data = await response.json();

    assert.equal(response.status, 200);
    assert.equal(data.success, true);
    assert.equal(data.data.divinationId, 'divination-1');
    assert.equal(insertedPayload?.user_id, 'user-1');
    assert.equal(insertedPayload?.solar_date, '2025-01-15');
    assert.equal(insertedPayload?.question, '测试问题');
});
