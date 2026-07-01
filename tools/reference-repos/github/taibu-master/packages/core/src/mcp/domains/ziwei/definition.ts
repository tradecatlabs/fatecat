import type { ToolDefinition } from '../../contract.js';

export const ziweiCalculateDefinition: ToolDefinition = {
  name: 'ziwei',
  description: '紫微斗数命盘 - 根据出生信息计算紫微命盘，输出十二宫位、星曜分布、四化、大限等信息。',
  inputSchema: {
    type: 'object',
    properties: {
      gender: {
        type: 'string',
        enum: ['male', 'female'],
        description: '性别',
      },
      birthYear: {
        type: 'number',
        description: '出生年 (1900-2100)',
      },
      birthMonth: {
        type: 'number',
        description: '出生月 (1-12)',
      },
      birthDay: {
        type: 'number',
        description: '出生日 (1-31)',
      },
      birthHour: {
        type: 'number',
        description: '出生时 (0-23)',
      },
      birthMinute: {
        type: 'number',
        description: '出生分 (0-59)',
        default: 0,
      },
      calendarType: {
        type: 'string',
        enum: ['solar', 'lunar'],
        description: '历法类型（solar=公历，lunar=农历）',
        default: 'solar',
      },
      isLeapMonth: {
        type: 'boolean',
        description: '农历闰月标记',
        default: false,
      },
      longitude: {
        type: 'number',
        description: '出生地经度',
      },
      detailLevel: {
        type: 'string',
        enum: ['default', 'full'],
        description: '输出细节级别。',
        default: 'default',
      },
    },
    required: ['gender', 'birthYear', 'birthMonth', 'birthDay', 'birthHour'],
    examples: [
      { gender: 'male', birthYear: 1990, birthMonth: 1, birthDay: 15, birthHour: 9 },
      { gender: 'female', birthYear: 1995, birthMonth: 6, birthDay: 20, birthHour: 23, calendarType: 'lunar' },
      { gender: 'male', birthYear: 1990, birthMonth: 1, birthDay: 15, birthHour: 9, longitude: 116.4 },
    ],
  },
  annotations: {
    readOnlyHint: true,
    destructiveHint: false,
    idempotentHint: true,
    openWorldHint: false,
  },
};
export const ziweiDefinition = ziweiCalculateDefinition;
