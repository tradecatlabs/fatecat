const HOUR_IN_MS = 3_600_000;

const CHINA_DST_OFFSET_MS = HOUR_IN_MS;

interface DstPeriod {
  startUtc: number;
  endUtc: number;
}

interface DstRule {
  offsetMs: number;
  getPeriod(year: number): DstPeriod | undefined;
}

const DST_RULES: Record<number, DstRule> = {
  8: {
    offsetMs: CHINA_DST_OFFSET_MS,
    getPeriod: (year) => CHINA_DST_PERIODS[year],
  },
};

/**
 * 针对不同地区的夏令时规则，对输入 UTC 时间进行归一化，返回标准时间。
 * 目前仅支持北京时区（UTC+8）的中国夏令时规则。
 */
export function normalizeDateByTimezone(
  date: Date,
  timezoneOffsetHours: number = -date.getTimezoneOffset() / 60,
): Date {
  const rule = DST_RULES[timezoneOffsetHours];
  if (!rule) {
    return date;
  }
  return applyDstRule(date, timezoneOffsetHours, rule);
}

function applyDstRule(date: Date, timezoneOffsetHours: number, rule: DstRule): Date {
  const localTimestamp = date.getTime() + timezoneOffsetHours * HOUR_IN_MS;
  const localYear = new Date(localTimestamp).getUTCFullYear();
  const period = rule.getPeriod(localYear);

  if (!period) {
    return date;
  }

  if (localTimestamp >= period.startUtc && localTimestamp < period.endUtc) {
    return new Date(date.getTime() - rule.offsetMs);
  }

  return date;
}

interface ChinaDstPeriodDefinition {
  year: number;
  start: PeriodPoint;
  end: PeriodPoint;
}

interface PeriodPoint {
  month: number; // 1-12
  day: number;
  hour: number;
  minute?: number;
}

const CHINA_DST_PERIOD_DEFINITIONS: readonly ChinaDstPeriodDefinition[] = [
  { year: 1986, start: { month: 5, day: 4, hour: 2 }, end: { month: 9, day: 14, hour: 2 } },
  { year: 1987, start: { month: 4, day: 12, hour: 2 }, end: { month: 9, day: 13, hour: 2 } },
  { year: 1988, start: { month: 4, day: 10, hour: 2 }, end: { month: 9, day: 11, hour: 2 } },
  { year: 1989, start: { month: 4, day: 16, hour: 2 }, end: { month: 9, day: 17, hour: 2 } },
  { year: 1990, start: { month: 4, day: 15, hour: 2 }, end: { month: 9, day: 16, hour: 2 } },
  { year: 1991, start: { month: 4, day: 14, hour: 2 }, end: { month: 9, day: 15, hour: 2 } },
] as const;

const CHINA_DST_PERIODS: Record<number, DstPeriod> = CHINA_DST_PERIOD_DEFINITIONS.reduce(
  (acc, period) => {
    acc[period.year] = {
      startUtc: createLocalReferenceTimestamp(period.year, period.start),
      endUtc: createLocalReferenceTimestamp(period.year, period.end),
    };
    return acc;
  },
  {} as Record<number, DstPeriod>,
);

function createLocalReferenceTimestamp(year: number, point: PeriodPoint) {
  return Date.UTC(year, point.month - 1, point.day, point.hour, point.minute ?? 0, 0);
}
