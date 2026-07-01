import type { ToolDefinition } from '../../contract.js';

export const daliurenDefinition: ToolDefinition = {
  name: 'daliuren',
  description: '大六壬排盘 - 根据日期时间起课，输出天地盘、四课、三传、神将、课体与时空信息。',
  inputSchema: {
    type: 'object',
    properties: {
      date: { type: 'string', description: '公历日期 (YYYY-MM-DD)' },
      hour: { type: 'number', description: '小时 (0-23)' },
      minute: { type: 'number', description: '分钟 (0-59)', default: 0 },
      timezone: { type: 'string', description: 'IANA 时区', default: 'Asia/Shanghai' },
      question: { type: 'string', description: '占事' },
      birthYear: { type: 'number', description: '出生年，用于本命/行年' },
      gender: { type: 'string', enum: ['male', 'female'], description: '性别，用于行年' },
      detailLevel: {
        type: 'string',
        enum: ['default', 'full'],
        description: '输出细节级别。',
        default: 'default',
      },
    },
    required: ['date', 'hour'],
    examples: [
      { date: '2026-03-15', hour: 16, minute: 53, timezone: 'Asia/Shanghai', question: '今日运势如何' },
      { date: '2026-03-15', hour: 16, timezone: 'Asia/Shanghai', birthYear: 1990, gender: 'male' },
    ],
  },
  annotations: {
    readOnlyHint: true,
    destructiveHint: false,
    idempotentHint: true,
    openWorldHint: false,
  },
};
