import { LunarHour } from "tyme4ts";
import { afterEach, describe, expect, it, vi } from "vitest";

import type { BranchKey, Palace, PalaceKey, StarKey } from "../../typings";

import { BRANCH, BRANCH_KEYS, PALACE_HANS, PALACE_KEYS, STAR_HANS, STEM } from "../../constants";
import { createZiWeiRuntime } from "../../context";
import { createPalace } from "../../models/palace";
import * as calendarUtils from "../../utils/calendar";
import * as decadeService from "../decade";

const { calculateDecade, calculateDecadeByDate, calculateYearly } = decadeService;

const sampleStars: StarKey[] = ["ZiWei", "TaiYang", "WuQu", "TianTong"];

function createTestPalace(index: number, branchKey: BranchKey): Palace {
  const key = PALACE_KEYS[index] as PalaceKey;
  const start = index * 10 + 1;
  return createPalace({
    index,
    key,
    name: PALACE_HANS[key].name,
    isLaiYin: false,
    stem: { key: "Jia", name: STEM.Jia },
    branch: { key: branchKey, name: BRANCH[branchKey] },
    stars: sampleStars.map((starKey) => ({
      key: starKey,
      name: STAR_HANS[starKey].name,
      abbr: STAR_HANS[starKey].abbr,
      type: "major",
    })),
    decadeRanges: [start, start + 9],
  });
}

function createTestPalaces() {
  return BRANCH_KEYS.map((branchKey, index) => createTestPalace(index, branchKey));
}

describe("services/decade", () => {
  afterEach(() => {
    vi.restoreAllMocks();
  });
  it("在有效与超出范围时均计算正确的流年", () => {
    expect(calculateYearly(0, 0, 1990, 1)).toEqual({ name: 1990, age: 1 });
    expect(calculateYearly(10, 0, 1990, 1)).toEqual({ name: 0, age: 0 });
  });

  it("创建本地化的大限宫位并保持确定性流年", () => {
    const runtime = createZiWeiRuntime();
    const palaces = createTestPalaces();

    const decade = calculateDecade(runtime, {
      palaces,
      index: 0,
      birthYear: 1990,
      birthYearBranchKey: "Zi",
    });

    expect(decade).toHaveLength(12);
    expect(decade[0]).toMatchObject({
      key: "Ming",
      name: runtime.i18n.$t("palace.Ming.decade"),
      yearly: { name: 1990, age: 1 },
    });
    expect(decade[10].yearly).toEqual({ name: 0, age: 0 });
  });

  it("找不到当前年龄对应大限时回退到命宫索引", () => {
    const runtime = createZiWeiRuntime();
    const palaces = createTestPalaces().map((palace) => ({
      ...palace,
      decadeRanges: [400, 409],
    }));

    const lunarHour = LunarHour.fromYmdHms(2300, 1, 1, 0, 0, 0);
    vi.spyOn(calendarUtils, "calculateLunisolarDateBySolar").mockReturnValue(lunarHour);
    vi.spyOn(calendarUtils, "calculateNatalDateBySolar").mockReturnValue({
      stemKey: "Jia",
      branchKey: "Zi",
      year: 2300,
      monthIndex: 0,
      day: 1,
      hourIndex: 0,
    });
    const expected = calculateDecade(runtime, {
      palaces,
      index: 0,
      birthYear: 1990,
      birthYearBranchKey: "Zi",
    });

    const result = calculateDecadeByDate(runtime, {
      palaces,
      birthYear: 1990,
      birthYearBranchKey: "Zi",
      date: new Date("2300-01-01T00:00:00Z"),
    });

    expect(result).toEqual(expected);
  });
});
