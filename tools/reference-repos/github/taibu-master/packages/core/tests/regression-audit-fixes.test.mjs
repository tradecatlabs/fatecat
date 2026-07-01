import test from 'node:test';
import assert from 'node:assert/strict';
import { execFileSync } from 'node:child_process';
import { Lunar, LunarMonth, LunarYear } from 'lunar-javascript';

import * as mcpCore from 'taibu-core';

function runQimenUnderTimeZone(timeZone) {
  const script = `
    import { calculateQimen } from 'taibu-core';
    const result = await calculateQimen({
      year: 2026,
      month: 3,
      day: 15,
      hour: 16,
      minute: 51,
    });
    console.log(JSON.stringify({
      siZhu: result.siZhu,
      dunType: result.dunType,
      juNumber: result.juNumber,
      xunShou: result.xunShou,
      zhiFu: result.zhiFu,
      zhiShi: result.zhiShi,
    }));
  `;

  return JSON.parse(
    execFileSync(process.execPath, ['--input-type=module', '-e', script], {
      cwd: process.cwd(),
      env: { ...process.env, TZ: timeZone },
      encoding: 'utf8',
    }).trim(),
  );
}

test('qimen should stay stable across process time zones for the same wall-clock input', () => {
  const utcResult = runQimenUnderTimeZone('UTC');
  const shanghaiResult = runQimenUnderTimeZone('Asia/Shanghai');

  assert.deepEqual(
    utcResult,
    shanghaiResult,
    'same wall-clock qimen input should not drift with process TZ',
  );
});

test('qimen should throw synchronously for invalid timezones', async () => {
  assert.throws(
    () =>
      mcpCore.calculateQimen({
        year: 2026,
        month: 3,
        day: 15,
        hour: 16,
        minute: 51,
        timezone: 'Asia/Shanghaix',
      }),
    /timezone/u,
  );
});

test('liuyao should reject date-only input because time affects the chart', async () => {
  await assert.rejects(
    () =>
      mcpCore.calculateLiuyao({
        question: '这周项目顺利吗',
        yongShenTargets: ['官鬼'],
        method: 'auto',
        date: '2026-02-11',
      }),
    /必须包含时间|YYYY-MM-DDTHH:MM/u,
  );
});

test('liuyao number casting should reject non-positive integers with a user-facing error', async () => {
  await assert.rejects(
    () =>
      mcpCore.calculateLiuyao({
        question: '数字起卦测试',
        yongShenTargets: ['官鬼'],
        method: 'number',
        numbers: [-1, 2],
        date: '2026-02-10T12:00:00',
      }),
    /正整数|自然数|numbers/u,
  );
});

test('almanac should reject impossible calendar dates instead of silently rolling over', async () => {
  await assert.rejects(
    () => mcpCore.calculateDailyAlmanac({ date: '2026-02-31' }),
    /日期无效|不存在/u,
  );
});

test('daliuren should reject invalid timezones instead of silently falling back', () => {
  assert.throws(
    () =>
      mcpCore.calculateDaliuren({
        date: '2024-01-01',
        hour: 10,
        minute: 0,
        timezone: 'Asia/Shanghaix',
      }),
    /timezone/u,
  );
});

test('ziwei should derive lifeMasterStar from the birth-year earthly branch', async () => {
  const result = await mcpCore.calculateZiwei({
    gender: 'male',
    birthYear: 2003,
    birthMonth: 9,
    birthDay: 2,
    birthHour: 10,
    birthMinute: 30,
  });

  assert.equal(result.lifeMasterStar, '武曲');
});

test('ziwei should support longitude correction for lunar input by normalizing through the equivalent solar birth time', async () => {
  const lunar = Lunar.fromYmdHms(2003, 8, 6, 0, 10, 0);
  const solar = lunar.getSolar();

  const correctedLunar = await mcpCore.calculateZiwei({
    gender: 'male',
    birthYear: 2003,
    birthMonth: 8,
    birthDay: 6,
    birthHour: 0,
    birthMinute: 10,
    calendarType: 'lunar',
    longitude: 73,
  });

  const correctedSolar = await mcpCore.calculateZiwei({
    gender: 'male',
    birthYear: solar.getYear(),
    birthMonth: solar.getMonth(),
    birthDay: solar.getDay(),
    birthHour: solar.getHour(),
    birthMinute: solar.getMinute(),
    calendarType: 'solar',
    longitude: 73,
  });

  assert.deepEqual(correctedLunar.fourPillars, correctedSolar.fourPillars);
  assert.equal(correctedLunar.solarDate, correctedSolar.solarDate);
  assert.equal(correctedLunar.timeRange, correctedSolar.timeRange);
  assert.equal(correctedLunar.trueSolarTimeInfo?.longitude, 73);
});

test('ziwei should reject invalid lunar leap months and out-of-range lunar days', async () => {
  let nonLeapYear = 1900;
  while (LunarYear.fromYear(nonLeapYear).getLeapMonth() !== 0) {
    nonLeapYear += 1;
  }

  assert.throws(
    () =>
      mcpCore.calculateZiwei({
        gender: 'female',
        birthYear: nonLeapYear,
        birthMonth: 1,
        birthDay: 1,
        birthHour: 10,
        birthMinute: 0,
        calendarType: 'lunar',
        isLeapMonth: true,
      }),
    /闰月/u,
  );

  const leapMonth = LunarYear.fromYear(2023).getLeapMonth();
  const leapMonthDayCount = LunarMonth.fromYm(2023, -Math.abs(leapMonth)).getDayCount();

  assert.throws(
    () =>
      mcpCore.calculateZiwei({
        gender: 'female',
        birthYear: 2023,
        birthMonth: Math.abs(leapMonth),
        birthDay: leapMonthDayCount + 1,
        birthHour: 10,
        birthMinute: 0,
        calendarType: 'lunar',
        isLeapMonth: true,
      }),
    /农历日期/u,
  );
});

test('bazi_dayun should keep xiaoYun coverage aligned with the upstream startAge', async () => {
  const result = await mcpCore.calculateBaziDayun({
    gender: 'male',
    birthYear: 1990,
    birthMonth: 1,
    birthDay: 1,
    birthHour: 12,
    birthMinute: 0,
    calendarType: 'solar',
  });

  assert.ok(result.xiaoYun.some((item) => item.age === 8), 'xiaoYun should include the age right before first daYun.startAge');
  assert.equal(result.startAge, 9, 'dayun output should expose first daYun.startAge for downstream adapters');
  assert.equal(result.list[0]?.startAge, 9, 'each dayun entry should expose its own startAge');
  assert.equal(result.list[0]?.liunianList[0]?.age, 9, 'liunian entries should expose derived age for web adapters');
});

test('ziwei should expose structured four pillars for direct consumers', async () => {
  const result = await mcpCore.calculateZiwei({
    gender: 'male',
    birthYear: 1990,
    birthMonth: 1,
    birthDay: 1,
    birthHour: 12,
    birthMinute: 0,
    calendarType: 'solar',
  });

  assert.equal(typeof result.fourPillars.year?.gan, 'string');
  assert.equal(typeof result.fourPillars.year?.zhi, 'string');
  assert.equal(result.fourPillars.year.gan + result.fourPillars.year.zhi, '己巳');
});
