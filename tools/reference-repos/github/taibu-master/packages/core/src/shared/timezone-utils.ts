export type ZonedDateTimeInput = {
  year: number;
  month: number;
  day: number;
  hour: number;
  minute?: number;
  second?: number;
};

export const DEFAULT_DIVINATION_TIMEZONE = 'Asia/Shanghai';

export function getTimeZoneOffsetMinutes(timeZone: string, date: Date): number {
  const formatter = new Intl.DateTimeFormat('en-US', {
    timeZone,
    hour12: false,
    year: 'numeric',
    month: '2-digit',
    day: '2-digit',
    hour: '2-digit',
    minute: '2-digit',
    second: '2-digit',
  });

  const parts = formatter.formatToParts(date);
  const values: Record<string, number> = {};
  for (const part of parts) {
    if (part.type !== 'literal') {
      values[part.type] = Number(part.value);
    }
  }

  const asUTC = Date.UTC(
    values.year,
    (values.month ?? 1) - 1,
    values.day ?? 1,
    values.hour ?? 0,
    values.minute ?? 0,
    values.second ?? 0,
  );
  return (asUTC - date.getTime()) / 60000;
}

export function zonedTimeToUtc(input: ZonedDateTimeInput, timeZone: string): Date {
  const { year, month, day, hour, minute = 0, second = 0 } = input;
  const utcGuess = new Date(Date.UTC(year, month - 1, day, hour, minute, second));

  let offsetMinutes: number;
  try {
    offsetMinutes = getTimeZoneOffsetMinutes(timeZone, utcGuess);
  } catch (error) {
    if (error instanceof RangeError) {
      throw new Error('timezone 无效');
    }
    throw error;
  }

  return new Date(utcGuess.getTime() - offsetMinutes * 60000);
}

/**
 * 将目标时区的壁钟时间转为一个 Date 对象，使其本地时间访问器
 * （.getHours()、.getMinutes() 等）返回目标时区的壁钟值。
 *
 * 前提：服务器时区在调用期间不发生变化（如 DST 切换）。
 * 适用于需要将时区壁钟时间传给仅接受 Date 对象的第三方库的场景。
 */
export function zonedWallClockToSystemDate(input: ZonedDateTimeInput, timeZone: string): Date {
  const utcDate = zonedTimeToUtc(input, timeZone);
  const targetOffset = getTimeZoneOffsetMinutes(timeZone, utcDate);
  const serverOffset = -utcDate.getTimezoneOffset();
  return new Date(utcDate.getTime() + (targetOffset - serverOffset) * 60000);
}
