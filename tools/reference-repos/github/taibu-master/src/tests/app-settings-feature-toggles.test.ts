import { test } from 'node:test';
import assert from 'node:assert/strict';

async function loadAppSettingsModule() {
  const modulePath = require.resolve('../lib/app-settings');
  delete require.cache[modulePath];
  return await import('../lib/app-settings');
}

test('getFeatureToggles reads feature toggles via like filter', async (t) => {
  const apiUtilsModule = require('../lib/api-utils') as typeof import('../lib/api-utils');
  const originalGetSystemAdminClient = apiUtilsModule.getSystemAdminClient;
  const originalConsoleError = console.error;
  const errorLogs: unknown[][] = [];

  apiUtilsModule.getSystemAdminClient = (() => ({
    from(table: string) {
      assert.equal(table, 'app_settings');
      return {
        select() {
          return {
            like(column: string, pattern: string) {
              assert.equal(column, 'setting_key');
              assert.equal(pattern, 'feature_disabled:%');
              return Promise.resolve({
                data: [
                  { setting_key: 'feature_disabled:chat', setting_value: true },
                  { setting_key: 'feature_disabled:knowledge-base', setting_value: false },
                ],
                error: null,
              });
            },
          };
        },
      };
    },
  })) as unknown as typeof apiUtilsModule.getSystemAdminClient;

  console.error = (...args: unknown[]) => {
    errorLogs.push(args);
  };

  t.after(() => {
    apiUtilsModule.getSystemAdminClient = originalGetSystemAdminClient;
    console.error = originalConsoleError;
    delete require.cache[require.resolve('../lib/app-settings')];
  });

  const appSettingsModule = await loadAppSettingsModule();
  const toggles = await appSettingsModule.getFeatureToggles();

  assert.equal(toggles.chat, true);
  assert.equal(toggles['knowledge-base'], false);
  assert.equal(errorLogs.length, 0);
});

test('isFeatureModuleEnabled caches single-feature reads', async (t) => {
  const apiUtilsModule = require('../lib/api-utils') as typeof import('../lib/api-utils');
  const originalGetSystemAdminClient = apiUtilsModule.getSystemAdminClient;
  let readCount = 0;

  apiUtilsModule.getSystemAdminClient = (() => ({
    from(table: string) {
      assert.equal(table, 'app_settings');
      return {
        select(columns: string) {
          assert.equal(columns, 'setting_value');
          return {
            eq(column: string, key: string) {
              assert.equal(column, 'setting_key');
              assert.equal(key, 'feature_disabled:knowledge-base');
              return {
                maybeSingle: async () => {
                  readCount += 1;
                  return { data: { setting_value: true }, error: null };
                },
              };
            },
          };
        },
      };
    },
  })) as unknown as typeof apiUtilsModule.getSystemAdminClient;

  t.after(() => {
    apiUtilsModule.getSystemAdminClient = originalGetSystemAdminClient;
    delete require.cache[require.resolve('../lib/app-settings')];
  });

  const appSettingsModule = await loadAppSettingsModule();
  const first = await appSettingsModule.isFeatureModuleEnabled('knowledge-base');
  const second = await appSettingsModule.isFeatureModuleEnabled('knowledge-base');

  assert.equal(first, false);
  assert.equal(second, false);
  assert.equal(readCount, 1);
});

test('setFeatureToggle refreshes cached single-feature value', async (t) => {
  const apiUtilsModule = require('../lib/api-utils') as typeof import('../lib/api-utils');
  const originalGetSystemAdminClient = apiUtilsModule.getSystemAdminClient;
  let readCount = 0;
  let upsertCount = 0;
  let disabledValue = true;

  apiUtilsModule.getSystemAdminClient = (() => ({
    from(table: string) {
      assert.equal(table, 'app_settings');
      return {
        select(columns: string) {
          assert.equal(columns, 'setting_value');
          return {
            eq(column: string, key: string) {
              assert.equal(column, 'setting_key');
              assert.equal(key, 'feature_disabled:chat');
              return {
                maybeSingle: async () => {
                  readCount += 1;
                  return { data: { setting_value: disabledValue }, error: null };
                },
              };
            },
          };
        },
        upsert(payload: { setting_key: string; setting_value: boolean }) {
          upsertCount += 1;
          assert.equal(payload.setting_key, 'feature_disabled:chat');
          disabledValue = payload.setting_value;
          return Promise.resolve({ error: null });
        },
      };
    },
  })) as unknown as typeof apiUtilsModule.getSystemAdminClient;

  t.after(() => {
    apiUtilsModule.getSystemAdminClient = originalGetSystemAdminClient;
    delete require.cache[require.resolve('../lib/app-settings')];
  });

  const appSettingsModule = await loadAppSettingsModule();

  assert.equal(await appSettingsModule.isFeatureModuleEnabled('chat'), false);
  assert.equal(readCount, 1);

  assert.equal(await appSettingsModule.setFeatureToggle('chat', false), true);
  assert.equal(upsertCount, 1);
  assert.equal(await appSettingsModule.isFeatureModuleEnabled('chat'), true);
  assert.equal(readCount, 1);
});
