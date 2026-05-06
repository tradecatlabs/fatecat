// biome-ignore-all lint/suspicious/noExplicitAny: false positive
import { afterEach, describe, expect, it, vi } from "vitest";

import { createZiWeiRuntime } from "../../context";
import * as natalService from "../../services/natal";
import { calculateNatalByLunisolar } from "../natal";

describe("pipelines/natal bridges", () => {
  afterEach(() => {
    vi.restoreAllMocks();
  });

  it("农历参数直接透传到 calculateNatal 且不包含真太阳时", () => {
    const runtime = createZiWeiRuntime();
    const natalSpy = vi.spyOn(natalService, "calculateNatal").mockReturnValue({} as any);

    const result = calculateNatalByLunisolar({
      name: "测试",
      gender: "Yang",
      date: "1999-1-5-3",
      language: "zh-Hant",
    })(runtime);

    expect(result).toBe(natalSpy.mock.results[0].value);
    const [ctx, payload, referenceDate] = natalSpy.mock.calls[0];
    expect(ctx).toBe(runtime);
    expect(payload).toMatchObject({
      name: "测试",
      gender: "Yang",
      solarDateByTrue: undefined,
    });
    expect(referenceDate).toBeUndefined();
    expect(runtime.i18n.getCurrentLanguage()).toBe("zh-Hant");
  });
});
