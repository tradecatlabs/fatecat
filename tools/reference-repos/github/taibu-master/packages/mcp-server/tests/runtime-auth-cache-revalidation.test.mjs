import test from 'node:test';
import assert from 'node:assert/strict';
import { createServer } from 'node:http';
import { spawn } from 'node:child_process';
import { resolve } from 'node:path';

function wait(ms) {
  return new Promise((resolveWait) => {
    setTimeout(resolveWait, ms);
  });
}

async function getFreePort() {
  const server = createServer();
  await new Promise((resolveListen, rejectListen) => {
    server.listen(0, '127.0.0.1', (error) => {
      if (error) rejectListen(error);
      else resolveListen();
    });
  });
  const address = server.address();
  if (!address || typeof address === 'string') {
    await new Promise((resolveClose) => server.close(() => resolveClose()));
    throw new Error('Failed to allocate free port');
  }
  const port = address.port;
  await new Promise((resolveClose) => server.close(() => resolveClose()));
  return port;
}

async function waitForHealth(port, childProcess) {
  const startedAt = Date.now();
  const timeoutMs = 10_000;

  while (Date.now() - startedAt < timeoutMs) {
    if (childProcess.exitCode !== null) {
      throw new Error(`MCP server exited early with code ${childProcess.exitCode}`);
    }

    try {
      const response = await fetch(`http://127.0.0.1:${port}/health`);
      if (response.ok) return;
    } catch {
      // Server not ready yet.
    }

    await wait(100);
  }

  throw new Error('Timed out waiting for MCP server health endpoint');
}

async function closeServer(server) {
  await new Promise((resolveClose) => server.close(() => resolveClose()));
}

async function stopProcess(childProcess) {
  if (childProcess.exitCode !== null) return;
  childProcess.kill('SIGTERM');
  await Promise.race([
    new Promise((resolveExit) => childProcess.once('exit', () => resolveExit(undefined))),
    wait(3_000),
  ]);
  if (childProcess.exitCode === null) {
    childProcess.kill('SIGKILL');
    await new Promise((resolveExit) => childProcess.once('exit', () => resolveExit(undefined)));
  }
}

test('dist auth middleware should revalidate cached key and reject revoked key after background check', async () => {
  let verifyCalls = 0;

  const fakeSupabase = createServer(async (req, res) => {
    const requestUrl = req.url || '';

    // Consume request stream to keep server behavior deterministic.
    for await (const chunk of req) {
      void chunk;
    }

    res.setHeader('Content-Type', 'application/json');

    if (req.method === 'POST' && requestUrl.startsWith('/rest/v1/rpc/mcp_verify_api_key')) {
      verifyCalls += 1;
      if (verifyCalls === 1) {
        res.writeHead(200);
        res.end(JSON.stringify([{ key_id: 'key-1', user_id: 'user-1' }]));
        return;
      }
      res.writeHead(200);
      res.end(JSON.stringify([]));
      return;
    }

    if (req.method === 'POST' && requestUrl.startsWith('/rest/v1/rpc/mcp_touch_key_last_used')) {
      res.writeHead(200);
      res.end(JSON.stringify(null));
      return;
    }

    if (req.method === 'POST' && requestUrl.startsWith('/auth/v1/token')) {
      res.writeHead(200);
      res.end(JSON.stringify({
        access_token: 'system-admin-access-token',
        token_type: 'bearer',
        expires_in: 3600,
        refresh_token: 'system-admin-refresh-token',
        user: { id: 'system-admin-user' },
        expires_at: Math.floor(Date.now() / 1000) + 3600,
      }));
      return;
    }

    res.writeHead(404);
    res.end(JSON.stringify({ error: 'not found' }));
  });

  const supabasePort = await getFreePort();
  await new Promise((resolveListen, rejectListen) => {
    fakeSupabase.listen(supabasePort, '127.0.0.1', (error) => {
      if (error) rejectListen(error);
      else resolveListen();
    });
  });

  const mcpPort = await getFreePort();
  const mcpCwd = resolve(process.cwd(), 'packages/mcp-server');
  const mcpProcess = spawn(process.execPath, ['dist/index.js'], {
    cwd: mcpCwd,
    env: {
      ...process.env,
      NODE_OPTIONS: '',
      NODE_ENV: 'test',
      PORT: String(mcpPort),
      MCP_HOST: '127.0.0.1',
      SUPABASE_URL: `http://127.0.0.1:${supabasePort}`,
      SUPABASE_ANON_KEY: 'test-anon-key',
      SUPABASE_SYSTEM_ADMIN_EMAIL: 'admin@example.com',
      SUPABASE_SYSTEM_ADMIN_PASSWORD: 'admin-password',
      MCP_ALLOWED_HOSTS: `127.0.0.1:${mcpPort}`,
    },
    stdio: ['ignore', 'ignore', 'pipe'],
  });

  let stderr = '';
  mcpProcess.stderr.on('data', (chunk) => {
    stderr += chunk.toString();
  });

  try {
    await waitForHealth(mcpPort, mcpProcess);

    const requestUrl = `http://127.0.0.1:${mcpPort}/mcp`;
    const headers = {
      'x-api-key': 'sk-mcp-taibu-test-key',
      'content-type': 'application/json',
      accept: 'application/json, text/event-stream',
    };

    const firstResponse = await fetch(requestUrl, {
      method: 'POST',
      headers,
      body: '{}',
    });

    assert.equal(
      firstResponse.status,
      400,
      'first request should pass auth and fail later with initialize validation error'
    );

    // Stale-while-revalidate: 第二次请求信任缓存立即放行，
    // 后台异步回源发现 key 已撤销并失效缓存。
    const secondResponse = await fetch(requestUrl, {
      method: 'POST',
      headers,
      body: '{}',
    });

    assert.equal(
      secondResponse.status,
      400,
      'second request should still pass auth (stale-while-revalidate fast path)'
    );

    // 等待后台异步回源完成并失效缓存
    await wait(500);

    const thirdResponse = await fetch(requestUrl, {
      method: 'POST',
      headers,
      body: '{}',
    });

    assert.equal(
      thirdResponse.status,
      401,
      `third request should be rejected after background revalidation invalidated cache; stderr: ${stderr}`
    );
    assert.ok(verifyCalls >= 2, 'cached key path should trigger background revalidation via RPC');
  } finally {
    await stopProcess(mcpProcess);
    await closeServer(fakeSupabase);
  }
});
