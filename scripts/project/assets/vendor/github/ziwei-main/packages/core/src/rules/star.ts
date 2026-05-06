import type { FiveElementSchemeValue, StarKey, StarMetaVO, StemKey } from "../typings";

import { BRANCH_KEYS, STEM_TRANSFORMATIONS, TRANSFORMATION_KEYS } from "../constants";
import { relativeIndex, wrapIndex } from "../utils/math";
import { memoize } from "../utils/memoize";

/**
 * 取五行局数，以日数取其余数以求紫微之位
 *
 * @remarks
 * 此函数通过日数（day）和五行局数（fiveElementNumValue）计算紫微和天府的宫位索引。
 * 计算逻辑包括以下步骤：
 * 1. 计算偏移量 (`offset`)。
 * 2. 计算商数 (`quotient`) 并确定初始紫微宫位索引。
 * 3. 根据偏移量的奇偶性调整紫微宫位索引。
 * 4. 根据紫微宫位索引计算天府宫位索引，天府与紫微本对一线。
 *
 * 宫位的索引范围为 0 至 11，分别对应十二地支中的十二宫，起始点为寅宫（索引为 0）。
 *
 * @param day - 日期（正整数，通常代表农历的日期）。
 * @param fiveElementNumValue - 五行局数，用于计算偏移量和商数。
 * ```
 */
export function calculateStarIndex(day: number, fiveElementSchemeValue: FiveElementSchemeValue) {
  // 使用数学公式直接计算偏移量和索引，无需循环
  const offset = wrapIndex(-(day % fiveElementSchemeValue), fiveElementSchemeValue);
  const divisor = day + offset;
  const quotient = Math.floor(divisor / fiveElementSchemeValue) % 12; // 商取余数
  const ziweiIndex = wrapIndex(quotient - 1 + offset * (offset % 2 === 0 ? 1 : -1));
  return { ziweiIndex, tianfuIndex: relativeIndex(ziweiIndex) };
}

export interface MinorStarIndices {
  zuofuIndex: number;
  youbiIndex: number;
  wenchangIndex: number;
  wenquIndex: number;
}

/**
 * 获取左右昌曲的排列索引
 *
 * 根据农历的月份和时辰，计算并返回左辅、右弼、文昌、文曲四颗小星的排列索引。
 *
 * @param monthIndex - 农历的月份索引（范围：0-11），用于计算星曜的排列位置
 * @param hourIndex - 时辰对应的地支索引（范围：0-11，其中 0 表示子时，1 表示丑时，以此类推）
 *
 * @returns {MinorStarIndices} 返回一个包含四颗小星排列索引的对象
 * - `zuofuIndex`: 左辅的排列索引
 * - `youbiIndex`: 右弼的排列索引
 * - `wenchangIndex`: 文昌的排列索引
 * - `wenquIndex`: 文曲的排列索引
 *
 * @example
 * ```typescript
 * const minorStarIndices = getMinorStarIndices(3, 5);
 * console.log(minorStarIndices);
 * // 输出示例:
 * // {
 * //   zuofuIndex: 6,
 * //   youbiIndex: 4,
 * //   wenchangIndex: 7,
 * //   wenquIndex: 8
 * // }
 * ```
 */
export function getMinorStarIndices(monthIndex: number, hourIndex: number): MinorStarIndices {
  // 获取地支索引（辰和戌的索引）
  const chenIndex = BRANCH_KEYS.indexOf("Chen") - 2; // 辰宫的索引
  const xuIndex = BRANCH_KEYS.indexOf("Xu") - 2; // 戌宫的索引

  // 根据月份和时辰计算左辅、右弼、文昌、文曲的目标宫位索引
  return {
    zuofuIndex: wrapIndex(chenIndex + monthIndex), // 左辅的索引
    youbiIndex: wrapIndex(xuIndex - monthIndex), // 右弼的索引
    wenchangIndex: wrapIndex(xuIndex - hourIndex), // 文昌的索引
    wenquIndex: wrapIndex(chenIndex + hourIndex), // 文曲的索引
  };
}

/**
 * 根据紫微天府的索引创建星辰元数组
 * @param ziweiIndex 紫微起点（逆时针）
 * @param tianfuIndex 天府起点（顺时针）
 * @returns 十二宫位元数组
 */
export function createMajorStarsMeta(
  ziweiIndex: number,
  tianfuIndex: number,
  onlyTransformation: boolean = false,
): StarMetaVO[] {
  function createMetaZiWeiStar({ key, galaxy }: Omit<StarMetaVO, "startIndex" | "direction">) {
    return { key, startIndex: ziweiIndex, direction: -1, galaxy } as const;
  }

  function createMetaTianFuStar({ key, galaxy }: Omit<StarMetaVO, "startIndex" | "direction">) {
    return { key, startIndex: tianfuIndex, direction: 1, galaxy } as const;
  }

  return [
    // 紫微星系（逆时针）
    createMetaZiWeiStar({ key: "ZiWei", galaxy: "C" }),
    createMetaZiWeiStar({ key: "TianJi", galaxy: "N" }),
    createMetaStar({ startIndex: ziweiIndex, direction: -1 }),
    createMetaZiWeiStar({ key: "TaiYang", galaxy: "N" }),
    createMetaZiWeiStar({ key: "WuQu", galaxy: "N" }),
    createMetaZiWeiStar({ key: "TianTong", galaxy: "N" }),
    createMetaStar({ startIndex: ziweiIndex, direction: -1 }),
    createMetaStar({ startIndex: ziweiIndex, direction: -1 }),
    createMetaZiWeiStar({ key: "LianZhen", galaxy: "N" }),

    // 天府星系（顺时针）
    onlyTransformation
      ? createMetaStar({ startIndex: ziweiIndex, direction: -1 })
      : createMetaStar({ key: "TianFu", startIndex: tianfuIndex, direction: 1 }),
    createMetaTianFuStar({ key: "TaiYin", galaxy: "S" }),
    createMetaTianFuStar({ key: "TanLang", galaxy: "S" }),
    createMetaTianFuStar({ key: "JuMen", galaxy: "S" }),
    onlyTransformation
      ? createMetaStar({ startIndex: ziweiIndex, direction: 1 })
      : createMetaStar({
          key: "TianXiang",
          startIndex: tianfuIndex,
          direction: 1,
          galaxy: undefined,
        }),

    createMetaTianFuStar({ key: "TianLiang", galaxy: "S" }),
    onlyTransformation
      ? createMetaStar({ startIndex: ziweiIndex, direction: 1 })
      : createMetaStar({
          key: "QiSha",
          startIndex: tianfuIndex,
          direction: 1,
          galaxy: undefined,
        }),
    createMetaStar({ startIndex: ziweiIndex, direction: 1 }),
    createMetaStar({ startIndex: ziweiIndex, direction: 1 }),
    createMetaStar({ startIndex: ziweiIndex, direction: 1 }),
    createMetaTianFuStar({ key: "PoJun", galaxy: "S" }),
  ];
}

export interface MinorStarsMetaCreateParams {
  zuofuIndex: number;
  youbiIndex: number;
  wenchangIndex: number;
  wenquIndex: number;
}

/**
 * 根据左右昌曲的初始索引创建元数组
 * @param param0
 * @returns
 */
export function createMinorStarsMeta({
  zuofuIndex,
  youbiIndex,
  wenchangIndex,
  wenquIndex,
}: MinorStarsMetaCreateParams): StarMetaVO[] {
  return [
    { key: "ZuoFu", startIndex: zuofuIndex, direction: 1, galaxy: "C" },
    { key: "YouBi", startIndex: youbiIndex, direction: -1, galaxy: "C" },
    { key: "WenChang", startIndex: wenchangIndex, direction: -1, galaxy: "C" },
    { key: "WenQu", startIndex: wenquIndex, direction: 1, galaxy: "C" },
  ];
}

export interface StarTransformationCalculateParams {
  stemKey: StemKey;
  starKey: StarKey;
}

/**
 * 根据指定的天干（stemKey）和星辰（starKey），计算星辰的化曜属性。
 *
 * @remarks
 * 此函数通过查找天干与星辰的对应关系，从 `_stemStarTransformations` 数据中获取化曜索引，
 * 并根据索引从 `_transformationKeys` 中提取对应的化曜键值，生成化曜对象。
 * 如果指定的天干没有对应的化曜星辰，则返回 `undefined`。
 *
 * @param stemKey - 天干的键值，用于确定化曜规则。
 * @param starKey - 星辰的键值，用于匹配天干的化曜规则。
 *
 * @returns 返回一个 `StarTransformation` 对象，包含以下属性：
 * ```ts
 * {
 *   key: TransformationKey; // 化曜的键值
 *   name: TransformationName; // 化曜的名称（多语言支持）
 * }
 * ```
 * 如果指定的天干没有对应的化曜星辰，则返回 `undefined`。
 *
 * @example
 * 以下是一个使用该函数的示例：
 * ```ts
 * const stemKey: StemKey = 'Jia';
 * const starKey: StarKey = 'Ziwei';
 *
 * const transformation = calculateStarTransformation(stemKey, starKey);
 * console.log(transformation);
 * // 输出：
 * // {
 * //   key: 'Lu',
 * //   name: '禄'
 * // }
 * ```
 */
export function calculateStarTransformation({
  starKey,
  stemKey,
}: StarTransformationCalculateParams) {
  const stemStarTransformation = STEM_TRANSFORMATIONS[stemKey];

  const starTransformationIndex = stemStarTransformation.indexOf(starKey);

  // 如果指定的天干没有该星辰化曜，返回默认值
  if (starTransformationIndex === -1) {
    return undefined;
  }
  return TRANSFORMATION_KEYS[starTransformationIndex];
}

export const memoCalculateStarTransformation = memoize(calculateStarTransformation, {
  getCacheKey: ({ stemKey, starKey }) => stemKey + starKey,
});

export function createMetaStar({ key, startIndex, direction, galaxy }: StarMetaVO) {
  return { key, startIndex, direction, galaxy } as const;
}
