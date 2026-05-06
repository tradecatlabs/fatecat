import { describe, expect, it } from "vitest";

import ZHHans from "../locales/zh-Hans";
import ZHHant from "../locales/zh-Hant";

describe("infra/i18n locales", () => {
  it("确保简繁翻译内容一致", () => {
    expect(ZHHans.star.ZiWei.name).toBe("紫微");
    expect(ZHHant.star.ZiWei.name).toBe("紫微");
    expect(ZHHans.palace.Ming.name).toBe("命宫");
    expect(ZHHant.palace.Ming.name).toBe("命宮");
  });

  it("定义共通的辅助文案", () => {
    expect(ZHHans.hour).toBe("时");
    expect(ZHHant.hour).toBe("時");
    expect(ZHHans.fiveElementScheme.Huo).toBe(ZHHant.fiveElementScheme.Huo);
  });
});
