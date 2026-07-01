import test from 'node:test';
import assert from 'node:assert/strict';

import {
  calculateZiwei,
  toZiweiJson,
  toZiweiText,
} from 'taibu-core';

const BASE_INPUT = {
  gender: 'male',
  birthYear: 1990,
  birthMonth: 6,
  birthDay: 15,
  birthHour: 10,
  calendarType: 'solar',
};

test('calculateZiwei should return12 palaces with required structure', () => {
  const result = calculateZiwei(BASE_INPUT);

  assert.ok(Array.isArray(result.palaces), 'palaces should be an array');
  assert.equal(result.palaces.length, 12, 'should have exactly 12 palaces');

  for (const palace of result.palaces) {
    assert.ok(typeof palace.name === 'string' && palace.name.length >0, `palace name should be non-empty string, got: ${palace.name}`);
    assert.ok(typeof palace.earthlyBranch === 'string' && palace.earthlyBranch.length > 0, `earthlyBranch should be non-empty string for palace ${palace.name}`);
    assert.ok(Array.isArray(palace.majorStars), `majorStars should be an array for palace ${palace.name}`);
    assert.ok(Array.isArray(palace.minorStars), `minorStars should be an array for palace ${palace.name}`);
  }
});

test('calculateZiwei should return lifeMasterStar, bodyMasterStar, and douJun as strings', () => {
  const result = calculateZiwei(BASE_INPUT);

  assert.ok(typeof result.lifeMasterStar === 'string' && result.lifeMasterStar.length > 0, 'lifeMasterStar should be a non-empty string');
  assert.ok(typeof result.bodyMasterStar === 'string' && result.bodyMasterStar.length > 0, 'bodyMasterStar should be a non-empty string');
  assert.ok(typeof result.douJun === 'string' && result.douJun.length > 0, 'douJun should be a non-empty string');
});

test('calculateZiwei should populate four pillars with valid gan-zhi pairs', () => {
  const result = calculateZiwei(BASE_INPUT);

  for (const pillarKey of ['year', 'month', 'day', 'hour']) {
    const pillar = result.fourPillars[pillarKey];
    assert.ok(typeof pillar.gan === 'string' && pillar.gan.length === 1, `fourPillars.${pillarKey}.gan should be a single character`);
    assert.ok(typeof pillar.zhi === 'string' && pillar.zhi.length === 1, `fourPillars.${pillarKey}.zhi should be a single character`);
}
});

test('calculateZiwei should include mutagenSummary with four transformations', () => {
  const result = calculateZiwei(BASE_INPUT);

  assert.ok(Array.isArray(result.mutagenSummary), 'mutagenSummary should be an array');
  assert.ok(result.mutagenSummary.length >= 4, 'mutagenSummary should have at least 4 entries');

  const mutagenTypes = new Set(result.mutagenSummary.map(m => m.mutagen));
  for (const expected of ['禄', '权', '科', '忌']) {
    assert.ok(mutagenTypes.has(expected), `mutagenSummary should include ${expected}`);
  }

  for (const item of result.mutagenSummary) {
    assert.ok(typeof item.starName === 'string' && item.starName.length > 0, 'each mutagen entry should have a starName');
    assert.ok(typeof item.palaceName === 'string' && item.palaceName.length > 0, 'each mutagen entry should have a palaceName');
  }
});

test('calculateZiwei should compute decadal list for all 12 palaces', () => {
  const result = calculateZiwei(BASE_INPUT);

  assert.ok(Array.isArray(result.decadalList), 'decadalList should be an array');
  assert.equal(result.decadalList.length, 12, 'decadalList should have 12 entries');

  for (const decadal of result.decadalList) {
    assert.ok(typeof decadal.startAge === 'number', 'startAge should be a number');
    assert.ok(typeof decadal.endAge === 'number', 'endAge should be a number');
    assert.ok(decadal.endAge > decadal.startAge, 'endAge should be greater than startAge');
    assert.ok(typeof decadal.heavenlyStem === 'string', 'heavenlyStem should be a string');
    assert.ok(typeof decadal.palace.name === 'string', 'palace.name should be a string');
}
});

test('calculateZiwei should produce different charts for male vs female with same birth data', () => {
  const maleResult = calculateZiwei(BASE_INPUT);
  const femaleResult = calculateZiwei({ ...BASE_INPUT, gender:'female' });

  // Small limit ordering differs between male and female
  const maleSmallLimitPalaces = (maleResult.smallLimit || []).map(s => s.palaceName).join(',');
  const femaleSmallLimitPalaces = (femaleResult.smallLimit || []).map(s => s.palaceName).join(',');
  assert.notEqual(maleSmallLimitPalaces, femaleSmallLimitPalaces, 'male and female small limit should differ');
});

test('calculateZiwei should accept lunar calendar input', () => {
  const lunarInput = {
    gender: 'male',
    birthYear: 1990,
    birthMonth: 5,
    birthDay: 15,
    birthHour: 10,
    calendarType: 'lunar',
  };
  const result = calculateZiwei(lunarInput);

  assert.ok(Array.isArray(result.palaces), 'palaces should be an array');
  assert.equal(result.palaces.length, 12, 'should have exactly 12 palaces');
  assert.ok(result.solarDate.length > 0, 'solarDate should be non-empty');
  assert.ok(result.lunarDate.length > 0, 'lunarDate should be non-empty');
});

test('toZiweiJson should return a well-formed canonical JSON object', () => {
  const result = calculateZiwei(BASE_INPUT);
  const json = toZiweiJson(result);

  assert.ok(json.基本信息, 'JSON should have 基本信息');
  assert.ok(typeof json.基本信息.阳历 === 'string', '基本信息.阳历 should be a string');
  assert.ok(typeof json.基本信息.五行局 === 'string', '基本信息.五行局 should be a string');
  assert.ok(typeof json.基本信息.命主 === 'string', '基本信息.命主 should be a string');
  assert.ok(Array.isArray(json.十二宫位), '十二宫位 should be an array');
  assert.equal(json.十二宫位.length, 12, '十二宫位 should have 12 entries');

  for (const palace of json.十二宫位) {
    assert.ok(typeof palace.宫位 === 'string', '宫位 should be a string');
    assert.ok(typeof palace.干支 === 'string', '干支 should be a string');
    assert.ok(Array.isArray(palace.主星及四化), '主星及四化 should be an array');
  }
});

test('toZiweiText should return a non-empty markdown string', () => {
  const result = calculateZiwei(BASE_INPUT);
  const text = toZiweiText(result);

  assert.ok(typeof text === 'string', 'text output should be a string');
  assert.ok(text.length > 100, 'text output should be substantial');
  assert.ok(text.includes('命宫'), 'text should mention 命宫');
});

test('toZiweiJson full detail should include extra fields like 斗君 and 命主星', () => {
  const result = calculateZiwei(BASE_INPUT);
  const json = toZiweiJson(result, { detailLevel: 'full' });

  assert.ok(json.基本信息.斗君, 'full detail should include 斗君');
  assert.ok(json.基本信息.命主星, 'full detail should include 命主星');
  assert.ok(json.基本信息.身主星, 'full detail should include 身主星');
});
