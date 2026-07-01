import test from 'node:test';
import assert from 'node:assert/strict';

import { calculateDailyAlmanac, toAlmanacJson, toAlmanacText } from 'taibu-core';

test('almanac basic output structure should include lunarDate and solarTerm fields', async () => {
  const result = await calculateDailyAlmanac({ date: '2026-04-10' });

  assert.ok(result.date, 'result should have date');
  assert.equal(result.date, '2026-04-10');
  assert.ok(result.dayInfo, 'result should have dayInfo');
  assert.ok(result.dayInfo.stem, 'dayInfo should have stem');
  assert.ok(result.dayInfo.branch, 'dayInfo should have branch');
  assert.ok(result.dayInfo.ganZhi, 'dayInfo should have ganZhi');

  assert.ok(result.almanac, 'result should have almanac');
  assert.ok(result.almanac.lunarDate, 'almanac should have lunarDate');
  assert.ok(result.almanac.lunarMonth, 'almanac should have lunarMonth');
  assert.ok(result.almanac.lunarDay, 'almanac should have lunarDay');
  assert.ok(result.almanac.zodiac, 'almanac should have zodiac');
  assert.ok(Array.isArray(result.almanac.suitable), 'suitable should be an array');
  assert.ok(Array.isArray(result.almanac.avoid), 'avoid should be an array');
});

test('almanac winter solstice (2025-12-21) should report solarTerm as 冬至', async () => {
  const result = await calculateDailyAlmanac({ date: '2025-12-21' });

  assert.ok(result.almanac, 'result should have almanac');
  assert.equal(result.almanac.solarTerm, '冬至', 'solarTerm should be冬至 on winter solstice');
});

test('almanac should return undefined solarTerm on a non-solar-term day', async () => {
const result = await calculateDailyAlmanac({ date: '2026-04-11' });

  assert.ok(result.almanac, 'result should have almanac');
  assert.equal(result.almanac.solarTerm, undefined, 'solarTerm should be undefined on a non-solar-term day');
});

test('almanac tenGod should be populated when dayMaster is provided', async () => {
const result = await calculateDailyAlmanac({ date: '2026-04-10', dayMaster: '甲' });

  assert.ok(result.tenGod, 'tenGod should exist when dayMaster is provided');
  assert.ok(typeof result.tenGod === 'string', 'tenGod should be a string');
});

test('almanac tenGod should be populated when birth date is provided', async () => {
  const result = await calculateDailyAlmanac({
    date: '2026-04-10',
    birthYear: 1990,
    birthMonth: 6,
    birthDay: 15,
  });

  assert.ok(result.tenGod, 'tenGod should exist when birth date is provided');
});

test('almanac should have directions and hourlyFortune', async () => {
  const result = await calculateDailyAlmanac({ date: '2026-04-10' });

  assert.ok(result.almanac.directions, 'almanac should have directions');
  assert.ok(result.almanac.directions.caiShen, 'directions should have caiShen');
  assert.ok(result.almanac.directions.xiShen, 'directions should have xiShen');
  assert.ok(result.almanac.directions.fuShen, 'directions should have fuShen');
  assert.ok(Array.isArray(result.almanac.hourlyFortune), 'hourlyFortune should be an array');
});

test('toAlmanacJson should return a non-empty canonical JSON object', async () => {
  const result = await calculateDailyAlmanac({ date: '2026-04-10' });
const json = toAlmanacJson(result);

  assert.ok(json, 'JSON output should be truthy');
  assert.ok(json.基础与个性化坐标, 'should have 基础与个性化坐标');
  assert.ok(json.基础与个性化坐标.日期, 'should have 日期');
  assert.ok(json.基础与个性化坐标.日干支, 'should have 日干支');
  assert.ok(json.传统黄历基调, 'should have 传统黄历基调');
  assert.ok(json.传统黄历基调.农历, 'should have 农历');
  assert.ok(json.传统黄历基调.生肖, 'should have 生肖');
  assert.ok(json.择日宜忌, 'should have 择日宜忌');
  assert.ok(Array.isArray(json.择日宜忌.宜), '宜 should be an array');
  assert.ok(Array.isArray(json.择日宜忌.忌), '忌 should be an array');
});

test('toAlmanacText should return a non-empty markdown string', async () => {
  const result = await calculateDailyAlmanac({ date: '2026-04-10' });
  const text = toAlmanacText(result);

  assert.ok(typeof text === 'string', 'text output should be a string');
  assert.ok(text.length > 0, 'text output should not be empty');
assert.match(text, /# 每日黄历/u, 'should contain main heading');
  assert.match(text, /农历/u, 'should contain lunar date info');
  assert.match(text, /宜/u, 'should contain suitable section');
  assert.match(text, /忌/u, 'should contain avoid section');
});

test('almanac should reject invalid date format', async () => {
  await assert.rejects(
    () => calculateDailyAlmanac({ date: '2026/04/10' }),
    /格式无效/u,
    'should reject non-YYYY-MM-DD format',
  );
});

test('almanac should reject invalid date values', async () => {
  await assert.rejects(
    () => calculateDailyAlmanac({ date: '2026-02-30' }),
    /日期无效/u,
    'should reject Feb 30',
  );
});
