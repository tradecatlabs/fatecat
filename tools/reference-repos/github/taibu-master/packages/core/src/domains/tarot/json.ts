import type {
  TarotCanonicalJSON
} from './json-types.js';
import {
  normalizeDetailLevelBinary
} from '../../shared/render-utils.js';
import type {
  TarotOutput
} from './types.js';
import type {
  TarotCanonicalTextOptions
} from '../shared/text-options.js';

export function renderTarotCanonicalJSON(
  result: TarotOutput,
  options: TarotCanonicalTextOptions = {},
): TarotCanonicalJSON {
  const detailLevel = normalizeDetailLevelBinary(options.detailLevel);
  const birthDate = options.birthDate?.trim() || result.birthDate;
  const basicInfo: TarotCanonicalJSON['问卜设定'] = { 牌阵: result.spreadName };
  if (result.question) basicInfo.问题 = result.question;
  if (detailLevel === 'full' && birthDate) basicInfo.出生日期 = birthDate;
  if (detailLevel === 'full' && result.seed) basicInfo.随机种子 = result.seed;

  const cards = result.cards.map((card) => {
    const isReversed = card.orientation === 'reversed';
    const entry: TarotCanonicalJSON['牌阵展开'][number] = {
      位置: card.position,
      塔罗牌: card.card.nameChinese,
      状态: isReversed ? '逆位' : '正位',
      核心基调: isReversed && card.reversedKeywords?.length ? card.reversedKeywords : card.card.keywords,
    };
    if (card.element) entry.元素 = card.element;
    if (card.astrologicalCorrespondence) entry.星象 = card.astrologicalCorrespondence;
    return entry;
  });

  const json: TarotCanonicalJSON = { 问卜设定: basicInfo, 牌阵展开: cards };

  if (detailLevel === 'full' && result.numerology) {
    json.求问者生命数字 = {
      人格牌: {
        对应塔罗: result.numerology.personalityCard.nameChinese,
        背景基调: result.numerology.personalityCard.keywords || [],
        元素: result.numerology.personalityCard.element,
        星象: result.numerology.personalityCard.astrologicalCorrespondence,
      },
      灵魂牌: {
        对应塔罗: result.numerology.soulCard.nameChinese,
        背景基调: result.numerology.soulCard.keywords || [],
        元素: result.numerology.soulCard.element,
        星象: result.numerology.soulCard.astrologicalCorrespondence,
      },
      年度牌: {
        年份: result.numerology.yearlyCard.year!,
        对应塔罗: result.numerology.yearlyCard.nameChinese,
        背景基调: result.numerology.yearlyCard.keywords || [],
        元素: result.numerology.yearlyCard.element,
        星象: result.numerology.yearlyCard.astrologicalCorrespondence,
      },
    };
  }

  return json;
}

// ===== 紫微 =====
