import { describe, expect, it } from "vitest";

import { oppositeIndex, relativeIndex, wrapIndex } from "../math";

describe("utils/math", () => {
  it("wrapIndex 会把索引限制在给定范围", () => {
    expect(wrapIndex(13)).toBe(1);
    expect(wrapIndex(-1)).toBe(11);
    expect(wrapIndex(25, 10)).toBe(5);
  });

  it("wrapIndex 传入非法 max 会抛错", () => {
    expect(() => wrapIndex(0, 0)).toThrow(/max/);
  });

  it("relativeIndex 计算 12 宫内的相对宫位", () => {
    expect(relativeIndex(0)).toBe(0);
    expect(relativeIndex(3)).toBe(9);
  });

  it("oppositeIndex 返回本对宫索引", () => {
    expect(oppositeIndex(0)).toBe(6);
    expect(oppositeIndex(11)).toBe(5);
  });
});
