import type { ToolDefinition } from '../../contract.js';

export const qimenCalculateDefinition: ToolDefinition = {
  name: 'qimen',
  description: '奇门遁甲排盘 - 根据指定时间排出奇门盘，输出九宫、九星、八门、八神、格局等信息。',
  inputSchema: {
    type: 'object',
    properties: {
      year: { type: 'number', description: '年 (1900-2100)' },
      month: { type: 'number', description: '月 (1-12)' },
      day: { type: 'number', description: '日 (1-31)' },
      hour: { type: 'number', description: '时 (0-23)' },
      minute: { type: 'number', description: '分 (0-59)', default: 0 },
      timezone: { type: 'string', description: 'IANA 时区', default: 'Asia/Shanghai' },
      question: { type: 'string', description: '占问事项' },
      panType: { type: 'string', enum: ['zhuan'], description: '盘式（zhuan=转盘）', default: 'zhuan' },
      juMethod: { type: 'string', enum: ['chaibu', 'maoshan'], description: '定局法（chaibu=拆补，maoshan=茅山）', default: 'chaibu' },
      zhiFuJiGong: { type: 'string', enum: ['ji_liuyi', 'ji_wugong'], description: '直符寄宫方式（ji_liuyi=寄六仪，ji_wugong=寄戊宫）', default: 'ji_liuyi' },
      detailLevel: {
        type: 'string',
        enum: ['default', 'full'],
        description: '输出细节级别。',
        default: 'default',
      },
    },
    required: ['year', 'month', 'day', 'hour'],
    examples: [
      { year: 2026, month: 3, day: 15, hour: 16, minute: 51, timezone: 'Asia/Shanghai', question: '事业发展如何？' },
    ],
  },
  annotations: {
    readOnlyHint: true,
    destructiveHint: false,
    idempotentHint: true,
    openWorldHint: false,
  },
};
export const qimenDefinition = qimenCalculateDefinition;
