import { describe, expect, it } from "vitest";

import { FIVE_ELEMENT_SCHEME } from "../../constants";
import { calculateFiveElementScheme } from "../element";

describe("rules/element", () => {
  it("returns 金四局 when命宫干支为甲寅", () => {
    const scheme = calculateFiveElementScheme("Wu", "Chou");
    expect(scheme).toMatchObject({
      fiveElementSchemeKey: "Jin",
      fiveElementSchemeName: FIVE_ELEMENT_SCHEME.Jin,
      fiveElementSchemeValue: 4,
    });
  });

  it("wraps indexes to cover跨越午未场景", () => {
    const scheme = calculateFiveElementScheme("Ding", "You");

    expect(scheme).toMatchObject({
      fiveElementSchemeKey: "Tu",
      fiveElementSchemeValue: 5,
    });
  });
});
