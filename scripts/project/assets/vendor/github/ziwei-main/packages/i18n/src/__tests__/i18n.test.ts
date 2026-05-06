import { describe, expect, test, vi } from "vitest";

import { createI18n, type I18nLanguages } from "../index";

const resources = {
  "zh-CN": {
    greeting: {
      welcome: "欢迎",
    },
    farewell: "再见",
    scoped: {
      message: "作用域消息",
    },
  },
  "zh-Hant": {
    greeting: {
      welcome: "歡迎",
    },
    farewell: "再見",
    onlyTraditional: "只有繁體",
    scoped: {
      message: "作用域訊息",
    },
  },
} as const;

describe("createI18n()", () => {
  test("能够读取嵌套与顶层键", () => {
    const i18n = createI18n({ lang: "zh-CN", resources });
    expect(i18n.$t("greeting.welcome")).toBe("欢迎");
    expect(i18n.$t("farewell")).toBe("再见");
  });

  test("支持回退语言链", () => {
    const i18n = createI18n({
      lang: "zh-CN",
      resources,
      fallbackLanguages: "zh-Hant",
    });

    expect(i18n.$t("onlyTraditional")).toBe("只有繁體");
    i18n.setFallbackLanguages(["zh-Hant"]);
    expect(i18n.$t("onlyTraditional")).toBe("只有繁體");
  });

  test("has() 能检查指定语言", () => {
    const i18n = createI18n({ lang: "zh-CN", resources });
    expect(i18n.has("onlyTraditional")).toBe(false);
    expect(i18n.has("onlyTraditional", "zh-Hant")).toBe(true);
    expect(i18n.has("onlyTraditional", "zh-CN")).toBe(false);
  });

  test("缺失文案时触发 onMissing", () => {
    const onMissing = vi.fn();
    const i18n = createI18n({ lang: "zh-CN", resources, onMissing });
    // @ts-expect-error: 故意访问不存在的 key
    expect(i18n.$t("unknown.key", "Default")).toBe("Default");
    expect(onMissing).toHaveBeenCalledWith({
      key: "unknown.key",
      languagesTried: ["zh-CN"],
    });
  });

  test("自定义分隔符", () => {
    const i18n = createI18n({ lang: "zh-CN", resources, separator: "/" });
    // @ts-expect-error: 分隔符不同于默认 schema
    expect(i18n.$t("scoped/message")).toBe("作用域消息");
  });

  test("自定义分隔符下的单段 key 也能解析", () => {
    const i18n = createI18n({ lang: "zh-CN", resources, separator: "/" });
    expect(i18n.$t("farewell")).toBe("再见");
  });

  test("自定义分隔符仍兼容默认分隔符", () => {
    const i18n = createI18n({ lang: "zh-CN", resources, separator: "/" });
    expect(i18n.$t("greeting.welcome")).toBe("欢迎");
  });

  test("扁平资源在自定义分隔符下同样兼容默认分隔符", () => {
    type FlatResources = Record<"zh-CN" | "zh-Hant", Record<string, string>>;
    const protoEntries: Record<string, string> = {
      "proto/message": "跳过",
    };
    const cn = Object.create(protoEntries) as Record<string, string>;
    cn["scoped/message"] = "作用域消息";
    const hant = Object.create(protoEntries) as Record<string, string>;
    hant["scoped/message"] = "作用域訊息";
    const flatResources: FlatResources = Object.create(null);
    flatResources["zh-CN"] = cn;
    flatResources["zh-Hant"] = hant;
    const i18n = createI18n({ lang: "zh-CN", resources: flatResources, separator: "/" });
    expect(i18n.$t("scoped/message")).toBe("作用域消息");
    expect(i18n.$t("scoped.message")).toBe("作用域消息");
  });

  test("语言资源会忽略继承属性", () => {
    const protoResource = {
      inherited: {
        skip: "proto",
      },
    };
    const derivedResource = Object.create(protoResource);
    Object.assign(derivedResource, resources["zh-CN"]);
    const protoMap = {
      prototypeLang: derivedResource,
    };
    const resourcesWithProto = Object.create(protoMap);
    resourcesWithProto["zh-CN"] = derivedResource;
    resourcesWithProto["zh-Hant"] = resources["zh-Hant"];

    const i18n = createI18n({
      lang: "zh-CN",
      resources: resourcesWithProto as typeof resources,
    });
    expect(i18n.$t("greeting.welcome")).toBe("欢迎");
  });

  test("非字符串值会被忽略", () => {
    const weirdResources = {
      "zh-CN": {
        numeric: 123,
      },
      "zh-Hant": {
        numeric: 456,
      },
    } as const;
    const i18n = createI18n({
      lang: "zh-CN",
      resources: weirdResources as unknown as typeof resources,
    });
    // @ts-expect-error: 非字符串值被跳过
    expect(i18n.$t("numeric")).toBe("Missing translation");
  });

  test("已有 legacy key 时不会重复写入（嵌套资源）", () => {
    const customResources = {
      "zh-CN": {
        "scoped.message": "优先 flat",
        "scoped/message": "slash 直接键",
        nested: {
          value: "still nested",
        },
      },
      "zh-Hant": {
        "scoped.message": "flat 繁体",
        "scoped/message": "slash 繁体",
        nested: {
          value: "nested 繁体",
        },
      },
    } as const;
    const i18n = createI18n({
      lang: "zh-CN",
      resources: customResources,
      separator: "/",
    });
    expect(i18n.$t("scoped.message")).toBe("优先 flat");
    expect(i18n.$t("scoped/message")).toBe("slash 直接键");
  });

  test("已有 legacy key 时不会重复写入（扁平资源）", () => {
    const customResources = {
      "zh-CN": {
        "scoped.message": "flat 记录",
        "scoped/message": "slash 记录",
      },
      "zh-Hant": {
        "scoped.message": "flat 繁体",
        "scoped/message": "slash 繁体",
      },
    } as const;
    const i18n = createI18n({
      lang: "zh-CN",
      resources: customResources,
      separator: "/",
    });
    expect(i18n.$t("scoped.message")).toBe("flat 记录");
    expect(i18n.$t("scoped/message")).toBe("slash 记录");
  });

  test("默认 fallback 与 option fallback 生效", () => {
    const i18nDefault = createI18n({ lang: "zh-CN", resources });
    // @ts-expect-error: 故意访问不存在的 key
    expect(i18nDefault.$t("unknown.key")).toBe("Missing translation");

    const i18nCustom = createI18n({ lang: "zh-CN", resources, fallback: "N/A" });
    // @ts-expect-error: 故意访问不存在的 key
    expect(i18nCustom.$t("unknown.key")).toBe("N/A");
    // @ts-expect-error: 故意访问不存在的 key
    expect(i18nCustom.$t("unknown.key", "Override")).toBe("Override");

    // key 存在但值不是字符串时也应该回退
    expect(i18nDefault.$t("greeting")).toBe("Missing translation");
  });

  test("fallback 链在 has() 中同样生效", () => {
    const i18n = createI18n({
      lang: "zh-CN",
      resources,
      fallbackLanguages: ["zh-Hant"],
    });
    expect(i18n.has("onlyTraditional")).toBe(true);
  });

  test("默认情况下回退链为空", () => {
    const i18n = createI18n({ lang: "zh-CN", resources });
    expect(i18n.getFallbackLanguages()).toEqual([]);
  });

  test("创建时的回退链会自动去重并过滤", () => {
    const i18n = createI18n({
      lang: "zh-CN",
      resources,
      // @ts-expect-error: 故意包含无效语言以测试过滤
      fallbackLanguages: ["zh-Hant", "zh-Hant", "en-US"],
    });
    expect(i18n.getFallbackLanguages()).toEqual(["zh-Hant"]);
  });

  test("空 key 会直接返回 fallback 并记录缺失", () => {
    const onMissing = vi.fn();
    const i18n = createI18n({
      lang: "zh-CN",
      resources,
      fallback: "N/A",
      fallbackLanguages: ["zh-Hant"],
      onMissing,
    });
    // @ts-expect-error: 空 key 非法
    expect(i18n.$t("")).toBe("N/A");
    expect(onMissing).toHaveBeenCalledWith({
      key: "",
      languagesTried: ["zh-CN", "zh-Hant"],
    });
  });

  test("回退链包含当前语言时不会重复尝试", () => {
    const onMissing = vi.fn();
    const i18n = createI18n({
      lang: "zh-CN",
      resources,
      fallbackLanguages: ["zh-CN", "zh-Hant"],
      onMissing,
    });
    // @ts-expect-error: 故意访问不存在的 key
    expect(i18n.$t("unknown.key")).toBe("Missing translation");
    expect(onMissing).toHaveBeenCalledWith({
      key: "unknown.key",
      languagesTried: ["zh-CN", "zh-Hant"],
    });
  });

  test("当前语言缺失资源时会继续尝试回退语言", () => {
    const brokenResources = {
      "zh-CN": null,
      "zh-Hant": resources["zh-Hant"],
    };
    const i18n = createI18n({
      lang: "zh-CN",
      // @ts-expect-error: 构造缺失资源的场景
      resources: brokenResources,
      fallbackLanguages: ["zh-Hant"],
    });
    expect(i18n.$t("onlyTraditional")).toBe("只有繁體");
  });

  test("语言变化监听与注销", () => {
    const i18n = createI18n({ lang: "zh-CN", resources });
    const spy = vi.fn();
    const dispose = i18n.onLanguageChange(spy);

    i18n.setCurrentLanguage("zh-Hant");
    expect(spy).toHaveBeenCalledWith("zh-Hant");

    dispose();
    i18n.setCurrentLanguage("zh-CN");
    expect(spy).toHaveBeenCalledTimes(1);
  });

  test("设置相同语言不会触发监听器", () => {
    const i18n = createI18n({ lang: "zh-CN", resources });
    const spy = vi.fn();
    i18n.onLanguageChange(spy);
    i18n.setCurrentLanguage("zh-CN");
    expect(spy).not.toHaveBeenCalled();
  });

  test("getCurrentLanguage 可读取当前语言", () => {
    const i18n = createI18n({ lang: "zh-CN", resources });
    expect(i18n.getCurrentLanguage()).toBe("zh-CN");
    i18n.setCurrentLanguage("zh-Hant");
    expect(i18n.getCurrentLanguage()).toBe("zh-Hant");
  });

  test("fallback 链会过滤无效语言", () => {
    const i18n = createI18n({ lang: "zh-CN", resources });
    // @ts-expect-error: 包含不受支持的语言
    i18n.setFallbackLanguages(["zh-Hant", "zh-Hant", "en-US"]);
    expect(i18n.getFallbackLanguages()).toEqual(["zh-Hant"]);
  });

  test("clearCache 与 getCacheStats", () => {
    const i18n = createI18n({ lang: "zh-CN", resources });
    expect(i18n.getCacheStats()).toEqual({ size: 0, enabled: true });
    i18n.$t("greeting.welcome");
    expect(i18n.getCacheStats()).toEqual({ size: 1, enabled: true });
    i18n.clearCache();
    expect(i18n.getCacheStats()).toEqual({ size: 0, enabled: true });
  });

  test("禁用缓存时不会命中缓存逻辑", () => {
    const i18n = createI18n({ lang: "zh-CN", resources, cache: false });
    expect(i18n.getCacheStats()).toEqual({ size: 0, enabled: false });
    i18n.$t("greeting.welcome");
    i18n.$t("greeting.welcome");
    expect(i18n.getCacheStats()).toEqual({ size: 0, enabled: false });
    i18n.setCurrentLanguage("zh-Hant");
    expect(i18n.getCacheStats()).toEqual({ size: 0, enabled: false });
  });

  test("fallback 链可被清空并恢复", () => {
    const i18n = createI18n({ lang: "zh-CN", resources, fallbackLanguages: "zh-Hant" });
    expect(i18n.getFallbackLanguages()).toEqual(["zh-Hant"]);
    i18n.setFallbackLanguages([]);
    expect(i18n.getFallbackLanguages()).toEqual([]);
    i18n.setFallbackLanguages("zh-Hant");
    expect(i18n.getFallbackLanguages()).toEqual(["zh-Hant"]);
  });

  test("getFallbackLanguages 返回值为快照，修改不会影响内部状态", () => {
    const i18n = createI18n({ lang: "zh-CN", resources, fallbackLanguages: "zh-Hant" });
    const snapshot = i18n.getFallbackLanguages() as string[];
    snapshot.push("fake");
    expect(i18n.getFallbackLanguages()).toEqual(["zh-Hant"]);
  });

  test("setCurrentLanguage 与 has() 遇到未知语言抛错", () => {
    const i18n = createI18n({ lang: "zh-CN", resources });
    // @ts-expect-error: 测试未知语言抛错
    expect(() => i18n.setCurrentLanguage("en-US")).toThrowError(/Language "en-US" is not provided/);
    // @ts-expect-error: 测试未知语言抛错
    expect(() => i18n.has("greeting.welcome", "en-US")).toThrowError(
      /Language "en-US" is not provided/,
    );
  });

  test("创建时传入未知默认语言抛错", () => {
    expect(() =>
      createI18n({
        // @ts-expect-error: 测试默认语言不受支持
        lang: "en-US",
        resources,
      }),
    ).toThrowError(/Language "en-US" is not provided/);
  });

  test("暴露支持的语言联合类型", () => {
    type SupportedLang = I18nLanguages<typeof resources>;
    const lang: SupportedLang = "zh-Hant";
    expect(lang).toBe("zh-Hant");

    const i18n = createI18n({ lang: "zh-CN", resources });
    const list = i18n.getAvailableLanguages();
    expect(list).toEqual(["zh-CN", "zh-Hant"]);

    // @ts-expect-error en-US 不在资源列表中
    const _invalid: SupportedLang = "en-US";
  });

  test("availableLanguages 会列出所有语言", () => {
    const i18n = createI18n({ lang: "zh-CN", resources });
    expect(i18n.getAvailableLanguages()).toEqual(["zh-CN", "zh-Hant"]);
  });
});
