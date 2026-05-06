import type { ZiWeiRuntime } from "../context";
import type { BranchKey, DecadeVO, Palace, YearlyVO } from "../typings";

import { PALACE_KEYS } from "../constants";
import { calculateCurrentPalaceIndex } from "../rules/palace";
import { calculateLunisolarDateBySolar, calculateNatalDateBySolar } from "../utils/calendar";
import { wrapIndex } from "../utils/math";

export interface DecadeByDateCalculateParams {
  palaces: Palace[];
  birthYearBranchKey: BranchKey;
  birthYear: number;
  date: Date;
}

export function calculateDecadeByDate(
  ctx: ZiWeiRuntime,
  { palaces, birthYearBranchKey, birthYear, date }: DecadeByDateCalculateParams,
) {
  // 默认获取指定日期的阴历年份，计算目标年份的大限索引
  const lunisolarDate = calculateLunisolarDateBySolar(date);
  const { year } = calculateNatalDateBySolar({ date: lunisolarDate, globalConfigs: ctx.configs });
  // 虚岁
  const age = year - birthYear + 1;
  // 当前所在年份的大命索引
  const horoscopeMainPalaceIndex = palaces.findIndex(
    (palace) => age >= palace.decadeRanges[0] && age <= palace.decadeRanges[1],
  );
  // 若当前大限找不到时，重置到本命宫的索引
  const fixHoroscopeMainPalaceIndex =
    horoscopeMainPalaceIndex === -1 ? 0 : horoscopeMainPalaceIndex;

  return calculateDecade(ctx, {
    palaces,
    index: fixHoroscopeMainPalaceIndex,
    birthYearBranchKey,
    birthYear,
  });
}

export interface DecadeCalculateParams {
  palaces: Palace[];
  /** 大运命宫的索引 */
  index: number;
  birthYearBranchKey: BranchKey;
  birthYear: number;
}

export function calculateDecade(
  ctx: ZiWeiRuntime,
  { palaces, index, birthYearBranchKey, birthYear }: DecadeCalculateParams,
) {
  // 1. 获取大限起始年龄
  const mainPalace = palaces[index];
  const majorStart = mainPalace.decadeRanges[0];

  // 2. 计算流年起始索引
  const birthYearIndex = palaces.findIndex((palace) => palace.branch.key === birthYearBranchKey);
  const yearlyStartIndex = wrapIndex(birthYearIndex + majorStart - 1);

  // 3. 一次性创建所有大限宫位
  return palaces.map((_, palaceIndex) =>
    createDecadePalace(ctx, {
      palaceIndex,
      mainPalaceIndex: index,
      yearlyStartIndex,
      birthYear,
      majorStart,
    }),
  );
}

export function calculateAllDecade(
  ctx: ZiWeiRuntime,
  params: Omit<DecadeCalculateParams, "index">,
): DecadeVO[][] {
  return params.palaces.map((_, palaceIndex) => {
    return calculateDecade(ctx, {
      ...params,
      index: palaceIndex,
    });
  });
}

export function calculateDecadeIndexByDate(
  ctx: ZiWeiRuntime,
  { palaces, birthYear, date }: DecadeByDateCalculateParams,
) {
  // 默认获取指定日期的阴历年份，计算目标年份的大限索引
  const lunisolarDate = calculateLunisolarDateBySolar(date);
  const { year } = calculateNatalDateBySolar({ date: lunisolarDate, globalConfigs: ctx.configs });
  // 虚岁
  const age = year - birthYear + 1;
  // 当前所在年份的大命索引
  const horoscopeMainPalaceIndex = palaces.findIndex(
    (palace) => age >= palace.decadeRanges[0] && age <= palace.decadeRanges[1],
  );
  // 若当前大限找不到时，重置到本命宫的索引
  const fixHoroscopeMainPalaceIndex =
    horoscopeMainPalaceIndex === -1 ? 0 : horoscopeMainPalaceIndex;

  return fixHoroscopeMainPalaceIndex;
}

export interface DecadePalaceCreateParams {
  palaceIndex: number;
  mainPalaceIndex: number;
  yearlyStartIndex: number;
  birthYear: number;
  majorStart: number;
}

export function createDecadePalace(
  ctx: ZiWeiRuntime,
  {
    palaceIndex,
    mainPalaceIndex,
    yearlyStartIndex,
    birthYear,
    majorStart,
  }: DecadePalaceCreateParams,
): DecadeVO {
  // 1. 计算宫位 key
  const currentPalaceIndex = calculateCurrentPalaceIndex(mainPalaceIndex, palaceIndex);
  const key = PALACE_KEYS[currentPalaceIndex];

  // 2. 计算流年信息
  const yearly = calculateYearly(palaceIndex, yearlyStartIndex, birthYear, majorStart);

  // 3. 返回宫位对象
  return {
    key,
    name: ctx.i18n.$t(`palace.${key}.decade`),
    yearly,
  };
}

export function calculateYearly(
  palaceIndex: number,
  yearlyStartIndex: number,
  birthYear: number,
  majorStart: number,
): YearlyVO {
  // 计算当前宫位在流年序列中的偏移量
  const offset = wrapIndex(palaceIndex - yearlyStartIndex);

  // 只有在大限范围内（0-9）才有有效的流年信息
  if (offset > 9) {
    return { name: 0, age: 0 };
  }

  return {
    name: birthYear + majorStart + offset - 1,
    age: majorStart + offset,
  };
}
