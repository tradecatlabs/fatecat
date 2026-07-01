import type { BaziArray } from './types';

/**
 * 全局神煞分析（基于已识别的神煞列表）
 */
export function analyzeGlobalShenSha(shenShaList: string[]): string[] {
  const analysis: string[] = [];

  if (shenShaList.includes('三奇贵人')) {
    analysis.push('整局天干顺布三奇，传统多视为悟性、机缘与贵人助力较易形成合力。');
  }

  return analysis;
}

/**
 * 计算全局神煞（四柱整体相关的神煞）
 */
export function calculateGlobalShenSha(baziArray: BaziArray): string[] {
  const globalShenSha: string[] = [];
  const gans = baziArray.map(([gan]) => gan);
  // 三奇贵人：《协纪辨方书》天上三奇甲戊庚、地下三奇乙丙丁、人中三奇辛壬癸。
  // 传统需天干按序在年/月/日/时中连续三柱顺布（如甲-戊-庚），原允许间隔为简化口径。
  const sequences: string[][] = [
    ['甲', '戊', '庚'], // 天上三奇
    ['乙', '丙', '丁'], // 地下三奇
    ['辛', '壬', '癸'], // 人中三奇
  ];
  const checks = [
    [gans[0], gans[1], gans[2]], // 年-月-日
    [gans[1], gans[2], gans[3]], // 月-日-时
  ];
  for (const seq of sequences) {
    if (checks.some(([a, b, c]) => a === seq[0] && b === seq[1] && c === seq[2])) {
      globalShenSha.push('三奇贵人');
      break;
    }
  }

  return globalShenSha;
}
