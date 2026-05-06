import { describe, expect, it } from "vitest";

import { STEM_TRANSFORMATIONS } from "../../constants";
import { createPalace } from "../palace";

describe("models/palace", () => {
  it("flying() 返回对应天干的四化星数组", () => {
    const palace = createPalace({
      index: 0,
      key: "Ming",
      name: "命宫",
      isLaiYin: false,
      stem: { key: "Jia", name: "甲" },
      branch: { key: "Zi", name: "子" },
      stars: [],
      decadeRanges: [1, 10],
    });

    expect(palace.flying()).toEqual(STEM_TRANSFORMATIONS.Jia);
  });
});
