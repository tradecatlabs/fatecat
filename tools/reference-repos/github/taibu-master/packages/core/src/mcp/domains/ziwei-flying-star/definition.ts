import type { ToolDefinition } from '../../contract.js';

export const ziweiFlyingStarDefinition: ToolDefinition = {
  name: 'ziwei_flying_star',
  description: '紫微斗数飞星 - 分析命盘中的四化飞布、自化、落宫与三方四正关系。',
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
      queries: {
        type: 'array',
        description: '查询列表',
        minItems: 1,
        items: {
          type: 'object',
          properties: {
            type: { type: 'string', enum: ['fliesTo', 'selfMutaged', 'mutagedPlaces', 'surroundedPalaces'], description: '查询类型（fliesTo=飞到，selfMutaged=自化，mutagedPlaces=四化落宫，surroundedPalaces=三方四正）' },
            from: { type: 'string', description: '起飞宫位' },
            to: { type: 'string', description: '目标宫位' },
            palace: { type: 'string', description: '查询宫位' },
            mutagens: { type: 'array', items: { type: 'string', enum: ['禄', '权', '科', '忌'] }, description: '四化类型列表' },
          },
          required: ['type'],
        },
      },
      detailLevel: {
        type: 'string',
        enum: ['default', 'full'],
        description: '输出细节级别。',
        default: 'default',
      },
    },
    required: ['gender', 'birthYear', 'birthMonth', 'birthDay', 'birthHour', 'queries'],
    examples: [
      {
        gender: 'male', birthYear: 1990, birthMonth: 1, birthDay: 15, birthHour: 9,
        queries: [
          { type: 'mutagedPlaces', palace: '命宫' },
          { type: 'surroundedPalaces', palace: '命宫' },
        ],
      },
    ],
  },
  annotations: {
    readOnlyHint: true,
    destructiveHint: false,
    idempotentHint: true,
    openWorldHint: false,
  },
};
