import type { TrueSolarTimeInfo } from './types.js';

/** 中国标准时区基准经度 (UTC+8) */
const STANDARD_MERIDIAN = 120;

export type SolarDateTimeInput = {
  birthYear: number;
  birthMonth: number;
  birthDay: number;
  birthHour: number;
  birthMinute?: number;
};

export type SolarDateTimeParts = {
  year: number;
  month: number;
  day: number;
  hour: number;
  minute: number;
  dayOffset: number;
};

/** 将小时转换为时辰索引（早子时=0, 丑时=1, ..., 晚子时=12） */
export function hourToTimeIndex(hour: number): number {
  if (hour >= 23) return 12;
  if (hour >= 0 && hour < 1) return 0;
  return Math.floor((hour + 1) / 2);
}

function equationOfTime(dayOfYear: number, year: number): number {
  const isLeap = (year % 4 === 0 && year % 100 !== 0) || year % 400 === 0;
  const totalDays = isLeap ? 366 : 365;
  const B = (2 * Math.PI * (dayOfYear - 81)) / totalDays;
  return 9.87 * Math.sin(2 * B) - 7.53 * Math.cos(B) - 1.5 * Math.sin(B);
}

function getDayOfYear(year: number, month: number, day: number): number {
  const d = new Date(year, month - 1, day);
  const start = new Date(year, 0, 1);
  return Math.floor((d.getTime() - start.getTime()) / 86400000) + 1;
}

function applyMinuteOffsetToSolarDateTime(
  input: SolarDateTimeInput,
  roundedOffsetMinutes: number,
): SolarDateTimeParts {
  const { birthYear, birthMonth, birthDay, birthHour, birthMinute = 0 } = input;
  const baseTime = Date.UTC(birthYear, birthMonth - 1, birthDay, birthHour, birthMinute, 0, 0);
  const shifted = new Date(baseTime + roundedOffsetMinutes * 60_000);
  const baseDay = Date.UTC(birthYear, birthMonth - 1, birthDay, 0, 0, 0, 0);
  const shiftedDay = Date.UTC(
    shifted.getUTCFullYear(),
    shifted.getUTCMonth(),
    shifted.getUTCDate(),
    0,
    0,
    0,
    0,
  );

  return {
    year: shifted.getUTCFullYear(),
    month: shifted.getUTCMonth() + 1,
    day: shifted.getUTCDate(),
    hour: shifted.getUTCHours(),
    minute: shifted.getUTCMinutes(),
    dayOffset: Math.round((shiftedDay - baseDay) / 86400000),
  };
}

export function resolveTrueSolarDateTime(
  input: SolarDateTimeInput,
  longitude: number,
): SolarDateTimeParts & { trueSolarTimeInfo: TrueSolarTimeInfo; } {
  const { birthYear, birthMonth, birthDay, birthHour, birthMinute = 0 } = input;
  const longitudeCorrection = (longitude - STANDARD_MERIDIAN) * 4;
  const dayOfYear = getDayOfYear(birthYear, birthMonth, birthDay);
  const eot = equationOfTime(dayOfYear, birthYear);
  const totalCorrectionMinutes = longitudeCorrection + eot;
  const roundedCorrectionMinutes = Math.round(totalCorrectionMinutes);
  const resolvedDateTime = applyMinuteOffsetToSolarDateTime(input, roundedCorrectionMinutes);
  const trueTimeIndex = hourToTimeIndex(resolvedDateTime.hour + resolvedDateTime.minute / 60);

  return {
    ...resolvedDateTime,
    trueSolarTimeInfo: {
      clockTime: `${String(birthHour).padStart(2, '0')}:${String(birthMinute).padStart(2, '0')}`,
      trueSolarTime: `${String(resolvedDateTime.hour).padStart(2, '0')}:${String(resolvedDateTime.minute).padStart(2, '0')}`,
      longitude,
      correctionMinutes: Math.round(totalCorrectionMinutes * 10) / 10,
      trueTimeIndex,
      dayOffset: resolvedDateTime.dayOffset,
    },
  };
}

export function calculateTrueSolarTime(
  input: SolarDateTimeInput,
  longitude: number,
): TrueSolarTimeInfo {
  return resolveTrueSolarDateTime(input, longitude).trueSolarTimeInfo;
}
