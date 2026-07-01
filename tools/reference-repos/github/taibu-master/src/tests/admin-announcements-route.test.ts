import { test } from 'node:test';
import assert from 'node:assert/strict';
import { NextRequest } from 'next/server';

process.env.NEXT_PUBLIC_SUPABASE_URL = process.env.NEXT_PUBLIC_SUPABASE_URL || 'http://localhost';
process.env.NEXT_PUBLIC_SUPABASE_ANON_KEY = process.env.NEXT_PUBLIC_SUPABASE_ANON_KEY || 'test-anon';

type InsertedAnnouncementPayload = {
  content: string;
  published_at: string;
};

type UpdatedAnnouncementPayload = {
  content: string;
};

test('admin announcements POST should create a published announcement with content only', async (t) => {
  const apiUtilsModule = require('../lib/api-utils') as any;
  const originalRequireAdminContext = apiUtilsModule.requireAdminContext;
  const originalGetSystemAdminClient = apiUtilsModule.getSystemAdminClient;

  let insertedPayload: InsertedAnnouncementPayload | null = null;

  apiUtilsModule.requireAdminContext = async () => ({
    user: { id: 'admin-1' },
    supabase: {},
  });
  apiUtilsModule.getSystemAdminClient = () => ({
    from: (table: string) => {
      assert.equal(table, 'announcements');
      return {
        insert: (payload: InsertedAnnouncementPayload) => {
          insertedPayload = payload;
          return {
            select: () => ({
              single: async () => ({
                data: {
                  id: 'announcement-1',
                  ...payload,
                  created_at: '2026-03-28T10:00:00.000Z',
                  updated_at: '2026-03-28T10:00:00.000Z',
                },
                error: null,
              }),
            }),
          };
        },
      };
    },
  });

  t.after(() => {
    apiUtilsModule.requireAdminContext = originalRequireAdminContext;
    apiUtilsModule.getSystemAdminClient = originalGetSystemAdminClient;
  });

  const { POST } = await import('../app/api/admin/announcements/route');
  const request = new NextRequest('http://localhost/api/admin/announcements', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({
      content: '今晚 23:00 到 23:30 进行短时维护',
    }),
  });

  const response = await POST(request);
  const payload = await response.json();

  assert.equal(response.status, 200);
  if (!insertedPayload) {
    throw new Error('expected insertedPayload to be captured');
  }
  const createdPayload: InsertedAnnouncementPayload = insertedPayload;
  assert.equal(createdPayload.content, '今晚 23:00 到 23:30 进行短时维护');
  assert.equal(typeof createdPayload.published_at, 'string');
  assert.equal(payload.announcement.id, 'announcement-1');
});

test('admin announcements POST should reject empty content', async (t) => {
  const apiUtilsModule = require('../lib/api-utils') as any;
  const originalRequireAdminContext = apiUtilsModule.requireAdminContext;

  apiUtilsModule.requireAdminContext = async () => ({
    user: { id: 'admin-1' },
    supabase: {},
  });

  t.after(() => {
    apiUtilsModule.requireAdminContext = originalRequireAdminContext;
  });

  const { POST } = await import('../app/api/admin/announcements/route');
  const request = new NextRequest('http://localhost/api/admin/announcements', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({
      content: '   ',
    }),
  });

  const response = await POST(request);
  const payload = await response.json();

  assert.equal(response.status, 400);
  assert.equal(payload.error, '公告内容不能为空');
});

test('admin announcements PATCH should update content without changing published_at', async (t) => {
  const apiUtilsModule = require('../lib/api-utils') as any;
  const originalRequireAdminContext = apiUtilsModule.requireAdminContext;
  const originalGetSystemAdminClient = apiUtilsModule.getSystemAdminClient;

  let updatedPayload: UpdatedAnnouncementPayload | null = null;

  apiUtilsModule.requireAdminContext = async () => ({
    user: { id: 'admin-1' },
    supabase: {},
  });
  apiUtilsModule.getSystemAdminClient = () => ({
    from: (table: string) => {
      assert.equal(table, 'announcements');
      return {
        select: () => ({
          eq: () => ({
            maybeSingle: async () => ({
              data: {
                id: 'announcement-1',
                content: '旧内容',
                published_at: '2026-03-28T10:00:00.000Z',
                created_at: '2026-03-28T10:00:00.000Z',
                updated_at: '2026-03-28T10:00:00.000Z',
              },
              error: null,
            }),
          }),
        }),
        update: (payload: UpdatedAnnouncementPayload) => {
          updatedPayload = payload;
          return {
            eq: () => ({
              select: () => ({
                single: async () => ({
                  data: {
                    id: 'announcement-1',
                    content: payload.content,
                    published_at: '2026-03-28T10:00:00.000Z',
                    created_at: '2026-03-28T10:00:00.000Z',
                    updated_at: '2026-03-28T12:00:00.000Z',
                  },
                  error: null,
                }),
              }),
            }),
          };
        },
      };
    },
  });

  t.after(() => {
    apiUtilsModule.requireAdminContext = originalRequireAdminContext;
    apiUtilsModule.getSystemAdminClient = originalGetSystemAdminClient;
  });

  const { PATCH } = await import('../app/api/admin/announcements/[id]/route');
  const request = new NextRequest('http://localhost/api/admin/announcements/announcement-1', {
    method: 'PATCH',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({
      content: '更新后的公告内容',
    }),
  });

  const response = await PATCH(request, { params: Promise.resolve({ id: 'announcement-1' }) });
  const payload = await response.json();

  assert.equal(response.status, 200);
  if (!updatedPayload) {
    throw new Error('expected updatedPayload to be captured');
  }
  const patchedPayload: UpdatedAnnouncementPayload = updatedPayload;
  assert.equal(patchedPayload.content, '更新后的公告内容');
  assert.equal(payload.announcement.publishedAt, '2026-03-28T10:00:00.000Z');
});

test('admin announcements PATCH should return 404 when announcement does not exist', async (t) => {
  const apiUtilsModule = require('../lib/api-utils') as any;
  const originalRequireAdminContext = apiUtilsModule.requireAdminContext;
  const originalGetSystemAdminClient = apiUtilsModule.getSystemAdminClient;

  apiUtilsModule.requireAdminContext = async () => ({
    user: { id: 'admin-1' },
    supabase: {},
  });
  apiUtilsModule.getSystemAdminClient = () => ({
    from: (table: string) => {
      assert.equal(table, 'announcements');
      return {
        select: () => ({
          eq: () => ({
            maybeSingle: async () => ({
              data: null,
              error: null,
            }),
          }),
        }),
      };
    },
  });

  t.after(() => {
    apiUtilsModule.requireAdminContext = originalRequireAdminContext;
    apiUtilsModule.getSystemAdminClient = originalGetSystemAdminClient;
  });

  const { PATCH } = await import('../app/api/admin/announcements/[id]/route');
  const response = await PATCH(new NextRequest('http://localhost/api/admin/announcements/missing', {
    method: 'PATCH',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ content: '新内容' }),
  }), { params: Promise.resolve({ id: 'missing' }) });
  const payload = await response.json();

  assert.equal(response.status, 404);
  assert.equal(payload.error, '公告不存在');
});

test('admin announcements DELETE should delete the target announcement', async (t) => {
  const apiUtilsModule = require('../lib/api-utils') as any;
  const originalRequireAdminContext = apiUtilsModule.requireAdminContext;
  const originalGetSystemAdminClient = apiUtilsModule.getSystemAdminClient;

  let deletedId: string | null = null;

  apiUtilsModule.requireAdminContext = async () => ({
    user: { id: 'admin-1' },
    supabase: {},
  });
  apiUtilsModule.getSystemAdminClient = () => ({
    from: (table: string) => {
      assert.equal(table, 'announcements');
      return {
        select: () => ({
          eq: () => ({
            maybeSingle: async () => ({
              data: {
                id: 'announcement-1',
                content: '旧内容',
                published_at: '2026-03-28T10:00:00.000Z',
                created_at: '2026-03-28T10:00:00.000Z',
                updated_at: '2026-03-28T10:00:00.000Z',
              },
              error: null,
            }),
          }),
        }),
        delete: () => ({
          eq: async (_column: string, value: string) => {
            deletedId = value;
            return { error: null };
          },
        }),
      };
    },
  });

  t.after(() => {
    apiUtilsModule.requireAdminContext = originalRequireAdminContext;
    apiUtilsModule.getSystemAdminClient = originalGetSystemAdminClient;
  });

  const { DELETE } = await import('../app/api/admin/announcements/[id]/route');
  const response = await DELETE(
    new NextRequest('http://localhost/api/admin/announcements/announcement-1', { method: 'DELETE' }),
    { params: Promise.resolve({ id: 'announcement-1' }) },
  );
  const payload = await response.json();

  assert.equal(response.status, 200);
  assert.equal(payload.success, true);
  assert.equal(deletedId, 'announcement-1');
});

test('admin announcements DELETE should return 404 when announcement does not exist', async (t) => {
  const apiUtilsModule = require('../lib/api-utils') as any;
  const originalRequireAdminContext = apiUtilsModule.requireAdminContext;
  const originalGetSystemAdminClient = apiUtilsModule.getSystemAdminClient;

  apiUtilsModule.requireAdminContext = async () => ({
    user: { id: 'admin-1' },
    supabase: {},
  });
  apiUtilsModule.getSystemAdminClient = () => ({
    from: (table: string) => {
      assert.equal(table, 'announcements');
      return {
        select: () => ({
          eq: () => ({
            maybeSingle: async () => ({
              data: null,
              error: null,
            }),
          }),
        }),
      };
    },
  });

  t.after(() => {
    apiUtilsModule.requireAdminContext = originalRequireAdminContext;
    apiUtilsModule.getSystemAdminClient = originalGetSystemAdminClient;
  });

  const { DELETE } = await import('../app/api/admin/announcements/[id]/route');
  const response = await DELETE(
    new NextRequest('http://localhost/api/admin/announcements/missing', { method: 'DELETE' }),
    { params: Promise.resolve({ id: 'missing' }) },
  );
  const payload = await response.json();

  assert.equal(response.status, 404);
  assert.equal(payload.error, '公告不存在');
});
