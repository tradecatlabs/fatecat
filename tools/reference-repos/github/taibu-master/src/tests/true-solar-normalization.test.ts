import test from 'node:test';
import assert from 'node:assert/strict';
import { Lunar } from 'lunar-javascript';
import { calculateBazi } from 'taibu-core/bazi';
import { calculateZiwei } from 'taibu-core/ziwei';

test('true solar correction should normalize rounded minutes instead of returning impossible :60 values', () => {
  const result = calculateZiwei({
    gender: 'male',
    birthYear: 2024,
    birthMonth: 1,
    birthDay: 1,
    birthHour: 0,
    birthMinute: 0,
    calendarType: 'solar',
    longitude: -179.1,
  });
  const info = result.trueSolarTimeInfo;

  assert.ok(info);
  assert.equal(info.trueSolarTime, '04:00');
  assert.equal(info.dayOffset, -1);
});

test('calculateBazi should normalize true-solar dates across month boundaries', async () => {
  const corrected = await calculateBazi({
    gender: 'male',
    birthYear: 2024,
    birthMonth: 3,
    birthDay: 1,
    birthHour: 0,
    birthMinute: 5,
    calendarType: 'solar',
    longitude: -180,
  });

  const normalized = await calculateBazi({
    gender: 'male',
    birthYear: 2024,
    birthMonth: 2,
    birthDay: 29,
    birthHour: 3,
    birthMinute: 52,
    calendarType: 'solar',
  });

  assert.deepEqual(corrected.fourPillars, normalized.fourPillars);
  assert.equal(corrected.dayMaster, normalized.dayMaster);
});

test('calculateZiwei should apply true-solar day offsets before building the chart date', async () => {
  const corrected = await calculateZiwei({
    gender: 'male',
    birthYear: 2024,
    birthMonth: 3,
    birthDay: 1,
    birthHour: 0,
    birthMinute: 5,
    calendarType: 'solar',
    longitude: -180,
  });

  const normalized = await calculateZiwei({
    gender: 'male',
    birthYear: 2024,
    birthMonth: 2,
    birthDay: 29,
    birthHour: 3,
    birthMinute: 52,
    calendarType: 'solar',
  });

  assert.equal(corrected.solarDate, normalized.solarDate);
  assert.equal(corrected.lunarDate, normalized.lunarDate);
  assert.deepEqual(corrected.fourPillars, normalized.fourPillars);
  assert.equal(corrected.timeRange, normalized.timeRange);
});

test('calculateZiwei should accept valid solar birthdays on the 31st', async () => {
  const result = await calculateZiwei({
    gender: 'male',
    birthYear: 1990,
    birthMonth: 1,
    birthDay: 31,
    birthHour: 10,
    birthMinute: 0,
    calendarType: 'solar',
  });

  assert.equal(result.solarDate, '1990-1-31');
});

test('calculateBazi should apply true solar correction for lunar input through the equivalent solar instant', async () => {
  const lunar = Lunar.fromYmdHms(2023, 8, 15, 23, 40, 0);
  const solar = lunar.getSolar();

  const correctedLunar = await calculateBazi({
    gender: 'female',
    birthYear: 2023,
    birthMonth: 8,
    birthDay: 15,
    birthHour: 23,
    birthMinute: 40,
    calendarType: 'lunar',
    longitude: 73,
  });

  const correctedSolar = await calculateBazi({
    gender: 'female',
    birthYear: solar.getYear(),
    birthMonth: solar.getMonth(),
    birthDay: solar.getDay(),
    birthHour: solar.getHour(),
    birthMinute: solar.getMinute(),
    calendarType: 'solar',
    longitude: 73,
  });

  assert.deepEqual(correctedLunar.fourPillars, correctedSolar.fourPillars);
  assert.equal(correctedLunar.dayMaster, correctedSolar.dayMaster);
  assert.deepEqual(correctedLunar.trueSolarTimeInfo, correctedSolar.trueSolarTimeInfo);
});

test('calculateZiwei should apply true solar correction for lunar input through the equivalent solar instant', async () => {
  const lunar = Lunar.fromYmdHms(2023, 8, 15, 23, 40, 0);
  const solar = lunar.getSolar();

  const correctedLunar = await calculateZiwei({
    gender: 'female',
    birthYear: 2023,
    birthMonth: 8,
    birthDay: 15,
    birthHour: 23,
    birthMinute: 40,
    calendarType: 'lunar',
    longitude: 73,
  });

  const correctedSolar = await calculateZiwei({
    gender: 'female',
    birthYear: solar.getYear(),
    birthMonth: solar.getMonth(),
    birthDay: solar.getDay(),
    birthHour: solar.getHour(),
    birthMinute: solar.getMinute(),
    calendarType: 'solar',
    longitude: 73,
  });

  assert.equal(correctedLunar.solarDate, correctedSolar.solarDate);
  assert.equal(correctedLunar.lunarDate, correctedSolar.lunarDate);
  assert.deepEqual(correctedLunar.fourPillars, correctedSolar.fourPillars);
  assert.deepEqual(correctedLunar.trueSolarTimeInfo, correctedSolar.trueSolarTimeInfo);
});
