import type { BranchKey, StemKey } from "../typings";

import { BRANCH_KEYS, STEM_KEYS } from "../constants";
import { wrapIndex } from "../utils/math";

/**
 * 起宫干：依据出生年干，按“五虎遁月诀”推算十二宫天干。
 *
 * 五虎遁月诀（以年推月）：
 * - 天干与“起始天干”索引对应关系如下（括号内为索引）：
 *   - 甲(0)、己(5) → 丙(2)
 *   - 乙(1)、庚(6) → 戊(4)
 *   - 丙(2)、辛(7) → 庚(6)
 *   - 丁(3)、壬(8) → 壬(8)
 *   - 戊(4)、癸(9) → 甲(0)
 *
 * @param stemKey - 出生年天干的 Key（如 "Jia" | "Yi" | ...）
 * @returns 基于五虎遁月诀推演得到的十二宫天干序列或映射
 */
export function calculatePalaceStemsAndBranches(stemKey: StemKey) {
  // 定义每组天干对应的起始天干索引
  const startIndices = [2, 4, 6, 8, 0];
  // 计算当前天干的起始索引
  const startIndex = startIndices[STEM_KEYS.indexOf(stemKey) % startIndices.length];

  return calculateStemAndBranches(startIndex);
}

export interface StemBranch {
  stemKey: StemKey;
  branchKey: BranchKey;
}

/**
 * 根据起始天干生成五虎遁月表
 * @param startStemIndex 天干起始索引 (0-9)
 * @param startBranchIndex 地支起始索引 (0-11) 默认为寅
 * @returns string[] 包含12个月份的天干地支组合
 */
export function calculateStemAndBranches(startStemIndex: number, startBranchIndex: number = 2) {
  const stemLength = STEM_KEYS.length;
  const branchLength = BRANCH_KEYS.length;
  // 天干和地支分别循环取值
  return BRANCH_KEYS.map<StemBranch>((_, i) => {
    const stemKey = STEM_KEYS[(startStemIndex + i) % stemLength];
    const branchKey = BRANCH_KEYS[(startBranchIndex + i) % branchLength];

    return {
      stemKey,
      branchKey,
    };
  });
}

/**
 * 计算命宫的索引
 * @param monthIndex 出生月数的索引
 * @param hourIndex 出生时数的索引
 * @returns 命宫的索引
 */
export function calculateMainPalaceIndex(monthIndex: number, hourIndex: number) {
  // 寅起正月，顺月逆时为命宫
  return wrapIndex(monthIndex - hourIndex);
}

/**
 * 根据命宫索引计算当前宫位的宫职索引 - 默认从寅宫开始
 * @param mainPalaceIndex 命宫索引
 * @param currentPalaceIndex 当前宫位索引
 * @returns 当前宫位的宫职索引
 */
export function calculateCurrentPalaceIndex(mainPalaceIndex: number, currentPalaceIndex: number) {
  return wrapIndex(mainPalaceIndex - currentPalaceIndex);
}

/**
 * 判断是否为来因宫
 *
 * 根据年天干、月天干和地支判断是否满足来因宫的条件。
 * 来因宫的定义是年天干与月天干相同，且地支不为子或丑。
 *
 * @param yearStem - 年天干（`StemKey` 类型）
 * @param monthStem - 月天干（`StemKey` 类型）
 * @param branch - 地支（`BranchKey` 类型）
 *
 * @returns {boolean} 返回布尔值，表示是否为来因宫：
 * - `true`: 是来因宫
 * - `false`: 不是来因宫
 */
export function isLaiYin(yearStem: StemKey, monthStem: StemKey, branch: BranchKey): boolean {
  const branches: BranchKey[] = ["Zi", "Chou"];

  return yearStem === monthStem && !branches.includes(branch);
}
