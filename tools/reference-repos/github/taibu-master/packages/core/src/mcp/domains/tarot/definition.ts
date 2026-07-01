import type { ToolDefinition } from '../../contract.js';

export const tarotDefinition: ToolDefinition = {
  name: 'tarot',
  description: '塔罗抽牌 - 根据问题与牌阵抽取塔罗牌，输出牌面结果及占卜参考信息。',
  inputSchema: {
    type: 'object',
    properties: {
      spreadType: {
        type: 'string',
        enum: ['single', 'three-card', 'love', 'celtic-cross', 'horseshoe', 'decision', 'mind-body-spirit', 'situation', 'yes-no'],
        description: '牌阵类型（single=单牌，three-card=三牌，love=爱情，celtic-cross=凯尔特十字，horseshoe=马蹄，decision=抉择，mind-body-spirit=身心灵，situation=处境，yes-no=是否）',
        default: 'single',
      },
      question: {
        type: 'string',
        description: '占卜问题',
      },
      allowReversed: {
        type: 'boolean',
        description: '是否允许逆位',
        default: true,
      },
      seed: {
        type: 'string',
        description: '随机种子',
      },
      birthYear: {
        type: 'number',
        description: '出生年，用于人格牌/灵魂牌/年度牌',
      },
      birthMonth: {
        type: 'number',
        description: '出生月 (1-12)，用于人格牌/灵魂牌/年度牌',
      },
      birthDay: {
        type: 'number',
        description: '出生日 (1-31)，用于人格牌/灵魂牌/年度牌',
      },
      detailLevel: {
        type: 'string',
        enum: ['default', 'full'],
        description: '输出细节级别。',
        default: 'default',
      },
    },
    required: [],
    examples: [
      { spreadType: 'three-card', question: '本月运势如何？' },
      { spreadType: 'love', question: '我和他的未来发展？', allowReversed: true },
      { spreadType: 'celtic-cross', question: '事业发展', birthYear: 1990, birthMonth: 5, birthDay: 15 },
    ],
  },
  annotations: {
    readOnlyHint: true,
    destructiveHint: false,
    idempotentHint: false,
    openWorldHint: false,
  },
};
