import { test } from 'node:test';
import assert from 'node:assert/strict';

process.env.NEXT_PUBLIC_SUPABASE_URL = process.env.NEXT_PUBLIC_SUPABASE_URL || 'http://localhost';
process.env.NEXT_PUBLIC_SUPABASE_ANON_KEY = process.env.NEXT_PUBLIC_SUPABASE_ANON_KEY || 'test-anon';

test('server ai-config should order enabled sources with active source first and expose source list', async (t) => {
  const supabaseServerModule = require('../lib/supabase-server') as any;
  const serverConfigPath = require.resolve('../lib/server/ai-config');
  delete require.cache[serverConfigPath];

  const originalGetSystemAdminClient = supabaseServerModule.getSystemAdminClient;

  supabaseServerModule.getSystemAdminClient = () => ({
    from: (table: string) => {
      assert.equal(table, 'ai_models');
      return {
        select: () => ({
          eq: () => ({
            order: async () => ({
              data: [
                {
                  model_key: 'deepseek-v3.2',
                  display_name: 'DeepSeek V3.2',
                  vendor: 'deepseek',
                  usage_type: 'chat',
                  routing_mode: 'auto',
                  supports_reasoning: false,
                  is_reasoning_default: false,
                  supports_vision: false,
                  default_temperature: '0.7',
                  default_max_tokens: 4000,
                  required_tier: 'free',
                  reasoning_required_tier: 'plus',
                  bindings: [
                    {
                      id: 'binding-2',
                      model_id_override: 'deepseek-v3.2',
                      reasoning_model_id: null,
                      is_enabled: true,
                      priority: 2,
                      gateway: {
                        gateway_key: 'octopus',
                        display_name: 'Octopus',
                        base_url: 'https://octopus.example/v1',
                        api_key_env_var: 'OCTOPUS_API_KEY',
                        transport: 'openai_compatible',
                        is_enabled: true,
                      },
                    },
                    {
                      id: 'binding-1',
                      model_id_override: 'deepseek-v3.2',
                      reasoning_model_id: null,
                      is_enabled: true,
                      priority: 1,
                      gateway: {
                        gateway_key: 'newapi',
                        display_name: 'NewAPI',
                        base_url: 'https://newapi.example/v1',
                        api_key_env_var: 'NEWAPI_API_KEY',
                        transport: 'openai_compatible',
                        is_enabled: true,
                      },
                    },
                  ],
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
    supabaseServerModule.getSystemAdminClient = originalGetSystemAdminClient;
    delete require.cache[serverConfigPath];
  });

  const serverConfig = require('../lib/server/ai-config') as typeof import('../lib/server/ai-config');
  serverConfig.clearModelCache();

  const model = await serverConfig.getModelConfigAsync('deepseek-v3.2');
  assert.ok(model, 'model should be resolved');
  assert.equal(model?.sourceKey, 'newapi');
  assert.equal(model?.apiUrl, 'https://newapi.example/v1/chat/completions');
  assert.equal(model?.transport, 'openai_compatible');
  assert.equal(model?.usageType, 'chat');
  assert.deepEqual(
    model?.sources?.map((source) => source.sourceKey),
    ['newapi', 'octopus'],
  );
});
