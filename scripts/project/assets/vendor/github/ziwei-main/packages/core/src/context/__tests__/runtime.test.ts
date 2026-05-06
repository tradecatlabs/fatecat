import { describe, expect, it, vi } from "vitest";

import { createZiWeiRuntime, resolveZiWeiRuntime } from "..";
import { getGlobalConfigs } from "../../infra/configs";
import { createZiWeiI18n } from "../../infra/i18n";

describe("context/createZiWeiRuntime", () => {
  it("在未注入选项时提供默认依赖", () => {
    const runtime = createZiWeiRuntime();
    const secondRuntime = createZiWeiRuntime();

    expect(runtime.i18n).toBeDefined();
    expect(runtime.configs).toMatchObject(getGlobalConfigs());
    expect(runtime.now()).toBeInstanceOf(Date);
    expect(runtime.i18n).not.toBe(secondRuntime.i18n);
  });

  it("支持注入自定义 i18n/config/now 实现", () => {
    const customI18n = createZiWeiI18n("zh-Hant");
    const customConfigs = getGlobalConfigs({ division: { day: "current" } });
    const now = vi.fn(() => new Date("2020-01-01T00:00:00+08:00"));

    const runtime = createZiWeiRuntime({
      i18n: customI18n,
      configs: customConfigs,
      now,
    });

    expect(runtime.i18n).toBe(customI18n);
    expect(runtime.configs).toBe(customConfigs);
    expect(runtime.now()).toEqual(new Date("2020-01-01T00:00:00+08:00"));
    expect(now).toHaveBeenCalledTimes(1);
  });

  it("resolveZiWeiRuntime 支持复用已创建的 runtime", () => {
    const runtime = createZiWeiRuntime({
      i18n: createZiWeiI18n("zh-Hant"),
      configs: getGlobalConfigs({ division: { day: "current" } }),
    });

    expect(resolveZiWeiRuntime({ runtime })).toBe(runtime);
  });
});
