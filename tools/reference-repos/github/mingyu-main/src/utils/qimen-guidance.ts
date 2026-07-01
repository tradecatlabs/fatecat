import type { QimenData, SupplementaryInfo } from '../types/divination';
import { analyzeQuestion } from '../services/prompts/shared/question-analyzer';

interface QimenQuestionHint {
  label: string;
  value: string;
  gongs: number[];
}

interface QimenPriorityPalace {
  gong: number;
  name: string;
  score: number;
  reasons: string[];
}

export function createQimenQuestionHints(
  question: string | undefined,
  data: QimenData,
  supplementaryInfo?: SupplementaryInfo,
): QimenQuestionHint[] {
  if (!question?.trim()) {
    return [];
  }

  const analysis = analyzeQuestion(question);
  const hints: QimenQuestionHint[] = [];

  if (analysis.types.isCareer) {
    hints.push({
      label: '事业参考',
      ...joinParts([
        buildDoorHint(data, '开门', '首看开门'),
        buildDoorHint(data, '生门', '兼看生门'),
      ]),
    });
  }

  if (analysis.types.isFinance) {
    hints.push({
      label: '财运参考',
      ...joinParts([
        buildDoorHint(data, '生门', '首看生门'),
        buildDoorHint(data, '开门', '兼看开门'),
      ]),
    });
  }

  if (analysis.types.isRelationship) {
    const relationParts = [
      buildGodHint(data, '六合', '可参六合'),
      buildStemHint(
        data,
        '乙',
        supplementaryInfo?.gender === '男' ? '男测可重点看乙奇' : '乙奇可参',
      ),
      buildStemHint(
        data,
        '庚',
        supplementaryInfo?.gender === '女' ? '女测可重点看庚金' : '庚金可参',
      ),
    ];
    hints.push({
      label: '感情参考',
      ...joinParts(relationParts),
    });
  }

  if (analysis.types.isHealth) {
    hints.push({
      label: '健康参考',
      ...joinParts([
        buildStarHint(data, '天芮', '首看天芮'),
        buildDoorHint(data, '死门', '兼看死门'),
      ]),
    });
  }

  if (analysis.types.isStudy) {
    hints.push({
      label: '学业参考',
      ...joinParts([buildStarHint(data, '天辅', '首看天辅')]),
    });
  }

  return hints.filter((item) => item.value !== '未命中对应参考宫位');
}

export function createQimenPriorityPalaces(
  question: string | undefined,
  data: QimenData,
  supplementaryInfo?: SupplementaryInfo,
): QimenPriorityPalace[] {
  const palaceMap = new Map<number, QimenPriorityPalace>();

  const ensurePalace = (gong: number): QimenPriorityPalace | null => {
    const found = data.jiuGongGe.find((item) => item.gong === gong);
    if (!found) {
      return null;
    }
    const existing = palaceMap.get(gong);
    if (existing) {
      return existing;
    }
    const created: QimenPriorityPalace = {
      gong,
      name: found.name,
      score: 0,
      reasons: [],
    };
    palaceMap.set(gong, created);
    return created;
  };

  const questionHints = createQimenQuestionHints(question, data, supplementaryInfo);
  questionHints.forEach((hint, hintIndex) => {
    const baseScore = Math.max(0, 100 - hintIndex * 10);
    hint.gongs.forEach((gong, gongIndex) => {
      const palace = ensurePalace(gong);
      if (!palace) return;
      palace.score += Math.max(10, baseScore - gongIndex * 5);
      palace.reasons.push(hint.label);
    });
  });

  data.palaceInsights?.forEach((insight) => {
    const palace = ensurePalace(insight.gong);
    if (!palace) return;
    palace.score += getInsightScore(insight.level);
    palace.reasons.push(`${insight.level}:${insight.summary}`);
  });

  data.patternDetails?.forEach((detail) => {
    const matchedPalaces = data.jiuGongGe.filter(
      (gong) => detail.tag.includes(`（${gong.name}`) || detail.tag.includes(`落${gong.name}`),
    );
    matchedPalaces.forEach((gong) => {
      const palace = ensurePalace(gong.gong);
      if (!palace) return;
      palace.score += 15;
      palace.reasons.push(detail.tag);
    });
  });

  return Array.from(palaceMap.values())
    .map((item) => ({
      ...item,
      reasons: Array.from(new Set(item.reasons)),
    }))
    .sort((a, b) => {
      if (b.score !== a.score) {
        return b.score - a.score;
      }
      return a.gong - b.gong;
    });
}

function getInsightScore(level: '有利' | '风险' | '关注'): number {
  switch (level) {
    case '关注':
      return 28;
    case '有利':
      return 24;
    case '风险':
      return 20;
    default:
      return 0;
  }
}

function joinParts(parts: Array<{ text: string; gong?: number } | null>): {
  value: string;
  gongs: number[];
} {
  const validParts = parts.filter(
    (part): part is { text: string; gong?: number } => !!part && !!part.text,
  );
  return {
    value:
      validParts.length > 0 ? validParts.map((part) => part.text).join('；') : '未命中对应参考宫位',
    gongs: Array.from(
      new Set(
        validParts
          .map((part) => part.gong)
          .filter((gong): gong is number => typeof gong === 'number'),
      ),
    ),
  };
}

function buildDoorHint(
  data: QimenData,
  door: string,
  label: string,
): { text: string; gong: number } | null {
  const gong = data.jiuGongGe.find((item) => item.renPan.door === door);
  return gong ? { text: `${label}，当前落${gong.name}`, gong: gong.gong } : null;
}

function buildGodHint(
  data: QimenData,
  god: string,
  label: string,
): { text: string; gong: number } | null {
  const gong = data.jiuGongGe.find((item) => item.shenPan.god === god);
  return gong ? { text: `${label}，当前落${gong.name}`, gong: gong.gong } : null;
}

function buildStarHint(
  data: QimenData,
  star: string,
  label: string,
): { text: string; gong: number } | null {
  const gong = data.jiuGongGe.find((item) => item.tianPan.star === star);
  return gong ? { text: `${label}，当前落${gong.name}`, gong: gong.gong } : null;
}

function buildStemHint(
  data: QimenData,
  stem: string,
  label: string,
): { text: string; gong?: number } | null {
  const tianGong = data.jiuGongGe.find((item) => item.tianPan.stem === stem);
  const diGong = data.jiuGongGe.find((item) => item.diPan.stem === stem);
  const parts: string[] = [];
  const gongs: number[] = [];

  if (tianGong) {
    parts.push(`天盘落${tianGong.name}`);
    gongs.push(tianGong.gong);
  }
  if (diGong) {
    parts.push(`地盘落${diGong.name}`);
    gongs.push(diGong.gong);
  }

  return parts.length > 0 ? { text: `${label}，${parts.join('，')}`, gong: gongs[0] } : null;
}
