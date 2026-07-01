import { test } from 'node:test';
import assert from 'node:assert/strict';
import { createPost, getPostDetail, getPosts } from '../lib/community';

type MockResponseInit = {
  ok: boolean;
  status: number;
  statusText?: string;
  body: unknown;
};

function createMockResponse(init: MockResponseInit): Response {
  return {
    ok: init.ok,
    status: init.status,
    statusText: init.statusText ?? '',
    json: async () => init.body,
  } as Response;
}

test('community client reads post list through browser api payload normalization', async (t) => {
  const originalFetch = global.fetch;
  global.fetch = (async () => createMockResponse({
    ok: true,
    status: 200,
    body: {
      posts: [{
        id: 'post-1',
        author_name: '命理爱好者',
        author_avatar_url: null,
        title: '标题',
        content: '内容',
        category: 'general',
        tags: [],
        view_count: 0,
        upvote_count: 0,
        downvote_count: 0,
        comment_count: 0,
        is_pinned: false,
        is_featured: false,
        is_deleted: false,
        created_at: '2026-04-11T00:00:00.000Z',
        updated_at: '2026-04-11T00:00:00.000Z',
      }],
      total: 1,
    },
  })) as typeof fetch;

  t.after(() => {
    global.fetch = originalFetch;
  });

  const result = await getPosts({ sortBy: 'latest' }, 1, 10);
  assert.equal(result.total, 1);
  assert.equal(result.posts.length, 1);
  assert.equal(result.posts[0]?.id, 'post-1');
});

test('community client returns null for 404 post detail responses', async (t) => {
  const originalFetch = global.fetch;
  global.fetch = (async () => createMockResponse({
    ok: false,
    status: 404,
    statusText: 'Not Found',
    body: { error: '帖子不存在' },
  })) as typeof fetch;

  t.after(() => {
    global.fetch = originalFetch;
  });

  const result = await getPostDetail('missing-post');
  assert.equal(result, null);
});

test('community client surfaces browser api error messages for writes', async (t) => {
  const originalFetch = global.fetch;
  global.fetch = (async () => createMockResponse({
    ok: false,
    status: 401,
    statusText: 'Unauthorized',
    body: { error: '认证失败' },
  })) as typeof fetch;

  t.after(() => {
    global.fetch = originalFetch;
  });

  await assert.rejects(
    () => createPost({ title: '标题', content: '内容', category: 'general' }),
    /认证失败/,
  );
});
