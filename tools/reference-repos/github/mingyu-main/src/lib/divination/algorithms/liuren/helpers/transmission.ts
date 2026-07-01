import type {
  LiurenClassicalRule,
  LiurenData,
  LiurenTransmission,
} from '../../../../../types/divination';

const LIUCHONG_MAP: Record<string, string> = {
  子: '午',
  丑: '未',
  寅: '申',
  卯: '酉',
  辰: '戌',
  巳: '亥',
  午: '子',
  未: '丑',
  申: '寅',
  酉: '卯',
  戌: '辰',
  亥: '巳',
};

export function buildTransmissionNote(stage: LiurenTransmission['stage'], relation: string) {
  const stagePrefixMap: Record<LiurenTransmission['stage'], string> = {
    初传: '事情起点',
    中传: '过程阶段',
    末传: '结果落点',
  };

  if (relation === '比和') {
    return `${stagePrefixMap[stage]}偏平稳，可按既定节奏推进。`;
  }
  if (relation.includes('生')) {
    return `${stagePrefixMap[stage]}有承接与转机，适合顺势发力。`;
  }
  if (relation.includes('克')) {
    return `${stagePrefixMap[stage]}阻力更明显，宜先拆解卡点。`;
  }

  return `${stagePrefixMap[stage]}变化较杂，需要边走边校正。`;
}

export function getTransmissionPattern(
  chu: string,
  zhong: string,
  mo: string,
): LiurenData['transmissionPattern'] {
  if (chu === zhong && zhong === mo) {
    return '伏吟';
  }
  if (LIUCHONG_MAP[chu] === mo) {
    return '反吟';
  }
  if (chu === mo) {
    return '回环';
  }

  return '递传';
}

export function getPatternTag(pattern: LiurenData['transmissionPattern']) {
  if (pattern === '伏吟') {
    return '伏吟';
  }
  if (pattern === '反吟') {
    return '反吟';
  }
  if (pattern === '回环') {
    return '回环';
  }

  return '递传';
}

export function buildTransmissionDetail(
  rule: string,
  _pattern: LiurenData['transmissionPattern'],
  transmissions: LiurenTransmission[],
  classicalRule?: LiurenClassicalRule,
) {
  const initialTransmission = transmissions[0];
  if (!initialTransmission) {
    throw new Error('buildTransmissionDetail 需要至少包含初传信息。');
  }
  const sourceText = classicalRule
    ? `；古籍依据按${classicalRule.source}之${classicalRule.rule}，${classicalRule.summary}`
    : '';
  return `取传采用${rule}，以${initialTransmission.stage}${initialTransmission.branch}为初传发用${sourceText}。`;
}
