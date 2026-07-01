import test from 'node:test';
import assert from 'node:assert/strict';

import { daysInSolarMonth, getBirthDateValidationMessage } from '../src/lib/date-validation';

test('公历月份天数工具应拒绝越界年月', () => {
  assert.equal(daysInSolarMonth(2024, 2), 29);
  assert.equal(daysInSolarMonth(2026, 2), 28);
  assert.throws(() => daysInSolarMonth(1899, 1), /年份需在 1900-2100 之间/);
  assert.throws(() => daysInSolarMonth(2101, 1), /年份需在 1900-2100 之间/);
  assert.throws(() => daysInSolarMonth(2026, 0), /月份需在 1-12 之间/);
  assert.throws(() => daysInSolarMonth(2026, 13), /月份需在 1-12 之间/);
});

test('出生日期校验文案应覆盖年月日基础边界', () => {
  assert.equal(
    getBirthDateValidationMessage({
      year: 1899,
      month: 1,
      day: 1,
      dateType: 'solar',
    }),
    '年份需在 1900-2100 之间。',
  );
  assert.equal(
    getBirthDateValidationMessage({
      year: 2026,
      month: 13,
      day: 1,
      dateType: 'solar',
    }),
    '月份需在 1-12 之间。',
  );
  assert.equal(
    getBirthDateValidationMessage({
      year: 2026,
      month: 2,
      day: 0,
      dateType: 'solar',
    }),
    '日期需在 1-28 之间。',
  );
  assert.equal(
    getBirthDateValidationMessage({
      year: 2026,
      month: 1,
      day: 0,
      dateType: 'lunar',
    }),
    '农历日期需在 1-30 之间。',
  );
});
