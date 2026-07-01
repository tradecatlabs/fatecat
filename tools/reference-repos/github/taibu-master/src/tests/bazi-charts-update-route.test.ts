import { test } from 'node:test';
import assert from 'node:assert/strict';
import { NextRequest } from 'next/server';

process.env.NEXT_PUBLIC_SUPABASE_URL = 'http://localhost';
process.env.NEXT_PUBLIC_SUPABASE_ANON_KEY = 'test-anon';

test('bazi chart create rejects missing birth_time', async (t) => {
    const apiUtils = require('../lib/api-utils') as {
        requireUserContext: typeof import('../lib/api-utils').requireUserContext;
    };
    const originalRequireUserContext = apiUtils.requireUserContext;
    let insertCalled = false;

    apiUtils.requireUserContext = (async () => ({
        user: { id: 'user-1' },
        supabase: {
            from() {
                return {
                    insert() {
                        insertCalled = true;
                        return {
                            select() {
                                return {
                                    maybeSingle: async () => ({
                                        data: { id: 'bazi-1' },
                                        error: null,
                                    }),
                                };
                            },
                        };
                    },
                };
            },
        },
    })) as unknown as typeof apiUtils.requireUserContext;

    t.after(() => {
        apiUtils.requireUserContext = originalRequireUserContext;
    });

    const { POST } = await import('../app/api/bazi/charts/route');
    const request = new NextRequest('http://localhost/api/bazi/charts', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
            payload: {
                name: '八字一号',
                gender: 'male',
                birth_date: '1990-01-01',
                birth_time: null,
            },
        }),
    });

    const response = await POST(request);
    const payload = await response.json();

    assert.equal(response.status, 400);
    assert.equal(payload.error, '八字命盘必须提供有效的出生时辰');
    assert.equal(insertCalled, false);
});

test('bazi chart update recomputes derived fields from merged existing chart data', async (t) => {
    const apiUtils = require('../lib/api-utils') as {
        requireUserContext: typeof import('../lib/api-utils').requireUserContext;
    };
    const originalRequireUserContext = apiUtils.requireUserContext;
    let updatedPayload: Record<string, unknown> | null = null;

    apiUtils.requireUserContext = (async () => ({
        user: { id: 'user-1' },
        supabase: {
            from(table: string) {
                assert.equal(table, 'bazi_charts');
                return {
                    select() {
                        return {
                            eq() {
                                return {
                                    eq() {
                                        return {
                                            maybeSingle: async () => ({
                                                data: {
                                                    id: '550e8400-e29b-41d4-a716-446655440000',
                                                    user_id: 'user-1',
                                                    gender: 'male',
                                                    birth_date: '1990-01-01',
                                                    birth_time: '08:00',
                                                    birth_place: '北京',
                                                    longitude: null,
                                                    calendar_type: 'solar',
                                                    is_leap_month: false,
                                                },
                                                error: null,
                                            }),
                                        };
                                    },
                                };
                            },
                        };
                    },
                    update(payload: Record<string, unknown>) {
                        updatedPayload = payload;
                        return {
                            eq() {
                                return {
                                    eq() {
                                        return {
                                            select() {
                                                return {
                                                    maybeSingle: async () => ({
                                                        data: { id: '550e8400-e29b-41d4-a716-446655440000' },
                                                        error: null,
                                                    }),
                                                };
                                            },
                                        };
                                    },
                                };
                            },
                        };
                    },
                };
            },
        },
    })) as unknown as typeof apiUtils.requireUserContext;

    t.after(() => {
        apiUtils.requireUserContext = originalRequireUserContext;
    });

    const { POST } = await import('../app/api/bazi/charts/update/route');
    const request = new NextRequest('http://localhost/api/bazi/charts/update', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
            chartId: '550e8400-e29b-41d4-a716-446655440000',
            payload: {
                birth_time: '09:30',
            },
        }),
    });

    const response = await POST(request);
    const payload = await response.json();

    assert.equal(response.status, 200);
    assert.equal(payload.success, true);
    assert.ok(updatedPayload);
    const updatedRecord = updatedPayload as Record<string, unknown>;
    assert.equal(updatedRecord.birth_time, '09:30');
    assert.equal(typeof updatedRecord.day_master, 'string');
    assert.equal(typeof updatedRecord.day_branch, 'string');
});

test('bazi chart update rejects merged records without valid birth_time', async (t) => {
    const apiUtils = require('../lib/api-utils') as {
        requireUserContext: typeof import('../lib/api-utils').requireUserContext;
    };
    const originalRequireUserContext = apiUtils.requireUserContext;
    let updateCalled = false;

    apiUtils.requireUserContext = (async () => ({
        user: { id: 'user-1' },
        supabase: {
            from(table: string) {
                assert.equal(table, 'bazi_charts');
                return {
                    select() {
                        return {
                            eq() {
                                return {
                                    eq() {
                                        return {
                                            maybeSingle: async () => ({
                                                data: {
                                                    id: '550e8400-e29b-41d4-a716-446655440000',
                                                    user_id: 'user-1',
                                                    gender: 'male',
                                                    birth_date: '1990-01-01',
                                                    birth_time: null,
                                                    birth_place: '北京',
                                                    longitude: null,
                                                    calendar_type: 'solar',
                                                    is_leap_month: false,
                                                },
                                                error: null,
                                            }),
                                        };
                                    },
                                };
                            },
                        };
                    },
                    update() {
                        updateCalled = true;
                        return {
                            eq() {
                                return {
                                    eq() {
                                        return {
                                            select() {
                                                return {
                                                    maybeSingle: async () => ({
                                                        data: { id: '550e8400-e29b-41d4-a716-446655440000' },
                                                        error: null,
                                                    }),
                                                };
                                            },
                                        };
                                    },
                                };
                            },
                        };
                    },
                };
            },
        },
    })) as unknown as typeof apiUtils.requireUserContext;

    t.after(() => {
        apiUtils.requireUserContext = originalRequireUserContext;
    });

    const { POST } = await import('../app/api/bazi/charts/update/route');
    const request = new NextRequest('http://localhost/api/bazi/charts/update', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
            chartId: '550e8400-e29b-41d4-a716-446655440000',
            payload: {
                name: '更新名称',
            },
        }),
    });

    const response = await POST(request);
    const payload = await response.json();

    assert.equal(response.status, 400);
    assert.equal(payload.error, '八字命盘必须提供有效的出生时辰');
    assert.equal(updateCalled, false);
});
