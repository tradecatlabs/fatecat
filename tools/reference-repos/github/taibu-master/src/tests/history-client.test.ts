import test from 'node:test';
import assert from 'node:assert/strict';

process.env.NEXT_PUBLIC_SUPABASE_URL = process.env.NEXT_PUBLIC_SUPABASE_URL || 'http://localhost';
process.env.NEXT_PUBLIC_SUPABASE_ANON_KEY = process.env.NEXT_PUBLIC_SUPABASE_ANON_KEY || 'test-anon';

test('loadHistorySummariesPage should throw when history summaries request fails', async (t) => {
  const originalFetch = global.fetch;
  const modulePath = require.resolve('../lib/history/client');

  global.fetch = (async () => new Response(JSON.stringify({
    error: '加载历史记录失败',
  }), {
    status: 500,
    headers: { 'Content-Type': 'application/json' },
  })) as typeof global.fetch;

  t.after(() => {
    global.fetch = originalFetch;
    delete require.cache[modulePath];
  });

  delete require.cache[modulePath];
  const { loadHistorySummariesPage } = require('../lib/history/client') as typeof import('../lib/history/client');

  await assert.rejects(
    () => loadHistorySummariesPage('mbti'),
    /加载历史记录失败/u,
  );
});

test('deleteHistorySummary should throw when delete request fails', async (t) => {
  const originalFetch = global.fetch;
  const modulePath = require.resolve('../lib/history/client');

  global.fetch = (async () => new Response(JSON.stringify({
    error: '删除历史记录失败',
  }), {
    status: 500,
    headers: { 'Content-Type': 'application/json' },
  })) as typeof global.fetch;

  t.after(() => {
    global.fetch = originalFetch;
    delete require.cache[modulePath];
  });

  delete require.cache[modulePath];
  const { deleteHistorySummary } = require('../lib/history/client') as typeof import('../lib/history/client');

  await assert.rejects(
    () => deleteHistorySummary('mbti', 'history-1'),
    /删除历史记录失败/u,
  );
});
