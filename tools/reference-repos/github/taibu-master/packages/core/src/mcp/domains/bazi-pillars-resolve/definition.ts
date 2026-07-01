import type { ToolDefinition } from '../../contract.js';

export const baziPillarsResolveDefinition: ToolDefinition = {
  name: 'bazi_pillars_resolve',
  description: '四柱反推 - 根据年柱、月柱、日柱、时柱反推出生时间候选列表。',
  inputSchema: {
    type: 'object',
    properties: {
      yearPillar: { type: 'string', description: '年柱干支（如“甲子”）' },
      monthPillar: { type: 'string', description: '月柱干支（如“乙丑”）' },
      dayPillar: { type: 'string', description: '日柱干支（如“丙寅”）' },
      hourPillar: { type: 'string', description: '时柱干支（如“丁卯”）' },
    },
    required: ['yearPillar', 'monthPillar', 'dayPillar', 'hourPillar'],
    examples: [
      { yearPillar: '甲子', monthPillar: '乙丑', dayPillar: '丙寅', hourPillar: '丁卯' },
      { yearPillar: '戊子', monthPillar: '庚丑', dayPillar: '辛卯', hourPillar: '癸巳' },
    ],
  },
  annotations: {
    readOnlyHint: true,
    destructiveHint: false,
    idempotentHint: true,
    openWorldHint: false,
  },
};
