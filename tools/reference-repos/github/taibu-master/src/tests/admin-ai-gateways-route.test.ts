import { test } from 'node:test';
import assert from 'node:assert/strict';
import { NextRequest } from 'next/server';

process.env.NEXT_PUBLIC_SUPABASE_URL = process.env.NEXT_PUBLIC_SUPABASE_URL || 'http://localhost';
process.env.NEXT_PUBLIC_SUPABASE_ANON_KEY = process.env.NEXT_PUBLIC_SUPABASE_ANON_KEY || 'test-anon';
process.env.NEWAPI_API_KEY = process.env.NEWAPI_API_KEY || 'newapi-key';

test('admin ai gateways GET should expose managed gateways with env key presence', async (t) => {
  const apiUtilsModule = require('../lib/api-utils') as any;
  const originalRequireAdminUser = apiUtilsModule.requireAdminUser;
  const originalGetSystemAdminClient = apiUtilsModule.getSystemAdminClient;

  apiUtilsModule.requireAdminUser = async () => ({ user: { id: 'admin-1' } });
  apiUtilsModule.getSystemAdminClient = () => ({
    from: (table: string) => {
      assert.equal(table, 'ai_gateways');
      return {
        select: () => ({
          order: async () => ({
            data: [
              {
                id: 'gateway-1',
                gateway_key: 'newapi',
                display_name: 'NewAPI',
                base_url: 'https://newapi.example/v1',
                api_key_env_var: 'NEWAPI_API_KEY',
                transport: 'openai_compatible',
                is_enabled: true,
                notes: null,
              },
              {
                id: 'gateway-2',
                gateway_key: 'octopus',
                display_name: 'Octopus',
                base_url: 'https://octopus.example/v1',
                api_key_env_var: 'OCTOPUS_API_KEY',
                transport: 'openai_compatible',
                is_enabled: false,
                notes: 'backup',
              },
            ],
            error: null,
          }),
        }),
      };
    },
  });

  t.after(() => {
    apiUtilsModule.requireAdminUser = originalRequireAdminUser;
    apiUtilsModule.getSystemAdminClient = originalGetSystemAdminClient;
  });

  const { GET } = await import('../app/api/admin/ai-gateways/route');
  const response = await GET(new NextRequest('http://localhost/api/admin/ai-gateways'));
  const body = await response.json();

  assert.equal(response.status, 200);
  assert.deepEqual(
    body.gateways.map((gateway: { gatewayKey: string; hasApiKey: boolean }) => ({
      gatewayKey: gateway.gatewayKey,
      hasApiKey: gateway.hasApiKey,
    })),
    [
      { gatewayKey: 'newapi', hasApiKey: true },
      { gatewayKey: 'octopus', hasApiKey: false },
    ],
  );
});

test('admin ai gateways PATCH should update managed gateway settings', async (t) => {
  const apiUtilsModule = require('../lib/api-utils') as any;
  const originalRequireAdminUser = apiUtilsModule.requireAdminUser;
  const originalGetSystemAdminClient = apiUtilsModule.getSystemAdminClient;
  const serverConfigModule = require('../lib/server/ai-config') as any;
  const originalClearModelCache = serverConfigModule.clearModelCache;

  let updatedPayload: Record<string, unknown> | null = null;
  let cacheCleared = false;

  apiUtilsModule.requireAdminUser = async () => ({ user: { id: 'admin-1' } });
  apiUtilsModule.getSystemAdminClient = () => ({
    from: (table: string) => {
      assert.equal(table, 'ai_gateways');
      return {
        update: (payload: Record<string, unknown>) => {
          updatedPayload = payload;
          return {
            eq: () => ({
              select: () => ({
                single: async () => ({
                  data: { id: 'gateway-1' },
                  error: null,
                }),
              }),
            }),
          };
        },
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

  const { PATCH } = await import('../app/api/admin/ai-gateways/[id]/route');
  const request = new NextRequest('http://localhost/api/admin/ai-gateways/gateway-1', {
    method: 'PATCH',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({
      displayName: 'NewAPI Gateway',
      baseUrl: 'https://gateway.example/v1',
      apiKeyEnvVar: 'NEWAPI_API_KEY',
      isEnabled: true,
      notes: 'primary',
    }),
  });

  const response = await PATCH(request, { params: Promise.resolve({ id: 'gateway-1' }) });

  assert.equal(response.status, 200);
  assert.deepEqual(updatedPayload, {
    display_name: 'NewAPI Gateway',
    base_url: 'https://gateway.example/v1',
    api_key_env_var: 'NEWAPI_API_KEY',
    is_enabled: true,
    notes: 'primary',
  });
  assert.equal(cacheCleared, true);
});
