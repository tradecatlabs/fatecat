/**
 * @file Bazi Utils
 * @description Contains stateless utility functions for Bazi calculations.
 */

import { BASIC_MAPPINGS, HIDDEN_STEMS, SEASON_STATUS, shenShaTypes } from './baziDefinitions';
import type { Wuxing } from './baziTypes';

const ctg = BASIC_MAPPINGS.HEAVENLY_STEMS as readonly string[];
const cdz = BASIC_MAPPINGS.EARTHLY_BRANCHES as readonly string[];
const wxtg = BASIC_MAPPINGS.STEM_WUXING as Wuxing[];
const wxdz = BASIC_MAPPINGS.BRANCH_WUXING as Wuxing[];

/**
 * 获取天干或地支的五行
 */
export function getWuxing(ganOrZhi: string): Wuxing | '未知' {
  const stemIndex = ctg.indexOf(ganOrZhi);
  if (stemIndex !== -1) return wxtg[stemIndex];
  const branchIndex = cdz.indexOf(ganOrZhi);
  if (branchIndex !== -1) return wxdz[branchIndex];
  return '未知';
}

/**
 * 获取天干阴阳
 */
export function getGanYinYang(gan: string): string {
  const stemIndex = ctg.indexOf(gan);
  if (stemIndex === -1) return '未知';
  return BASIC_MAPPINGS.STEM_YINYANG[stemIndex];
}

/**
 * 获取两个天干之间的十神关系
 */
export function getTenGod(gan: string, dayMaster: string): string {
  const ganIndex = ctg.indexOf(gan);
  const dayMasterIndex = ctg.indexOf(dayMaster);
  if (ganIndex === -1 || dayMasterIndex === -1) return '未知';
  const tenGodMatrix = [
    ['比肩', '劫财', '食神', '伤官', '偏财', '正财', '七杀', '正官', '偏印', '正印'],
    ['劫财', '比肩', '伤官', '食神', '正财', '偏财', '正官', '七杀', '正印', '偏印'],
    ['偏印', '正印', '比肩', '劫财', '食神', '伤官', '偏财', '正财', '七杀', '正官'],
    ['正印', '偏印', '劫财', '比肩', '伤官', '食神', '正财', '偏财', '正官', '七杀'],
    ['七杀', '正官', '偏印', '正印', '比肩', '劫财', '食神', '伤官', '偏财', '正财'],
    ['正官', '七杀', '正印', '偏印', '劫财', '比肩', '伤官', '食神', '正财', '偏财'],
    ['偏财', '正财', '七杀', '正官', '偏印', '正印', '比肩', '劫财', '食神', '伤官'],
    ['正财', '偏财', '正官', '七杀', '正印', '偏印', '劫财', '比肩', '伤官', '食神'],
    ['食神', '伤官', '偏财', '正财', '七杀', '正官', '偏印', '正印', '比肩', '劫财'],
    ['伤官', '食神', '正财', '偏财', '正官', '七杀', '正印', '偏印', '劫财', '比肩'],
  ];
  return tenGodMatrix[dayMasterIndex][ganIndex];
}

/**
 * 获取地支对应的十神（取藏干主气）
 */
export function getTenGodForBranch(zhi: string, dayMaster: string): string {
  const mainHiddenStem = HIDDEN_STEMS[zhi]?.[0];
  if (mainHiddenStem) {
    return getTenGod(mainHiddenStem, dayMaster);
  }
  return '未知';
}

/**
 * 获取月支对应的五行旺衰状态
 * @param monthBranch 月支
 * @returns 一个包含各五行状态的对象
 */
export function getSeasonStatus(monthBranch: string): Record<string, string> {
  return SEASON_STATUS[monthBranch] || {};
}
/**
 * 获取神煞属性 (吉/凶/中性)
 * @param shensha 神煞名称
 * @returns 属性名称
 */
export const getShenShaType = (shensha: string): '吉' | '凶' | '中性' => {
  if (shenShaTypes.lucky.includes(shensha)) {
    return '吉';
  } else if (shenShaTypes.unlucky.includes(shensha)) {
    return '凶';
  } else {
    return '中性';
  }
};
