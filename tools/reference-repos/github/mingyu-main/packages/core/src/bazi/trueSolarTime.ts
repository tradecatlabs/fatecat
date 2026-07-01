import type { SolarDateTimeInfo } from './baziTypes';
import { daysInSolarMonth } from '../calendar/date-validation';

export interface TrueSolarTimeResult {
  correctedTime: SolarDateTimeInfo;
  longitudeCorrectionMinutes: number;
  equationOfTimeMinutes: number;
  totalCorrectionMinutes: number;
}

function getDayOfYear(year: number, month: number, day: number): number {
  const current = new Date(Date.UTC(year, month - 1, day));
  const start = new Date(Date.UTC(year, 0, 1));
  return Math.floor((current.getTime() - start.getTime()) / 86400000) + 1;
}

function assertIntegerInRange(value: number, label: string, min: number, max: number) {
  if (!Number.isInteger(value) || value < min || value > max) {
    throw new Error(`${label}需在 ${min}-${max} 之间。`);
  }
}

function validateSolarDate(year: number, month: number, day: number) {
  assertIntegerInRange(year, '年份', 1900, 2100);
  assertIntegerInRange(month, '月份', 1, 12);
  if (!Number.isInteger(day) || day < 1) {
    throw new Error('日期不能小于 1。');
  }

  const maxDay = daysInSolarMonth(year, month);
  if (day > maxDay) {
    throw new Error(`日期需在 1-${maxDay} 之间。`);
  }
}

function validateTimePart(hour: number, minute: number) {
  assertIntegerInRange(hour, '小时', 0, 23);
  assertIntegerInRange(minute, '分钟', 0, 59);
}

function validateLongitude(value: number, label: string) {
  if (!Number.isFinite(value) || value < -180 || value > 180) {
    throw new Error(`${label}需在 -180 到 180 之间。`);
  }
}

function toDateTimeInfo(date: Date): SolarDateTimeInfo {
  return {
    year: date.getUTCFullYear(),
    month: date.getUTCMonth() + 1,
    day: date.getUTCDate(),
    hour: date.getUTCHours(),
    minute: date.getUTCMinutes(),
    second: date.getUTCSeconds(),
  };
}

export function calculateEquationOfTimeMinutes(year: number, month: number, day: number): number {
  validateSolarDate(year, month, day);
  const dayOfYear = getDayOfYear(year, month, day);
  const angle = (2 * Math.PI * (dayOfYear - 81)) / 364;
  return 9.87 * Math.sin(2 * angle) - 7.53 * Math.cos(angle) - 1.5 * Math.sin(angle);
}

export function calculateTrueSolarTime(
  standardTime: Pick<SolarDateTimeInfo, 'year' | 'month' | 'day' | 'hour' | 'minute'>,
  longitude: number,
  standardMeridian = 120,
): TrueSolarTimeResult {
  validateSolarDate(standardTime.year, standardTime.month, standardTime.day);
  validateTimePart(standardTime.hour, standardTime.minute);
  validateLongitude(longitude, '经度');
  validateLongitude(standardMeridian, '标准经线');

  const equationOfTimeMinutes = calculateEquationOfTimeMinutes(
    standardTime.year,
    standardTime.month,
    standardTime.day,
  );
  const longitudeCorrectionMinutes = (longitude - standardMeridian) * 4;
  const totalCorrectionMinutes = equationOfTimeMinutes + longitudeCorrectionMinutes;

  const correctedDate = new Date(
    Date.UTC(
      standardTime.year,
      standardTime.month - 1,
      standardTime.day,
      standardTime.hour,
      standardTime.minute,
      0,
    ),
  );
  correctedDate.setTime(correctedDate.getTime() + totalCorrectionMinutes * 60000);

  return {
    correctedTime: toDateTimeInfo(correctedDate),
    longitudeCorrectionMinutes,
    equationOfTimeMinutes,
    totalCorrectionMinutes,
  };
}
