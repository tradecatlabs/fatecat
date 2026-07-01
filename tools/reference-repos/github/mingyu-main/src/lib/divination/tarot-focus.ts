import type { TarotData } from '../../types/divination';

type TarotFocusRule = {
  spreadTypes?: string[];
  positionKeywords: string[];
};

const TAROT_POSITION_PRIORITY: TarotFocusRule[] = [
  {
    spreadTypes: ['single'],
    positionKeywords: ['当前指引'],
  },
  {
    spreadTypes: ['three'],
    positionKeywords: ['现在', '未来', '过去'],
  },
  {
    spreadTypes: ['love'],
    positionKeywords: ['关系现状', '发展建议', '未来走向', '你的内心', '对方的内心'],
  },
  {
    spreadTypes: ['career'],
    positionKeywords: ['当前状况', '行动建议', '结果', '机会', '挑战', '优势'],
  },
  {
    spreadTypes: ['decision'],
    positionKeywords: ['现状', '最佳建议', '选择A结果', '选择B结果', '选择A', '选择B'],
  },
];

export function formatTarotCardLabel(card: TarotData['cards'][number]) {
  return `${card.position}${card.name}（${card.reversed ? '逆位' : '正位'}）`;
}

export function getTarotFocusCards(data: TarotData) {
  if (!data.cards?.length) {
    return [];
  }

  const matchedRule = TAROT_POSITION_PRIORITY.find(
    (rule) => !rule.spreadTypes || rule.spreadTypes.includes(data.spreadType),
  );

  if (!matchedRule) {
    return data.cards.slice(0, 3);
  }

  const ordered = matchedRule.positionKeywords
    .map((keyword) => data.cards.find((card) => card.position.includes(keyword)))
    .filter((card): card is TarotData['cards'][number] => Boolean(card));

  const unique = ordered.filter(
    (card, index) => ordered.findIndex((item) => item === card) === index,
  );
  return unique.length > 0 ? unique.slice(0, 3) : data.cards.slice(0, 3);
}
