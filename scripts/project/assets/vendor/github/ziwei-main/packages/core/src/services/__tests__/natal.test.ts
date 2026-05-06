import { afterEach, describe, expect, it, vi } from "vitest";

import { createZiWeiRuntime } from "../../context";
import * as decadeService from "../decade";
import { calculateNatal } from "../natal";

const baseParams = {
  name: "测试命主",
  gender: "Yang",
  monthIndex: 0,
  day: 15,
  hourIndex: 2,
  birthYear: 1993,
  birthYearStemKey: "Gui",
  birthYearBranchKey: "You",
  solarDate: "1993-08-08 08:00",
  lunisolarDate: "癸酉年正月十五 丑时",
  sexagenaryCycleDate: "癸酉年",
} as const;

describe("services/natal", () => {
  afterEach(() => {
    vi.restoreAllMocks();
  });

  it("返回包含本地化信息的命盘与大限", () => {
    const runtime = createZiWeiRuntime({
      now: () => new Date("2030-01-01T00:00:00+08:00"),
    });

    const natal = calculateNatal(
      runtime,
      {
        ...baseParams,
        solarDateByTrue: "1993-08-08 07:48",
      },
      new Date("2010-01-01T00:00:00+08:00"),
    );

    expect(natal.name).toBe(baseParams.name);
    expect(natal.gender).toContain("男");
    expect(natal.palaces).toHaveLength(12);
    expect(natal.decade).toHaveLength(12);
    expect(natal.decadeDirection).toBe(-1);
    expect(natal.getDecade(0)).toHaveLength(12);
    expect(natal.getDecadeIndex()).toBeGreaterThanOrEqual(0);
  });
  it("缺省姓名时回退为匿名并使用 runtime.now", () => {
    const now = new Date("2040-01-01T00:00:00+08:00");
    const runtime = createZiWeiRuntime({
      now: () => now,
    });
    // 现在 calculateNatal 内部通过 calculateDecadeIndexByDate 来推断大限索引
    const decadeSpy = vi.spyOn(decadeService, "calculateDecadeIndexByDate");

    const natal = calculateNatal(runtime, {
      ...baseParams,
      name: undefined as unknown as string,
      gender: "Yin",
      birthYearStemKey: "Yi",
    });

    expect(natal.name).toBe("匿名");
    expect(natal.decadeDirection).toBe(1);
    expect(decadeSpy).toHaveBeenCalledWith(runtime, expect.objectContaining({ date: now }));
  });
});
