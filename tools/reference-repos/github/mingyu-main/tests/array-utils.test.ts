import test from 'node:test';
import assert from 'node:assert/strict';
import { uniqueNonEmptyStrings } from '../src/lib/array-utils';

test('uniqueNonEmptyStrings 会按顺序去重并过滤空值', () => {
  assert.deepEqual(uniqueNonEmptyStrings(['流年落宫', '流年落宫', undefined, '', '帝旺', '帝旺']), [
    '流年落宫',
    '帝旺',
  ]);
});
