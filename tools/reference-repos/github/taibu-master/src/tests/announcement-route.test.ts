import { test } from 'node:test';
import assert from 'node:assert/strict';
import { NextRequest } from 'next/server';

process.env.NEXT_PUBLIC_SUPABASE_URL = process.env.NEXT_PUBLIC_SUPABASE_URL || 'http://localhost';
process.env.NEXT_PUBLIC_SUPABASE_ANON_KEY = process.env.NEXT_PUBLIC_SUPABASE_ANON_KEY || 'test-anon';

test('announcements GET should return history ordered by published_at desc', async (t) => {
  const apiUtilsModule = require('../lib/api-utils') as any;
  const originalGetSystemAdminClient = apiUtilsModule.getSystemAdminClient;

  apiUtilsModule.getSystemAdminClient = () => ({
    from: (table: string) => {
      assert.equal(table, 'announcements');
      return {
        select: () => ({
          order: () => ({
            range: async () => ({
              data: [
                {
                  id: 'announcement-2',
                  content: '较新的公告',
                  published_at: '2026-03-28T10:00:00.000Z',
                  created_at: '2026-03-28T10:00:00.000Z',
                  updated_at: '2026-03-28T10:00:00.000Z',
                },
                {
                  id: 'announcement-1',
                  content: '较早的公告',
                  published_at: '2026-03-27T10:00:00.000Z',
                  created_at: '2026-03-27T10:00:00.000Z',
                  updated_at: '2026-03-27T10:00:00.000Z',
                },
                {
                  id: 'announcement-0',
                  content: '下一页公告',
                  published_at: '2026-03-26T10:00:00.000Z',
                  created_at: '2026-03-26T10:00:00.000Z',
                  updated_at: '2026-03-26T10:00:00.000Z',
                },
              ],
              error: null,
            }),
          }),
        }),
      };
    },
  });

  t.after(() => {
    apiUtilsModule.getSystemAdminClient = originalGetSystemAdminClient;
  });

  const { GET } = await import('../app/api/announcements/route');
  const response = await GET(new NextRequest('http://localhost/api/announcements?limit=2'));
  const payload = await response.json();

  assert.equal(response.status, 200);
  assert.deepEqual(
    payload.announcements.map((item: { id: string }) => item.id),
    ['announcement-2', 'announcement-1'],
  );
  assert.deepEqual(payload.pagination, {
    hasMore: true,
    nextOffset: 2,
  });
});

test('announcements GET latest should return the newest announcement only', async (t) => {
  const apiUtilsModule = require('../lib/api-utils') as any;
  const originalGetSystemAdminClient = apiUtilsModule.getSystemAdminClient;

  apiUtilsModule.getSystemAdminClient = () => ({
    from: (table: string) => {
      assert.equal(table, 'announcements');
      return {
        select: () => ({
          order: () => ({
            limit: () => ({
              maybeSingle: async () => ({
                data: {
                  id: 'announcement-2',
                  content: '最新公告',
                  published_at: '2026-03-28T10:00:00.000Z',
                  created_at: '2026-03-28T10:00:00.000Z',
                  updated_at: '2026-03-28T10:00:00.000Z',
                },
                error: null,
              }),
            }),
          }),
        }),
      };
    },
  });

  t.after(() => {
    apiUtilsModule.getSystemAdminClient = originalGetSystemAdminClient;
  });

  const { GET } = await import('../app/api/announcements/route');
  const response = await GET(new NextRequest('http://localhost/api/announcements?latest=1'));
  const payload = await response.json();

  assert.equal(response.status, 200);
  assert.equal(payload.announcement.id, 'announcement-2');
});

test('announcements GET count should return total announcement count', async (t) => {
  const apiUtilsModule = require('../lib/api-utils') as any;
  const originalGetSystemAdminClient = apiUtilsModule.getSystemAdminClient;

  apiUtilsModule.getSystemAdminClient = () => ({
    from: (table: string) => {
      assert.equal(table, 'announcements');
      return {
        select: (_columns: string, options: Record<string, unknown>) => {
          assert.deepEqual(options, { count: 'exact', head: true });
          return {
            then(resolve: (value: { data: null; error: null; count: number }) => unknown) {
              return Promise.resolve(resolve({ data: null, error: null, count: 4 }));
            },
          };
        },
      };
    },
  });

  t.after(() => {
    apiUtilsModule.getSystemAdminClient = originalGetSystemAdminClient;
  });

  const { GET } = await import('../app/api/announcements/route');
  const response = await GET(new NextRequest('http://localhost/api/announcements?count=1'));
  const payload = await response.json();

  assert.equal(response.status, 200);
  assert.equal(payload.count, 4);
});
