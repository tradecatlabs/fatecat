import test from 'node:test';
import assert from 'node:assert/strict';
import * as mcpCore from 'taibu-core';

test('tarot should be deterministic with identical seed', async () => {
  const seed = 'seed-tarot-1';
  const input = { spreadType: 'three-card', question: '感情', allowReversed: true, seed };

  const a = await mcpCore.calculateTarot(input);
  const b = await mcpCore.calculateTarot(input);

  assert.equal(a.seed, seed);
  assert.equal(b.seed, seed);
  assert.deepEqual(a.cards, b.cards);
});

test('almanac should return consistent results for same date', async () => {
  const input = { dayMaster: '甲', date: '2026-02-11' };

  const a = await mcpCore.calculateDailyAlmanac(input);
  const b = await mcpCore.calculateDailyAlmanac(input);

  assert.equal(a.date, b.date);
  assert.equal(a.dayInfo.ganZhi, b.dayInfo.ganZhi);
  assert.equal(a.seed, undefined);
  assert.equal(a.scores, undefined);
  assert.equal(a.advice, undefined);
  assert.equal(a.luckyColor, undefined);
  assert.equal(a.luckyDirection, undefined);
});

test('liuyao(auto) should be deterministic with identical seed', async () => {
  const seed = 'seed-liuyao-1';
  const input = {
    question: '这周项目顺利吗',
    yongShenTargets: ['官鬼'],
    method: 'auto',
    date: '2026-02-11T09:00:00',
    seed,
  };

  const a = await mcpCore.calculateLiuyao(input);
  const b = await mcpCore.calculateLiuyao(input);

  assert.equal(a.seed, seed);
  assert.equal(b.seed, seed);
  assert.equal(a.hexagramName, b.hexagramName);
  assert.deepEqual(a.changedLines, b.changedLines);
});

test('same seed should be stable within scope and different across scopes', async () => {
  const base = {
    spreadType: 'single',
    question: '同一问题',
    allowReversed: true,
    seed: 'seed-shared-1',
  };

  const userA1 = await mcpCore.calculateTarot({ ...base, seedScope: 'user-a' });
  const userA2 = await mcpCore.calculateTarot({ ...base, seedScope: 'user-a' });
  const userB = await mcpCore.calculateTarot({ ...base, seedScope: 'user-b' });

  assert.equal(userA1.seed, userA2.seed);
  assert.deepEqual(userA1.cards, userA2.cards);
  assert.notEqual(userA1.seed, userB.seed);
});
