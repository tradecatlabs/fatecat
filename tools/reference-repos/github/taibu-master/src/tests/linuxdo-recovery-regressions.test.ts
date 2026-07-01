import test from 'node:test';
import assert from 'node:assert/strict';
import { NextRequest } from 'next/server';

process.env.LINUXDO_CLIENT_ID = 'linuxdo-client-id';
process.env.LINUXDO_CLIENT_SECRET = 'linuxdo-client-secret';
process.env.SUPABASE_SECRET_KEY = 'supabase-management-secret';
process.env.NEXT_PUBLIC_SUPABASE_URL = 'http://localhost';
process.env.NEXT_PUBLIC_SUPABASE_ANON_KEY = 'test-anon';

type SessionResult = {
  data: { session: { user: { id: string } } | null };
  error: { message?: string } | null;
};

type AuthAdminUser = {
  id: string;
  email: string;
  user_metadata?: Record<string, unknown> | null;
};

function buildCallbackRequest() {
  const stateValue = encodeURIComponent(JSON.stringify({
    state: 'expected-state',
    codeVerifier: 'code-verifier',
  }));

  return new NextRequest(
    'http://localhost/api/auth/linuxdo/callback?code=oauth-code&state=expected-state',
    {
      headers: {
        cookie: `linuxdo-oauth-state=${stateValue}`,
      },
    },
  );
}

test('generateDeterministicPassword should stay stable when only linuxdo client secret rotates', async (t) => {
  const linuxdoModule = await import('../lib/oauth/linuxdo');
  const originalClientSecret = process.env.LINUXDO_CLIENT_SECRET;
  const originalSupabaseSecret = process.env.SUPABASE_SECRET_KEY;

  process.env.SUPABASE_SECRET_KEY = 'stable-auth-secret';
  process.env.LINUXDO_CLIENT_SECRET = 'linuxdo-client-secret-v1';
  const first = linuxdoModule.generateDeterministicPassword('linuxdo-user-stable');

  process.env.LINUXDO_CLIENT_SECRET = 'linuxdo-client-secret-v2';
  const second = linuxdoModule.generateDeterministicPassword('linuxdo-user-stable');

  t.after(() => {
    process.env.LINUXDO_CLIENT_SECRET = originalClientSecret;
    process.env.SUPABASE_SECRET_KEY = originalSupabaseSecret;
  });

  assert.equal(first, second);
});

test('linuxdo callback should sign bound users in with stored auth email and synced password', async (t) => {
  const linuxdoModule = require('../lib/oauth/linuxdo') as {
    exchangeCode: (code: string, verifier: string, redirectUri: string) => Promise<{ access_token: string }>;
    fetchUserInfo: (accessToken: string) => Promise<Record<string, unknown>>;
    generateDeterministicPassword: (sub: string) => string;
  };
  const apiUtilsModule = require('../lib/api-utils') as {
    createAnonClient: () => {
      auth: {
        signInWithPassword: (credentials: { email: string; password: string }) => Promise<SessionResult>;
      };
    };
    getAuthAdminClient: () => {
      auth: {
        admin: {
          getUserById: (id: string) => Promise<{ data: { user: AuthAdminUser | null }; error: null }>;
          updateUserById: (
            id: string,
            payload: Record<string, unknown>,
          ) => Promise<{ data: { user: AuthAdminUser | null }; error: null }>;
        };
      };
    } | null;
    getSystemAdminClient: () => {
      from: (table: string) => Record<string, unknown>;
      rpc: (fn: string, args: Record<string, unknown>) => Promise<{ data: { status: string }; error: null }>;
    };
  };
  const authSessionModule = require('../lib/auth-session') as {
    setSessionCookies: (response: Response, session: unknown) => void;
  };

  const originalExchangeCode = linuxdoModule.exchangeCode;
  const originalFetchUserInfo = linuxdoModule.fetchUserInfo;
  const originalGenerateDeterministicPassword = linuxdoModule.generateDeterministicPassword;
  const originalCreateAnonClient = apiUtilsModule.createAnonClient;
  const originalGetAuthAdminClient = apiUtilsModule.getAuthAdminClient;
  const originalGetServiceRoleClient = apiUtilsModule.getSystemAdminClient;
  const originalSetSessionCookies = authSessionModule.setSessionCookies;

  let signInEmail = '';
  let signInPassword = '';
  let updatePayload: Record<string, unknown> | null = null;

  linuxdoModule.exchangeCode = async () => ({ access_token: 'access-token' });
  linuxdoModule.fetchUserInfo = async () => ({
    sub: 'linuxdo-user-bound',
    preferred_username: 'bound-user',
    name: 'Bound User',
    email: 'new-relay@example.com',
    email_verified: true,
    picture: 'https://cdn.example.com/bound.png',
  });
  linuxdoModule.generateDeterministicPassword = () => 'rotated-password';

  apiUtilsModule.createAnonClient = () => ({
    auth: {
      signInWithPassword: async ({ email, password }) => {
        signInEmail = email;
        signInPassword = password;
        return {
          data: {
            session: {
              user: { id: 'bound-user-id' },
            },
          },
          error: null,
        };
      },
    },
  });

  apiUtilsModule.getAuthAdminClient = () => ({
    auth: {
      admin: {
        getUserById: async () => ({
          data: {
            user: {
              id: 'bound-user-id',
              email: 'stored-auth@example.com',
              user_metadata: {},
            },
          },
          error: null,
        }),
        updateUserById: async (_id: string, payload: Record<string, unknown>) => {
          updatePayload = payload;
          return {
            data: {
              user: {
                id: 'bound-user-id',
                email: 'stored-auth@example.com',
              },
            },
            error: null,
          };
        },
      },
    },
  });

  apiUtilsModule.getSystemAdminClient = () => ({
    from: (table: string) => {
      if (table === 'user_oauth_providers') {
        return {
          select: () => ({
            eq: () => ({
              eq: () => ({
                maybeSingle: async () => ({ data: { user_id: 'bound-user-id' }, error: null }),
              }),
            }),
          }),
        };
      }

      if (table === 'users') {
        return {
          select: () => ({
            eq: () => ({
              maybeSingle: async () => ({ data: { id: 'bound-user-id' }, error: null }),
            }),
          }),
        };
      }

      throw new Error(`unexpected table: ${table}`);
    },
    rpc: async () => ({
      data: { status: 'ok' },
      error: null,
    }),
  });

  authSessionModule.setSessionCookies = () => {};

  t.after(() => {
    linuxdoModule.exchangeCode = originalExchangeCode;
    linuxdoModule.fetchUserInfo = originalFetchUserInfo;
    linuxdoModule.generateDeterministicPassword = originalGenerateDeterministicPassword;
    apiUtilsModule.createAnonClient = originalCreateAnonClient;
    apiUtilsModule.getAuthAdminClient = originalGetAuthAdminClient;
    apiUtilsModule.getSystemAdminClient = originalGetServiceRoleClient;
    authSessionModule.setSessionCookies = originalSetSessionCookies;
  });

  const { GET } = await import('../app/api/auth/linuxdo/callback/route');
  const response = await GET(buildCallbackRequest());

  assert.equal(response.status, 307);
  assert.equal(response.headers.get('location'), 'http://localhost/');
  assert.equal(signInEmail, 'stored-auth@example.com');
  assert.equal(signInPassword, 'rotated-password');
  const updatedUser = updatePayload as Record<string, unknown> | null;
  assert.ok(updatedUser);
  assert.equal(updatedUser.password, 'rotated-password');
  assert.equal(
    (updatedUser.user_metadata as Record<string, unknown>)?.linuxdo_sub,
    'linuxdo-user-bound',
  );
});

test('linuxdo callback should recover a missing public user row for bound providers after auth sync', async (t) => {
  const linuxdoModule = require('../lib/oauth/linuxdo') as {
    exchangeCode: (code: string, verifier: string, redirectUri: string) => Promise<{ access_token: string }>;
    fetchUserInfo: (accessToken: string) => Promise<Record<string, unknown>>;
    generateDeterministicPassword: (sub: string) => string;
  };
  const apiUtilsModule = require('../lib/api-utils') as {
    createAnonClient: () => {
      auth: {
        signInWithPassword: (credentials: { email: string; password: string }) => Promise<SessionResult>;
      };
    };
    getAuthAdminClient: () => {
      auth: {
        admin: {
          getUserById: (id: string) => Promise<{ data: { user: AuthAdminUser | null }; error: null }>;
          updateUserById: (
            id: string,
            payload: Record<string, unknown>,
          ) => Promise<{ data: { user: AuthAdminUser | null }; error: null }>;
        };
      };
    } | null;
    getSystemAdminClient: () => {
      from: (table: string) => Record<string, unknown>;
      rpc: (fn: string, args: Record<string, unknown>) => Promise<{ data: { status: string }; error: null }>;
    };
  };
  const authSessionModule = require('../lib/auth-session') as {
    setSessionCookies: (response: Response, session: unknown) => void;
  };

  const originalExchangeCode = linuxdoModule.exchangeCode;
  const originalFetchUserInfo = linuxdoModule.fetchUserInfo;
  const originalGenerateDeterministicPassword = linuxdoModule.generateDeterministicPassword;
  const originalCreateAnonClient = apiUtilsModule.createAnonClient;
  const originalGetAuthAdminClient = apiUtilsModule.getAuthAdminClient;
  const originalGetServiceRoleClient = apiUtilsModule.getSystemAdminClient;
  const originalSetSessionCookies = authSessionModule.setSessionCookies;

  let signInEmail = '';
  let signInPassword = '';
  let didSync = false;

  linuxdoModule.exchangeCode = async () => ({ access_token: 'access-token' });
  linuxdoModule.fetchUserInfo = async () => ({
    sub: 'linuxdo-user-bound-recover',
    preferred_username: 'bound-recover',
    name: 'Bound Recover',
    email: 'fresh-relay@example.com',
    email_verified: true,
    picture: 'https://cdn.example.com/recover.png',
  });
  linuxdoModule.generateDeterministicPassword = () => 'rotated-password';

  apiUtilsModule.createAnonClient = () => ({
    auth: {
      signInWithPassword: async ({ email, password }) => {
        signInEmail = email;
        signInPassword = password;
        return {
          data: {
            session: {
              user: { id: 'bound-recover-id' },
            },
          },
          error: null,
        };
      },
    },
  });

  apiUtilsModule.getAuthAdminClient = () => ({
    auth: {
      admin: {
        getUserById: async () => ({
          data: {
            user: {
              id: 'bound-recover-id',
              email: 'stored-auth@example.com',
              user_metadata: {},
            },
          },
          error: null,
        }),
        updateUserById: async () => {
          didSync = true;
          return {
            data: {
              user: {
                id: 'bound-recover-id',
                email: 'stored-auth@example.com',
                user_metadata: {},
              },
            },
            error: null,
          };
        },
      },
    },
  });

  apiUtilsModule.getSystemAdminClient = () => ({
    from: (table: string) => {
      if (table === 'user_oauth_providers') {
        return {
          select: () => ({
            eq: () => ({
              eq: () => ({
                maybeSingle: async () => ({ data: { user_id: 'bound-recover-id' }, error: null }),
              }),
            }),
          }),
        };
      }

      if (table === 'users') {
        return {
          select: () => ({
            eq: () => ({
              maybeSingle: async () => ({
                data: didSync ? { id: 'bound-recover-id' } : null,
                error: null,
              }),
            }),
          }),
        };
      }

      throw new Error(`unexpected table: ${table}`);
    },
    rpc: async () => ({
      data: { status: 'ok' },
      error: null,
    }),
  });

  authSessionModule.setSessionCookies = () => {};

  t.after(() => {
    linuxdoModule.exchangeCode = originalExchangeCode;
    linuxdoModule.fetchUserInfo = originalFetchUserInfo;
    linuxdoModule.generateDeterministicPassword = originalGenerateDeterministicPassword;
    apiUtilsModule.createAnonClient = originalCreateAnonClient;
    apiUtilsModule.getAuthAdminClient = originalGetAuthAdminClient;
    apiUtilsModule.getSystemAdminClient = originalGetServiceRoleClient;
    authSessionModule.setSessionCookies = originalSetSessionCookies;
  });

  const { GET } = await import('../app/api/auth/linuxdo/callback/route');
  const response = await GET(buildCallbackRequest());

  assert.equal(response.status, 307);
  assert.equal(response.headers.get('location'), 'http://localhost/');
  assert.equal(didSync, true);
  assert.equal(signInEmail, 'stored-auth@example.com');
  assert.equal(signInPassword, 'rotated-password');
});

test('linuxdo callback should reject bound providers when public user row is missing and auth sync is unavailable', async (t) => {
  const linuxdoModule = require('../lib/oauth/linuxdo') as {
    exchangeCode: (code: string, verifier: string, redirectUri: string) => Promise<{ access_token: string }>;
    fetchUserInfo: (accessToken: string) => Promise<Record<string, unknown>>;
    generateDeterministicPassword: (sub: string) => string;
  };
  const apiUtilsModule = require('../lib/api-utils') as {
    createAnonClient: () => {
      auth: {
        signInWithPassword: (credentials: { email: string; password: string }) => Promise<SessionResult>;
      };
    };
    getAuthAdminClient: () => null;
    getSystemAdminClient: () => {
      from: (table: string) => Record<string, unknown>;
      rpc: (fn: string, args: Record<string, unknown>) => Promise<{ data: { status: string }; error: null }>;
    };
  };
  const authSessionModule = require('../lib/auth-session') as {
    setSessionCookies: (response: Response, session: unknown) => void;
  };

  const originalExchangeCode = linuxdoModule.exchangeCode;
  const originalFetchUserInfo = linuxdoModule.fetchUserInfo;
  const originalGenerateDeterministicPassword = linuxdoModule.generateDeterministicPassword;
  const originalCreateAnonClient = apiUtilsModule.createAnonClient;
  const originalGetAuthAdminClient = apiUtilsModule.getAuthAdminClient;
  const originalGetServiceRoleClient = apiUtilsModule.getSystemAdminClient;
  const originalSetSessionCookies = authSessionModule.setSessionCookies;

  let signInCalled = false;

  linuxdoModule.exchangeCode = async () => ({ access_token: 'access-token' });
  linuxdoModule.fetchUserInfo = async () => ({
    sub: 'linuxdo-user-missing-public',
    preferred_username: 'missing-public',
    name: 'Missing Public User',
    email: 'missing-public@example.com',
    email_verified: true,
    picture: 'https://cdn.example.com/missing-public.png',
  });
  linuxdoModule.generateDeterministicPassword = () => 'stable-password';

  apiUtilsModule.createAnonClient = () => ({
    auth: {
      signInWithPassword: async () => {
        signInCalled = true;
        return {
          data: {
            session: {
              user: { id: 'bound-user-id' },
            },
          },
          error: null,
        };
      },
    },
  });

  apiUtilsModule.getAuthAdminClient = () => null;
  apiUtilsModule.getSystemAdminClient = () => ({
    from: (table: string) => {
      if (table === 'user_oauth_providers') {
        return {
          select: () => ({
            eq: () => ({
              eq: () => ({
                maybeSingle: async () => ({ data: { user_id: 'bound-user-id' }, error: null }),
              }),
            }),
          }),
        };
      }

      if (table === 'users') {
        return {
          select: () => ({
            eq: () => ({
              maybeSingle: async () => ({ data: null, error: null }),
            }),
          }),
        };
      }

      throw new Error(`unexpected table: ${table}`);
    },
    rpc: async () => ({
      data: { status: 'ok' },
      error: null,
    }),
  });
  authSessionModule.setSessionCookies = () => {
    throw new Error('setSessionCookies should not be called');
  };

  t.after(() => {
    linuxdoModule.exchangeCode = originalExchangeCode;
    linuxdoModule.fetchUserInfo = originalFetchUserInfo;
    linuxdoModule.generateDeterministicPassword = originalGenerateDeterministicPassword;
    apiUtilsModule.createAnonClient = originalCreateAnonClient;
    apiUtilsModule.getAuthAdminClient = originalGetAuthAdminClient;
    apiUtilsModule.getSystemAdminClient = originalGetServiceRoleClient;
    authSessionModule.setSessionCookies = originalSetSessionCookies;
  });

  const { GET } = await import('../app/api/auth/linuxdo/callback/route');
  const response = await GET(buildCallbackRequest());

  assert.equal(response.status, 307);
  assert.equal(response.headers.get('location'), 'http://localhost/?error=user_not_found');
  assert.equal(signInCalled, false);
});

test('linuxdo callback should recover missing provider bindings via admin user lookup before creating a new auth user', async (t) => {
  const linuxdoModule = require('../lib/oauth/linuxdo') as {
    exchangeCode: (code: string, verifier: string, redirectUri: string) => Promise<{ access_token: string }>;
    fetchUserInfo: (accessToken: string) => Promise<Record<string, unknown>>;
    generateDeterministicPassword: (sub: string) => string;
  };
  const apiUtilsModule = require('../lib/api-utils') as {
    createAnonClient: () => {
      auth: {
        signInWithPassword: (credentials: { email: string; password: string }) => Promise<SessionResult>;
      };
    };
    getAuthAdminClient: () => {
      auth: {
        admin: {
          listUsers: (options?: { page?: number; perPage?: number }) => Promise<{
            data: { users: AuthAdminUser[] };
            error: null;
          }>;
          updateUserById: (
            id: string,
            payload: Record<string, unknown>,
          ) => Promise<{ data: { user: AuthAdminUser | null }; error: null }>;
          createUser: (payload: Record<string, unknown>) => Promise<{
            data: { user: AuthAdminUser | null };
            error: { message: string } | null;
          }>;
        };
      };
    } | null;
    getSystemAdminClient: () => {
      from: (table: string) => Record<string, unknown>;
      rpc: (fn: string, args: Record<string, unknown>) => Promise<{ data: { status: string }; error: null }>;
    };
  };
  const authSessionModule = require('../lib/auth-session') as {
    setSessionCookies: (response: Response, session: unknown) => void;
  };

  const originalExchangeCode = linuxdoModule.exchangeCode;
  const originalFetchUserInfo = linuxdoModule.fetchUserInfo;
  const originalGenerateDeterministicPassword = linuxdoModule.generateDeterministicPassword;
  const originalCreateAnonClient = apiUtilsModule.createAnonClient;
  const originalGetAuthAdminClient = apiUtilsModule.getAuthAdminClient;
  const originalGetServiceRoleClient = apiUtilsModule.getSystemAdminClient;
  const originalSetSessionCookies = authSessionModule.setSessionCookies;

  let listUsersCalls = 0;
  let createUserCalls = 0;
  let signInEmail = '';
  let updatePayload: Record<string, unknown> | null = null;

  linuxdoModule.exchangeCode = async () => ({ access_token: 'access-token' });
  linuxdoModule.fetchUserInfo = async () => ({
    sub: 'linuxdo-user-recover',
    preferred_username: 'recover-user',
    name: 'Recover User',
    email: 'relay-now@example.com',
    email_verified: true,
    picture: 'https://cdn.example.com/recover.png',
  });
  linuxdoModule.generateDeterministicPassword = () => 'stable-password';

  apiUtilsModule.createAnonClient = () => ({
    auth: {
      signInWithPassword: async ({ email }) => {
        signInEmail = email;
        return {
          data: {
            session: {
              user: { id: 'recover-user-id' },
            },
          },
          error: null,
        };
      },
    },
  });

  apiUtilsModule.getAuthAdminClient = () => ({
    auth: {
      admin: {
        getUserById: async () => ({
          data: { user: null },
          error: { message: 'not found' },
        }),
        listUsers: async () => {
          listUsersCalls += 1;
          return {
            data: {
              users: [
                {
                  id: 'recover-user-id',
                  email: 'stored-auth@example.com',
                  user_metadata: {
                    linuxdo_sub: 'linuxdo-user-recover',
                  },
                },
              ],
            },
            error: null,
          };
        },
        updateUserById: async (_id: string, payload: Record<string, unknown>) => {
          updatePayload = payload;
          return {
            data: {
              user: {
                id: 'recover-user-id',
                email: 'stored-auth@example.com',
              },
            },
            error: null,
          };
        },
        createUser: async () => {
          createUserCalls += 1;
          return {
            data: { user: null },
            error: { message: 'User already registered' },
          };
        },
      },
    },
  });

  apiUtilsModule.getSystemAdminClient = () => ({
    from: (table: string) => {
      if (table === 'user_oauth_providers') {
        return {
          select: () => ({
            eq: () => ({
              eq: () => ({
                maybeSingle: async () => ({ data: null, error: null }),
              }),
            }),
          }),
        };
      }

      throw new Error(`unexpected table: ${table}`);
    },
    rpc: async () => ({
      data: { status: 'ok' },
      error: null,
    }),
  });

  authSessionModule.setSessionCookies = () => {};

  t.after(() => {
    linuxdoModule.exchangeCode = originalExchangeCode;
    linuxdoModule.fetchUserInfo = originalFetchUserInfo;
    linuxdoModule.generateDeterministicPassword = originalGenerateDeterministicPassword;
    apiUtilsModule.createAnonClient = originalCreateAnonClient;
    apiUtilsModule.getAuthAdminClient = originalGetAuthAdminClient;
    apiUtilsModule.getSystemAdminClient = originalGetServiceRoleClient;
    authSessionModule.setSessionCookies = originalSetSessionCookies;
  });

  const { GET } = await import('../app/api/auth/linuxdo/callback/route');
  const response = await GET(buildCallbackRequest());

  assert.equal(response.status, 307);
  assert.equal(response.headers.get('location'), 'http://localhost/');
  assert.equal(listUsersCalls, 1);
  assert.equal(createUserCalls, 0);
  assert.equal(signInEmail, 'stored-auth@example.com');
  const reboundUser = updatePayload as Record<string, unknown> | null;
  assert.ok(reboundUser);
  assert.equal(
    (reboundUser.user_metadata as Record<string, unknown>)?.linuxdo_sub,
    'linuxdo-user-recover',
  );
  assert.equal(
    ((reboundUser.user_metadata as Record<string, unknown>)?.linuxdo_provider_metadata as Record<string, unknown>)?.sub,
    'linuxdo-user-recover',
  );
});
