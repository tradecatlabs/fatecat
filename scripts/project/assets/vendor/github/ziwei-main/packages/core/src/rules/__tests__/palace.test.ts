import { describe, expect, it } from "vitest";

import { BRANCH_KEYS } from "../../constants";
import {
  calculateCurrentPalaceIndex,
  calculateMainPalaceIndex,
  calculatePalaceStemsAndBranches,
  isLaiYin,
} from "../palace";

describe("rules/palace", () => {
  it("按五虎遁月规则推算宫位干支序列", () => {
    const result = calculatePalaceStemsAndBranches("Jia");

    expect(result).toHaveLength(12);
    expect(result[0]).toMatchObject({ stemKey: "Bing", branchKey: "Yin" });
    expect(result[1]).toMatchObject({ stemKey: "Ding", branchKey: "Mao" });
    expect(result.at(-1)).toMatchObject({ stemKey: "Ding", branchKey: BRANCH_KEYS[1] });
  });

  it("遵循顺月逆时计算命宫索引", () => {
    expect(calculateMainPalaceIndex(0, 0)).toBe(0);
    expect(calculateMainPalaceIndex(0, 2)).toBe(10);
    expect(calculateMainPalaceIndex(5, 9)).toBe(8);
  });

  it("将宫位索引转换为命宫视角的序号", () => {
    expect(calculateCurrentPalaceIndex(0, 0)).toBe(0);
    expect(calculateCurrentPalaceIndex(0, 11)).toBe(1);
    expect(calculateCurrentPalaceIndex(6, 3)).toBe(3);
  });

  it("仅在干相同且支非子丑时判定为来因宫", () => {
    expect(isLaiYin("Jia", "Jia", "Yin")).toBe(true);
    expect(isLaiYin("Jia", "Yi", "Yin")).toBe(false);
    expect(isLaiYin("Jia", "Jia", "Zi")).toBe(false);
  });
});
