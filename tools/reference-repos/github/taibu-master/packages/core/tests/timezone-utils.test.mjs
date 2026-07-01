import test from 'node:test';
import assert from 'node:assert/strict';
import { createRequire } from 'node:module';

const require = createRequire(import.meta.url);
const { zonedTimeToUtc } = require('../src/shared/timezone-utils.ts');

test('zonedTimeToUtc converts Asia/Shanghai local time to UTC', () => {
  const date = zonedTimeToUtc({
    year: 2024,
    month: 1,
    day: 1,
    hour: 8,
    minute: 0,
    second: 0,
  }, 'Asia/Shanghai');

  assert.equal(date.getUTCFullYear(), 2024);
  assert.equal(date.getUTCMonth(), 0);
  assert.equal(date.getUTCDate(), 1);
  assert.equal(date.getUTCHours(), 0);
  assert.equal(date.getUTCMinutes(), 0);
});
