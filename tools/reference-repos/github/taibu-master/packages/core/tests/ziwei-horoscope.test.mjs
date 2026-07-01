import test from 'node:test';
import assert from 'node:assert/strict';

import {
  calculateZiweiHoroscope,
  toZiweiHoroscopeJson,
  toZiweiHoroscopeText,
} from 'taibu-core';

const BASE_INPUT = {
  gender: 'male',
  birthYear: 1990,
  birthMonth: 6,
  birthDay: 15,
  birthHour: 10,
  calendarType: 'solar',
};

test('calculateZiweiHoroscope should return all period layers', () => {
  const result = calculateZiweiHoroscope({
    ...BASE_INPUT,
    targetDate: '2026-04-10',
  });

  assert.ok(result.decadal, 'decadal required');
  assert.ok(result.yearly, 'yearly required');
  assert.ok(result.monthly, 'monthly required');
  assert.ok(result.daily, 'daily required');
  assert.ok(result.hourly, 'hourly required');
  assert.ok(result.age, 'age required');
  assert.ok(result.solarDate, 'solarDate required');
  assert.ok(result.lunarDate, 'lunarDate required');
  assert.equal(result.targetDate, '2026-04-10', 'targetDate should echo input');
});

test('calculateZiweiHoroscope period entries should have required fields', () => {
  const result = calculateZiweiHoroscope({
    ...BASE_INPUT,
    targetDate: '2026-04-10',
  });

  for (const key of ['decadal', 'yearly', 'monthly', 'daily', 'hourly']) {
    const period = result[key];
    assert.ok(typeof period.index === 'number', `${key}.index should be a number`);
    assert.ok(typeof period.name === 'string', `${key}.name should be a string`);
    assert.ok(typeof period.heavenlyStem === 'string', `${key}.heavenlyStem should be a string`);
    assert.ok(typeof period.earthlyBranch === 'string', `${key}.earthlyBranch should be a string`);
    assert.ok(Array.isArray(period.palaceNames), `${key}.palaceNames should be an array`);
    assert.ok(Array.isArray(period.mutagen), `${key}.mutagen should be an array`);
  }
});

test('calculateZiweiHoroscope age should include nominalAge', () => {
  const result = calculateZiweiHoroscope({
    ...BASE_INPUT,
    targetDate: '2026-04-10',
  });

  assert.ok(typeof result.age.nominalAge === 'number', 'age.nominalAge should be a number');
  assert.ok(result.age.nominalAge > 0, 'nominalAge should be positive');
});

test('calculateZiweiHoroscope should include transit stars for the flow year', () => {
  const result = calculateZiweiHoroscope({
    ...BASE_INPUT,
    targetDate: '2026-04-10',
  });

  assert.ok(Array.isArray(result.transitStars), 'transitStars should be an array');
  assert.ok(result.transitStars.length > 0, 'transitStars should not be empty');

  for (const star of result.transitStars) {
    assert.ok(typeof star.starName === 'string', 'each transit star should have starName');
    assert.ok(typeof star.palaceName === 'string', 'each transit star should have palaceName');
}
});

test('calculateZiweiHoroscope should reflect hasExplicitTargetTime correctly', () => {
  const withoutTime = calculateZiweiHoroscope({
    ...BASE_INPUT,
    targetDate: '2026-04-10',
  });
  assert.equal(withoutTime.hasExplicitTargetTime, false, 'should be false without targetTimeIndex');

  const withTime = calculateZiweiHoroscope({
    ...BASE_INPUT,
    targetDate: '2026-04-10',
    targetTimeIndex:5,
  });
  assert.equal(withTime.hasExplicitTargetTime, true, 'should be true with targetTimeIndex');
});

test('toZiweiHoroscopeJson should return well-formed canonical JSON', () => {
  const result = calculateZiweiHoroscope({
    ...BASE_INPUT,
    targetDate: '2026-04-10',
  });
  const json = toZiweiHoroscopeJson(result);

  assert.ok(json.基本信息, 'JSON should have 基本信息');
  assert.ok(typeof json.基本信息.目标日期 === 'string', '基本信息.目标日期 should be a string');
  assert.ok(typeof json.基本信息.五行局 === 'string', '基本信息.五行局 should be a string');
assert.ok(Array.isArray(json.运限叠宫), '运限叠宫 should be an array');
  assert.ok(json.运限叠宫.length >= 5, '运限叠宫 should have at least 5 layers');

  for (const entry of json.运限叠宫) {
    assert.ok(typeof entry.层次 === 'string', '层次 should be a string');
    assert.ok(typeof entry.干支 === 'string', '干支 should be a string');
    assert.ok(Array.isArray(entry.运限四化), '运限四化 should be an array');
  }
});

test('toZiweiHoroscopeJson full detail should include extra basic info fields', () => {
  const result = calculateZiweiHoroscope({
    ...BASE_INPUT,
    targetDate: '2026-04-10',
  });
  const json = toZiweiHoroscopeJson(result, { detailLevel: 'full' });

  assert.ok(json.基本信息.阳历, 'full detail should include 阳历');
  assert.ok(json.基本信息.农历, 'full detail should include 农历');
  assert.ok(json.基本信息.命主, 'full detail should include 命主');
  assert.ok(json.基本信息.身主, 'full detail should include 身主');
});

test('toZiweiHoroscopeText should return a non-empty markdown string', () => {
  const result = calculateZiweiHoroscope({
    ...BASE_INPUT,
    targetDate: '2026-04-10',
  });
  const text = toZiweiHoroscopeText(result);

  assert.ok(typeof text === 'string', 'text output should be a string');
  assert.ok(text.length > 100, 'text output should be substantial');
});
