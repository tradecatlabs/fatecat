import type { ToolDefinition } from '../../contract.js';

export const ziweiHoroscopeDefinition: ToolDefinition = {
  name: 'ziwei_horoscope',
  description: '紫微斗数运限 - 根据出生信息与目标日期计算大限、小限、流年、流月、流日、流时等运限信息。',
  inputSchema: {
    type: 'object',
    properties: {
      gender: { type: 'string', enum: ['male', 'female'], description: '性别' },
      birthYear: { type: 'number', description: '出生年 (1900-2100)' },
      birthMonth: { type: 'number', description: '出生月 (1-12)' },
      birthDay: { type: 'number', description: '出生日 (1-31)' },
      birthHour: { type: 'number', description: '出生时 (0-23)' },
      birthMinute: { type: 'number', description: '出生分 (0-59)', default: 0 },
      calendarType: { type: 'string', enum: ['solar', 'lunar'], description: '历法类型（solar=公历，lunar=农历）', default: 'solar' },
      isLeapMonth: { type: 'boolean', description: '农历闰月标记', default: false },
      longitude: {
        type: 'number',
        description: '出生地经度',
      },
      targetDate: { type: 'string', description: '目标日期 (YYYY-MM-DD，省略时取当前日期)' },
      targetTimeIndex: { type: 'number', description: '目标流时时段序号 (0-12)' },
      detailLevel: {
        type: 'string',
        enum: ['default', 'full'],
        description: '输出细节级别。',
        default: 'default',
      },
    },
    required: ['gender', 'birthYear', 'birthMonth', 'birthDay', 'birthHour'],
    examples: [
      { gender: 'male', birthYear: 1990, birthMonth: 1, birthDay: 15, birthHour: 9, targetDate: '2026-03-13' },
    ],
  },
  annotations: {
    readOnlyHint: true,
    destructiveHint: false,
    idempotentHint: true,
    openWorldHint: false,
  },
};
