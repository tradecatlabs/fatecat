import type { ToolDefinition } from '../../contract.js';

export const liuyaoDefinition: ToolDefinition = {
  name: 'liuyao',
  description: '六爻排卦 - 根据问题与起卦信息排出六爻盘面，输出卦象、爻位、用神体系、关系判断与时机提示。',
  inputSchema: {
    type: 'object',
    properties: {
      question: {
        type: 'string',
        minLength: 1,
        description: '占卜问题',
      },
      yongShenTargets: {
        type: 'array',
        minItems: 1,
        description: '用神目标列表，由调用方按占问主题选择',
        items: {
          type: 'string',
          enum: ['父母', '兄弟', '子孙', '妻财', '官鬼'],
        },
      },
      method: {
        type: 'string',
        enum: ['auto', 'select', 'time', 'number'],
        description: '起卦方式（auto=自动，select=指定卦，time=时间，number=数字）',
        default: 'auto',
      },
      numbers: {
        type: 'array',
        items: { type: 'number' },
        minItems: 2,
        maxItems: 3,
        description: '数字起卦使用的数字序列',
      },
      hexagramName: {
        type: 'string',
        description: '选卦模式下的本卦卦名或卦码',
      },
      changedHexagramName: {
        type: 'string',
        description: '选卦模式下的变卦卦名或卦码',
      },
      date: {
        type: 'string',
        description: '占卜日期时间（YYYY-MM-DDTHH:MM[:SS] 或 YYYY-MM-DD HH:MM[:SS]）',
      },
      detailLevel: {
        type: 'string',
        enum: ['default', 'more', 'full'],
        description: '输出细节级别。',
        default: 'default',
      },
    },
    required: ['question', 'yongShenTargets', 'date'],
    allOf: [
      {
        if: {
          properties: {
            method: { const: 'number' },
          },
          required: ['method'],
        },
        then: {
          required: ['numbers'],
        },
      },
      {
        if: {
          properties: {
            method: { const: 'select' },
          },
          required: ['method'],
        },
        then: {
          required: ['hexagramName'],
        },
      },
    ],
    examples: [
      { question: '本月事业运势如何？', yongShenTargets: ['官鬼'], method: 'auto', date: '2026-02-10T09:30:00' },
      { question: '财运怎么样？', yongShenTargets: ['妻财'], hexagramName: '天火同人', date: '2026-02-10 14:00:00' },
    ],
  },
  annotations: {
    readOnlyHint: true,
    destructiveHint: false,
    idempotentHint: false,
    openWorldHint: false,
  },
};
