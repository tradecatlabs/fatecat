import test from 'node:test';
import assert from 'node:assert/strict';

process.env.NEXT_PUBLIC_SUPABASE_URL = process.env.NEXT_PUBLIC_SUPABASE_URL || 'http://localhost';
process.env.NEXT_PUBLIC_SUPABASE_ANON_KEY = process.env.NEXT_PUBLIC_SUPABASE_ANON_KEY || 'test-anon';

test('buildDreamContextPayload should reuse cached payload within TTL', async (t) => {
  const apiUtilsModule = require('../lib/api-utils') as typeof import('../lib/api-utils');
  const baziModule = require('../lib/data-sources/bazi') as typeof import('../lib/data-sources/bazi');
  const fortuneModule = require('../lib/data-sources/fortune') as typeof import('../lib/data-sources/fortune');
  const caseProfileModule = require('../lib/server/bazi-case-profile') as typeof import('../lib/server/bazi-case-profile');
  const modulePath = require.resolve('../lib/chat/chat-context');

  const originalGetSystemAdminClient = apiUtilsModule.getSystemAdminClient;
  const originalFormatForAI = baziModule.baziProvider.formatForAI;
  const originalDailyFortuneGet = fortuneModule.dailyFortuneProvider.get;
  const originalGetBaziCaseProfileByChartId = caseProfileModule.getBaziCaseProfileByChartId;

  let userSettingsReads = 0;
  let baziChartMetaReads = 0;
  let baziChartReads = 0;
  let fortuneReads = 0;

  apiUtilsModule.getSystemAdminClient = (() => ({
    from(table: string) {
      if (table === 'user_settings') {
        return {
          select() {
            return {
              eq() {
                return {
                  maybeSingle: async () => {
                    userSettingsReads += 1;
                    return {
                      data: { default_bazi_chart_id: 'chart-1' },
                      error: null,
                    };
                  },
                };
              },
            };
          },
        };
      }

      if (table === 'bazi_charts') {
        return {
          select(columns: string) {
            assert.doesNotMatch(columns, /^\*$/u);
            if (columns === 'id, updated_at') {
              return {
                eq() {
                  return {
                    eq() {
                      return {
                        maybeSingle: async () => {
                          baziChartMetaReads += 1;
                          return {
                            data: {
                              id: 'chart-1',
                              updated_at: '2026-03-27T00:00:00.000Z',
                            },
                            error: null,
                          };
                        },
                      };
                    },
                  };
                },
              };
            }
            return {
              eq() {
                return {
                  eq() {
                    return {
                      maybeSingle: async () => {
                        baziChartReads += 1;
                        return {
	                          data: {
	                            id: 'chart-1',
	                            name: '测试命盘',
	                            gender: 'male',
	                            birth_date: '1990-01-01',
	                            birth_time: '08:00',
	                            birth_place: '上海',
	                            calendar_type: 'solar',
	                            is_leap_month: false,
	                          },
                          error: null,
                        };
                      },
                    };
                  },
                };
              },
              order() {
                return {
                  limit() {
                    return {
                      maybeSingle: async () => {
                        throw new Error('latest fallback should not be used');
                      },
                    };
                  },
                };
              },
            };
          },
        };
      }

      if (table === 'bazi_case_profiles') {
        return {
          select() {
            return {
              eq() {
                return {
                  eq() {
                    return {
                      maybeSingle: async () => ({ data: null, error: null }),
                    };
                  },
                };
              },
            };
          },
        };
      }

      throw new Error(`Unexpected table: ${table}`);
    },
  })) as unknown as typeof apiUtilsModule.getSystemAdminClient;

  baziModule.baziProvider.formatForAI = (() => '命盘文本') as typeof baziModule.baziProvider.formatForAI;
  fortuneModule.dailyFortuneProvider.get = (async () => {
    fortuneReads += 1;
    return {
      id: 'today',
      name: '今日运势',
      content: '今日运势文本',
      createdAt: new Date().toISOString(),
    };
  }) as typeof fortuneModule.dailyFortuneProvider.get;
  caseProfileModule.getBaziCaseProfileByChartId = (async () => null) as typeof caseProfileModule.getBaziCaseProfileByChartId;

  t.after(() => {
    apiUtilsModule.getSystemAdminClient = originalGetSystemAdminClient;
    baziModule.baziProvider.formatForAI = originalFormatForAI;
    fortuneModule.dailyFortuneProvider.get = originalDailyFortuneGet;
    caseProfileModule.getBaziCaseProfileByChartId = originalGetBaziCaseProfileByChartId;
    delete require.cache[modulePath];
  });

  delete require.cache[modulePath];
  const chatContextModule = require('../lib/chat/chat-context') as typeof import('../lib/chat/chat-context');

  const first = await chatContextModule.buildDreamContextPayload('user-1');
  const second = await chatContextModule.buildDreamContextPayload('user-1');

  assert.equal(first.payload.baziText, '命盘文本');
  assert.equal(second.payload.fortuneText, '今日运势文本');
  assert.equal(userSettingsReads, 2);
  assert.equal(baziChartMetaReads, 2);
  assert.equal(baziChartReads, 1);
  assert.equal(fortuneReads, 1);
});

test('buildDreamContextPayload should key latest-chart cache by resolved chart id', async (t) => {
  const apiUtilsModule = require('../lib/api-utils') as typeof import('../lib/api-utils');
  const baziModule = require('../lib/data-sources/bazi') as typeof import('../lib/data-sources/bazi');
  const fortuneModule = require('../lib/data-sources/fortune') as typeof import('../lib/data-sources/fortune');
  const caseProfileModule = require('../lib/server/bazi-case-profile') as typeof import('../lib/server/bazi-case-profile');
  const modulePath = require.resolve('../lib/chat/chat-context');

  const originalGetSystemAdminClient = apiUtilsModule.getSystemAdminClient;
  const originalFormatForAI = baziModule.baziProvider.formatForAI;
  const originalDailyFortuneGet = fortuneModule.dailyFortuneProvider.get;
  const originalGetBaziCaseProfileByChartId = caseProfileModule.getBaziCaseProfileByChartId;

  let latestChartId = 'chart-1';
  let latestMetaReads = 0;
  let baziChartReads = 0;

  apiUtilsModule.getSystemAdminClient = (() => ({
    from(table: string) {
      if (table === 'user_settings') {
        return {
          select() {
            return {
              eq() {
                return {
                  maybeSingle: async () => ({
                    data: { default_bazi_chart_id: null },
                    error: null,
                  }),
                };
              },
            };
          },
        };
      }

      if (table === 'bazi_charts') {
        return {
          select(columns: string) {
            if (columns === 'id, updated_at') {
              return {
                eq() {
                  return {
                    order() {
                      return {
                        limit() {
                          return {
                            maybeSingle: async () => {
                              latestMetaReads += 1;
                              return {
                                data: latestChartId ? {
                                  id: latestChartId,
                                  updated_at: `${latestChartId}-updated`,
                                } : null,
                                error: null,
                              };
                            },
                          };
                        },
                      };
                    },
                  };
                },
              };
            }

            return {
              eq() {
                return {
                  eq() {
                    return {
                      maybeSingle: async () => {
                        baziChartReads += 1;
                        return {
	                          data: latestChartId ? {
	                            id: latestChartId,
	                            name: latestChartId,
	                            gender: 'male',
	                            birth_date: '1990-01-01',
	                            birth_time: '08:00',
	                            birth_place: '上海',
	                            calendar_type: 'solar',
	                            is_leap_month: false,
	                          } : null,
                          error: null,
                        };
                      },
                    };
                  },
                };
              },
            };
          },
        };
      }

      if (table === 'bazi_case_profiles') {
        return {
          select() {
            return {
              eq() {
                return {
                  eq() {
                    return {
                      maybeSingle: async () => ({ data: null, error: null }),
                    };
                  },
                };
              },
            };
          },
        };
      }

      throw new Error(`Unexpected table: ${table}`);
    },
  })) as unknown as typeof apiUtilsModule.getSystemAdminClient;

  baziModule.baziProvider.formatForAI = ((chart: { id?: string }) => `命盘:${chart.id}`) as typeof baziModule.baziProvider.formatForAI;
  fortuneModule.dailyFortuneProvider.get = (async () => ({
    id: 'today',
    name: '今日运势',
    content: '今日运势文本',
    createdAt: new Date().toISOString(),
  })) as typeof fortuneModule.dailyFortuneProvider.get;
  caseProfileModule.getBaziCaseProfileByChartId = (async () => null) as typeof caseProfileModule.getBaziCaseProfileByChartId;

  t.after(() => {
    apiUtilsModule.getSystemAdminClient = originalGetSystemAdminClient;
    baziModule.baziProvider.formatForAI = originalFormatForAI;
    fortuneModule.dailyFortuneProvider.get = originalDailyFortuneGet;
    caseProfileModule.getBaziCaseProfileByChartId = originalGetBaziCaseProfileByChartId;
    delete require.cache[modulePath];
  });

  delete require.cache[modulePath];
  const chatContextModule = require('../lib/chat/chat-context') as typeof import('../lib/chat/chat-context');

  const first = await chatContextModule.buildDreamContextPayload('user-1');
  const second = await chatContextModule.buildDreamContextPayload('user-1');
  latestChartId = 'chart-2';
  const third = await chatContextModule.buildDreamContextPayload('user-1');

  assert.equal(first.payload.baziText, '命盘:chart-1');
  assert.equal(second.payload.baziText, '命盘:chart-1');
  assert.equal(third.payload.baziText, '命盘:chart-2');
  assert.equal(latestMetaReads, 3);
  assert.equal(baziChartReads, 2);
});
