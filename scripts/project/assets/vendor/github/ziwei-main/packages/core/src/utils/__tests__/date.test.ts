import { LunarHour, SolarTime } from "tyme4ts";
import { afterEach, describe, expect, it, vi } from "vitest";

import { createZiWeiRuntime } from "../../context";
import { getGlobalConfigs } from "../../infra/configs";
import {
  calculateHourByIndex,
  calculateLunisolarDateBySolar,
  calculateNatalDateBySolar,
  calculateZiWeiDate,
  fixLeapMonth,
  getStemAndBranchByYear,
  normalizeHour,
} from "../calendar";
import { getLunisolarDateText, getSolarDateText } from "../format";
import { calculateTrueSolarTime } from "../trueSolarTime";

const defaultConfigs = getGlobalConfigs();

afterEach(() => {
  vi.restoreAllMocks();
});

describe("utils/date", () => {
  it("解析紫微日期字符串为农历参数", () => {
    const result = calculateZiWeiDate("2024-02-10-3");

    expect(result).toEqual({
      stemKey: "Jia",
      branchKey: "Chen",
      monthIndex: 1,
      day: 10,
      hourIndex: 3,
    });
  });

  it("根据公历年份推导干支并校验范围", () => {
    expect(getStemAndBranchByYear(2024)).toEqual([0, 4]); // 甲辰
    expect(() => getStemAndBranchByYear(0)).toThrow(RangeError);
  });

  it("按配置决定晚子时是否跨日", () => {
    const lateZi = LunarHour.fromYmdHms(2024, 1, 1, 23, 0, 0);
    const normalized = normalizeHour(lateZi, defaultConfigs);

    expect(normalized.getLunarDay().getDay()).toBe(lateZi.getLunarDay().next(1).getDay());

    const keepCurrent = normalizeHour(lateZi, getGlobalConfigs({ division: { day: "current" } }));
    expect(keepCurrent.getLunarDay().getDay()).toBe(lateZi.getLunarDay().getDay());
  });

  it("依据阴历时辰与配置推导命盘日期", () => {
    const lateZi = LunarHour.fromYmdHms(2024, 1, 1, 23, 0, 0);
    const result = calculateNatalDateBySolar({
      date: lateZi,
      globalConfigs: defaultConfigs,
    });

    expect(result.stemKey).toBe("Jia");
    expect(result.branchKey).toBe("Chen");
    expect(result.monthIndex).toBe(0);
    expect(result.day).toBeGreaterThan(lateZi.getLunarDay().getDay());
    expect(result.hourIndex).toBe(0);
  });

  it("统一格式化时辰与阳历文本输出", () => {
    expect(calculateHourByIndex(4)).toEqual([8, 30, 0]);

    const date = new Date(2024, 2, 5, 7, 6, 0);
    expect(getSolarDateText(date)).toBe("2024-03-05 07:06");

    const solarTime = SolarTime.fromYmdHms(2024, 3, 5, 7, 6, 0);
    expect(getSolarDateText(solarTime)).toBe("2024-03-05 07:06");
  });

  it("将阳历转换为阴阳合历并生成文案", () => {
    const solarDate = new Date("2024-02-10T08:00:00+08:00");
    const lunarHour = calculateLunisolarDateBySolar(solarDate);

    expect(lunarHour.getYear()).toBe(2024);

    const runtime = createZiWeiRuntime();
    const text = getLunisolarDateText(lunarHour, 0, runtime.i18n);
    expect(text).toContain("年");
    expect(text).toMatch(/子时$/);
  });

  it("按照 month division 策略处理闰月", () => {
    const spy = vi.spyOn(LunarHour, "fromYmdHms").mockReturnValue(createMockHour());

    const leapHour = createMockLeapLunarHour();
    fixLeapMonth(leapHour, getGlobalConfigs({ division: { month: "last" } }));
    expect(spy).toHaveBeenLastCalledWith(2023, 5, 16, 23, 0, 0);

    fixLeapMonth(leapHour, getGlobalConfigs({ division: { month: "next" } }));
    expect(spy).toHaveBeenLastCalledWith(2023, 7, 16, 23, 0, 0);

    const early = createMockLeapLunarHour({ day: 10, hour: 10 });
    fixLeapMonth(early, getGlobalConfigs({ division: { month: "normal" } }));
    expect(spy).toHaveBeenLastCalledWith(2023, 5, 10, 10, 0, 0);

    const late = createMockLeapLunarHour({ day: 15, hour: 23 });
    fixLeapMonth(late, getGlobalConfigs({ division: { month: "normal" } }));
    expect(spy).toHaveBeenLastCalledWith(2023, 7, 15, 23, 0, 0);
  });

  it("依据 NOAA 公式计算真太阳时", () => {
    const base = new Date("2024-03-05T08:00:00+08:00");
    const corrected = calculateTrueSolarTime(base, 116.38333, 8);

    const diffMinutes = (corrected.getTime() - base.getTime()) / 60000;
    expect(diffMinutes).toBeCloseTo(-26.3092, 3);
    expect(corrected.toISOString()).toBe("2024-03-04T23:33:41.447Z");
  });
});

function createMockLeapLunarHour(options: { day?: number; hour?: number } = {}) {
  const year = new MockLunarYear(2023);
  const month = new MockLunarMonth(5, 6, year, true);
  const day = new MockLunarDay(options.day ?? 16, month);
  return new MockLunarHour(day, options.hour ?? 23) as unknown as LunarHour;
}

function createMockHour() {
  const year = new MockLunarYear(2023);
  const month = new MockLunarMonth(6, 6, year, false);
  const day = new MockLunarDay(16, month);
  return new MockLunarHour(day, 23) as unknown as LunarHour;
}

function wrapLunarDay(value: number, base: number = 30) {
  return ((((value - 1) % base) + base) % base) + 1;
}

class MockLunarYear {
  constructor(private value: number) {}

  getYear() {
    return this.value;
  }
}

class MockLunarMonth {
  constructor(
    public index: number,
    public monthWithLeap: number,
    private year: MockLunarYear,
    private leap: boolean,
  ) {}

  getMonth() {
    return this.index;
  }

  getMonthWithLeap() {
    return this.monthWithLeap;
  }

  getLunarYear() {
    return this.year;
  }

  isLeap() {
    return this.leap;
  }
}

class MockLunarDay {
  constructor(
    private dayValue: number,
    private month: MockLunarMonth,
  ) {}

  getDay() {
    return this.dayValue;
  }

  getLunarMonth() {
    return this.month;
  }

  next(offset: number) {
    const direction = offset >= 0 ? 1 : -1;
    const nextMonth = new MockLunarMonth(
      this.month.index + direction,
      this.month.monthWithLeap + direction,
      this.month.getLunarYear(),
      false,
    );
    return new MockLunarDay(wrapLunarDay(this.dayValue + offset), nextMonth);
  }
}

class MockLunarHour {
  constructor(
    private day: MockLunarDay,
    private hour: number,
    private minute: number = 0,
    private second: number = 0,
  ) {}

  getLunarDay() {
    return this.day;
  }

  getHour() {
    return this.hour;
  }

  getMinute() {
    return this.minute;
  }

  getSecond() {
    return this.second;
  }
}
