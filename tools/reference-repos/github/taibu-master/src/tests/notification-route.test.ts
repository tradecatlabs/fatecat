import test from 'node:test';
import assert from 'node:assert/strict';
import { NextRequest } from 'next/server';

process.env.NEXT_PUBLIC_SUPABASE_URL = 'http://localhost';
process.env.NEXT_PUBLIC_SUPABASE_ANON_KEY = 'test-anon';

test('notifications GET should use head count query for unread badge requests', async (t) => {
  const apiUtils = require('../lib/api-utils') as {
    requireUserContext: typeof import('../lib/api-utils').requireUserContext;
  };
  const notificationServer = require('../lib/notification-server') as {
    pruneExpiredNotifications: typeof import('../lib/notification-server').pruneExpiredNotifications;
  };
  const originalRequireUserContext = apiUtils.requireUserContext;
  const originalPruneExpiredNotifications = notificationServer.pruneExpiredNotifications;

  const queryState: {
    columns?: string;
    options?: Record<string, unknown>;
    eqCalls: Array<{ column: string; value: unknown }>;
    gteCalls: Array<{ column: string; value: unknown }>;
  } = {
    eqCalls: [],
    gteCalls: [],
  };

  apiUtils.requireUserContext = (async () => ({
    user: { id: 'user-1' },
    supabase: {
      from(table: string) {
        assert.equal(table, 'notifications');
        return {
          select(columns: string, options?: Record<string, unknown>) {
            queryState.columns = columns;
            queryState.options = options;
            const query = {
              eq(column: string, value: unknown) {
                queryState.eqCalls.push({ column, value });
                return query;
              },
              gte(column: string, value: unknown) {
                queryState.gteCalls.push({ column, value });
                return query;
              },
              order() {
                throw new Error('count query should not sort notifications');
              },
              limit() {
                throw new Error('count query should not apply list limit');
              },
              then(resolve: (value: { data: null; error: null; count: number }) => unknown) {
                return Promise.resolve(resolve({ data: null, error: null, count: 5 }));
              },
            };
            return query;
          },
        };
      },
    },
  })) as unknown as typeof apiUtils.requireUserContext;
  notificationServer.pruneExpiredNotifications = (async () => 0) as typeof notificationServer.pruneExpiredNotifications;

  t.after(() => {
    apiUtils.requireUserContext = originalRequireUserContext;
    notificationServer.pruneExpiredNotifications = originalPruneExpiredNotifications;
  });

  const { GET } = await import('../app/api/notifications/route');
  const response = await GET(new NextRequest('http://localhost/api/notifications?count=1&unread=1'));
  const payload = await response.json();

  assert.equal(response.status, 200);
  assert.equal(payload.count, 5);
  assert.equal(queryState.columns, 'id');
  assert.deepEqual(queryState.options, { count: 'exact', head: true });
  assert.deepEqual(queryState.eqCalls, [
    { column: 'user_id', value: 'user-1' },
    { column: 'is_read', value: false },
  ]);
  assert.deepEqual(queryState.gteCalls.map((item) => item.column), ['created_at']);
});

test('notifications GET should not prune expired rows for unread badge requests', async (t) => {
  const apiUtils = require('../lib/api-utils') as {
    requireUserContext: typeof import('../lib/api-utils').requireUserContext;
  };
  const notificationServer = require('../lib/notification-server') as {
    pruneExpiredNotifications: typeof import('../lib/notification-server').pruneExpiredNotifications;
  };
  const originalRequireUserContext = apiUtils.requireUserContext;
  const originalPruneExpiredNotifications = notificationServer.pruneExpiredNotifications;

  let pruneCalled = false;

  apiUtils.requireUserContext = (async () => ({
    user: { id: 'user-1' },
    supabase: {
      from() {
        return {
          select() {
            const query = {
              eq() {
                return query;
              },
              gte() {
                return query;
              },
              then(resolve: (value: { data: null; error: null; count: number }) => unknown) {
                return Promise.resolve(resolve({ data: null, error: null, count: 2 }));
              },
            };
            return query;
          },
        };
      },
    },
  })) as unknown as typeof apiUtils.requireUserContext;
  notificationServer.pruneExpiredNotifications = (async () => {
    pruneCalled = true;
    return 0;
  }) as typeof notificationServer.pruneExpiredNotifications;

  t.after(() => {
    apiUtils.requireUserContext = originalRequireUserContext;
    notificationServer.pruneExpiredNotifications = originalPruneExpiredNotifications;
  });

  const { GET } = await import('../app/api/notifications/route');
  const response = await GET(new NextRequest('http://localhost/api/notifications?count=1&unread=1'));
  const payload = await response.json();

  assert.equal(response.status, 200);
  assert.equal(payload.count, 2);
  assert.equal(pruneCalled, false);
});

test('notifications GET list should filter notifications to the most recent 3 days', async (t) => {
  const apiUtils = require('../lib/api-utils') as {
    requireUserContext: typeof import('../lib/api-utils').requireUserContext;
  };
  const notificationServer = require('../lib/notification-server') as {
    pruneExpiredNotifications: typeof import('../lib/notification-server').pruneExpiredNotifications;
  };
  const originalRequireUserContext = apiUtils.requireUserContext;
  const originalPruneExpiredNotifications = notificationServer.pruneExpiredNotifications;

  const gteCalls: Array<{ column: string; value: unknown }> = [];

  apiUtils.requireUserContext = (async () => ({
    user: { id: 'user-1' },
    supabase: {
      from(table: string) {
        assert.equal(table, 'notifications');
        return {
          select() {
            const query = {
              eq() {
                return query;
              },
              gte(column: string, value: unknown) {
                gteCalls.push({ column, value });
                return query;
              },
              order() {
                return query;
              },
              range() {
                return Promise.resolve({
                  data: [
                    {
                      id: 'notification-1',
                      user_id: 'user-1',
                      type: 'system',
                      title: '标题',
                      content: '内容',
                      is_read: false,
                      link: null,
                      created_at: '2026-03-28T00:00:00.000Z',
                    },
                    {
                      id: 'notification-2',
                      user_id: 'user-1',
                      type: 'system',
                      title: '标题2',
                      content: '内容2',
                      is_read: true,
                      link: null,
                      created_at: '2026-03-27T00:00:00.000Z',
                    },
                    {
                      id: 'notification-3',
                      user_id: 'user-1',
                      type: 'system',
                      title: '标题3',
                      content: '内容3',
                      is_read: true,
                      link: null,
                      created_at: '2026-03-26T00:00:00.000Z',
                    },
                  ],
                  error: null,
                });
              },
            };
            return query;
          },
        };
      },
    },
  })) as unknown as typeof apiUtils.requireUserContext;
  notificationServer.pruneExpiredNotifications = (async () => 0) as typeof notificationServer.pruneExpiredNotifications;

  t.after(() => {
    apiUtils.requireUserContext = originalRequireUserContext;
    notificationServer.pruneExpiredNotifications = originalPruneExpiredNotifications;
  });

  const { GET } = await import('../app/api/notifications/route');
  const response = await GET(new NextRequest('http://localhost/api/notifications?limit=2'));
  const payload = await response.json();

  assert.equal(response.status, 200);
  assert.deepEqual(payload.notifications.map((item: { id: string }) => item.id), ['notification-1', 'notification-2']);
  assert.deepEqual(payload.pagination, {
    hasMore: true,
    nextOffset: 2,
  });
  assert.equal(gteCalls.length, 1);
  assert.equal(gteCalls[0].column, 'created_at');
  assert.equal(typeof gteCalls[0].value, 'string');
});

test('notifications PATCH should not prune before mark-one updates', async (t) => {
  const apiUtils = require('../lib/api-utils') as {
    requireUserContext: typeof import('../lib/api-utils').requireUserContext;
  };
  const notificationServer = require('../lib/notification-server') as {
    pruneExpiredNotifications: typeof import('../lib/notification-server').pruneExpiredNotifications;
  };
  const originalRequireUserContext = apiUtils.requireUserContext;
  const originalPruneExpiredNotifications = notificationServer.pruneExpiredNotifications;

  let pruneCalled = false;
  let updatedId: string | null = null;

  apiUtils.requireUserContext = (async () => ({
    user: { id: 'user-1' },
    supabase: {
      from(table: string) {
        assert.equal(table, 'notifications');
        return {
          update(payload: Record<string, unknown>) {
            assert.deepEqual(payload, { is_read: true });
            return {
              eq(column: string, value: unknown) {
                if (column === 'id') {
                  updatedId = value as string;
                }
                return this;
              },
            };
          },
        };
      },
    },
  })) as unknown as typeof apiUtils.requireUserContext;
  notificationServer.pruneExpiredNotifications = (async () => {
    pruneCalled = true;
    return 0;
  }) as typeof notificationServer.pruneExpiredNotifications;

  t.after(() => {
    apiUtils.requireUserContext = originalRequireUserContext;
    notificationServer.pruneExpiredNotifications = originalPruneExpiredNotifications;
  });

  const { PATCH } = await import('../app/api/notifications/route');
  const response = await PATCH(new NextRequest('http://localhost/api/notifications', {
    method: 'PATCH',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ action: 'mark-one', id: 'notification-1' }),
  }));
  const payload = await response.json();

  assert.equal(response.status, 200);
  assert.deepEqual(payload, { success: true });
  assert.equal(updatedId, 'notification-1');
  assert.equal(pruneCalled, false);
});

test('notifications DELETE should not prune before deleting selected ids', async (t) => {
  const apiUtils = require('../lib/api-utils') as {
    requireUserContext: typeof import('../lib/api-utils').requireUserContext;
  };
  const notificationServer = require('../lib/notification-server') as {
    pruneExpiredNotifications: typeof import('../lib/notification-server').pruneExpiredNotifications;
  };
  const originalRequireUserContext = apiUtils.requireUserContext;
  const originalPruneExpiredNotifications = notificationServer.pruneExpiredNotifications;

  let pruneCalled = false;
  let deletedIds: string[] | null = null;

  apiUtils.requireUserContext = (async () => ({
    user: { id: 'user-1' },
    supabase: {
      from(table: string) {
        assert.equal(table, 'notifications');
        return {
          delete() {
            return {
              in(column: string, ids: string[]) {
                assert.equal(column, 'id');
                deletedIds = ids;
                return this;
              },
              eq() {
                return Promise.resolve({ error: null });
              },
            };
          },
        };
      },
    },
  })) as unknown as typeof apiUtils.requireUserContext;
  notificationServer.pruneExpiredNotifications = (async () => {
    pruneCalled = true;
    return 0;
  }) as typeof notificationServer.pruneExpiredNotifications;

  t.after(() => {
    apiUtils.requireUserContext = originalRequireUserContext;
    notificationServer.pruneExpiredNotifications = originalPruneExpiredNotifications;
  });

  const { DELETE } = await import('../app/api/notifications/route');
  const response = await DELETE(new NextRequest('http://localhost/api/notifications?id=notification-1&id=notification-2', {
    method: 'DELETE',
  }));
  const payload = await response.json();

  assert.equal(response.status, 200);
  assert.deepEqual(payload, { success: true });
  assert.deepEqual(deletedIds, ['notification-1', 'notification-2']);
  assert.equal(pruneCalled, false);
});

test('getUnreadCount should read count from top-level response', async () => {
  const originalFetch = global.fetch;
  global.fetch = async () => new Response(JSON.stringify({ count: 7 }), {
    status: 200,
    headers: { 'Content-Type': 'application/json' },
  }) as Response;

  try {
    const { getUnreadCount } = await import('../lib/notification');
    const count = await getUnreadCount();
    assert.equal(count, 7);
  } finally {
    global.fetch = originalFetch;
  }
});

test('getUnreadCount should throw when unread count request fails', async () => {
  const originalFetch = global.fetch;
  global.fetch = async () => new Response(JSON.stringify({ error: '获取通知失败' }), {
    status: 500,
    headers: { 'Content-Type': 'application/json' },
  }) as Response;

  try {
    const { getUnreadCount } = await import('../lib/notification');
    await assert.rejects(
      () => getUnreadCount(),
      /获取通知失败/u,
    );
  } finally {
    global.fetch = originalFetch;
  }
});

test('unread query should not rely on a cold bootstrap zero as fresh initial data', async () => {
  const originalFetch = global.fetch;
  let fetchCount = 0;

  global.fetch = async () => {
    fetchCount += 1;
    return new Response(JSON.stringify({ count: 3 }), {
      status: 200,
      headers: { 'Content-Type': 'application/json' },
    }) as Response;
  };

  try {
    const { getUnreadCount } = await import('../lib/notification');
    const count = await getUnreadCount();
    assert.equal(count, 3);
    assert.equal(fetchCount, 1);
  } finally {
    global.fetch = originalFetch;
  }
});

test('getNotificationsPage should throw when notifications request fails', async () => {
  const originalFetch = global.fetch;
  global.fetch = async () => new Response(JSON.stringify({ error: '获取通知列表失败' }), {
    status: 500,
    headers: { 'Content-Type': 'application/json' },
  }) as Response;

  try {
    const { getNotificationsPage } = await import('../lib/notification');
    await assert.rejects(
      () => getNotificationsPage({ limit: 20, offset: 0 }),
      /获取通知列表失败/u,
    );
  } finally {
    global.fetch = originalFetch;
  }
});
