import { map, pipe } from "remeda";

import type { ZiWeiRuntime } from "../context";
import type { StemBranch } from "../rules/palace";
import type { Star, StemKey } from "../typings";

import { BRANCH_KEYS } from "../constants";
import { createStar } from "../models/star";
import {
  createMajorStarsMeta,
  createMinorStarsMeta,
  getMinorStarIndices,
  memoCalculateStarTransformation,
} from "../rules/star";
import { oppositeIndex, wrapIndex } from "../utils/math";

export type StarsCalculateParams = Omit<
  MajorStarsCalculateParams & MinorStarsCalculateParams,
  "stars"
>;

export function calculateStars(
  ctx: ZiWeiRuntime,
  {
    stemBranches,
    ziweiIndex,
    tianfuIndex,
    birthYearStemKey,
    monthIndex,
    hourIndex,
  }: StarsCalculateParams,
) {
  const stars = map(BRANCH_KEYS, () => []);
  if (ctx.configs.star === "onlyMajor") {
    return calculateMajorStars(ctx, {
      stars,
      stemBranches,
      ziweiIndex,
      tianfuIndex,
      birthYearStemKey,
    });
  }
  return pipe(
    stars,
    (stars) =>
      calculateMajorStars(ctx, {
        stars,
        stemBranches,
        ziweiIndex,
        tianfuIndex,
        birthYearStemKey,
      }),
    (stars) =>
      calculateMinorStars(ctx, {
        stars,
        stemBranches,
        monthIndex,
        hourIndex,
        birthYearStemKey,
      }),
  );
}

export interface MajorStarsCalculateParams {
  stars: Star[][];
  /** 十二宫天干序列 */
  stemBranches: StemBranch[];
  /** 紫微星的索引 */
  ziweiIndex: number;
  /** 天府星的索引 */
  tianfuIndex: number;
  /** 出生年干 Key */
  birthYearStemKey: StemKey;
}

/**
 * 计算紫微斗数的主星分布
 *
 * 此函数根据出生日期、五行局数值以及天干信息，计算主星的宫位分布和化曜情况。
 *
 * @param params - 计算主星所需的参数
 * @param params.day - 出生日期，用于确定星曜分布的起始点
 * @param params.fiveElementNumValue - 五行局的数值，用于计算星曜位置
 * @param params.birthYearStemKey - 出生天干的键值，用于确定星曜化曜类型
 *
 * @returns 返回一个包含星曜分布的数组，每个宫位包含对应的星曜信息
 */
export function calculateMajorStars(
  ctx: ZiWeiRuntime,
  { stars, stemBranches, ziweiIndex, tianfuIndex, birthYearStemKey }: MajorStarsCalculateParams,
) {
  const _majorStars = createMajorStarsMeta(
    ziweiIndex,
    tianfuIndex,
    ctx.configs.star === "onlyTransformation",
  );

  return _majorStars.reduce((result, { key, startIndex, direction, galaxy }, index) => {
    if (key) {
      const targetIndex = wrapIndex(startIndex + direction * (index - (index >= 9 ? 9 : 0)));
      const stemKey = stemBranches[targetIndex].stemKey;
      const oppositeStemKey = stemBranches[oppositeIndex(targetIndex)].stemKey;

      const yt_key = memoCalculateStarTransformation({
        stemKey: birthYearStemKey,
        starKey: key,
      });

      const st_exit_key = memoCalculateStarTransformation({
        stemKey,
        starKey: key,
      });
      const st_entry_key = memoCalculateStarTransformation({
        stemKey: oppositeStemKey,
        starKey: key,
      });

      const star = createStar({
        key,
        name: ctx.i18n.$t(`star.${key}.name`),
        abbr: ctx.i18n.$t(`star.${key}.abbr`),
        type: "major",
        galaxy,
        YT: yt_key && {
          key: yt_key,
          name: ctx.i18n.$t(`transformation.${yt_key}`),
        },
        ST: {
          exit: st_exit_key && {
            key: st_exit_key,
            name: ctx.i18n.$t(`transformation.${st_exit_key}`),
          },
          entry: st_entry_key && {
            key: st_entry_key,
            name: ctx.i18n.$t(`transformation.${st_entry_key}`),
          },
        },
      });
      result[targetIndex].push(star);
    }
    return result;
  }, stars);
}

export interface MinorStarsCalculateParams {
  stars: Star[][];
  /** 十二宫天干序列 */
  stemBranches: StemBranch[];
  /** 出生月数索引 */
  monthIndex: number;
  /** 出生时辰索引 */
  hourIndex: number;
  /** 出生年干 Key  */
  birthYearStemKey: StemKey;
}

/**
 * 计算并安置左右昌曲小星
 *
 * 此函数根据农历月份、时辰以及年天干，计算左右昌曲小星的排列位置，并生成包含完整星曜信息的数据结构。
 *
 * @param params - 一个包含以下字段的参数对象：
 * - `monthIndex` - 农历月份索引（范围：0-11），用于确定小星的排列索引。
 * - `hourIndex` - 时辰对应的地支索引（范围：0-11，其中 0 表示子时，1 表示丑时，以此类推）。
 * - `birthYearStemKey` - 出生年干（`StemKey` 类型），用于计算星曜的四化。
 *
 * @returns 返回一个包含左右昌曲小星的星曜数据结构，每个宫位包含一个星曜数组。每颗星曜包含以下信息：
 * - `key`: 星曜的唯一标识符。
 * - `nameKey`: 星曜名称的Key
 * - `type`: 星曜的类型（固定为 `"minor"`）。
 * - `galaxy`: 星曜所属的星系
 * - `YT`: 星曜的四化结果（由年天干与星曜的交互计算得出）。
 */
export function calculateMinorStars(
  ctx: ZiWeiRuntime,
  { stars, stemBranches, monthIndex, hourIndex, birthYearStemKey }: MinorStarsCalculateParams,
) {
  const minorStarIndices = getMinorStarIndices(monthIndex, hourIndex);
  const _minorStars = createMinorStarsMeta(minorStarIndices);

  return _minorStars.reduce((result, { key, startIndex, galaxy }) => {
    if (key) {
      const stemKey = stemBranches[startIndex].stemKey;
      const oppositeStemKey = stemBranches[oppositeIndex(startIndex)].stemKey;

      const yt_key = memoCalculateStarTransformation({
        stemKey: birthYearStemKey,
        starKey: key,
      });

      const st_exit_key = memoCalculateStarTransformation({
        stemKey,
        starKey: key,
      });
      const st_entry_key = memoCalculateStarTransformation({
        stemKey: oppositeStemKey,
        starKey: key,
      });

      const star = createStar({
        key,
        name: ctx.i18n.$t(`star.${key}.name`),
        abbr: ctx.i18n.$t(`star.${key}.abbr`),
        type: "minor",
        galaxy,
        YT: yt_key && {
          key: yt_key,
          name: ctx.i18n.$t(`transformation.${yt_key}`),
        },
        ST: {
          exit: st_exit_key && {
            key: st_exit_key,
            name: ctx.i18n.$t(`transformation.${st_exit_key}`),
          },
          entry: st_entry_key && {
            key: st_entry_key,
            name: ctx.i18n.$t(`transformation.${st_entry_key}`),
          },
        },
      });
      result[startIndex].push(star);
    }
    return result;
  }, stars);
}

export interface StarsByStemBranchCalculateParams {
  birthYearStemKey: StemKey;
  stemBranches: StemBranch[];
  ziweiIndex: number;
  tianfuIndex: number;
}

// 根据指定的干支来计算星辰排列
export function calculateStarsByStemBranch(
  ctx: ZiWeiRuntime,
  { birthYearStemKey, ziweiIndex, tianfuIndex, stemBranches }: StarsByStemBranchCalculateParams,
) {
  const stars: Star[][] = map(BRANCH_KEYS, () => []);

  const _majorStars = createMajorStarsMeta(ziweiIndex, tianfuIndex);
  return _majorStars.reduce((result, { key, startIndex, direction, galaxy }, index) => {
    if (key) {
      const targetIndex = wrapIndex(startIndex + direction * (index - (index >= 9 ? 9 : 0)));
      const stemKey = stemBranches[targetIndex].stemKey;
      const oppositeStemKey = stemBranches[oppositeIndex(targetIndex)].stemKey;

      const yt_key = memoCalculateStarTransformation({
        stemKey: birthYearStemKey,
        starKey: key,
      });

      const st_exit_key = memoCalculateStarTransformation({
        stemKey,
        starKey: key,
      });
      const st_entry_key = memoCalculateStarTransformation({
        stemKey: oppositeStemKey,
        starKey: key,
      });

      const star = createStar({
        key,
        name: ctx.i18n.$t(`star.${key}.name`),
        abbr: ctx.i18n.$t(`star.${key}.abbr`),
        type: "major",
        galaxy,
        YT: yt_key && {
          key: yt_key,
          name: ctx.i18n.$t(`transformation.${yt_key}`),
        },
        ST: {
          exit: st_exit_key && {
            key: st_exit_key,
            name: ctx.i18n.$t(`transformation.${st_exit_key}`),
          },
          entry: st_entry_key && {
            key: st_entry_key,
            name: ctx.i18n.$t(`transformation.${st_entry_key}`),
          },
        },
      });
      result[targetIndex].push(star);
    }
    return result;
  }, stars);
}
