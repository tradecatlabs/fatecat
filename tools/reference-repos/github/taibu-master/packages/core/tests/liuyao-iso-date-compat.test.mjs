import test from 'node:test';
import assert from 'node:assert/strict';
import * as mcpCore from 'taibu-core';

test('liuyao should accept ISO timestamps with timezone offsets', async () => {
  const result = await mcpCore.calculateLiuyao({
    question: '这个计划能推进吗',
    yongShenTargets: ['官鬼'],
    method: 'select',
    hexagramName: '天火同人',
    date: '2024-01-02T10:00:00+08:00',
  });

  assert.equal(typeof result.hexagramName, 'string');
  assert.equal(Array.isArray(result.fullYaos), true);
});
