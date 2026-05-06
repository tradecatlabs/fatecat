import type { LunarHour, SolarTime } from "tyme4ts";

import { EightChar } from "tyme4ts";

const PILLAR_UNIT = /^[甲乙丙丁戊己庚辛壬癸][子丑寅卯辰巳午未申酉戌亥]$/;
type PillarTuple = [string, string, string, string];

export type SexagenaryDateInput = string;

export interface SexagenaryCycleOptions {
  /**
   * 60 年周期的起始公历年份
   *
   * 例如传入 1984，则会在 [1984, 2043] 这个干支轮回中寻找唯一的匹配时间。
   */
  cycleStartYear: number;
}

export interface SexagenaryToLunisolarResult {
  /** 匹配到的阳历时间 */
  solarTime: SolarTime;
  /** 对应的阴阳合历时辰 */
  lunarHour: LunarHour;
}

function parseStringInput(input: string): PillarTuple {
  const trimmed = input.trim();
  if (trimmed.length !== 8) {
    throw new Error("Sexagenary input must be 8 characters like 甲子乙丑丙寅丁卯");
  }

  const chunks: string[] = [];
  for (let i = 0; i < 8; i += 2) {
    const entry = trimmed.slice(i, i + 2);
    if (!PILLAR_UNIT.test(entry)) {
      throw new Error(`Invalid pillar "${entry}" at position ${i / 2}`);
    }
    chunks.push(entry);
  }
  return chunks as PillarTuple;
}

function resolvePillars(input: SexagenaryDateInput): PillarTuple {
  if (typeof input !== "string") {
    throw new Error("Sexagenary input only accepts compact string like 甲子乙丑丙寅丁卯");
  }
  return parseStringInput(input);
}

/**
 * 依据干支（四柱）推算阴历时间。
 *
 * `tyme4ts` 的 `EightChar#getSolarTimes` 提供了在指定时间区间内
 * 查找匹配干支的阳历时间。由于干支每 60 年循环一次，此函数通过
 * `cycleStartYear` 指定一个 60 年的时间窗口来唯一确定结果。
 *
 * @param sexagenaryDate 干支日期，可以是带有“年/月/日/时”后缀的字符串，或显式的四柱对象
 * @param options.cycleStartYear 用于确定 60 年周期的起始年份
 *
 * @returns 对应的阳历/阴阳合历时间
 *
 * @throws RangeError 当 60 年窗口内没有找到匹配的干支日期时抛出
 */
export function calculateLunisolarDateBySexagenary(
  sexagenaryDate: SexagenaryDateInput,
  { cycleStartYear }: SexagenaryCycleOptions,
): SexagenaryToLunisolarResult {
  if (!Number.isInteger(cycleStartYear)) {
    throw new RangeError("cycleStartYear 必须是整数年份");
  }
  const startYear = cycleStartYear;
  const endYear = cycleStartYear + 59;
  const [year, month, day, hour] = resolvePillars(sexagenaryDate);
  const eightChar = new EightChar(year, month, day, hour);
  const solarTimes = eightChar.getSolarTimes(startYear, endYear);
  if (solarTimes.length === 0) {
    throw new RangeError(
      `未在 ${startYear}-${endYear} 找到 ${year}${month}${day}${hour} 对应的时间`,
    );
  }
  const solarTime = solarTimes[0];
  return {
    solarTime,
    lunarHour: solarTime.getLunarHour(),
  };
}
