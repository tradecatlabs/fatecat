import { EightChar, SolarTime } from "tyme4ts";
import { describe, expect, it, vi } from "vitest";

import { calculateLunisolarDateBySexagenary } from "../sexagenary";

describe("干支转阴历", () => {
  it("在给定 60 年周期内匹配四柱日期", () => {
    const targetSolar = SolarTime.fromYmdHms(1993, 8, 8, 8, 0, 0);
    const eightChar = targetSolar.getLunarHour().getEightChar().toString().replace(/\s+/g, "");

    const { solarTime, lunarHour } = calculateLunisolarDateBySexagenary(eightChar, {
      cycleStartYear: 1984,
    });

    expect(solarTime.getYear()).toBe(targetSolar.getYear());
    expect(solarTime.getMonth()).toBe(targetSolar.getMonth());
    expect(solarTime.getDay()).toBe(targetSolar.getDay());
    expect(solarTime.getHour()).toBe(targetSolar.getHour());
    expect(solarTime.getMinute()).toBe(targetSolar.getMinute());
    expect(lunarHour.getEightChar().toString().replace(/\s+/g, "")).toBe(eightChar);
  });

  it("解析无分隔符的四柱字符串", () => {
    const { solarTime } = calculateLunisolarDateBySexagenary("癸酉庚申辛酉壬辰", {
      cycleStartYear: 1984,
    });

    expect(solarTime.getYear()).toBe(1993);
    expect(solarTime.getMonth()).toBe(8);
    expect(solarTime.getDay()).toBe(8);
    expect(solarTime.getHour()).toBe(8);
  });

  it("识别同一干支在上一轮 60 年周期中的对应日期", () => {
    const targetSolar = SolarTime.fromYmdHms(1993, 8, 8, 8, 0, 0);
    const eightChar = targetSolar.getLunarHour().getEightChar().toString().replace(/\s+/g, "");

    const { solarTime } = calculateLunisolarDateBySexagenary(eightChar, {
      cycleStartYear: 1924,
    });

    expect(targetSolar.getYear() - solarTime.getYear()).toBe(60);
  });

  it("拒绝长度不足 8 的字符串", () => {
    expect(() =>
      calculateLunisolarDateBySexagenary("甲子乙丑", {
        cycleStartYear: 1984,
      }),
    ).toThrow("Sexagenary input must be 8 characters");
  });

  it("拒绝包含非法干支的输入", () => {
    expect(() =>
      calculateLunisolarDateBySexagenary("甲子乙丑AA丁卯", {
        cycleStartYear: 1984,
      }),
    ).toThrow('Invalid pillar "AA" at position 2');
  });

  it("非字符串入参直接抛错", () => {
    expect(() =>
      calculateLunisolarDateBySexagenary({} as unknown as string, {
        cycleStartYear: 1984,
      }),
    ).toThrow("Sexagenary input only accepts compact string");
  });

  it("cycleStartYear 必须是整数", () => {
    expect(() =>
      calculateLunisolarDateBySexagenary("癸酉庚申辛酉壬辰", {
        cycleStartYear: 1984.5,
      }),
    ).toThrow("cycleStartYear 必须是整数年份");
  });

  it("无匹配结果时抛出 RangeError", () => {
    const spy = vi
      .spyOn(EightChar.prototype, "getSolarTimes")
      .mockReturnValue([] as unknown as SolarTime[]);

    expect(() =>
      calculateLunisolarDateBySexagenary("癸酉庚申辛酉壬辰", {
        cycleStartYear: 1984,
      }),
    ).toThrow("未在 1984-2043 找到 癸酉庚申辛酉壬辰 对应的时间");

    spy.mockRestore();
  });
});
