import test from 'node:test';
import assert from 'node:assert/strict';
import { executeTool, listToolDefinitions } from 'taibu-core/mcp';

test('core should only expose canonical renamed tool names', async () => {
  const toolNames = new Set(listToolDefinitions().map((item) => item.name));

  for (const name of ['liuyao', 'tarot', 'almanac', 'bazi_dayun']) {
    assert.equal(toolNames.has(name), true, `${name} should remain in the canonical tool list`);
  }

  for (const alias of ['liuyao_analyze', 'tarot_draw', 'daily_fortune', 'dayun_calculate']) {
    assert.equal(toolNames.has(alias), false, `${alias} should not remain as an extra alias tool`);
    await assert.rejects(
      () => executeTool(alias, {}),
      /未知工具/u,
      `${alias} should be rejected once tool names have been renamed`,
    );
  }
});

test('mcp input validation should reject non-object arguments at the protocol boundary', async () => {
  await assert.rejects(
    () => executeTool('bazi', null),
    /输入必须是一个对象/u,
  );
});

test('mcp input validation should recurse into nested array items', async () => {
  await assert.rejects(
    () => executeTool('ziwei_flying_star', {
      gender: 'male',
      birthYear: 1990,
      birthMonth: 1,
      birthDay: 1,
      birthHour: 9,
      queries: [{}],
    }),
    /queries\[0\]\.type/u,
  );
});

test('mcp input validation should honor method-specific schema branches', async () => {
  await assert.rejects(
    () => executeTool('meihua', {
      question: '尺寸起卦',
      method: 'measure',
      majorValue: 2,
      minorValue: 3,
      date: '2026-04-04T10:30:00',
    }),
    /measureKind/u,
  );
});
