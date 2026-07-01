import test from 'node:test';
import assert from 'node:assert/strict';

import {
  calculateZiweiFlyingStar,
  toZiweiFlyingStarJson,
  toZiweiFlyingStarText,
} from 'taibu-core';

const BASE_BIRTH = {
  gender: 'male',
  birthYear: 1990,
  birthMonth: 6,
  birthDay: 15,
  birthHour: 10,
  calendarType: 'solar',
};

test('calculateZiweiFlyingStar should return results array for mutagedPlaces query', async () => {
  const result = await calculateZiweiFlyingStar({
    ...BASE_BIRTH,
    queries: [
      { type: 'mutagedPlaces', palace: '命宫' },
    ],
  });

  assert.ok(Array.isArray(result.results), 'results should be an array');
  assert.equal(result.results.length, 1, 'should have exactly 1 result for 1 query');

  const first = result.results[0];
  assert.equal(first.queryIndex, 0, 'queryIndex should be 0');
  assert.equal(first.type, 'mutagedPlaces', 'type should be mutagedPlaces');
  assert.ok(Array.isArray(first.result), 'mutagedPlaces result should be an array');
  assert.equal(first.result.length, 4, 'mutagedPlaces should return 4 entries (禄权科忌)');

  for (const place of first.result) {
    assert.ok(typeof place.mutagen === 'string', 'each place should have mutagen');
    assert.ok(place.targetPalace === null || typeof place.targetPalace === 'string', 'targetPalace should be null or string');
  }
});

test('calculateZiweiFlyingStar should handle fliesTo query', async () => {
  const result = await calculateZiweiFlyingStar({
    ...BASE_BIRTH,
    queries: [
      { type: 'fliesTo', from: '命宫', to: '财帛', mutagens: ['禄'] },
    ],
  });

  assert.equal(result.results.length, 1);
  const first = result.results[0];
  assert.equal(first.type, 'fliesTo');
  assert.equal(typeof first.result, 'boolean', 'fliesTo result should be boolean');
  assert.ok(first.sourcePalaceGanZhi, 'should include sourcePalaceGanZhi');
assert.ok(Array.isArray(first.actualFlights), 'should include actualFlights');
});

test('calculateZiweiFlyingStar should handle selfMutaged query', async () => {
  const result = await calculateZiweiFlyingStar({
    ...BASE_BIRTH,
    queries: [
      { type: 'selfMutaged', palace: '命宫', mutagens: ['禄', '忌'] },
    ],
  });

  assert.equal(result.results.length, 1);
  const first = result.results[0];
  assert.equal(first.type, 'selfMutaged');
  assert.equal(typeof first.result, 'boolean', 'selfMutaged result should be boolean');
});

test('calculateZiweiFlyingStar should handle surroundedPalaces query', async () => {
  const result = await calculateZiweiFlyingStar({
    ...BASE_BIRTH,
    queries: [
      { type: 'surroundedPalaces', palace: '命宫' },
    ],
  });

  assert.equal(result.results.length, 1);
  const first = result.results[0];
  assert.equal(first.type, 'surroundedPalaces');

  const surrounded = first.result;
  assert.ok(surrounded.target && typeof surrounded.target.name === 'string', 'should have target palace');
  assert.ok(surrounded.opposite && typeof surrounded.opposite.name === 'string', 'should have opposite palace');
  assert.ok(surrounded.wealth && typeof surrounded.wealth.name === 'string', 'should have wealth palace');
  assert.ok(surrounded.career && typeof surrounded.career.name === 'string', 'should have career palace');
});

test('calculateZiweiFlyingStar should process multiple queries in a single call', async () => {
const result = await calculateZiweiFlyingStar({
    ...BASE_BIRTH,
    queries: [
      { type: 'mutagedPlaces', palace: '命宫' },
      { type: 'fliesTo', from: '命宫', to: '夫妻', mutagens: ['忌'] },
      { type: 'surroundedPalaces', palace: '财帛' },
    ],
  });

  assert.equal(result.results.length, 3, 'should return 3 results for 3 queries');
  assert.equal(result.results[0].queryIndex, 0);
  assert.equal(result.results[1].queryIndex, 1);
  assert.equal(result.results[2].queryIndex, 2);
});

test('calculateZiweiFlyingStar should reject empty queries array', async () => {
  await assert.rejects(
    () => calculateZiweiFlyingStar({ ...BASE_BIRTH, queries: [] }),
    /queries.*空/u,
  );
});

test('toZiweiFlyingStarJson should return well-formed canonical JSON', async () => {
  const result = await calculateZiweiFlyingStar({
    ...BASE_BIRTH,
    queries: [
      { type: 'mutagedPlaces', palace: '命宫' },
],
  });
  const json = toZiweiFlyingStarJson(result);

  assert.ok(Array.isArray(json.查询结果), '查询结果 should be an array');
  assert.equal(json.查询结果.length, 1);

  const entry = json.查询结果[0];
  assert.ok(typeof entry.查询序号 === 'number', '查询序号 should be a number');
  assert.ok(typeof entry.查询类型 === 'string', '查询类型 should be a string');
  assert.ok(Array.isArray(entry.四化落宫), '四化落宫 should be an array for mutagedPlaces');
});

test('toZiweiFlyingStarText should return a non-empty markdown string', async () => {
  const result = await calculateZiweiFlyingStar({
    ...BASE_BIRTH,
    queries: [
      { type: 'mutagedPlaces', palace: '命宫' },
    ],
  });
  const text = toZiweiFlyingStarText(result);

  assert.ok(typeof text === 'string', 'text output should be a string');
  assert.ok(text.length > 20, 'text output should be substantial');
  assert.ok(text.includes('飞星'), 'text should mention 飞星');
});
