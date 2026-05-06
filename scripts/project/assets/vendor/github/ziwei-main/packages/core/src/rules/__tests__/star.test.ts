import { describe, expect, it } from "vitest";

import { calculateStarIndex, calculateStarTransformation, getMinorStarIndices } from "../star";

describe("rules/star", () => {
  it("根据日数与五行局推算紫微/天府索引", () => {
    const result = calculateStarIndex(15, 3);

    expect(result).toEqual({ ziweiIndex: 4, tianfuIndex: 8 });

    const offsetResult = calculateStarIndex(21, 5);
    expect(offsetResult).toEqual({ ziweiIndex: 8, tianfuIndex: 4 });
  });

  it("根据月序与时辰推导左右昌曲索引", () => {
    expect(getMinorStarIndices(0, 0)).toEqual({
      zuofuIndex: 2,
      youbiIndex: 8,
      wenchangIndex: 8,
      wenquIndex: 2,
    });

    expect(getMinorStarIndices(5, 7)).toEqual({
      zuofuIndex: 7,
      youbiIndex: 3,
      wenchangIndex: 1,
      wenquIndex: 9,
    });
  });

  it("映射天干与星曜得到禄权科忌并在缺省时返回 undefined", () => {
    expect(
      calculateStarTransformation({
        stemKey: "Jia",
        starKey: "LianZhen",
      }),
    ).toBe("A");

    expect(
      calculateStarTransformation({
        stemKey: "Jia",
        starKey: "TianXiang",
      }),
    ).toBeUndefined();
  });
});
