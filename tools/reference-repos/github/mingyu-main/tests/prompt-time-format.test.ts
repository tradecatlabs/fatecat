import test from 'node:test';
import assert from 'node:assert/strict';
import { readFileSync } from 'node:fs';
import { resolve } from 'node:path';
import { formatPromptCurrentTime } from '../src/lib/prompt-time';

test('提示词当前时间应同时给出公历、农历、干支历与节气', () => {
  const date = new Date(2025, 0, 2, 3, 4);
  assert.equal(
    formatPromptCurrentTime(date),
    [
      '公历：2025年1月2日 3时4分',
      '农历：甲辰年十二月初三 寅时',
      '干支历：甲辰年 丙子月 辛未日 庚寅时',
      '当前节气：冬至',
    ].join('\n'),
  );
});

test('八字、紫微和反推时辰提示词应复用统一时间格式 helper', () => {
  const source = [
    readFileSync(resolve('src/utils/ai/aiPrompts.ts'), 'utf8'),
    readFileSync(resolve('src/lib/birth-time-reverse/prompts.ts'), 'utf8'),
    readFileSync(resolve('src/lib/full-chart-engine/ziwei.ts'), 'utf8'),
    readFileSync(resolve('src/pages/ResultPage/ResultPage.helpers.ts'), 'utf8'),
  ].join('\n');

  assert.match(source, /formatPromptCurrentTime/);
  assert.match(readFileSync(resolve('src/lib/prompt-time.ts'), 'utf8'), /干支历：/);
  assert.doesNotMatch(source, /toLocaleString\('zh-CN'\)/);
});
