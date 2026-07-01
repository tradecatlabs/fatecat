import { test } from 'node:test';
import assert from 'node:assert/strict';
import { NextRequest } from 'next/server';

process.env.NEXT_PUBLIC_SUPABASE_URL = process.env.NEXT_PUBLIC_SUPABASE_URL || 'http://localhost';
process.env.NEXT_PUBLIC_SUPABASE_ANON_KEY = process.env.NEXT_PUBLIC_SUPABASE_ANON_KEY || 'test-anon';

test('admin ai model PATCH should update editable base fields including modelKey', async (t) => {
  const apiUtilsModule = require('../lib/api-utils') as any;
  const serverConfigModule = require('../lib/server/ai-config') as any;
  const originalRequireAdminUser = apiUtilsModule.requireAdminUser;
  const originalGetSystemAdminClient = apiUtilsModule.getSystemAdminClient;
  const originalClearModelCache = serverConfigModule.clearModelCache;

  let rpcArgs: Record<string, unknown> | null = null;
  let cacheCleared = false;

  apiUtilsModule.requireAdminUser = async () => ({ user: { id: 'admin-1' } });
  apiUtilsModule.getSystemAdminClient = () => ({
    rpc: async (fn: string, args: Record<string, unknown>) => {
      assert.equal(fn, 'admin_update_ai_model_and_cleanup_bindings');
      rpcArgs = args;
      return {
        data: {
          status: 'ok',
          model: { id: 'model-1' },
        },
        error: null,
      };
    },
  });
  serverConfigModule.clearModelCache = () => {
    cacheCleared = true;
  };

  t.after(() => {
    apiUtilsModule.requireAdminUser = originalRequireAdminUser;
    apiUtilsModule.getSystemAdminClient = originalGetSystemAdminClient;
    serverConfigModule.clearModelCache = originalClearModelCache;
  });

  const { PATCH } = await import('../app/api/admin/ai-models/[id]/route');
  const request = new NextRequest('http://localhost/api/admin/ai-models/model-1', {
    method: 'PATCH',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({
      modelKey: 'gpt-5.4-mini',
      displayName: 'ChatGPT 5.4 Mini',
      vendor: 'openai',
      description: 'edited',
    }),
  });

  const response = await PATCH(request, { params: Promise.resolve({ id: 'model-1' }) });

  assert.equal(response.status, 200);
  assert.deepEqual(rpcArgs, {
    p_model_id: 'model-1',
    p_patch: {
      model_key: 'gpt-5.4-mini',
      display_name: 'ChatGPT 5.4 Mini',
      vendor: 'openai',
      description: 'edited',
    },
  });
  assert.equal(cacheCleared, true);
});

test('admin ai model PATCH should not clear inherited bindings when validation fails', async (t) => {
  const apiUtilsModule = require('../lib/api-utils') as any;
  const serverConfigModule = require('../lib/server/ai-config') as any;
  const originalRequireAdminUser = apiUtilsModule.requireAdminUser;
  const originalGetSystemAdminClient = apiUtilsModule.getSystemAdminClient;
  const originalClearModelCache = serverConfigModule.clearModelCache;

  let modelUpdated = false;
  let bindingCleared = false;
  let cacheCleared = false;

  apiUtilsModule.requireAdminUser = async () => ({ user: { id: 'admin-1' } });
  apiUtilsModule.getSystemAdminClient = () => ({
    from: (table: string) => {
      if (table === 'ai_models') {
        return {
          update: () => {
            modelUpdated = true;
            return {
              eq: () => ({
                select: () => ({
                  single: async () => ({
                    data: { id: 'model-1' },
                    error: null,
                  }),
                }),
              }),
            };
          },
        };
      }
      if (table === 'ai_model_gateway_bindings') {
        return {
          update: () => {
            bindingCleared = true;
            return {
              eq: () => ({
                eq: async () => ({ error: null }),
              }),
            };
          },
        };
      }
      throw new Error(`Unexpected table ${table}`);
    },
  });
  serverConfigModule.clearModelCache = () => {
    cacheCleared = true;
  };

  t.after(() => {
    apiUtilsModule.requireAdminUser = originalRequireAdminUser;
    apiUtilsModule.getSystemAdminClient = originalGetSystemAdminClient;
    serverConfigModule.clearModelCache = originalClearModelCache;
  });

  const { PATCH } = await import('../app/api/admin/ai-models/[id]/route');
  const request = new NextRequest('http://localhost/api/admin/ai-models/model-1', {
    method: 'PATCH',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({
      modelKey: 'gpt-5.4-mini',
      usageType: 'invalid-type',
    }),
  });

  const response = await PATCH(request, { params: Promise.resolve({ id: 'model-1' }) });
  const payload = await response.json();

  assert.equal(response.status, 400);
  assert.equal(payload.error, '无效的 usageType 值');
  assert.equal(modelUpdated, false);
  assert.equal(bindingCleared, false);
  assert.equal(cacheCleared, false);
});

test('admin ai model DELETE should remove model and clear cache', async (t) => {
  const apiUtilsModule = require('../lib/api-utils') as any;
  const serverConfigModule = require('../lib/server/ai-config') as any;
  const originalRequireAdminUser = apiUtilsModule.requireAdminUser;
  const originalGetSystemAdminClient = apiUtilsModule.getSystemAdminClient;
  const originalClearModelCache = serverConfigModule.clearModelCache;

  let deletedModelId: string | null = null;
  let cacheCleared = false;

  apiUtilsModule.requireAdminUser = async () => ({ user: { id: 'admin-1' } });
  apiUtilsModule.getSystemAdminClient = () => ({
    from: (table: string) => {
      assert.equal(table, 'ai_models');
      return {
        delete: () => ({
          eq: async (column: string, value: string) => {
            assert.equal(column, 'id');
            deletedModelId = value;
            return { error: null };
          },
        }),
      };
    },
  });
  serverConfigModule.clearModelCache = () => {
    cacheCleared = true;
  };

  t.after(() => {
    apiUtilsModule.requireAdminUser = originalRequireAdminUser;
    apiUtilsModule.getSystemAdminClient = originalGetSystemAdminClient;
    serverConfigModule.clearModelCache = originalClearModelCache;
  });

  const { DELETE } = await import('../app/api/admin/ai-models/[id]/route');
  const request = new NextRequest('http://localhost/api/admin/ai-models/model-1', {
    method: 'DELETE',
  });

  const response = await DELETE(request, { params: Promise.resolve({ id: 'model-1' }) });

  assert.equal(response.status, 200);
  assert.equal(deletedModelId, 'model-1');
  assert.equal(cacheCleared, true);
});

test('admin ai model PATCH should return 409 when transactional update reports model key conflict', async (t) => {
  const apiUtilsModule = require('../lib/api-utils') as any;
  const serverConfigModule = require('../lib/server/ai-config') as any;
  const originalRequireAdminUser = apiUtilsModule.requireAdminUser;
  const originalGetSystemAdminClient = apiUtilsModule.getSystemAdminClient;
  const originalClearModelCache = serverConfigModule.clearModelCache;

  let cacheCleared = false;

  apiUtilsModule.requireAdminUser = async () => ({ user: { id: 'admin-1' } });
  apiUtilsModule.getSystemAdminClient = () => ({
    rpc: async () => ({
      data: { status: 'conflict' },
      error: null,
    }),
  });
  serverConfigModule.clearModelCache = () => {
    cacheCleared = true;
  };

  t.after(() => {
    apiUtilsModule.requireAdminUser = originalRequireAdminUser;
    apiUtilsModule.getSystemAdminClient = originalGetSystemAdminClient;
    serverConfigModule.clearModelCache = originalClearModelCache;
  });

  const { PATCH } = await import('../app/api/admin/ai-models/[id]/route');
  const request = new NextRequest('http://localhost/api/admin/ai-models/model-1', {
    method: 'PATCH',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({
      modelKey: 'gpt-5.4-mini',
      displayName: 'ChatGPT 5.4 Mini',
      description: 'after',
    }),
  });

  const response = await PATCH(request, { params: Promise.resolve({ id: 'model-1' }) });
  const payload = await response.json();

  assert.equal(response.status, 409);
  assert.equal(payload.error, '模型 ID 已存在');
  assert.equal(cacheCleared, false);
});
