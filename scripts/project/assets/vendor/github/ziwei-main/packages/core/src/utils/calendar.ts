import { LunarHour, SolarTime } from "tyme4ts";

import type { GlobalConfigs } from "../infra/configs";
import type { BranchKey, StemKey } from "../typings";

import { BRANCH_KEYS, STEM_KEYS } from "../constants";
import { getHourIndex } from "../rules/date";
import { wrapIndex } from "./math";

/**
 * 解析形如 "YYYY-m-d-hourIndex" 的紫微日期字符串为内部参数。
 */
export function calculateZiWeiDate(date: string) {
  const [year, month, day, hourIndex] = date.split("-").map(Number);
  const [stemIndex, branchIndex] = getStemAndBranchByYear(year);
  return {
    stemKey: STEM_KEYS[stemIndex],
    branchKey: BRANCH_KEYS[branchIndex],
    monthIndex: month - 1,
    day,
    hourIndex,
  };
}

/**
 * 根据小时时分割策略归一化“晚子时”（23:00）。
 */
export function normalizeHour(date: LunarHour, globalConfigs: GlobalConfigs) {
  if (globalConfigs.division.day === "normal") {
    const isLateZi = date.getHour() === 23;
    if (isLateZi) {
      const nextLunarDay = date.getLunarDay().next(1);
      const nextLunarMonth = nextLunarDay.getLunarMonth();
      const nextLunarYear = nextLunarMonth.getLunarYear();

      return LunarHour.fromYmdHms(
        nextLunarYear.getYear(),
        nextLunarMonth.getMonthWithLeap(),
        nextLunarDay.getDay(),
        date.getHour(),
        date.getMinute(),
        date.getSecond(),
      );
    }
  }
  return date;
}

/**
 * 按配置处理闰月映射（上月/下月/15日前后）。
 *
 * 注意：存在极端情况未覆盖，必要时再迭代。
 */
export function fixLeapMonth(date: LunarHour, globalConfigs: GlobalConfigs): LunarHour {
  let targetDay = date.getLunarDay();
  let targetMonth = targetDay.getLunarMonth();
  let targetYear = targetMonth.getLunarYear();

  if (targetMonth.isLeap()) {
    if (globalConfigs.division.month === "last") {
      targetDay = targetDay.next(-30);
      targetMonth = targetDay.getLunarMonth();
      targetYear = targetMonth.getLunarYear();
    }
    if (globalConfigs.division.month === "next") {
      targetDay = targetDay.next(30);
      targetMonth = targetDay.getLunarMonth();
      targetYear = targetMonth.getLunarYear();
    }
    if (globalConfigs.division.month === "normal") {
      const day = targetDay.getDay();
      if (day < 15 || (day === 15 && date.getHour() !== 23)) {
        targetDay = targetDay.next(-30);
        targetMonth = targetDay.getLunarMonth();
      } else {
        targetDay = targetDay.next(30);
        targetMonth = targetDay.getLunarMonth();
      }
      targetYear = targetMonth.getLunarYear();
    }

    return LunarHour.fromYmdHms(
      targetYear.getYear(),
      targetMonth.getMonthWithLeap(),
      targetDay.getDay(),
      date.getHour(),
      date.getMinute(),
      date.getSecond(),
    );
  }

  return date;
}

export interface LunisolarDateParams {
  date: LunarHour;
  globalConfigs: GlobalConfigs;
}

export interface FixedLunarDate {
  stemKey: StemKey;
  branchKey: BranchKey;
  year: number;
  monthIndex: number;
  day: number;
  hourIndex: number;
}

/**
 * 从阴阳合历时辰与配置推导命盘所需的年、月、日、时索引。
 */
export function calculateNatalDateBySolar({
  date,
  globalConfigs,
}: LunisolarDateParams): FixedLunarDate {
  const targetLunarHour = fixLeapMonth(normalizeHour(date, globalConfigs), globalConfigs);

  const targetLunarDay = targetLunarHour.getLunarDay();
  const targetLunarMonth = targetLunarDay.getLunarMonth();
  const targetLunarYear = targetLunarMonth.getLunarYear();

  // 计算修正后的时辰索引（0-11 为正常时辰，12 为晚子时）
  const hourIndex = getHourIndex(targetLunarHour.getHour());
  const year = targetLunarYear.getYear();
  const [stemIndex, branchIndex] = getStemAndBranchByYear(year);

  return {
    stemKey: STEM_KEYS[stemIndex],
    branchKey: BRANCH_KEYS[branchIndex],
    year,
    monthIndex: targetLunarMonth.getMonth() - 1,
    day: targetLunarDay.getDay(),
    hourIndex: wrapIndex(hourIndex),
  };
}

/**
 * JS Date → 阴阳合历时辰。
 */
export function calculateLunisolarDateBySolar(date: Date) {
  const solarTime = SolarTime.fromYmdHms(
    date.getFullYear(),
    date.getMonth() + 1,
    date.getDate(),
    date.getHours(),
    date.getMinutes(),
    date.getSeconds(),
  );
  return solarTime.getLunarHour();
}

/**
 * 根据公历年份计算对应的天干地支索引。
 */
export function getStemAndBranchByYear(year: number): [number, number] {
  if (year < 1 || year > 9999) {
    throw new RangeError("年份必须在 1 到 9999 之间");
  }
  const stemIndex = wrapIndex((year - 4) % 10, 10);
  const branchIndex = wrapIndex((year - 4) % 12);
  return [stemIndex, branchIndex];
}

/**
 * 根据地支时辰索引计算中位时分秒，供构造 LunarHour 使用。
 */
export function calculateHourByIndex(hourIndex: number) {
  return [hourIndex * 2, 30, 0] as const;
}
