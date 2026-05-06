import { describe, expect, it } from "vitest";

import { computeExitArrowLayout, type Orientation, orientationFromPalaceIndex } from "../starUtil";

describe("orientationFromPalaceIndex", () => {
  it("maps palace index 0..11 to expected orientation", () => {
    const expected: Orientation[] = [
      "bottom",
      "left",
      "left",
      "top",
      "top",
      "top",
      "top",
      "right",
      "right",
      "bottom",
      "bottom",
      "bottom",
    ];
    for (let i = 0; i < expected.length; i++) {
      expect(orientationFromPalaceIndex(i)).toBe(expected[i]);
    }
  });
});

describe("computeExitArrowLayout", () => {
  const base = {
    x: 100,
    y: 200,
    index: 0,
    fontSize: 10,
    fontLineHeight: 1,
    palaceStrokeWidth: 2,
    selfTransformationMarginTop: 4,
    palaceSide: 300,
    boardStrokeWidth: 1,
    boardPadding: 5,
    selfTransformationFontSize: 12,
    palacePadding: 8,
  };

  it("computes layout for left orientation", () => {
    const layout = computeExitArrowLayout({ ...base, orientation: "left" });
    expect(layout.points).toEqual([
      [105, 228],
      [105, 235],
      [-1, 235],
    ]);
    expect(layout.label.x).toBeCloseTo(-10.2, 4);
    expect(layout.label.y).toBeCloseTo(239.2, 4);
  });

  it("computes layout for right orientation", () => {
    const layout = computeExitArrowLayout({ ...base, orientation: "right" });
    expect(layout.points).toEqual([
      [105, 228],
      [105, 235],
      [301, 235],
    ]);
    expect(layout.label.x).toBeCloseTo(310.2, 4);
    expect(layout.label.y).toBeCloseTo(239.2, 4);
  });

  it("computes layout for top orientation", () => {
    const layout = computeExitArrowLayout({ ...base, orientation: "top" });
    expect(layout.points).toEqual([
      [105, 196],
      [105, 191],
    ]);
    expect(layout.label.x).toBe(105);
    expect(layout.label.y).toBe(186);
  });

  it("computes layout for bottom orientation", () => {
    const layout = computeExitArrowLayout({ ...base, orientation: "bottom" });
    expect(layout.points).toEqual([
      [105, 228],
      [105, 301],
    ]);
    expect(layout.label.x).toBe(105);
    expect(layout.label.y).toBeCloseTo(314.742, 4);
  });
});
