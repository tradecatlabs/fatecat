import type { ZiWeiRuntime } from "../context";
import type { FiveElementSchemeValue, Palace, StemKey } from "../typings";

import { PALACE_KEYS } from "../constants";
import { createPalace } from "../models/palace";
import { calculateDecadeRanges } from "../rules/decade";
import { calculateCurrentPalaceIndex, isLaiYin, type StemBranch } from "../rules/palace";
import { calculateStars, calculateStarsByStemBranch } from "./star";

export interface PalacesCalculateParams {
  /** 十二宫干支序列 */
  stemBranches: StemBranch[];
  /** 出生年干 Key */
  birthYearStemKey: StemKey;
  /** 命宫的索引 */
  mainPalaceIndex: number;
  /** 命宫的索引 */
  ziweiIndex: number;
  /** 命宫的索引 */
  tianfuIndex: number;
  /** 出生月数索引 */
  monthIndex: number;
  /** 出生时辰索引 */
  hourIndex: number;
  /** 大限流向，1为顺行，-1为逆行 */
  decadeDirection: 1 | -1;
  /** 五行局数 */
  fiveElementSchemeValue: FiveElementSchemeValue;
}

export function calculatePalaces(
  ctx: ZiWeiRuntime,
  {
    stemBranches,
    birthYearStemKey,
    mainPalaceIndex,
    ziweiIndex,
    tianfuIndex,
    monthIndex,
    hourIndex,
    decadeDirection,
    fiveElementSchemeValue,
  }: PalacesCalculateParams,
) {
  const stars = calculateStars(ctx, {
    stemBranches,
    birthYearStemKey,
    ziweiIndex,
    tianfuIndex,
    monthIndex,
    hourIndex,
  });

  const decadeRanges = calculateDecadeRanges(
    mainPalaceIndex,
    decadeDirection,
    fiveElementSchemeValue,
  );

  const palaces = stemBranches.map<Palace>(({ stemKey, branchKey }, index) => {
    const currentPalaceIndex = calculateCurrentPalaceIndex(mainPalaceIndex, index);
    const key = PALACE_KEYS[currentPalaceIndex];
    const palace = createPalace({
      index,
      key,
      name: ctx.i18n.$t(`palace.${key}.name`),
      stem: {
        key: stemKey,
        name: ctx.i18n.$t(`stem.${stemKey}`),
      },
      branch: {
        key: branchKey,
        name: ctx.i18n.$t(`branch.${branchKey}`),
      },
      isLaiYin: isLaiYin(birthYearStemKey, stemKey, branchKey),
      stars: stars[index],
      decadeRanges: decadeRanges[index],
    });
    return palace;
  });

  return palaces;
}

export interface PalacesByStemBranchCalculateParams {
  /** 十二宫干支序列 */
  stemBranches: StemBranch[];
  /** 出生年干 Key */
  birthYearStemKey: StemKey;
  /** 命宫索引 */
  mainPalaceIndex: number;
  ziweiIndex: number;
  tianfuIndex: number;
}

export function calculatePalacesByStemBranch(
  ctx: ZiWeiRuntime,
  {
    stemBranches,
    birthYearStemKey,
    mainPalaceIndex,
    ziweiIndex,
    tianfuIndex,
  }: PalacesByStemBranchCalculateParams,
) {
  const stars = calculateStarsByStemBranch(ctx, {
    stemBranches,
    birthYearStemKey,
    ziweiIndex,
    tianfuIndex,
  });

  const palaces = stemBranches.map<Palace>(({ stemKey, branchKey }, index) => {
    const currentPalaceIndex = calculateCurrentPalaceIndex(mainPalaceIndex, index);
    const key = PALACE_KEYS[currentPalaceIndex];
    const palace = createPalace({
      index,
      key,
      name: ctx.i18n.$t(`palace.${key}.name`),
      stem: {
        key: stemKey,
        name: ctx.i18n.$t(`stem.${stemKey}`),
      },
      branch: {
        key: branchKey,
        name: ctx.i18n.$t(`branch.${branchKey}`),
      },
      isLaiYin: isLaiYin(birthYearStemKey, stemKey, branchKey),
      stars: stars[index],
      decadeRanges: [],
    });
    return palace;
  });
  return palaces;
}
