import { test } from 'node:test';
import assert from 'node:assert/strict';
import { zonedTimeToUtc } from 'taibu-core/timezone-utils';

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

test('zonedTimeToUtc keeps UTC time unchanged', () => {
    const date = zonedTimeToUtc({
        year: 2024,
        month: 6,
        day: 1,
        hour: 12,
        minute: 30,
        second: 0,
    }, 'UTC');

    assert.equal(date.getUTCHours(), 12);
    assert.equal(date.getUTCMinutes(), 30);
});
