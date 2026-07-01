/**
 * 渲染层共享工具函数
 * 消除 text.ts / json.ts 之间的重复实现
 */

import type { DetailLevel } from '../domains/shared/types.js';
import type { ZiweiOutput } from '../domains/ziwei/types.js';

// ===== DetailLevel 归一化 =====

/**
 * 2 级归一化：将 detailLevel 映射到 'default' | 'full'
 * 适用于大多数术数的 text / json 渲染。
 */
export function normalizeDetailLevelBinary(
  detailLevel?: DetailLevel,
): 'default' | 'full' {
  if (detailLevel === 'full' || detailLevel === 'more') {
    return 'full';
  }
  return 'default';
}

/**
 * 3 级归一化：将 detailLevel 映射到 'default' | 'more' | 'full'
 * 仅用于六爻这类确实存在中间层级输出的场景。
 */
export function normalizeDetailLevel3Way(
  detailLevel?: DetailLevel,
): DetailLevel {
  if (detailLevel === 'more') return 'more';
  if (detailLevel === 'full') return 'full';
  return 'default';
}

// ===== 共享 Helper 函数 =====

/**
 * 构建神系 Map：以 targetLiuQin 为 key
 * 用于六爻渲染中快速查找用神/原神/忌神/仇神的归属
 */
export function buildShenSystemMap<T extends { targetLiuQin: string; }>(systems: T[]): Map<string, T> {
  return new Map(systems.map((system) => [system.targetLiuQin, system] as const));
}

/**
 * 六爻关系标签映射：过滤掉"平"标签
 */
export function mapLiuyaoRelationLabel(label: string | undefined): string | undefined {
  if (!label || label === '平') return undefined;
  return label;
}

/**
 * 格式化紫微规范农历日期：用干支年替换原始文本中的年份部分
 */
export function formatZiweiCanonicalLunarDate(result: ZiweiOutput): string {
  const raw = result.lunarDate?.trim();
  if (!raw) return '';
  const yearLabel = `${result.fourPillars.year.gan}${result.fourPillars.year.zhi}年`;
  if (!raw.includes('年')) return raw;
  const [, ...rest] = raw.split('年');
  const suffix = rest.join('年').trim();
  return suffix ? `${yearLabel}${suffix}` : yearLabel;
}

/**
 * 紫微飞星查询类型映射：英文 key → 中文标签
 */
export function mapZiweiFlyingStarQueryType(type: string): string {
  switch (type) {
    case 'fliesTo':
      return '飞化判断';
    case 'selfMutaged':
      return '自化判断';
    case 'mutagedPlaces':
      return '四化落宫';
    case 'surroundedPalaces':
      return '三方四正';
    default:
      return type;
  }
}
