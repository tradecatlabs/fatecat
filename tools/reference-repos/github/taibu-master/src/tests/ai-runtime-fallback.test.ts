import { test } from 'node:test';
import assert from 'node:assert/strict';

process.env.NEWAPI_API_KEY = 'newapi-key';
process.env.OCTOPUS_API_KEY = 'octopus-key';

test('callAI should fall back from primary source to backup source', async (t) => {
  const aiModule = require('../lib/ai/ai') as any;
  const serverConfigModule = require('../lib/server/ai-config') as any;

  const originalGetModelConfigAsync = serverConfigModule.getModelConfigAsync;
  const originalFetch = global.fetch;

  const urls: string[] = [];

  serverConfigModule.getModelConfigAsync = async () => ({
    id: 'deepseek-v3.2',
    name: 'DeepSeek V3.2',
    vendor: 'deepseek',
    usageType: 'chat',
    modelId: 'deepseek-v3.2',
    apiUrl: 'https://newapi.example/v1/chat/completions',
    apiKeyEnvVar: 'NEWAPI_API_KEY',
    sourceKey: 'newapi',
    transport: 'openai_compatible',
    supportsReasoning: false,
    defaultMaxTokens: 4000,
    sources: [
      {
        sourceKey: 'newapi',
        sourceName: 'NewAPI',
        apiUrl: 'https://newapi.example/v1/chat/completions',
        apiKeyEnvVar: 'NEWAPI_API_KEY',
        modelIdOverride: 'deepseek-v3.2',
        transport: 'openai_compatible',
        priority: 1,
        isActive: true,
        isEnabled: true,
      },
      {
        sourceKey: 'octopus',
        sourceName: 'Octopus',
        apiUrl: 'https://octopus.example/v1/chat/completions',
        apiKeyEnvVar: 'OCTOPUS_API_KEY',
        modelIdOverride: 'deepseek-v3.2',
        transport: 'openai_compatible',
        priority: 2,
        isActive: false,
        isEnabled: true,
      },
    ],
  });

  global.fetch = (async (input: Parameters<typeof fetch>[0]) => {
    urls.push(String(input));
    if (String(input).includes('newapi')) {
      return new Response('upstream failure', { status: 502 });
    }
    return Response.json({
      choices: [{ index: 0, message: { content: 'backup-success' } }],
    });
  }) as typeof fetch;

  t.after(() => {
    serverConfigModule.getModelConfigAsync = originalGetModelConfigAsync;
    global.fetch = originalFetch;
  });

  const result = await aiModule.callAI(
    [{ role: 'user', content: 'hello' }],
    'general',
    'deepseek-v3.2',
    '',
  );

  assert.equal(result, 'backup-success');
  assert.deepEqual(urls, [
    'https://newapi.example/v1/chat/completions',
    'https://octopus.example/v1/chat/completions',
  ]);
});

test('callAI should honor fixed octopus routing mode', async (t) => {
  const aiModule = require('../lib/ai/ai') as any;
  const serverConfigModule = require('../lib/server/ai-config') as any;

  const originalGetModelConfigAsync = serverConfigModule.getModelConfigAsync;
  const originalFetch = global.fetch;

  const urls: string[] = [];

  serverConfigModule.getModelConfigAsync = async () => ({
    id: 'deepseek-v3.2',
    name: 'DeepSeek V3.2',
    vendor: 'deepseek',
    usageType: 'chat',
    routingMode: 'octopus',
    modelId: 'deepseek-v3.2',
    apiUrl: 'https://newapi.example/v1/chat/completions',
    apiKeyEnvVar: 'NEWAPI_API_KEY',
    sourceKey: 'newapi',
    transport: 'openai_compatible',
    supportsReasoning: false,
    defaultMaxTokens: 4000,
    sources: [
      {
        sourceKey: 'newapi',
        sourceName: 'NewAPI',
        apiUrl: 'https://newapi.example/v1/chat/completions',
        apiKeyEnvVar: 'NEWAPI_API_KEY',
        modelIdOverride: 'deepseek-v3.2',
        transport: 'openai_compatible',
        priority: 1,
        isActive: true,
        isEnabled: true,
      },
      {
        sourceKey: 'octopus',
        sourceName: 'Octopus',
        apiUrl: 'https://octopus.example/v1/chat/completions',
        apiKeyEnvVar: 'OCTOPUS_API_KEY',
        modelIdOverride: 'deepseek-v3.2',
        transport: 'openai_compatible',
        priority: 2,
        isActive: false,
        isEnabled: true,
      },
    ],
  });

  global.fetch = (async (input: Parameters<typeof fetch>[0]) => {
    urls.push(String(input));
    return Response.json({
      choices: [{ index: 0, message: { content: 'octopus-only' } }],
    });
  }) as typeof fetch;

  t.after(() => {
    serverConfigModule.getModelConfigAsync = originalGetModelConfigAsync;
    global.fetch = originalFetch;
  });

  const result = await aiModule.callAI(
    [{ role: 'user', content: 'hello' }],
    'general',
    'deepseek-v3.2',
    '',
  );

  assert.equal(result, 'octopus-only');
  assert.deepEqual(urls, ['https://octopus.example/v1/chat/completions']);
});
