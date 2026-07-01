import { test } from 'node:test';
import assert from 'node:assert/strict';

import { buildDraftTitle } from '../lib/chat/draft-title';

test('buildDraftTitle uses the first sentence from the first user question', () => {
  assert.equal(buildDraftTitle('帮我看一下事业运怎么样？另外也看看财运。'), '帮我看一下事业运怎么样');
  assert.equal(buildDraftTitle('  第一行问题\n第二行补充  '), '第一行问题');
  assert.equal(buildDraftTitle('Need help with my visa. Also review my plan.'), 'Need help with my visa');
  assert.equal(buildDraftTitle('帮我比较 GPT-4.1 和 Gemini 2.5 的区别'), '帮我比较 GPT-4.1 和 Gemini 2.5 的区别');
  assert.equal(buildDraftTitle('https://api.example.com/v1 这样写可以吗？我不确定。'), 'https://api.example.com/v1 这样写可以吗');
  assert.equal(buildDraftTitle('https://api.example.com/v1?foo=1 这样可以吗？我不确定。'), 'https://api.example.com/v1?foo=1 这样可以吗');
});

test('buildDraftTitle falls back to normalized text when there is no sentence boundary', () => {
  assert.equal(buildDraftTitle('   请帮我分析明年的整体发展   '), '请帮我分析明年的整体发展');
  assert.equal(buildDraftTitle(''), '新对话');
});
