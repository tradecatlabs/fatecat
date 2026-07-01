import test from 'node:test';
import assert from 'node:assert/strict';
import { NextRequest } from 'next/server';

import { POST } from '@/app/api/amap/geocode/route';

test('amap geocode route should return a resolved longitude and latitude for a valid place', async (t) => {
    process.env.AMAP_WEB_SERVICE_KEY = 'test-amap-key';
    const originalFetch = global.fetch;

    global.fetch = async () => new Response(JSON.stringify({
        status: '1',
        count: '1',
        geocodes: [
            {
                formatted_address: '广东省河源市源城区',
                location: '114.700446,23.743538',
                adcode: '441602',
                level: 'district',
            },
        ],
    }), {
        status: 200,
        headers: { 'content-type': 'application/json' },
    });

    t.after(() => {
        global.fetch = originalFetch;
        delete process.env.AMAP_WEB_SERVICE_KEY;
    });

    const response = await POST(new NextRequest('http://localhost/api/amap/geocode', {
        method: 'POST',
        body: JSON.stringify({ place: '广东省 河源市 源城区' }),
    }));

    assert.equal(response.status, 200);
    const payload = await response.json() as {
        resolved: boolean;
        longitude?: number;
        latitude?: number;
        provider?: string;
        level?: string;
    };

    assert.equal(payload.resolved, true);
    assert.equal(payload.longitude, 114.700446);
    assert.equal(payload.latitude, 23.743538);
    assert.equal(payload.provider, 'amap');
    assert.equal(payload.level, 'district');
});

test('amap geocode route should gracefully degrade when place precision is too low', async (t) => {
    process.env.AMAP_WEB_SERVICE_KEY = 'test-amap-key';
    const originalFetch = global.fetch;

    global.fetch = async () => new Response(JSON.stringify({
        status: '1',
        count: '1',
        geocodes: [
            {
                formatted_address: '广东省',
                location: '113.266530,23.132191',
                adcode: '440000',
                level: '省',
            },
        ],
    }), {
        status: 200,
        headers: { 'content-type': 'application/json' },
    });

    t.after(() => {
        global.fetch = originalFetch;
        delete process.env.AMAP_WEB_SERVICE_KEY;
    });

    const response = await POST(new NextRequest('http://localhost/api/amap/geocode', {
        method: 'POST',
        body: JSON.stringify({ place: '广东省' }),
    }));

    assert.equal(response.status, 200);
    const payload = await response.json() as {
        resolved: boolean;
        reason?: string;
    };

    assert.equal(payload.resolved, false);
    assert.equal(payload.reason, 'precision_too_low');
});
