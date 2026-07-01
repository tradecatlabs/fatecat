/**
 * 四柱反推候选出生时间
 */

import { Solar } from 'lunar-javascript';
import { DI_ZHI, TIAN_GAN } from '../../data/ganzhi.js';
import type {
  BaziPillarsResolveCandidate,
  BaziPillarsResolveInput,
  BaziPillarsResolveOutput,
} from './types.js';

export type {
  BaziPillarsResolveCandidate,
  BaziPillarsResolveInput,
  BaziPillarsResolveOutput,
} from './types.js';

type Stem = (typeof TIAN_GAN)[number];
type Branch = (typeof DI_ZHI)[number];

type ParsedPillar = {
  stem: Stem;
  branch: Branch;
};

type ParsedPillars = {
  year: ParsedPillar;
  month: ParsedPillar;
  day: ParsedPillar;
  hour: ParsedPillar;
};

const HOUR_BRANCH_MAP: Record<Branch, number[]> = {
  '子': [23, 0],
  '丑': [1, 2],
  '寅': [3, 4],
  '卯': [5, 6],
  '辰': [7, 8],
  '巳': [9, 10],
  '午': [11, 12],
  '未': [13, 14],
  '申': [15, 16],
  '酉': [17, 18],
  '戌': [19, 20],
  '亥': [21, 22],
};

function isValidPillar(stem: Stem, branch: Branch): boolean {
  const stemIndex = TIAN_GAN.indexOf(stem);
  const branchIndex = DI_ZHI.indexOf(branch);
  return stemIndex % 2 === branchIndex % 2;
}

function parsePillar(raw: string, field: string): ParsedPillar {
  if (typeof raw !== 'string' || raw.length !== 2) {
    throw new Error(`${field} 必须是 2 字干支，例如“甲子”`);
  }

  const stem = raw[0] as Stem;
  const branch = raw[1] as Branch;

  if (!TIAN_GAN.includes(stem)) {
    throw new Error(`${field} 天干无效：${raw[0]}`);
  }
  if (!DI_ZHI.includes(branch)) {
    throw new Error(`${field} 地支无效：${raw[1]}`);
  }
  if (!isValidPillar(stem, branch)) {
    throw new Error(`${field} 不是有效干支组合：${raw}`);
  }

  return { stem, branch };
}

function toSolarText(year: number, month: number, day: number, hour: number, minute: number): string {
  const yyyy = String(year).padStart(4, '0');
  const mm = String(month).padStart(2, '0');
  const dd = String(day).padStart(2, '0');
  const hh = String(hour).padStart(2, '0');
  const mi = String(minute).padStart(2, '0');
  return `${yyyy}-${mm}-${dd} ${hh}:${mi}`;
}

function toLunarText(solar: Solar, hourBranch: Branch): string {
  const lunar = solar.getLunar();
  return `农历${lunar.getYearInChinese()}年${lunar.getMonthInChinese()}月${lunar.getDayInChinese()} ${hourBranch}时`;
}

function reverseYear(yearPillar: ParsedPillar): number[] {
  const years: number[] = [];
  for (let year = 1900; year <= 2100; year++) {
    try {
      const jan = Solar.fromYmd(year, 1, 15).getLunar().getEightChar();
      if (jan.getYearGan() === yearPillar.stem && jan.getYearZhi() === yearPillar.branch) {
        years.push(year);
        continue;
      }

      const jun = Solar.fromYmd(year, 6, 15).getLunar().getEightChar();
      if (jun.getYearGan() === yearPillar.stem && jun.getYearZhi() === yearPillar.branch) {
        years.push(year);
      }
    } catch {
      // ignore
    }
  }
  return years;
}

function reverseMonth(year: number, yearPillar: ParsedPillar, monthPillar: ParsedPillar): number[] {
  const months: number[] = [];
  for (let month = 1; month <= 12; month++) {
    const checkDays = [1, 15];
    for (const day of checkDays) {
      try {
        const ec = Solar.fromYmd(year, month, day).getLunar().getEightChar();
        if (
          ec.getYearGan() === yearPillar.stem &&
          ec.getYearZhi() === yearPillar.branch &&
          ec.getMonthGan() === monthPillar.stem &&
          ec.getMonthZhi() === monthPillar.branch
        ) {
          months.push(month);
          break;
        }
      } catch {
        // ignore
      }
    }
  }
  return months;
}

function reverseDay(year: number, month: number, dayPillar: ParsedPillar): number[] {
  const days: number[] = [];
  const maxDay = new Date(year, month, 0).getDate();
  for (let day = 1; day <= maxDay; day++) {
    try {
      const ec = Solar.fromYmd(year, month, day).getLunar().getEightChar();
      if (ec.getDayGan() === dayPillar.stem && ec.getDayZhi() === dayPillar.branch) {
        days.push(day);
      }
    } catch {
      // ignore
    }
  }
  return days;
}

function buildNextCallArgs(candidate: BaziPillarsResolveCandidate['nextCall']['arguments']) {
  return {
    tool: 'bazi' as const,
    arguments: candidate,
    missing: ['gender'] as ['gender'],
  };
}

function reversePillarsToCandidates(pillars: ParsedPillars): BaziPillarsResolveCandidate[] {
  const candidates: BaziPillarsResolveCandidate[] = [];
  const seen = new Set<string>();

  const years = reverseYear(pillars.year);
  for (const year of years) {
    const months = reverseMonth(year, pillars.year, pillars.month);
    for (const month of months) {
      const days = reverseDay(year, month, pillars.day);
      for (const day of days) {
        for (const hour of HOUR_BRANCH_MAP[pillars.hour.branch]) {
          try {
            const solar = Solar.fromYmdHms(year, month, day, hour, 0, 0);
            const ec = solar.getLunar().getEightChar();

            // 最终强校验：年/月/日/时干支必须全部匹配
            const matches =
              ec.getYearGan() === pillars.year.stem &&
              ec.getYearZhi() === pillars.year.branch &&
              ec.getMonthGan() === pillars.month.stem &&
              ec.getMonthZhi() === pillars.month.branch &&
              ec.getDayGan() === pillars.day.stem &&
              ec.getDayZhi() === pillars.day.branch &&
              ec.getTimeGan() === pillars.hour.stem &&
              ec.getTimeZhi() === pillars.hour.branch;

            if (!matches) continue;

            const lunar = solar.getLunar();
            const lunarMonthRaw = lunar.getMonth();
            const isLeapMonth = lunarMonthRaw < 0;
            const lunarYear = lunar.getYear();
            const lunarMonth = Math.abs(lunarMonthRaw);
            const lunarDay = lunar.getDay();

            // 农历去重：同一农历年月日（含闰月）与同一时辰仅保留一个候选
            const key = `${lunarYear}-${lunarMonth}-${lunarDay}-${isLeapMonth ? 1 : 0}-${pillars.hour.branch}`;
            if (seen.has(key)) continue;
            seen.add(key);

            const nextArgs = {
              birthYear: lunarYear,
              birthMonth: lunarMonth,
              birthDay: lunarDay,
              birthHour: hour,
              birthMinute: 0,
              calendarType: 'lunar' as const,
              isLeapMonth,
            };

            candidates.push({
              candidateId: `cand_${candidates.length + 1}`,
              isLeapMonth,
              birthYear: lunarYear,
              birthMonth: lunarMonth,
              birthDay: lunarDay,
              birthHour: hour,
              birthMinute: 0,
              solarText: toSolarText(year, month, day, hour, 0),
              lunarText: toLunarText(solar, pillars.hour.branch),
              nextCall: buildNextCallArgs(nextArgs),
            });
          } catch {
            // ignore
          }
        }
      }
    }
  }

  return candidates;
}

export async function calculateBaziPillarsResolve(
  input: BaziPillarsResolveInput,
): Promise<BaziPillarsResolveOutput> {
  const parsed: ParsedPillars = {
    year: parsePillar(input.yearPillar, 'yearPillar'),
    month: parsePillar(input.monthPillar, 'monthPillar'),
    day: parsePillar(input.dayPillar, 'dayPillar'),
    hour: parsePillar(input.hourPillar, 'hourPillar'),
  };

  const candidates = reversePillarsToCandidates(parsed);

  return {
    pillars: {
      yearPillar: `${parsed.year.stem}${parsed.year.branch}`,
      monthPillar: `${parsed.month.stem}${parsed.month.branch}`,
      dayPillar: `${parsed.day.stem}${parsed.day.branch}`,
      hourPillar: `${parsed.hour.stem}${parsed.hour.branch}`,
    },
    count: candidates.length,
    candidates,
  };
}
