import test from 'node:test';
import assert from 'node:assert/strict';

import * as mcpCore from 'taibu-core';

test('mcp liuyao uses fixed najia for 天风姤 and should not treat second yao as 妻财', async () => {
  const result = await mcpCore.calculateLiuyao({
    question: '问财运',
    yongShenTargets: ['妻财'],
    method: 'select',
    hexagramName: '天风姤',
    date: '2026-02-10T12:00:00',
  });

  const naJiaList = result.fullYaos.map((yao) => yao.naJia);
  assert.deepEqual(naJiaList, ['丑', '亥', '酉', '午', '申', '戌']);
  assert.equal(result.fullYaos[1]?.liuQin, '子孙');
});

test('mcp liuyao should reject empty question instead of producing formal interpretation context', async () => {
  await assert.rejects(
    () => mcpCore.calculateLiuyao({
      question: '',
      yongShenTargets: [],
      method: 'select',
      hexagramName: '乾为天',
      date: '2026-02-10T12:00:00',
    }),
    /请先明确问题后再解卦/u
  );
});
