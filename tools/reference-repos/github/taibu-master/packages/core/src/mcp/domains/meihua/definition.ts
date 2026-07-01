import type { ToolDefinition } from '../../contract.js';

export const meihuaDefinition: ToolDefinition = {
  name: 'meihua',
  description: '梅花易数起卦 - 根据时间、字占、物数、报数等方式起卦，输出起卦信息、卦盘与体用推演。',
  inputSchema: {
    type: 'object',
    properties: {
      question: {
        type: 'string',
        minLength: 1,
        description: '占卜问题',
      },
      date: {
        type: 'string',
        description: '起卦日期时间（YYYY-MM-DDTHH:MM[:SS]）',
      },
      method: {
        type: 'string',
        enum: ['time', 'count_with_time', 'text_split', 'measure', 'classifier_pair', 'select', 'number_pair', 'number_triplet'],
        description: '起卦方式（time=时间，count_with_time=物数或声数，text_split=字占，measure=丈尺尺寸，classifier_pair=类象对，select=指定卦，number_pair/number_triplet=报数）',
      },
      count: {
        type: 'number',
        description: '物数或声数起卦的数量',
      },
      countCategory: {
        type: 'string',
        enum: ['item', 'sound'],
        description: '数量来源（item=物数，sound=声数）',
      },
      text: {
        type: 'string',
        description: '字占文本。',
      },
      textSplitMode: {
        type: 'string',
        enum: ['auto', 'count', 'sentence_pair', 'stroke'],
        description: '字占拆分方式（auto=自动，count=按字数，sentence_pair=按句，stroke=按笔画）',
      },
      multiSentenceStrategy: {
        type: 'string',
        enum: ['first', 'last'],
        description: '多句文本的取句方式（first=首句，last=末句）',
      },
      sentences: {
        type: 'array',
        items: { type: 'string' },
        minItems: 2,
        maxItems: 2,
        description: '上下卦对应的两句文本',
      },
      leftStrokeCount: {
        type: 'number',
        description: '左半边或上半边笔画数',
      },
      rightStrokeCount: {
        type: 'number',
        description: '右半边或下半边笔画数',
      },
      measureKind: {
        type: 'string',
        enum: ['丈尺', '尺寸'],
        description: '量法（丈尺=丈尺，尺寸=尺寸）',
      },
      majorValue: {
        type: 'number',
        description: '大单位数值',
      },
      minorValue: {
        type: 'number',
        description: '小单位数值',
      },
      upperCue: {
        type: 'string',
        description: '上卦类象提示词',
      },
      upperCueCategory: {
        type: 'string',
        enum: ['direction', 'color', 'weather', 'person', 'body', 'animal', 'object', 'shape', 'trigram'],
        description: '上卦类象类别',
      },
      lowerCue: {
        type: 'string',
        description: '下卦类象提示词',
      },
      lowerCueCategory: {
        type: 'string',
        enum: ['direction', 'color', 'weather', 'person', 'body', 'animal', 'object', 'shape', 'trigram'],
        description: '下卦类象类别',
      },
      hexagramName: {
        type: 'string',
        description: '指定本卦卦名或卦码',
      },
      upperTrigram: {
        type: 'string',
        description: '指定上卦',
      },
      lowerTrigram: {
        type: 'string',
        description: '指定下卦',
      },
      movingLine: {
        type: 'number',
        description: '指定动爻 (1-6)',
      },
      numbers: {
        type: 'array',
        items: { type: 'number' },
        minItems: 2,
        maxItems: 3,
        description: '报数序列',
      },
      detailLevel: {
        type: 'string',
        enum: ['default', 'full'],
        description: '输出细节级别。',
        default: 'default',
      },
    },
    required: ['question', 'date'],
    allOf: [
      {
        if: {
          properties: {
            method: { const: 'count_with_time' },
          },
          required: ['method'],
        },
        then: {
          required: ['count', 'countCategory'],
        },
      },
      {
        if: {
          properties: {
            method: { const: 'text_split' },
          },
          required: ['method'],
        },
        then: {
          anyOf: [
            {
              properties: {
                textSplitMode: { const: 'stroke' },
              },
              required: ['textSplitMode', 'leftStrokeCount', 'rightStrokeCount'],
            },
            {
              properties: {
                textSplitMode: { const: 'sentence_pair' },
              },
              required: ['textSplitMode'],
              anyOf: [
                { required: ['sentences'] },
                { required: ['text'] },
              ],
            },
            {
              required: ['text'],
            },
          ],
        },
      },
      {
        if: {
          properties: {
            method: { const: 'measure' },
          },
          required: ['method'],
        },
        then: {
          required: ['measureKind', 'majorValue', 'minorValue'],
        },
      },
      {
        if: {
          properties: {
            method: { const: 'classifier_pair' },
          },
          required: ['method'],
        },
        then: {
          required: ['upperCue', 'lowerCue'],
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
          required: ['movingLine'],
          anyOf: [
            { required: ['hexagramName'] },
            { required: ['upperTrigram', 'lowerTrigram'] },
          ],
        },
      },
      {
        if: {
          properties: {
            method: { const: 'number_pair' },
          },
          required: ['method'],
        },
        then: {
          required: ['numbers'],
          properties: {
            numbers: {
              type: 'array',
              items: { type: 'number' },
              minItems: 2,
              maxItems: 2,
            },
          },
        },
      },
      {
        if: {
          properties: {
            method: { const: 'number_triplet' },
          },
          required: ['method'],
        },
        then: {
          required: ['numbers'],
          properties: {
            numbers: {
              type: 'array',
              items: { type: 'number' },
              minItems: 3,
              maxItems: 3,
            },
          },
        },
      },
    ],
    examples: [
      { question: '这次合作能否谈成？', method: 'time', date: '2026-04-04T10:30:00' },
      { question: '丢失物品能否找回？', method: 'count_with_time', count: 7, countCategory: 'item', date: '2026-04-04T10:30:00' },
      { question: '这件事进展如何？', method: 'measure', measureKind: '丈尺', majorValue: 2, minorValue: 3, date: '2026-04-04T10:30:00' },
      { question: '此事后续如何？', method: 'number_pair', numbers: [3, 8], date: '2026-04-04T10:30:00' },
    ],
  },
  annotations: {
    readOnlyHint: true,
    destructiveHint: false,
    idempotentHint: false,
    openWorldHint: false,
  },
};
