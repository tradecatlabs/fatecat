/**
 * 共享工具函数和常量
 *
 * 干支基础常量统一从 ../data/ganzhi.ts 汇总导出。
 */

import {
  DI_ZHI,
  GAN_WUXING,
  getStemYinYang,
  TIAN_GAN,
} from '../data/ganzhi.js';

export {
  DI_ZHI,
  GAN_WUXING, getStemYinYang, STEM_ELEMENTS, TIAN_GAN, YI_MA_MAP, ZHI_WUXING
} from '../data/ganzhi.js';
export type { DiZhi, TianGan } from '../data/ganzhi.js';

// 五行顺序
export const WU_XING_ORDER = ['木', '火', '土', '金', '水'];

// 获取五行生克关系
export function getElementRelation(from: string, to: string): string {
  const fromIdx = WU_XING_ORDER.indexOf(from);
  const toIdx = WU_XING_ORDER.indexOf(to);

  if (from === to) return 'same';
  if ((fromIdx + 1) % 5 === toIdx) return 'produce';
  if ((toIdx + 1) % 5 === fromIdx) return 'produced';
  if ((fromIdx + 2) % 5 === toIdx) return 'control';
  return 'controlled';
}

// 计算十神
export function calculateTenGod(dayStem: string, targetStem: string): string {
  if (dayStem === targetStem) return '比肩';

  const dayElement = GAN_WUXING[dayStem];
  const targetElement = GAN_WUXING[targetStem];
  const dayYY = getStemYinYang(dayStem);
  const targetYY = getStemYinYang(targetStem);
  const sameYY = dayYY === targetYY;

  const relation = getElementRelation(dayElement, targetElement);

  const tenGodMap: Record<string, [string, string]> = {
    'same': ['比肩', '劫财'],
    'produce': ['食神', '伤官'],
    'control': ['偏财', '正财'],
    'controlled': ['七杀', '正官'],
    'produced': ['偏印', '正印'],
  };

  return tenGodMap[relation][sameYY ? 0 : 1];
}

// 共享八字规则表（从 shensha 导入）
import { DI_SHI_ORDER, XUN_KONG_TABLE } from '../data/shensha.js';

const DI_SHI_START_BRANCH: Record<string, string> = {
  '甲': '亥',
  '乙': '午',
  '丙': '寅',
  '丁': '酉',
  '戊': '寅',
  '己': '酉',
  '庚': '巳',
  '辛': '子',
  '壬': '申',
  '癸': '卯',
};

// 计算空亡
export function getKongWang(dayGan: string, dayZhi: string): { xun: string; kongZhi: [string, string]; } {
  const ganIdx = TIAN_GAN.indexOf(dayGan as typeof TIAN_GAN[number]);
  const zhiIdx = DI_ZHI.indexOf(dayZhi as typeof DI_ZHI[number]);
  if (ganIdx < 0 || zhiIdx < 0) {
    return { xun: '甲子旬', kongZhi: XUN_KONG_TABLE['甲子旬'] };
  }

  const xunStart = (zhiIdx - ganIdx + 12) % 12;
  const xunNames = ['甲子旬', '甲戌旬', '甲申旬', '甲午旬', '甲辰旬', '甲寅旬'];
  const xunStartZhi = ['子', '戌', '申', '午', '辰', '寅'];
  const startZhi = DI_ZHI[xunStart];
  const xunIdx = xunStartZhi.indexOf(startZhi);
  const xun = xunNames[xunIdx] || '甲子旬';

  return {
    xun,
    kongZhi: XUN_KONG_TABLE[xun],
  };
}

// 获取十二长生（按日主天干）
export function getDiShi(dayStem: string, branch: string): string {
  const startBranch = DI_SHI_START_BRANCH[dayStem];
  const startIdx = DI_ZHI.indexOf(startBranch as typeof DI_ZHI[number]);
  const branchIdx = DI_ZHI.indexOf(branch as typeof DI_ZHI[number]);
  if (startIdx < 0 || branchIdx < 0) return '';

  const isYang = getStemYinYang(dayStem) === 'yang';
  const offset = isYang
    ? (branchIdx - startIdx + 12) % 12
    : (startIdx - branchIdx + 12) % 12;

  return DI_SHI_ORDER[offset] || '';
}
