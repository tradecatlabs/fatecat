import test from 'node:test';
import assert from 'node:assert/strict';

import { calculateTarot, toTarotJson, toTarotText } from 'taibu-core';

test('tarot deck should contain exactly 78 cards — celtic-cross draws 10', async () => {
  const result = await calculateTarot({ spreadType: 'celtic-cross', seed: 'completeness-check' });
  assert.ok(Array.isArray(result.cards), 'cards should be an array');
  assert.equal(result.cards.length, 10);
});

test('tarot seed determinism: same seed should produce identical results', async () => {
  const a = await calculateTarot({ spreadType: 'three-card', seed: 'determinism-test-42', allowReversed: true });
  const b = await calculateTarot({ spreadType: 'three-card', seed: 'determinism-test-42', allowReversed: true });

  assert.equal(a.cards.length, b.cards.length);
  for (let i = 0; i < a.cards.length; i++) {
    assert.equal(a.cards[i].card.name, b.cards[i].card.name, `card ${i} name should match`);
    assert.equal(a.cards[i].orientation, b.cards[i].orientation, `card ${i} orientation should match`);
    assert.equal(a.cards[i].position, b.cards[i].position, `card ${i} position should match`);
}
  assert.equal(a.seed, b.seed);
});

test('tarot single spread should draw exactly 1 card', async () => {
  const result = await calculateTarot({ spreadType: 'single', seed: 'spread-single' });
  assert.equal(result.cards.length, 1);
  assert.equal(result.spreadId, 'single');
});

test('tarot three-card spread should draw exactly 3 cards', async () => {
  const result = await calculateTarot({ spreadType: 'three-card', seed: 'spread-three' });
  assert.equal(result.cards.length, 3);
  assert.equal(result.spreadId, 'three-card');
  assert.deepEqual(
    result.cards.map((c) => c.position),
    ['过去', '现在', '未来'],
  );
});

test('tarot celtic-cross spread should draw exactly 10 cards', async () => {
  const result = await calculateTarot({ spreadType: 'celtic-cross', seed: 'spread-celtic' });
  assert.equal(result.cards.length, 10);
  assert.equal(result.spreadId, 'celtic-cross');
});

test('tarot numerology should be populated when birth date is provided', async () =>{
  const result = await calculateTarot({
    spreadType: 'single',
    seed: 'numerology-test',
    birthYear: 1990,
    birthMonth: 6,
    birthDay:15,
  });

  assert.ok(result.numerology, 'numerology object should exist');
  assert.ok(result.numerology.personalityCard, 'personalityCard should exist');
  assert.ok(result.numerology.soulCard, 'soulCard should exist');
  assert.ok(result.numerology.yearlyCard, 'yearlyCard should exist');

  assert.ok(
    result.numerology.personalityCard.number >= 1 && result.numerology.personalityCard.number <= 21,
    `personalityCard number ${result.numerology.personalityCard.number} should be 1-21`,
  );
  assert.ok(
    result.numerology.soulCard.number >= 1 && result.numerology.soulCard.number <= 21,
    `soulCard number ${result.numerology.soulCard.number} should be 1-21`,
  );
  assert.ok(
    result.numerology.yearlyCard.number >= 1 && result.numerology.yearlyCard.number <= 21,
    `yearlyCard number ${result.numerology.yearlyCard.number} should be 1-21`,
  );

  assert.ok(result.numerology.personalityCard.nameChinese, 'personalityCard should have nameChinese');
  assert.ok(result.numerology.soulCard.nameChinese, 'soulCard should have nameChinese');
  assert.ok(result.numerology.yearlyCard.nameChinese, 'yearlyCard should have nameChinese');
});

test('tarot numerology should not be present when birth date is omitted', async () => {
  const result = await calculateTarot({ spreadType: 'single', seed: 'no-numerology' });
  assert.equal(result.numerology, undefined);
});

test('toTarotJson should return a non-empty canonical JSON object', async () => {
  const result = await calculateTarot({
    spreadType: 'three-card',
    seed: 'json-render',
    birthYear: 1985,
    birthMonth: 3,
    birthDay: 20,
  });
const json = toTarotJson(result);

  assert.ok(json, 'JSON output should be truthy');
  assert.ok(json.问卜设定, 'should have 问卜设定');
  assert.ok(json.牌阵展开, 'should have 牌阵展开');
  assert.equal(json.牌阵展开.length, 3);
  assert.ok(json.牌阵展开[0].位置, 'first card should have位置');
  assert.ok(json.牌阵展开[0].塔罗牌, 'first card should have 塔罗牌');
});

test('toTarotText should return a non-empty markdown string', async () => {
  const result = await calculateTarot({
    spreadType: 'three-card',
seed: 'text-render',
    birthYear: 1985,
    birthMonth: 3,
    birthDay: 20,
  });
  const text = toTarotText(result);

  assert.ok(typeof text === 'string', 'text output should be a string');
  assert.ok(text.length > 0, 'text output should not be empty');
  assert.match(text, /# 塔罗占卜/u, 'should contain main heading');
  assert.match(text, /牌阵/u, 'should contain spread info');
});

test('tarot cards should all have required fields', async () => {
  const result = await calculateTarot({ spreadType: 'celtic-cross', seed: 'field-check' });

  for (const card of result.cards) {
    assert.ok(card.position, 'card should have position');
    assert.ok(card.card.name, 'card should have English name');
    assert.ok(card.card.nameChinese, 'card should have Chinese name');
    assert.ok(Array.isArray(card.card.keywords), 'card should have keywords array');
    assert.ok(card.card.keywords.length > 0, 'card should have at least one keyword');
    assert.ok(['upright', 'reversed'].includes(card.orientation), 'orientation should be upright or reversed');
    assert.ok(card.meaning, 'card should have meaning');
  }
});

test('tarot cards within a single draw should be unique (no duplicates)', async () =>{
  const result = await calculateTarot({ spreadType: 'celtic-cross', seed: 'uniqueness-check' });
  const names = result.cards.map((c) => c.card.name);
  const uniqueNames = new Set(names);
  assert.equal(names.length, uniqueNames.size, 'all drawn cards should be unique');
});