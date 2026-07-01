import test from 'node:test';
import assert from 'node:assert/strict';

import {
  buildZiweiChartInput,
  calculateZiweiDisplayPayload,
} from '../src/lib/full-chart-engine/ziwei';

test('紫微排盘入口应拒绝空白数字文本和不存在的出生日期', () => {
  assert.throws(
    () =>
      buildZiweiChartInput({
        name: '本人',
        gender: 'female',
        dateType: 'solar',
        year: ' ',
        month: '5',
        day: '20',
        timeIndex: 6,
        isLeapMonth: false,
      }),
    /出生年份必须是整数/,
  );

  assert.throws(
    () =>
      buildZiweiChartInput({
        name: '本人',
        gender: 'female',
        dateType: 'solar',
        year: '1995',
        month: '2',
        day: '31',
        timeIndex: 6,
        isLeapMonth: false,
      }),
    /日期需在 1-28 之间/,
  );

  assert.throws(
    () =>
      buildZiweiChartInput({
        name: '本人',
        gender: 'female',
        dateType: 'solar',
        year: '1995',
        month: '5',
        day: '20',
        timeIndex: ' ' as unknown as number,
        isLeapMonth: false,
      }),
    /出生时辰必须是整数/,
  );
});

test('紫微指定行运 payload 应输出补零后的公历日期', async () => {
  const input = buildZiweiChartInput({
    name: '本人',
    gender: 'female',
    dateType: 'solar',
    year: '1995',
    month: '5',
    day: '20',
    timeIndex: 6,
    isLeapMonth: false,
  });

  const payload = await calculateZiweiDisplayPayload({
    input,
    dateStr: '2101-02-28',
    hourIndex: 6,
    scope: 'daily',
  });

  assert.equal(payload.active_scope.solar_date, '2101-02-28');
});
