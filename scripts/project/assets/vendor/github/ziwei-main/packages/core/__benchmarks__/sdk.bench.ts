import { bench, describe } from "vitest";

import { createZiWeiByLunisolar } from "../src";

/**
 * Standardized Benchmark Template for ziwei-core
 *
 * 包含三类测试：
 * 1. Baseline 基准
 * 2. 多参数 Case 对比（A/B/C…）
 * 3. 大规模压力测试（Stress Test）
 *
 * 你可以按需增加或删减。
 */

describe("Baseline Benchmark", () => {
  // ================================
  // 1. Baseline Benchmark
  // ================================
  bench(
    "Baseline — 1999-2-10 01 (Yang)",
    () => {
      createZiWeiByLunisolar({
        name: "baseline",
        gender: "Yang",
        date: "1999-2-10-1",
      });
    },
    {
      time: 2000,
      warmupTime: 500,
    },
  );
});
