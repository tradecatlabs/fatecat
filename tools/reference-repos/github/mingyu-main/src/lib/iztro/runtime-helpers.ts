import type FunctionalAstrolabe from 'iztro/lib/astro/FunctionalAstrolabe';
import type FunctionalHoroscope from 'iztro/lib/astro/FunctionalHoroscope';
import type { Config } from 'iztro/lib/data/types';
import type { ChartInput } from '../../types/chart';
import { daysInSolarMonth } from '../date-validation';

export function normalizeChartInput(input: ChartInput): ChartInput {
  return {
    ...input,
    name: input.name?.trim() ?? '',
    birthDate: input.birthDate.trim(),
    fixLeap: input.fixLeap ?? true,
  };
}

export function buildIztroConfig(input: ChartInput): Config {
  return {
    algorithm: input.algorithm,
    yearDivide: input.yearDivide,
    horoscopeDivide: input.horoscopeDivide,
    ageDivide: input.ageDivide,
    dayDivide: input.dayDivide,
  };
}

function timeToIndex(hour: number) {
  if (hour === 0) {
    return 0;
  }

  if (hour === 23) {
    return 12;
  }

  return Math.floor((hour + 1) / 2);
}

export async function buildAstrolabeFromInput(input: ChartInput): Promise<FunctionalAstrolabe> {
  const normalized = normalizeChartInput(input);
  const { astro } = await import('iztro');

  return astro.withOptions({
    type: normalized.dateType,
    dateStr: normalized.birthDate,
    timeIndex: normalized.birthTimeIndex,
    gender: normalized.gender,
    isLeapMonth: normalized.isLeapMonth,
    fixLeap: normalized.fixLeap,
    language: 'zh-CN',
    config: buildIztroConfig(normalized),
  }) as FunctionalAstrolabe;
}

export function formatLocalDate(date: Date): string {
  const year = date.getFullYear();
  const month = String(date.getMonth() + 1).padStart(2, '0');
  const day = String(date.getDate()).padStart(2, '0');

  return `${year}-${month}-${day}`;
}

export function getDefaultHoroscopeContext(now = new Date()) {
  if (!(now instanceof Date) || Number.isNaN(now.getTime())) {
    throw new Error('当前时间不是有效日期。');
  }

  return {
    dateStr: formatLocalDate(now),
    hourIndex: timeToIndex(now.getHours()),
  };
}

export function buildHoroscope(
  astrolabe: FunctionalAstrolabe,
  dateStr: string,
  hourIndex: number,
): FunctionalHoroscope {
  return astrolabe.horoscope(dateStr, hourIndex) as FunctionalHoroscope;
}

export function shiftLocalDate(
  dateStr: string,
  amount: number,
  unit: 'year' | 'month' | 'day',
): string {
  const { year, month, day } = parseSolarDateKey(dateStr);
  if (!Number.isInteger(amount)) {
    throw new Error('日期位移量必须是整数。');
  }

  let date: Date;

  if (unit === 'year') {
    const targetYear = year + amount;
    const targetDay = Math.min(day, daysInGregorianMonth(targetYear, month));
    date = new Date(targetYear, month - 1, targetDay);
  } else if (unit === 'month') {
    const totalMonthIndex = year * 12 + (month - 1) + amount;
    const targetYear = Math.floor(totalMonthIndex / 12);
    const targetMonth = (totalMonthIndex % 12) + 1;
    const targetDay = Math.min(day, daysInGregorianMonth(targetYear, targetMonth));
    date = new Date(targetYear, targetMonth - 1, targetDay);
  } else {
    date = new Date(year, month - 1, day);
    date.setDate(date.getDate() + amount);
  }

  return formatLocalDate(date);
}

function parseSolarDateKey(dateStr: string): { year: number; month: number; day: number } {
  const match = /^(\d{4})-(\d{2})-(\d{2})$/.exec(dateStr.trim());
  if (!match) {
    throw new Error('日期格式需为 YYYY-MM-DD。');
  }

  const year = Number(match[1]);
  const month = Number(match[2]);
  const day = Number(match[3]);
  if (!Number.isInteger(year) || year < 1900 || year > 2100) {
    throw new Error('年份需在 1900-2100 之间。');
  }
  if (!Number.isInteger(month) || month < 1 || month > 12) {
    throw new Error('月份需在 1-12 之间。');
  }

  const maxDay = daysInSolarMonth(year, month);
  if (!Number.isInteger(day) || day < 1) {
    throw new Error('日期不能小于 1。');
  }
  if (day > maxDay) {
    throw new Error(`日期需在 1-${maxDay} 之间。`);
  }

  return { year, month, day };
}

function daysInGregorianMonth(year: number, month: number) {
  if (!Number.isInteger(year)) {
    throw new Error('年份必须是整数。');
  }
  if (!Number.isInteger(month) || month < 1 || month > 12) {
    throw new Error('月份需在 1-12 之间。');
  }

  return new Date(Date.UTC(year, month, 0)).getUTCDate();
}
