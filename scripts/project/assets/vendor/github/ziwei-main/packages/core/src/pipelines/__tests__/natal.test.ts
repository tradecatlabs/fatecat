import { afterEach, describe, expect, it, vi } from "vitest";

import type { CreateZiWeiSolarParams } from "../../typings";

import { createZiWeiRuntime } from "../../context";
import * as formatUtils from "../../utils/format";
import * as trueSolarUtils from "../../utils/trueSolarTime";
import { calculateNatalBySolar } from "../natal";

const baseSolarDate = new Date("1993-08-08T08:00:00+08:00");

function createSolarParams(
  overrides: Partial<CreateZiWeiSolarParams> = {},
): CreateZiWeiSolarParams {
  return {
    name: "测试命主",
    gender: "Yang",
    date: baseSolarDate,
    longitude: 116.38333,
    timezone: 8,
    useTrueSolarTime: true,
    ...overrides,
  };
}

describe("pipelines/natal", () => {
  afterEach(() => {
    vi.restoreAllMocks();
  });

  it("referenceDate 可覆盖大限计算时间", () => {
    const referenceDate = new Date("2010-02-12T00:00:00+08:00");
    const runtime = createZiWeiRuntime({
      now: () => new Date("2035-01-01T00:00:00+08:00"),
    });
    const runtimeReference = createZiWeiRuntime({
      now: () => referenceDate,
    });

    const params = createSolarParams({ useTrueSolarTime: false });

    const natalWithOverride = calculateNatalBySolar({ ...params, referenceDate })(runtime);
    const natalWithRuntimeNow = calculateNatalBySolar(params)(runtimeReference);

    expect(natalWithOverride.decade).toEqual(natalWithRuntimeNow.decade);
  });

  it("仅在启用真太阳时填充 solarDateByTrue", () => {
    const runtime = createZiWeiRuntime({
      now: () => new Date("2030-01-01T00:00:00+08:00"),
    });

    const natalWithTrueSolar = calculateNatalBySolar(
      createSolarParams({
        longitude: 121.4737,
        useTrueSolarTime: true,
      }),
    )(runtime);
    const natalWithoutTrueSolar = calculateNatalBySolar(
      createSolarParams({
        longitude: 121.4737,
        useTrueSolarTime: false,
      }),
    )(runtime);

    expect(natalWithTrueSolar.solarDateByTrue).toBeDefined();
    expect(natalWithoutTrueSolar.solarDateByTrue).toBeUndefined();
  });

  it("每次调用前都切换运行时语言", () => {
    const runtime = createZiWeiRuntime({
      now: () => new Date("2030-01-01T00:00:00+08:00"),
    });

    const hansParams = createSolarParams({ language: "zh-Hans", useTrueSolarTime: false });
    const hantParams = createSolarParams({ language: "zh-Hant", useTrueSolarTime: false });

    const hansNatal = calculateNatalBySolar(hansParams)(runtime);
    const hantNatal = calculateNatalBySolar(hantParams)(runtime);
    const hansAgain = calculateNatalBySolar(hansParams)(runtime);

    expect(hansNatal.hour.endsWith("时")).toBe(true);
    expect(hantNatal.hour.endsWith("時")).toBe(true);
    expect(hansAgain.hour.endsWith("时")).toBe(true);
  });

  it("缺省经度时会使用默认经度", () => {
    const runtime = createZiWeiRuntime({
      now: () => new Date("2030-01-01T00:00:00+08:00"),
    });
    const params = createSolarParams({ useTrueSolarTime: true });

    delete (params as { longitude?: number }).longitude;

    const trueSolarTime = new Date("1993-08-08T07:45:00+08:00");
    const spy = vi.spyOn(trueSolarUtils, "calculateTrueSolarTime").mockReturnValue(trueSolarTime);

    const natal = calculateNatalBySolar(params)(runtime);
    const expectedText = formatUtils.getSolarDateText(trueSolarTime);

    expect(spy).toHaveBeenCalledWith(baseSolarDate, 116.38333, 8);
    expect(natal.solarDateByTrue).toBe(expectedText);
  });

  it("显式传入 undefined 也会回退到默认经度", () => {
    const runtime = createZiWeiRuntime({
      now: () => new Date("2030-01-01T00:00:00+08:00"),
    });
    const params = createSolarParams({ useTrueSolarTime: true });
    (params as { longitude?: number }).longitude = undefined;

    const trueSolarTime = new Date("1993-08-08T07:40:00+08:00");
    const spy = vi.spyOn(trueSolarUtils, "calculateTrueSolarTime").mockReturnValue(trueSolarTime);

    const natal = calculateNatalBySolar(params)(runtime);
    const expectedText = formatUtils.getSolarDateText(trueSolarTime);

    expect(spy).toHaveBeenCalledWith(baseSolarDate, 116.38333, 8);
    expect(natal.solarDateByTrue).toBe(expectedText);
  });
});
