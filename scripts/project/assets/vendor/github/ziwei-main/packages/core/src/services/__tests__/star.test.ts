import { afterEach, describe, expect, it, vi } from "vitest";

import { createZiWeiRuntime } from "../../context";
import { getGlobalConfigs } from "../../infra/configs";
import { calculatePalaceStemsAndBranches } from "../../rules/palace";
import * as starRules from "../../rules/star";
import { calculateStarIndex } from "../../rules/star";
import { calculateMinorStars, calculateStars } from "../star";

describe("services/star", () => {
  it("计算主星与辅星并输出本地化四化", () => {
    const runtime = createZiWeiRuntime();
    const stemBranches = calculatePalaceStemsAndBranches("Jia");
    const { ziweiIndex, tianfuIndex } = calculateStarIndex(15, 3);
    const stars = calculateStars(runtime, {
      stemBranches,
      birthYearStemKey: "Jia",
      ziweiIndex,
      tianfuIndex,
      monthIndex: 0,
      hourIndex: 0,
    });

    expect(stars).toHaveLength(12);
    expect(stars.every((list) => Array.isArray(list))).toBe(true);
    expect(stars[ziweiIndex].some((star) => star.key === "ZiWei")).toBe(true);
    expect(stars[tianfuIndex].some((star) => star.key === "TianFu")).toBe(true);

    const lianZhen = stars.flat().find((star) => star.key === "LianZhen");
    expect(lianZhen?.YT?.name).toBe(runtime.i18n.$t("transformation.A"));
    expect(lianZhen?.ST?.exit?.name).toBeDefined();
  });

  it("onlyMajor 配置时跳过小星计算", () => {
    const runtime = createZiWeiRuntime({ configs: getGlobalConfigs({ star: "onlyMajor" }) });
    const stemBranches = calculatePalaceStemsAndBranches("Jia");
    const { ziweiIndex, tianfuIndex } = calculateStarIndex(15, 3);

    const stars = calculateStars(runtime, {
      stemBranches,
      birthYearStemKey: "Jia",
      ziweiIndex,
      tianfuIndex,
      monthIndex: 0,
      hourIndex: 0,
    });

    expect(stars.flat().some((star) => star.type === "minor")).toBe(false);
    expect(stars[ziweiIndex].some((star) => star.key === "ZiWei")).toBe(true);
  });

  it("onlyTransformation 配置时保留四化相关主星并照常挂载辅星", () => {
    const runtime = createZiWeiRuntime({
      configs: getGlobalConfigs({ star: "onlyTransformation" }),
    });
    const stemBranches = calculatePalaceStemsAndBranches("Jia");
    const { ziweiIndex, tianfuIndex } = calculateStarIndex(15, 3);

    const stars = calculateStars(runtime, {
      stemBranches,
      birthYearStemKey: "Jia",
      ziweiIndex,
      tianfuIndex,
      monthIndex: 0,
      hourIndex: 0,
    });

    const flattened = stars.flat();
    expect(flattened.some((star) => star.key === "TianFu")).toBe(false);
    expect(flattened.some((star) => star.key === "TianXiang" || star.key === "QiSha")).toBe(false);
    expect(flattened.some((star) => star.type === "minor")).toBe(true);
  });
});

describe("services/star minor branch", () => {
  afterEach(() => {
    vi.restoreAllMocks();
  });

  it("生成小星并包含 entry/exit 自化", () => {
    const runtime = createZiWeiRuntime();
    const stemBranches = calculatePalaceStemsAndBranches("Jia");
    const stars = stemBranches.map(() => []);

    vi.spyOn(starRules, "memoCalculateStarTransformation").mockReturnValue("A");

    const result = calculateMinorStars(runtime, {
      stars,
      stemBranches,
      birthYearStemKey: "Jia",
      monthIndex: 0,
      hourIndex: 0,
    });

    const flattened = result.flat();
    const entryStar = flattened.find((star) => star.ST?.entry);
    const exitStar = flattened.find((star) => star.ST?.exit);
    expect(entryStar?.ST?.entry).toBeDefined();
    expect(exitStar?.ST?.exit).toBeDefined();
  });

  it("忽略缺少星键的元数据项", () => {
    const runtime = createZiWeiRuntime();
    const stemBranches = calculatePalaceStemsAndBranches("Jia");
    const stars = stemBranches.map(() => []);

    vi.spyOn(starRules, "createMinorStarsMeta").mockReturnValue([
      { key: undefined, startIndex: 0, direction: 1, galaxy: undefined },
    ]);

    const result = calculateMinorStars(runtime, {
      stars,
      stemBranches,
      birthYearStemKey: "Jia",
      monthIndex: 0,
      hourIndex: 0,
    });

    expect(result.flat()).toHaveLength(0);
  });
});
