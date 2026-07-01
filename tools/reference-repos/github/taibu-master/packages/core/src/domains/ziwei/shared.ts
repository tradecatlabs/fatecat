/**
 * 紫微斗数共享工具函数
 */

import { astro } from 'iztro';
import { Lunar, LunarMonth, LunarYear } from 'lunar-javascript';
import type { BirthTimeInput, DiZhi, Gender, StarInfo, TrueSolarTimeInfo } from '../shared/types.js';
import { hourToTimeIndex, resolveTrueSolarDateTime } from '../shared/true-solar.js';

export type { BirthTimeInput, DiZhi, Gender, StarInfo, TrueSolarTimeInfo } from '../shared/types.js';
export { calculateTrueSolarTime, hourToTimeIndex, resolveTrueSolarDateTime } from '../shared/true-solar.js';

export const MUTAGEN_NAMES = ['禄', '权', '科', '忌'] as const;
export type MutagenName = typeof MUTAGEN_NAMES[number];
type Astrolabe = ReturnType<typeof astro.bySolar>;
type IztroStar = {
  name: string;
  type?: string;
  brightness?: string;
  mutagen?: string;
};

/** 天干四化表: stem → [禄星, 权星, 科星, 忌星] */
export const STEM_MUTAGEN_TABLE: Record<string, [string, string, string, string]> = {
  '甲': ['廉贞', '破军', '武曲', '太阳'],
  '乙': ['天机', '天梁', '紫微', '太阴'],
  '丙': ['天同', '天机', '文昌', '廉贞'],
  '丁': ['太阴', '天同', '天机', '巨门'],
  '戊': ['贪狼', '太阴', '右弼', '天机'],
  '己': ['武曲', '贪狼', '天梁', '文曲'],
  '庚': ['太阳', '武曲', '太阴', '天同'],
  '辛': ['巨门', '太阳', '文曲', '文昌'],
  '壬': ['天梁', '紫微', '左辅', '武曲'],
  '癸': ['破军', '巨门', '太阴', '贪狼'],
};

import { DI_ZHI } from '../../data/ganzhi.js';
export { DI_ZHI };

/** 禄存所在地支：按年干查表 */
export const LUCUN_TABLE: Record<string, string> = {
  '甲': '寅', '乙': '卯', '丙': '巳', '丁': '午',
  '戊': '巳', '己': '午', '庚': '申', '辛': '酉',
  '壬': '亥', '癸': '子',
};

/** 计算流年虚岁列表 */
export function computeLiuNianAges(palaceBranch: DiZhi, birthYearBranch: DiZhi, max = 60): number[] {
  const pIdx = DI_ZHI.indexOf(palaceBranch);
  const bIdx = DI_ZHI.indexOf(birthYearBranch);
  if (pIdx < 0 || bIdx < 0) return [];
  const offset = (pIdx - bIdx + 12) % 12;
  const ages: number[] = [];
  for (let age = offset + 1; age <= max; age += 12) ages.push(age);
  return ages;
}

/**
 * 计算子年斗君地支
 *
 * 公式来源：iztro FunctionalAstrolabe.js 流月算法
 * 「流年地支逆数到生月所在宫位，再从该宫位顺数到生时，为正月所在宫位」
 *
 * 斗君 = 子年正月宫位地支
 *   = DI_ZHI[(13 - lunarMonth + hourBranchIdx) % 12]
 *
 * 其中 hourBranchIdx 为时辰地支绝对索引（子=0, 丑=1, ..., 亥=11）
 * timeIndex 12（晚子时）与 timeIndex 0（早子时）同为子，取 % 12
 */
export function computeDouJun(lunarMonth: number, timeIndex: number): string {
  // timeIndex: 早子时=0, 丑=1, ..., 亥=11, 晚子时=12 → 子=0
  const hourBranchIdx = timeIndex % 12;
  return DI_ZHI[(13 - lunarMonth + hourBranchIdx + 12) % 12];
}

/** 将 iztro Star 映射为 StarInfo */
export function mapStar(star: IztroStar): StarInfo {
  return {
    name: star.name,
    type: star.type,
    brightness: star.brightness,
    mutagen: star.mutagen,
  };
}

function validateLunarBirthInput(params: {
  birthYear: number;
  birthMonth: number;
  birthDay: number;
  birthHour: number;
  birthMinute: number;
  isLeapMonth: boolean;
}): { lunar: ReturnType<typeof Lunar.fromYmdHms>; solar: ReturnType<ReturnType<typeof Lunar.fromYmdHms>['getSolar']>; } {
  const {
    birthYear,
    birthMonth,
    birthDay,
    birthHour,
    birthMinute,
    isLeapMonth,
  } = params;

  if (!Number.isInteger(birthMonth) || birthMonth < 1 || birthMonth > 12) {
    throw new Error(`农历月份无效：${birthMonth}月不存在。请输入 1-12 之间的整数。`);
  }

  const leapMonth = LunarYear.fromYear(birthYear).getLeapMonth();
  if (isLeapMonth && leapMonth !== birthMonth) {
    throw new Error(`农历闰月无效：${birthYear}年没有闰${birthMonth}月，请检查该年是否有闰月。`);
  }

  const lunarMonth = isLeapMonth ? -Math.abs(birthMonth) : birthMonth;
  let lunarMonthInfo: ReturnType<typeof LunarMonth.fromYm>;
  try {
    lunarMonthInfo = LunarMonth.fromYm(birthYear, lunarMonth);
  } catch {
    throw new Error(`农历月份无效：${birthYear}年${isLeapMonth ? '闰' : ''}${birthMonth}月不存在。`);
  }

  if (!lunarMonthInfo) {
    throw new Error(`农历月份无效：${birthYear}年${isLeapMonth ? '闰' : ''}${birthMonth}月不存在。`);
  }

  const dayCount = lunarMonthInfo.getDayCount();
  if (birthDay < 1 || birthDay > dayCount) {
    throw new Error(`农历日期无效：${birthYear}年${isLeapMonth ? '闰' : ''}${birthMonth}月只有${dayCount}天，请输入 1-${dayCount} 之间的日期。`);
  }

  let lunar: ReturnType<typeof Lunar.fromYmdHms>;
  try {
    lunar = Lunar.fromYmdHms(birthYear, lunarMonth, birthDay, birthHour, birthMinute, 0);
  } catch {
    throw new Error(`农历日期无效：${birthYear}年${isLeapMonth ? '闰' : ''}${birthMonth}月${birthDay}日不存在，请检查日期是否正确。`);
  }

  return {
    lunar,
    solar: lunar.getSolar(),
  };
}

/** 校验出生参数并创建星盘 */
export function createAstrolabe(input: BirthTimeInput & { gender: Gender; }): Astrolabe {
  const {
    gender,
    birthYear,
    birthMonth,
    birthDay,
    birthHour,
    birthMinute = 0,
    calendarType = 'solar',
    isLeapMonth = false,
  } = input;

  if (gender !== 'male' && gender !== 'female') {
    throw new Error('gender 必须是 "male" 或 "female"');
  }
  if (!Number.isInteger(birthYear) || birthYear < 1900 || birthYear > 2100) {
    throw new Error('birthYear 必须是 1900-2100 之间的整数');
  }
  if (!Number.isInteger(birthMonth) || birthMonth < 1 || birthMonth > 12) {
    throw new Error('birthMonth 必须是 1-12 之间的整数');
  }
  if (!Number.isInteger(birthDay) || birthDay < 1) {
    throw new Error('birthDay 必须是合法日期');
  }
  if (calendarType === 'solar') {
    const maxSolarDay = new Date(birthYear, birthMonth, 0).getDate();
    if (birthDay > maxSolarDay) {
      throw new Error(`birthDay 必须是 1-${maxSolarDay} 之间的整数`);
    }
  } else {
    if (birthDay > 30) {
      throw new Error('birthDay 必须是 1-30 之间的整数');
    }

    const leapMonth = LunarYear.fromYear(birthYear).getLeapMonth();
    if (isLeapMonth && leapMonth !== birthMonth) {
      throw new Error(`农历闰月无效：${birthYear}年没有闰${birthMonth}月，请检查该年是否有闰月。`);
    }

    const lunarMonth = isLeapMonth ? -Math.abs(birthMonth) : birthMonth;
    let lunarMonthInfo: ReturnType<typeof LunarMonth.fromYm>;
    try {
      lunarMonthInfo = LunarMonth.fromYm(birthYear, lunarMonth);
    } catch {
      throw new Error(`农历月份无效：${birthYear}年${isLeapMonth ? '闰' : ''}${birthMonth}月不存在。`);
    }
    if (!lunarMonthInfo) {
      throw new Error(`农历月份无效：${birthYear}年${isLeapMonth ? '闰' : ''}${birthMonth}月不存在。`);
    }

    const dayCount = lunarMonthInfo.getDayCount();
    if (birthDay > dayCount) {
      throw new Error(`农历日期无效：${birthYear}年${isLeapMonth ? '闰' : ''}${birthMonth}月只有${dayCount}天，请输入 1-${dayCount} 之间的日期。`);
    }
  }
  if (!Number.isInteger(birthHour) || birthHour < 0 || birthHour > 23) {
    throw new Error('birthHour 必须是 0-23 之间的整数');
  }

  const dateStr = `${birthYear}-${birthMonth}-${birthDay}`;
  const hourValue = birthHour + birthMinute / 60;
  const timeIndex = hourToTimeIndex(hourValue);
  const genderStr = gender === 'male' ? '男' : '女';

  if (calendarType === 'lunar') {
    return astro.byLunar(dateStr, timeIndex, genderStr, isLeapMonth, true, 'zh-CN');
  }
  return astro.bySolar(dateStr, timeIndex, genderStr, true, 'zh-CN');
}

/**
 * 创建星盘（支持真太阳时校正）
 *
 * 当提供 longitude 时，先计算真太阳时，再用归一化后的日期与时辰索引排盘。
 */
export function createAstrolabeWithTrueSolar(
  input: BirthTimeInput & { gender: Gender; longitude?: number; },
): { astrolabe: Astrolabe; trueSolarTimeInfo?: TrueSolarTimeInfo; } {
  const { longitude, ...baseInput } = input;

  if (longitude == null) {
    return { astrolabe: createAstrolabe(baseInput) };
  }

  if (typeof longitude !== 'number' || longitude < -180 || longitude > 180) {
    throw new Error('longitude 必须是 -180 到 180 之间的数字');
  }

  const {
    gender,
    birthYear,
    birthMonth,
    birthDay,
    birthHour,
    birthMinute = 0,
    calendarType = 'solar',
    isLeapMonth = false,
  } = input;

  const baseSolarInput = calendarType === 'lunar'
    ? (() => {
      const prepared = validateLunarBirthInput({
        birthYear,
        birthMonth,
        birthDay,
        birthHour,
        birthMinute,
        isLeapMonth,
      });
      return {
        birthYear: prepared.solar.getYear(),
        birthMonth: prepared.solar.getMonth(),
        birthDay: prepared.solar.getDay(),
        birthHour: prepared.solar.getHour(),
        birthMinute: prepared.solar.getMinute(),
      };
    })()
    : { birthYear, birthMonth, birthDay, birthHour, birthMinute };

  const resolvedDateTime = resolveTrueSolarDateTime(
    baseSolarInput,
    longitude,
  );
  const trueSolarTimeInfo = resolvedDateTime.trueSolarTimeInfo;

  const dateStr = `${resolvedDateTime.year}-${resolvedDateTime.month}-${resolvedDateTime.day}`;
  const genderStr = gender === 'male' ? '男' : '女';

  return {
    astrolabe: astro.bySolar(dateStr, trueSolarTimeInfo.trueTimeIndex, genderStr, true, 'zh-CN'),
    trueSolarTimeInfo,
  };
}
