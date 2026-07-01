import test from 'node:test';
import assert from 'node:assert/strict';

import * as mcpCore from 'taibu-core';

test('meihua time method basic output', () => {
  const result = mcpCore.calculateMeihua({
    method: 'time',
    date: '2026-04-10T14:30:00',
    question: '今日运势如何',
  });
  assert.ok(result.bodyTrigram, 'bodyTrigram required');
  assert.ok(result.useTrigram, 'useTrigram required');
  assert.ok(result.mainHexagram, 'mainHexagram required');
  assert.ok(result.movingLine, 'movingLine required');
  assert.ok(result.bodyUseRelation, 'bodyUseRelation required');
});

test('meihua count_with_time method', () => {
  const result = mcpCore.calculateMeihua({
    method: 'count_with_time',
    count: 15,
    countCategory: 'item',
    date: '2026-04-10T14:30:00',
    question: '事业前景',
  });
  assert.ok(result.mainHexagram, 'mainHexagram required');
  assert.ok(result.bodyTrigram, 'bodyTrigram required');
  assert.ok(result.useTrigram, 'useTrigram required');
});

test('meihua text_split method', () => {
  const result = mcpCore.calculateMeihua({
    method: 'text_split',
    text: '天地人和',
    date: '2026-04-10T14:30:00',
    question: '天地人卦象',
  });
  assert.ok(result.mainHexagram, 'mainHexagram required');
  assert.ok(result.bodyTrigram, 'bodyTrigram required for text_split');
  assert.ok(result.useTrigram, 'useTrigram required for text_split');
});

test('meihua JSON rendering', () => {
  const output = mcpCore.calculateMeihua({
method: 'time',
    date: '2026-04-10T14:30:00',
    question: '测试JSON渲染',
  });
  const json = mcpCore.toMeihuaJson(output);
assert.ok(json.卦盘, 'json should have 卦盘');
  assert.ok(json.卦盘.本卦, 'json should have 卦盘.本卦');
  assert.ok(json.卦盘.本卦.卦名, 'json should have 卦盘.本卦.卦名');
  assert.ok(json.卦盘.本卦.上卦, 'json should have 上卦');
  assert.ok(json.卦盘.本卦.下卦, 'json should have 下卦');
});

test('meihua text rendering', () => {
  const output = mcpCore.calculateMeihua({
    method: 'time',
    date: '2026-04-10T14:30:00',
    question: '测试文本渲染',
  });
  const text = mcpCore.toMeihuaText(output);
  assert.ok(text.length > 0);
});
