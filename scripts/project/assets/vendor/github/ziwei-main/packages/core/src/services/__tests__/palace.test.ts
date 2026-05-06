import { describe, expect, it } from "vitest";

import { createZiWeiRuntime } from "../../context";
import { calculateDecadeRanges } from "../../rules/decade";
import { calculateFiveElementScheme } from "../../rules/element";
import { calculateMainPalaceIndex, calculatePalaceStemsAndBranches } from "../../rules/palace";
import { calculateStarIndex } from "../../rules/star";
import { calculatePalaces } from "../palace";

describe("services/palace", () => {
  it("构建带本地化信息与大限范围的十二宫", () => {
    const runtime = createZiWeiRuntime();
    const monthIndex = 0;
    const hourIndex = 0;
    const stemBranches = calculatePalaceStemsAndBranches("Jia");
    const mainPalaceIndex = calculateMainPalaceIndex(monthIndex, hourIndex);
    const { fiveElementSchemeValue } = calculateFiveElementScheme("Jia", "Yin");
    const { ziweiIndex, tianfuIndex } = calculateStarIndex(15, fiveElementSchemeValue);
    const decadeRanges = calculateDecadeRanges(mainPalaceIndex, 1, fiveElementSchemeValue);

    const palaces = calculatePalaces(runtime, {
      stemBranches,
      birthYearStemKey: "Jia",
      mainPalaceIndex,
      ziweiIndex,
      tianfuIndex,
      monthIndex,
      hourIndex,
      decadeDirection: 1,
      fiveElementSchemeValue,
    });

    expect(palaces).toHaveLength(12);
    expect(palaces[0]).toMatchObject({
      key: "Ming",
      name: runtime.i18n.$t("palace.Ming.name"),
      decadeRanges: decadeRanges[0],
    });
    expect(palaces[0].branch.name).toBe(runtime.i18n.$t("branch.Yin"));
    expect(palaces[0].stars).toHaveLength(0);
    expect(palaces[ziweiIndex].stars.some((star) => star.key === "ZiWei")).toBe(true);
    expect(palaces[tianfuIndex].stars.some((star) => star.key === "TianFu")).toBe(true);
  });
});
