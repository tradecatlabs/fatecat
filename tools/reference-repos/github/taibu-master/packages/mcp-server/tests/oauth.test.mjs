import test from 'node:test';
import assert from 'node:assert/strict';
import { resolve } from 'node:path';
import { pathToFileURL } from 'node:url';

const distRoot = resolve(process.cwd(), 'packages/mcp-server/dist');

function moduleUrl(relativePath) {
  const url = pathToFileURL(resolve(distRoot, relativePath));
  url.searchParams.set('t', `${Date.now()}-${Math.random()}`);
  return url.href;
}

async function importDist(relativePath) {
  return import(moduleUrl(relativePath));
}

async function withEnv(temp, fn) {
  const prev = new Map();
  for (const [key, value] of Object.entries(temp)) {
    prev.set(key, process.env[key]);
    if (value === undefined) {
      delete process.env[key];
    } else {
      process.env[key] = value;
    }
  }

  try {
    return await fn();
  } finally {
    for (const [key, value] of prev.entries()) {
      if (value === undefined) {
        delete process.env[key];
      } else {
        process.env[key] = value;
      }
    }
  }
}

test('verifyAccessToken should reject token when aud is outside allowed audiences', async () => {
  await withEnv(
    {
      MCP_JWT_SECRET: 'x'.repeat(32),
      MCP_ISSUER_URL: 'https://mcp.mingai.fun',
      MCP_ALLOWED_TOKEN_AUDIENCES: 'https://mcp.mingai.fun/mcp,https://mcp.mingai.fun',
    },
    async () => {
      const { signAccessToken, verifyAccessToken } = await importDist('oauth/jwt.js');
      const { token } = await signAccessToken(
        'user-1',
        'client-1',
        'mcp:tools',
        'https://evil.example.com/mcp'
      );

      await assert.rejects(
        () => verifyAccessToken(token),
        /Invalid access token/
      );
    }
  );
});

test('verifyAccessToken should accept token with configured audience', async () => {
  await withEnv(
    {
      MCP_JWT_SECRET: 'y'.repeat(32),
      MCP_ISSUER_URL: 'https://mcp.mingai.fun',
      MCP_ALLOWED_TOKEN_AUDIENCES: 'https://mcp.mingai.fun/mcp',
    },
    async () => {
      const { signAccessToken, verifyAccessToken } = await importDist('oauth/jwt.js');
      const { token } = await signAccessToken(
        'user-2',
        'client-2',
        'mcp:tools',
        'https://mcp.mingai.fun/mcp'
      );

      const auth = await verifyAccessToken(token);
      assert.equal(auth.clientId, 'client-2');
      assert.deepEqual(auth.scopes, ['mcp:tools']);
      assert.equal(auth.extra?.userId, 'user-2');
    }
  );
});

test('getAllowedTokenAudiences should keep /mcp resource compatibility when env only contains issuer', async () => {
  await withEnv(
    {
      MCP_ISSUER_URL: 'https://mcp.mingai.fun',
      MCP_ALLOWED_TOKEN_AUDIENCES: 'https://mcp.mingai.fun',
    },
    async () => {
      const { getAllowedTokenAudiences } = await importDist('oauth/jwt.js');
      const { validateOAuthLoginRequest } = await importDist('oauth/login-validation.js');

      const audiences = getAllowedTokenAudiences(new URL('https://mcp.mingai.fun'));
      assert.ok(
        audiences.includes('https://mcp.mingai.fun/mcp'),
        'audience list should include issuer/mcp for resourceServerUrl compatibility'
      );

      const result = validateOAuthLoginRequest({
        client: {
          client_id: 'client-1',
          redirect_uris: ['https://chat.openai.com/aip/mcp/callback'],
          scope: 'mcp:tools',
        },
        redirectUri: 'https://chat.openai.com/aip/mcp/callback',
        scope: 'mcp:tools',
        resource: 'https://mcp.mingai.fun/mcp',
        issuerUrl: new URL('https://mcp.mingai.fun'),
        allowedAudiences: audiences,
      });

      assert.equal(result.ok, true);
      assert.equal(result.value.resource, 'https://mcp.mingai.fun/mcp');
    }
  );
});

test('validateOAuthLoginRequest should reject tampered redirect_uri/scope/resource', async () => {
  const { validateOAuthLoginRequest } = await importDist('oauth/login-validation.js');

  const client = {
    client_id: 'client-1',
    redirect_uris: ['https://chat.openai.com/aip/mcp/callback'],
    scope: 'mcp:tools',
  };

  const badRedirect = validateOAuthLoginRequest({
    client,
    redirectUri: 'https://evil.example.com/callback',
    scope: 'mcp:tools',
    resource: 'https://mcp.mingai.fun/mcp',
    issuerUrl: new URL('https://mcp.mingai.fun'),
    allowedAudiences: ['https://mcp.mingai.fun/mcp'],
  });
  assert.equal(badRedirect.ok, false);
  assert.equal(badRedirect.error, 'Invalid redirect_uri');

  const badScope = validateOAuthLoginRequest({
    client,
    redirectUri: 'https://chat.openai.com/aip/mcp/callback',
    scope: 'mcp:tools admin:all',
    resource: 'https://mcp.mingai.fun/mcp',
    issuerUrl: new URL('https://mcp.mingai.fun'),
    allowedAudiences: ['https://mcp.mingai.fun/mcp'],
  });
  assert.equal(badScope.ok, false);
  assert.equal(badScope.error, 'Invalid scope');

  const badResource = validateOAuthLoginRequest({
    client,
    redirectUri: 'https://chat.openai.com/aip/mcp/callback',
    scope: 'mcp:tools',
    resource: 'https://evil.example.com/mcp',
    issuerUrl: new URL('https://mcp.mingai.fun'),
    allowedAudiences: ['https://mcp.mingai.fun/mcp'],
  });
  assert.equal(badResource.ok, false);
  assert.equal(badResource.error, 'Invalid resource');
});

test('validateOAuthLoginRequest should normalize and accept valid OAuth login params', async () => {
  const { validateOAuthLoginRequest } = await importDist('oauth/login-validation.js');

  const result = validateOAuthLoginRequest({
    client: {
      client_id: 'client-1',
      redirect_uris: [
        'https://chat.openai.com/aip/mcp/callback',
        'https://chat.openai.com/aip/mcp/callback/'
      ],
      scope: 'mcp:tools',
    },
    redirectUri: 'https://chat.openai.com/aip/mcp/callback',
    scope: 'mcp:tools',
    resource: 'https://mcp.mingai.fun/mcp',
    issuerUrl: new URL('https://mcp.mingai.fun'),
    allowedAudiences: ['https://mcp.mingai.fun/mcp'],
  });

  assert.equal(result.ok, true);
  assert.equal(result.value.redirectUri, 'https://chat.openai.com/aip/mcp/callback');
  assert.equal(result.value.scope, 'mcp:tools');
  assert.equal(result.value.resource, 'https://mcp.mingai.fun/mcp');
  assert.deepEqual(result.value.scopes, ['mcp:tools']);
});

test('validateOAuthLoginRequest should fallback to issuer audience when allowedAudiences is empty', async () => {
  const { validateOAuthLoginRequest } = await importDist('oauth/login-validation.js');

  const ok = validateOAuthLoginRequest({
    client: {
      client_id: 'client-1',
      redirect_uris: ['https://chat.openai.com/aip/mcp/callback'],
      scope: 'mcp:tools',
    },
    redirectUri: 'https://chat.openai.com/aip/mcp/callback',
    scope: 'mcp:tools',
    resource: 'https://mcp.mingai.fun',
    issuerUrl: new URL('https://mcp.mingai.fun'),
    allowedAudiences: [],
  });

  assert.equal(ok.ok, true);
  assert.equal(ok.value.resource, 'https://mcp.mingai.fun/');

  const bad = validateOAuthLoginRequest({
    client: {
      client_id: 'client-1',
      redirect_uris: ['https://chat.openai.com/aip/mcp/callback'],
      scope: 'mcp:tools',
    },
    redirectUri: 'https://chat.openai.com/aip/mcp/callback',
    scope: 'mcp:tools',
    resource: 'https://evil.example.com/mcp',
    issuerUrl: new URL('https://mcp.mingai.fun'),
    allowedAudiences: [],
  });
  assert.equal(bad.ok, false);
  assert.equal(bad.error, 'Invalid resource');
});

test('getAuthorizationCode should query unused code and map row', async () => {
  const { getAuthorizationCode } = await importDist('oauth/store.js');
  const calls = [];

  const chain = {
    eq(field, value) {
      calls.push(['eq', field, value]);
      return chain;
    },
    gt(field, value) {
      calls.push(['gt', field, value]);
      return chain;
    },
    select(columns) {
      calls.push(['select', columns]);
      return chain;
    },
    async maybeSingle() {
      return {
        data: {
          code: 'code-1',
          client_id: 'client-1',
          user_id: 'user-1',
          redirect_uri: 'https://chat.openai.com/aip/mcp/callback',
          code_challenge: 'challenge-1',
          code_challenge_method: 'S256',
          scope: 'mcp:tools',
          resource: 'https://mcp.mingai.fun/mcp',
          expires_at: new Date(Date.now() + 60000).toISOString(),
        },
        error: null,
      };
    },
  };

  const supabase = {
    from(table) {
      calls.push(['from', table]);
      return {
        select(columns) {
          calls.push(['select', columns]);
          return chain;
        },
      };
    },
  };

  const result = await getAuthorizationCode('code-1', supabase);

  assert.equal(result?.code, 'code-1');
  assert.equal(result?.clientId, 'client-1');
  assert.deepEqual(calls[0], ['from', 'mcp_oauth_codes']);
  assert.deepEqual(calls[1], ['select', '*']);
  assert.ok(calls.some((call) => call[0] === 'eq' && call[1] === 'used' && call[2] === false));
  assert.ok(calls.some((call) => call[0] === 'gt' && call[1] === 'expires_at'));
});

test('getAuthorizationCode should return null when no row is found', async () => {
  const { getAuthorizationCode } = await importDist('oauth/store.js');

  const chain = {
    eq() {
      return chain;
    },
    gt() {
      return chain;
    },
    select() {
      return chain;
    },
    async maybeSingle() {
      return { data: null, error: null };
    },
  };

  const supabase = {
    from() {
      return {
        select() {
          return chain;
        },
      };
    },
  };

  const result = await getAuthorizationCode('not-found', supabase);
  assert.equal(result, null);
});

test('exchangeAuthorizationCodeTransactionally should call rpc with refresh token expiry', async () => {
  const { exchangeAuthorizationCodeTransactionally } = await importDist('oauth/store.js');
  const calls = [];
  const supabase = {
    rpc(fn, args) {
      calls.push([fn, args]);
      return Promise.resolve({ data: { status: 'ok' }, error: null });
    },
  };

  const status = await exchangeAuthorizationCodeTransactionally({
    authorizationCode: 'code-1',
    refreshToken: 'refresh-1',
  }, supabase);

  assert.equal(status, 'ok');
  assert.equal(calls.length, 1);
  assert.equal(calls[0][0], 'mcp_exchange_authorization_code');
  assert.equal(calls[0][1].p_code, 'code-1');
  assert.equal(calls[0][1].p_refresh_token, 'refresh-1');
  assert.equal(typeof calls[0][1].p_expires_at, 'string');
});

test('rotateRefreshTokenTransactionally should call rpc with scope/resource', async () => {
  const { rotateRefreshTokenTransactionally } = await importDist('oauth/store.js');
  const calls = [];
  const supabase = {
    rpc(fn, args) {
      calls.push([fn, args]);
      return Promise.resolve({ data: { status: 'ok' }, error: null });
    },
  };

  const status = await rotateRefreshTokenTransactionally({
    refreshToken: 'refresh-1',
    newRefreshToken: 'refresh-2',
    scope: 'mcp:tools',
    resource: 'https://mcp.mingai.fun/mcp',
  }, supabase);

  assert.equal(status, 'ok');
  assert.equal(calls.length, 1);
  assert.equal(calls[0][0], 'mcp_rotate_refresh_token');
  assert.equal(calls[0][1].p_refresh_token, 'refresh-1');
  assert.equal(calls[0][1].p_new_refresh_token, 'refresh-2');
  assert.equal(calls[0][1].p_scope, 'mcp:tools');
  assert.equal(calls[0][1].p_resource, 'https://mcp.mingai.fun/mcp');
  assert.equal(typeof calls[0][1].p_expires_at, 'string');
});

test('exchangeAuthorizationCode should reject mismatched resource binding', async () => {
  const { TaiBuOAuthProvider } = await importDist('oauth/provider.js');
  let signCalls = 0;
  let exchangeCalls = 0;

  const provider = new TaiBuOAuthProvider({
    getAuthorizationCode: async () => ({
      code: 'code-1',
      clientId: 'client-1',
      userId: 'user-1',
      redirectUri: 'https://chat.openai.com/aip/mcp/callback',
      codeChallenge: 'challenge',
      codeChallengeMethod: 'S256',
      scope: 'mcp:tools',
      resource: 'https://mcp.mingai.fun/mcp',
      expiresAt: new Date(Date.now() + 10000),
    }),
    signAccessToken: async () => {
      signCalls += 1;
      return { token: 'access-token', expiresIn: 3600 };
    },
    generateRefreshToken: () => 'refresh-token',
    exchangeAuthorizationCodeTransactionally: async () => {
      exchangeCalls += 1;
      return 'ok';
    },
  });

  await assert.rejects(
    () => provider.exchangeAuthorizationCode(
      { client_id: 'client-1' },
      'code-1',
      undefined,
      'https://chat.openai.com/aip/mcp/callback',
      new URL('https://evil.example.com/mcp')
    ),
    /Authorization code resource mismatch/
  );
  assert.equal(signCalls, 0);
  assert.equal(exchangeCalls, 0);
});

test('exchangeAuthorizationCode should persist through transactional exchange', async () => {
  const { TaiBuOAuthProvider } = await importDist('oauth/provider.js');
  const steps = [];
  let savedRefreshToken;

  const provider = new TaiBuOAuthProvider({
    getAuthorizationCode: async () => ({
      code: 'code-1',
      clientId: 'client-1',
      userId: 'user-1',
      redirectUri: 'https://chat.openai.com/aip/mcp/callback',
      codeChallenge: 'challenge',
      codeChallengeMethod: 'S256',
      scope: 'mcp:tools',
      resource: 'https://mcp.mingai.fun/mcp',
      expiresAt: new Date(Date.now() + 10000),
    }),
    signAccessToken: async () => {
      steps.push('sign');
      return { token: 'access-token', expiresIn: 3600 };
    },
    generateRefreshToken: () => 'refresh-token',
    exchangeAuthorizationCodeTransactionally: async ({ refreshToken }) => {
      steps.push('persist');
      savedRefreshToken = refreshToken;
      return 'ok';
    },
  });

  const result = await provider.exchangeAuthorizationCode(
    { client_id: 'client-1' },
    'code-1',
    undefined,
    'https://chat.openai.com/aip/mcp/callback',
    new URL('https://mcp.mingai.fun/mcp')
  );

  assert.deepEqual(steps, ['sign', 'persist']);
  assert.equal(savedRefreshToken, 'refresh-token');
  assert.equal(result.access_token, 'access-token');
  assert.equal(result.refresh_token, 'refresh-token');
});

test('exchangeAuthorizationCode should fail when transactional exchange loses the race', async () => {
  const { TaiBuOAuthProvider } = await importDist('oauth/provider.js');

  const provider = new TaiBuOAuthProvider({
    getAuthorizationCode: async () => ({
      code: 'code-1',
      clientId: 'client-1',
      userId: 'user-1',
      redirectUri: 'https://chat.openai.com/aip/mcp/callback',
      codeChallenge: 'challenge',
      codeChallengeMethod: 'S256',
      scope: 'mcp:tools',
      resource: 'https://mcp.mingai.fun/mcp',
      expiresAt: new Date(Date.now() + 10000),
    }),
    signAccessToken: async () => ({ token: 'access-token', expiresIn: 3600 }),
    generateRefreshToken: () => 'refresh-token',
    exchangeAuthorizationCodeTransactionally: async () => 'invalid_code',
  });

  await assert.rejects(
    () => provider.exchangeAuthorizationCode(
      { client_id: 'client-1' },
      'code-1',
      undefined,
      'https://chat.openai.com/aip/mcp/callback',
      new URL('https://mcp.mingai.fun/mcp')
    ),
    /Invalid or expired authorization code/
  );
});

test('exchangeRefreshToken should reject mismatched resource binding', async () => {
  const { TaiBuOAuthProvider } = await importDist('oauth/provider.js');
  let signCalls = 0;
  let rotationCalls = 0;

  const provider = new TaiBuOAuthProvider({
    getActiveRefreshToken: async () => ({
      userId: 'user-1',
      clientId: 'client-1',
      scope: 'mcp:tools',
      resource: 'https://mcp.mingai.fun/mcp',
    }),
    signAccessToken: async () => {
      signCalls += 1;
      return { token: 'access-token', expiresIn: 3600 };
    },
    generateRefreshToken: () => 'new-refresh-token',
    rotateRefreshTokenTransactionally: async () => {
      rotationCalls += 1;
      return 'ok';
    },
  });

  await assert.rejects(
    () => provider.exchangeRefreshToken(
      { client_id: 'client-1' },
      'refresh-token',
      ['mcp:tools'],
      new URL('https://evil.example.com/mcp')
    ),
    /Refresh token resource mismatch/
  );
  assert.equal(signCalls, 0);
  assert.equal(rotationCalls, 0, 'should not rotate token before resource validation');
});

test('exchangeRefreshToken should reject scope escalation and keep token active', async () => {
  const { TaiBuOAuthProvider } = await importDist('oauth/provider.js');
  let signCalls = 0;
  let rotationCalls = 0;

  const provider = new TaiBuOAuthProvider({
    getActiveRefreshToken: async () => ({
      userId: 'user-1',
      clientId: 'client-1',
      scope: 'mcp:tools',
      resource: 'https://mcp.mingai.fun/mcp',
    }),
    signAccessToken: async () => {
      signCalls += 1;
      return { token: 'access-token', expiresIn: 3600 };
    },
    generateRefreshToken: () => 'new-refresh-token',
    rotateRefreshTokenTransactionally: async () => {
      rotationCalls += 1;
      return 'ok';
    },
  });

  await assert.rejects(
    () => provider.exchangeRefreshToken(
      { client_id: 'client-1' },
      'refresh-token',
      ['mcp:tools', 'admin:all'],
      new URL('https://mcp.mingai.fun/mcp')
    ),
    /Refresh token scope escalation not allowed/
  );

  assert.equal(signCalls, 0);
  assert.equal(rotationCalls, 0, 'should not rotate token when scope validation fails');
});

test('exchangeRefreshToken should default scope to mcp:tools when stored scope is empty', async () => {
  const { TaiBuOAuthProvider } = await importDist('oauth/provider.js');
  let rotated = 0;
  let signedScope;
  let signedResource;
  let rotatedScope;
  let rotatedResource;

  const provider = new TaiBuOAuthProvider({
    getActiveRefreshToken: async () => ({
      userId: 'user-1',
      clientId: 'client-1',
      scope: null,
      resource: 'https://mcp.mingai.fun/mcp',
    }),
    signAccessToken: async (_userId, _clientId, scope, resource) => {
      signedScope = scope;
      signedResource = resource;
      return { token: 'access-token', expiresIn: 3600 };
    },
    generateRefreshToken: () => 'rotated-refresh-token',
    rotateRefreshTokenTransactionally: async (params) => {
      rotated += 1;
      rotatedScope = params.scope;
      rotatedResource = params.resource;
      return 'ok';
    },
  });

  const result = await provider.exchangeRefreshToken(
    { client_id: 'client-1' },
    'refresh-token',
    undefined,
    undefined,
  );

  assert.equal(result.scope, 'mcp:tools');
  assert.equal(signedScope, 'mcp:tools');
  assert.equal(rotatedScope, 'mcp:tools');
  assert.equal(signedResource, 'https://mcp.mingai.fun/mcp');
  assert.equal(rotatedResource, 'https://mcp.mingai.fun/mcp');
  assert.equal(rotated, 1);
});

test('exchangeRefreshToken should fail when transactional rotation loses the race', async () => {
  const { TaiBuOAuthProvider } = await importDist('oauth/provider.js');

  const provider = new TaiBuOAuthProvider({
    getActiveRefreshToken: async () => ({
      userId: 'user-1',
      clientId: 'client-1',
      scope: 'mcp:tools',
      resource: 'https://mcp.mingai.fun/mcp',
    }),
    signAccessToken: async () => ({ token: 'access-token', expiresIn: 3600 }),
    generateRefreshToken: () => 'rotated-refresh-token',
    rotateRefreshTokenTransactionally: async () => 'invalid_refresh_token',
  });

  await assert.rejects(
    () => provider.exchangeRefreshToken(
      { client_id: 'client-1' },
      'refresh-token',
      ['mcp:tools'],
      new URL('https://mcp.mingai.fun/mcp')
    ),
    /Invalid or expired refresh token/
  );
});

test('getActiveRefreshToken should return stored resource binding', async () => {
  const { getActiveRefreshToken } = await importDist('oauth/store.js');
  const supabase = {
    from() {
      return {
        select() {
          return {
            eq() { return this; },
            gt() { return this; },
            maybeSingle: async () => ({
              data: {
                user_id: 'user-1',
                client_id: 'client-1',
                scope: 'mcp:tools',
                resource: 'https://mcp.mingai.fun/mcp',
              },
              error: null,
            }),
          };
        },
      };
    },
  };

  const active = await getActiveRefreshToken('refresh-token', supabase);
  assert.equal(active?.resource, 'https://mcp.mingai.fun/mcp');
});

test('cleanupOAuthArtifactsTransactionally should call cleanup rpc with current timestamp', async () => {
  const { cleanupOAuthArtifactsTransactionally } = await importDist('oauth/store.js');
  const calls = [];
  const supabase = {
    rpc(fn, args) {
      calls.push([fn, args]);
      return Promise.resolve({
        data: {
          status: 'ok',
          deleted_codes: 1,
          deleted_tokens: 2,
          deleted_clients: 3,
          orphan_clients: 3,
          total_clients: 5,
        },
        error: null,
      });
    },
  };

  const result = await cleanupOAuthArtifactsTransactionally('2026-04-09T12:00:00.000Z', supabase);

  assert.equal(calls.length, 1);
  assert.equal(calls[0][0], 'mcp_cleanup_oauth_artifacts');
  assert.deepEqual(calls[0][1], {
    p_now: '2026-04-09T12:00:00.000Z',
  });
  assert.deepEqual(result, {
    deleted_codes: 1,
    deleted_tokens: 2,
    deleted_clients: 3,
    orphan_clients: 3,
    total_clients: 5,
  });
});
