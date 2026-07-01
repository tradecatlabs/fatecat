import test from 'node:test';
import assert from 'node:assert/strict';
import crypto from 'node:crypto';
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

function createResponseRecorder() {
  const handlers = new Map();
  let statusCode = 200;
  let payload;

  return {
    status(code) {
      statusCode = code;
      return this;
    },
    json(body) {
      payload = body;
      return this;
    },
    on(event, handler) {
      handlers.set(event, handler);
      return this;
    },
    close() {
      const onClose = handlers.get('close');
      if (onClose) onClose();
    },
    get statusCode() {
      return statusCode;
    },
    get payload() {
      return payload;
    },
  };
}

test('dualAuthMiddleware should reject invalid bearer token without API key fallback', async () => {
  const { dualAuthMiddleware } = await importDist('middleware.js');

  const middleware = dualAuthMiddleware({
    async verifyAccessToken() {
      throw new Error('bad token');
    },
  });

  const req = {
    headers: {
      authorization: 'Bearer bad-token',
      'x-api-key': 'legacy-key',
    },
  };

  const res = createResponseRecorder();
  let nextCalled = false;
  await middleware(req, res, () => {
    nextCalled = true;
  });

  assert.equal(nextCalled, false);
  assert.equal(res.statusCode, 401);
  assert.deepEqual(res.payload, { error: 'Invalid or expired access token' });
});

test('dualAuthMiddleware should set user auth when bearer token is valid', async () => {
  const { dualAuthMiddleware } = await importDist('middleware.js');

  const middleware = dualAuthMiddleware({
    async verifyAccessToken() {
      return {
        token: 'token',
        clientId: 'client-1',
        scopes: ['mcp:tools'],
        extra: { userId: 'user-1' },
      };
    },
  });

  const req = {
    headers: {
      authorization: 'Bearer valid-token',
    },
  };

  const res = createResponseRecorder();
  let nextCalled = false;
  await middleware(req, res, () => {
    nextCalled = true;
  });

  assert.equal(nextCalled, true);
  assert.deepEqual(req.mcpAuth, { userId: 'user-1', keyId: 'oauth:client-1' });
});

test('dualAuthMiddleware should accept lowercase bearer scheme', async () => {
  const { dualAuthMiddleware } = await importDist('middleware.js');

  const middleware = dualAuthMiddleware({
    async verifyAccessToken() {
      return {
        token: 'token',
        clientId: 'client-1',
        scopes: ['mcp:tools'],
        extra: { userId: 'user-1' },
      };
    },
  });

  const req = {
    headers: {
      authorization: 'bearer valid-token',
    },
  };

  const res = createResponseRecorder();
  let nextCalled = false;
  await middleware(req, res, () => {
    nextCalled = true;
  });

  assert.equal(nextCalled, true);
  assert.deepEqual(req.mcpAuth, { userId: 'user-1', keyId: 'oauth:client-1' });
});

test('sseConnectionLimitMiddleware should block the 4th concurrent GET for one user', async () => {
  const { sseConnectionLimitMiddleware } = await importDist('middleware.js');

  const userId = `u-${crypto.randomUUID()}`;
  const openConnections = [];

  for (let i = 0; i < 3; i += 1) {
    const req = { method: 'GET', mcpAuth: { userId } };
    const res = createResponseRecorder();
    let nextCalled = false;
    sseConnectionLimitMiddleware(req, res, () => {
      nextCalled = true;
    });
    assert.equal(nextCalled, true);
    openConnections.push(res);
  }

  const blockedReq = { method: 'GET', mcpAuth: { userId } };
  const blockedRes = createResponseRecorder();
  let blockedNext = false;
  sseConnectionLimitMiddleware(blockedReq, blockedRes, () => {
    blockedNext = true;
  });

  assert.equal(blockedNext, false);
  assert.equal(blockedRes.statusCode, 429);
  assert.deepEqual(blockedRes.payload, { error: 'Too many SSE connections' });

  for (const connection of openConnections) {
    connection.close();
  }
});

test('sseConnectionLimitMiddleware should release slot when connection closes', async () => {
  const { sseConnectionLimitMiddleware } = await importDist('middleware.js');

  const userId = `u-${crypto.randomUUID()}`;
  const req = { method: 'GET', mcpAuth: { userId } };
  const res = createResponseRecorder();

  let nextCalled = false;
  sseConnectionLimitMiddleware(req, res, () => {
    nextCalled = true;
  });
  assert.equal(nextCalled, true);

  res.close();

  const req2 = { method: 'GET', mcpAuth: { userId } };
  const res2 = createResponseRecorder();
  let nextCalled2 = false;
  sseConnectionLimitMiddleware(req2, res2, () => {
    nextCalled2 = true;
  });

  assert.equal(nextCalled2, true);
  assert.equal(res2.statusCode, 200);
  res2.close();
});
