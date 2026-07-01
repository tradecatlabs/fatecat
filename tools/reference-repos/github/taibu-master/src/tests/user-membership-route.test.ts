import test from 'node:test';
import assert from 'node:assert/strict';

process.env.NEXT_PUBLIC_SUPABASE_URL = process.env.NEXT_PUBLIC_SUPABASE_URL || 'http://localhost';
process.env.NEXT_PUBLIC_SUPABASE_ANON_KEY = process.env.NEXT_PUBLIC_SUPABASE_ANON_KEY || 'test-anon';

function mockUserContext<T extends object>(user: unknown, db: T) {
  return {
    user,
    accessToken: null,
    db,
    supabase: db,
  };
}

test('user membership route should return lightweight normalized membership payload', async (t) => {
  const apiUtilsModule = require('../lib/api-utils') as any;
  const routePath = require.resolve('../app/api/user/membership/route');

  const originalRequireUserContext = apiUtilsModule.requireUserContext;
  const originalJsonOk = apiUtilsModule.jsonOk;
  const originalJsonError = apiUtilsModule.jsonError;

  apiUtilsModule.requireUserContext = async () => mockUserContext(
    { id: 'user-1' },
    {
      from(table: string) {
        assert.equal(table, 'users');
        return {
          select(columns: string) {
            assert.match(columns, /membership/u);
            return {
              eq(column: string, value: string) {
                assert.equal(column, 'id');
                assert.equal(value, 'user-1');
                return {
                  maybeSingle: async () => ({
                    data: {
                      membership: 'pro',
                      membership_expires_at: '2099-01-01T00:00:00.000Z',
                      ai_chat_count: 88,
                    },
                    error: null,
                  }),
                };
              },
            };
          },
        };
      },
    },
  );
  apiUtilsModule.jsonOk = (payload: unknown, status = 200) => Response.json(payload, { status });
  apiUtilsModule.jsonError = (message: string, status = 400) => Response.json({ error: message }, { status });

  t.after(() => {
    apiUtilsModule.requireUserContext = originalRequireUserContext;
    apiUtilsModule.jsonOk = originalJsonOk;
    apiUtilsModule.jsonError = originalJsonError;
    delete require.cache[routePath];
  });

  delete require.cache[routePath];
  const routeModule = require('../app/api/user/membership/route') as typeof import('../app/api/user/membership/route');
  const response = await routeModule.GET(new Request('http://localhost/api/user/membership') as never);
  const payload = await response.json();

  assert.equal(response.status, 200);
  assert.equal(payload.userId, 'user-1');
  assert.equal(payload.membership.type, 'pro');
  assert.equal(payload.membership.aiChatCount, 88);
  assert.equal(payload.membership.isActive, true);
});

test('user membership route should return 500 when user row is missing', async (t) => {
  const apiUtilsModule = require('../lib/api-utils') as any;
  const routePath = require.resolve('../app/api/user/membership/route');

  const originalRequireUserContext = apiUtilsModule.requireUserContext;
  const originalJsonOk = apiUtilsModule.jsonOk;
  const originalJsonError = apiUtilsModule.jsonError;

  apiUtilsModule.requireUserContext = async () => mockUserContext(
    { id: 'user-1' },
    {
      from() {
        return {
          select() {
            return {
              eq() {
                return {
                  maybeSingle: async () => ({
                    data: null,
                    error: null,
                  }),
                };
              },
            };
          },
        };
      },
    },
  );
  apiUtilsModule.jsonOk = (payload: unknown, status = 200) => Response.json(payload, { status });
  apiUtilsModule.jsonError = (message: string, status = 400) => Response.json({ error: message }, { status });

  t.after(() => {
    apiUtilsModule.requireUserContext = originalRequireUserContext;
    apiUtilsModule.jsonOk = originalJsonOk;
    apiUtilsModule.jsonError = originalJsonError;
    delete require.cache[routePath];
  });

  delete require.cache[routePath];
  const routeModule = require('../app/api/user/membership/route') as typeof import('../app/api/user/membership/route');
  const response = await routeModule.GET(new Request('http://localhost/api/user/membership') as never);
  const payload = await response.json();

  assert.equal(response.status, 500);
  assert.equal(payload.error, '获取会员信息失败');
});
