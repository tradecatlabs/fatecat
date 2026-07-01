import test from 'node:test';
import assert from 'node:assert/strict';

import * as mcpCore from 'taibu-core';

test('liuyao rejects missing yongShenTargets when question is provided', async () => {
  await assert.rejects(
    () =>
      mcpCore.calculateLiuyao({
        question: '近期事业如何',
        method: 'select',
        hexagramName: '天火同人',
        date: '2026-02-10T12:00:00',
      }),
    /yongShenTargets|分析目标|请选择/u,
  );
});

test('liuyao rejects empty yongShenTargets when question is provided', async () => {
  await assert.rejects(
    () =>
      mcpCore.calculateLiuyao({
        question: '近期事业如何',
        yongShenTargets: [],
        method: 'select',
        hexagramName: '天火同人',
        date: '2026-02-10T12:00:00',
      }),
    /yongShenTargets|分析目标|请选择|请先判断并填写/u,
  );
});

test('liuyao rejects empty question with explicit empty yongShenTargets', async () => {
  await assert.rejects(
    () =>
      mcpCore.calculateLiuyao({
        question: '',
        yongShenTargets: [],
        method: 'select',
        hexagramName: '天火同人',
        date: '2026-02-10T12:00:00',
      }),
    /请先明确问题后再解卦/u,
  );
});

test('liuyao rejects omitted yongShenTargets even when question is empty', async () => {
  await assert.rejects(
    () =>
      mcpCore.calculateLiuyao({
        question: '',
        method: 'select',
        hexagramName: '天火同人',
        date: '2026-02-10T12:00:00',
      }),
    /请先明确问题后再解卦/u,
  );
});

test('liuyao rejects non-array yongShenTargets even when question is empty', async () => {
  await assert.rejects(
    () =>
      mcpCore.calculateLiuyao({
        question: '',
        yongShenTargets: null,
        method: 'select',
        hexagramName: '天火同人',
        date: '2026-02-10T12:00:00',
      }),
    /请先明确问题后再解卦/u,
  );
});

test('liuyao rejects non-string question to avoid contract bypass', async () => {
  await assert.rejects(
    () =>
      mcpCore.calculateLiuyao({
        question: 123,
        yongShenTargets: [],
        method: 'select',
        hexagramName: '天火同人',
        date: '2026-02-10T12:00:00',
      }),
    /请先明确问题后再解卦/u,
  );
});

test('liuyao rejects illegal yongShenTargets values', async () => {
  await assert.rejects(
    () =>
      mcpCore.calculateLiuyao({
        question: '近期事业如何',
        yongShenTargets: ['官鬼', '无效目标'],
        method: 'select',
        hexagramName: '天火同人',
        date: '2026-02-10T12:00:00',
      }),
    /yongShenTargets|非法|无效/u,
  );
});

test('liuyao accepts explicit multiple targets in strict mode', async () => {
  const result = await mcpCore.calculateLiuyao({
    question: '考试结果和排名怎么样',
    yongShenTargets: ['官鬼', '父母'],
    method: 'select',
    hexagramName: '天火同人',
    date: '2026-02-10T12:00:00',
  });

  assert.ok(Array.isArray(result.yongShen));
  assert.ok(result.yongShen.some((group) => group.targetLiuQin === '官鬼'));
  assert.ok(result.yongShen.some((group) => group.targetLiuQin === '父母'));
  for (const group of result.yongShen) {
    assert.ok(Array.isArray(group.candidates));
    assert.ok(group.selected, 'every group should include selected');
    assert.equal(typeof group.selectionNote, 'string');
    assert.equal('source' in group, false);
  }
});
