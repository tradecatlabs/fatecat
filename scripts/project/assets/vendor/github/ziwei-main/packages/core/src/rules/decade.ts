import type { FiveElementSchemeValue } from "../typings";

import { wrapIndex } from "../utils/math";

/**
 * 计算以 mainIndex 为起点、按指定方向遍历 12 宫位的“10 年大运区间”。
 *
 * 规则说明：
 * - 共遍历 12 步（对应 12 宫位），方向由 decadeDirection 决定（顺时针 1 / 逆时针 -1）。
 * - 第 i 步（i 从 0 到 11）的区间为 [base + 10*i, base + 10*i + 9]，
 *   其中 base 为 fiveElementSchemeValue。
 * - 目标宫位索引通过 wrapIndex 做环形处理，确保在 0..11 范围内。
 *
 * 参数：
 * - mainIndex: number
 *   起始宫位索引，范围应为 0..11。
 *
 * - decadeDirection: 1 | -1
 *   遍历方向：1 表示顺时针（索引递增），-1 表示逆时针（索引递减）。
 *
 * - fiveElementSchemeValue: FiveElementSchemeValue
 *   初始的大运起点值（第一个 10 年区间的起始值）。
 *
 * 返回：
 * - [number, number]
 *   长度为 12 的数组，数组下标为环形后的宫位索引，
 *   值为对应宫位的大运区间 [start, end]（含头含尾）。
 *
 * 复杂度：
 * - 时间复杂度 O(12)（常数）
 * - 空间复杂度 O(12)
 */
export function calculateDecadeRanges(
  mainIndex: number,
  decadeDirection: 1 | -1,
  fiveElementSchemeValue: FiveElementSchemeValue,
) {
  const decadeRanges = Array<[number, number]>(12);

  for (let i = 0; i < 12; i++) {
    const idx = wrapIndex(mainIndex + decadeDirection * i);
    const start = fiveElementSchemeValue + 10 * i;
    decadeRanges[idx] = [start, start + 9];
  }
  return decadeRanges;
}
