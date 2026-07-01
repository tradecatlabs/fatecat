/**
 * 天干地支核心常量（单一来源）
 *
 * 所有模块应从此文件导入干支、五行映射等基础常量，
 * 避免在各处重复定义。
 */

import type { DiZhi as DiZhiType, TianGan as TianGanType } from '../domains/shared/types.js';

// 天干列表
export const TIAN_GAN = ['甲', '乙', '丙', '丁', '戊', '己', '庚', '辛', '壬', '癸'] as const;
export type TianGan = TianGanType;

// 地支列表
export const DI_ZHI = ['子', '丑', '寅', '卯', '辰', '巳', '午', '未', '申', '酉', '戌', '亥'] as const;
export type DiZhi = DiZhiType;

// 天干五行对应表
export const GAN_WUXING: Record<string, string> = {
  '甲': '木', '乙': '木',
  '丙': '火', '丁': '火',
  '戊': '土', '己': '土',
  '庚': '金', '辛': '金',
  '壬': '水', '癸': '水',
};

/** @deprecated 使用 GAN_WUXING 代替 */
export const STEM_ELEMENTS = GAN_WUXING;

// 地支五行对应表
export const ZHI_WUXING: Record<string, string> = {
  子: '水', 丑: '土', 寅: '木', 卯: '木', 辰: '土', 巳: '火',
  午: '火', 未: '土', 申: '金', 酉: '金', 戌: '土', 亥: '水',
};

// 驿马：日支三合局 → 马星地支
export const YI_MA_MAP: Record<string, string> = {
  '寅': '申', '午': '申', '戌': '申',
  '申': '寅', '子': '寅', '辰': '寅',
  '巳': '亥', '酉': '亥', '丑': '亥',
  '亥': '巳', '卯': '巳', '未': '巳',
};

// 获取天干阴阳
export function getStemYinYang(stem: string): 'yang' | 'yin' {
  const idx = TIAN_GAN.indexOf(stem as typeof TIAN_GAN[number]);
  return idx >= 0 && idx % 2 === 0 ? 'yang' : 'yin';
}
