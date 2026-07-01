import test from 'node:test';
import assert from 'node:assert/strict';
import { getPersonReferenceLabel, getPersonSectionTitle } from '../src/lib/input-labels';

test('个人排盘时主表单不应显示第一人信息', () => {
  assert.equal(getPersonSectionTitle('single', 'self'), '个人信息');
  assert.equal(getPersonReferenceLabel('single', 'self'), '个人');
});

test('合盘时仍应区分第一人和第二人', () => {
  assert.equal(getPersonSectionTitle('compatibility', 'self'), '第一人信息');
  assert.equal(getPersonSectionTitle('compatibility', 'partner'), '第二人信息');
  assert.equal(getPersonReferenceLabel('compatibility', 'self'), '第一人');
  assert.equal(getPersonReferenceLabel('compatibility', 'partner'), '第二人');
});
