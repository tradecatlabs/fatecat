import { describe, expect, it } from "vitest";

import { normalizeDateByTimezone } from "../timezone";

describe("utils/timezone", () => {
  it("在 1987 年夏令时范围内的北京时间减一小时", () => {
    const summer = new Date("1987-07-01T08:00:00+08:00");
    const normalized = normalizeDateByTimezone(summer, 8);

    expect(normalized.getTime()).toBe(summer.getTime() - 3_600_000);
  });

  it("1986 年使用特例的起止日期进行归一化", () => {
    const before = new Date("1986-05-03T12:00:00+08:00");
    const during = new Date("1986-08-01T12:00:00+08:00");
    const after = new Date("1986-09-20T12:00:00+08:00");

    expect(normalizeDateByTimezone(before, 8).getTime()).toBe(before.getTime());
    expect(normalizeDateByTimezone(during, 8).getTime()).toBe(during.getTime() - 3_600_000);
    expect(normalizeDateByTimezone(after, 8).getTime()).toBe(after.getTime());
  });

  it("未识别的时区或年份不会调整时间", () => {
    const unsupportedZone = new Date("1993-08-08T08:00:00+08:00");
    const nonDstYear = new Date("1995-08-08T08:00:00+08:00");

    expect(normalizeDateByTimezone(unsupportedZone, 7).getTime()).toBe(unsupportedZone.getTime());
    expect(normalizeDateByTimezone(nonDstYear, 8).getTime()).toBe(nonDstYear.getTime());
  });

  it("边界时刻在 2:00 启用或结束夏令时", () => {
    const startBoundaryBefore = new Date("1988-04-10T01:59:59+08:00");
    const startBoundaryAfter = new Date("1988-04-10T02:00:00+08:00");
    const endBoundaryBefore = new Date("1988-09-11T01:59:59+08:00");
    const endBoundaryAfter = new Date("1988-09-11T02:00:00+08:00");

    expect(normalizeDateByTimezone(startBoundaryBefore, 8).getTime()).toBe(
      startBoundaryBefore.getTime(),
    );
    expect(normalizeDateByTimezone(startBoundaryAfter, 8).getTime()).toBe(
      startBoundaryAfter.getTime() - 3_600_000,
    );
    expect(normalizeDateByTimezone(endBoundaryBefore, 8).getTime()).toBe(
      endBoundaryBefore.getTime() - 3_600_000,
    );
    expect(normalizeDateByTimezone(endBoundaryAfter, 8).getTime()).toBe(endBoundaryAfter.getTime());
  });
});
