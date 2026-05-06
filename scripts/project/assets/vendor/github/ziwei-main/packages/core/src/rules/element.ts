import type { BranchKey, StemKey } from "../typings";

import {
  BRANCH_KEYS,
  FIVE_ELEMENT_SCHEME,
  FIVE_ELEMENT_SCHEME_VALUE,
  FIVE_ELEMENT_TABLE,
  STEM_KEYS,
} from "../constants";

/**
 *
 * @param stemKey 出生年干
 * @param branchKey 命宫地支
 * @returns
 */
export function calculateFiveElementScheme(stemKey: StemKey, branchKey: BranchKey) {
  // 获取天干和地支的索引
  const stemIndex = STEM_KEYS.indexOf(stemKey);
  const branchIndex = BRANCH_KEYS.indexOf(branchKey);

  // 计算天干和地支对应的五行局编号
  const stemNumber = stemIndex % 5;
  const branchNumber = Math.floor(branchIndex / 2);

  // 计算五行局的信息
  const fiveElementSchemeKey = FIVE_ELEMENT_TABLE[stemNumber][branchNumber];
  const fiveElementSchemeName = FIVE_ELEMENT_SCHEME[fiveElementSchemeKey];
  const fiveElementSchemeValue = FIVE_ELEMENT_SCHEME_VALUE[fiveElementSchemeKey];

  return {
    fiveElementSchemeKey,
    fiveElementSchemeName,
    fiveElementSchemeValue,
  };
}
