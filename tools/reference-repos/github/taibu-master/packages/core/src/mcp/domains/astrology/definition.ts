import type { ToolDefinition } from '../../contract.js';

export const astrologyDefinition: ToolDefinition = {
  name: 'astrology',
  description: '西方占星命盘 - 根据出生信息计算本命盘与流运盘，输出基础坐标、命盘锚点、本命主星与流运触发。',
  inputSchema: {
    type: 'object',
    properties: {
      birthYear: { type: 'number', description: '出生年 (> 0)' },
      birthMonth: { type: 'number', description: '出生月 (1-12)' },
      birthDay: { type: 'number', description: '出生日 (1-31)' },
      birthHour: { type: 'number', description: '出生时 (0-23)' },
      birthMinute: { type: 'number', description: '出生分 (0-59)', default: 0 },
      latitude: { type: 'number', description: '出生地纬度 (-90 到 90)' },
      longitude: { type: 'number', description: '出生地经度 (-180 到 180)' },
      birthPlace: { type: 'string', description: '出生地点文本' },
      transitDateTime: { type: 'string', description: '流运时刻（YYYY-MM-DDTHH:mm[:ss] 或带时区偏移的 ISO 时间；省略时取当前时刻）' },
      houseSystem: { type: 'string', enum: ['placidus'], description: '宫制类型（placidus）', default: 'placidus' },
      detailLevel: {
        type: 'string',
        enum: ['default', 'more', 'full'],
        description: '输出细节级别。',
        default: 'default',
      },
    },
    required: ['birthYear', 'birthMonth', 'birthDay', 'birthHour'],
    allOf: [
      {
        if: {
          required: ['latitude'],
        },
        then: {
          required: ['longitude'],
        },
      },
      {
        if: {
          required: ['longitude'],
        },
        then: {
          required: ['latitude'],
        },
      },
      {
        if: {
          properties: {
            detailLevel: { const: 'full' },
          },
          required: ['detailLevel'],
        },
        then: {
          required: ['latitude', 'longitude'],
        },
      },
    ],
    examples: [
      {
        birthYear: 1990,
        birthMonth: 1,
        birthDay: 1,
        birthHour: 12,
        birthMinute: 30,
        latitude: 40.7128,
        longitude: -74.006,
        transitDateTime: '2026-04-10T09:30:00',
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
