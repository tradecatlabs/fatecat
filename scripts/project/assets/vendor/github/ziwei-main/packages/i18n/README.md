# @ziweijs/i18n

类型安全、零依赖的国际化工具，提供轻量的 `createI18n` 工厂方法，适用于 `@ziweijs/core` 以及其他需要简单字典查找的场景。直接传入资源对象即可自动推导语言键和值类型，无需手动声明泛型。

## 特性
- 自动推导语言与嵌套键，`I18nLanguages`、`TranslationKey` 等类型可直出联合类型；
- 分隔符可自定义（默认为 `"."`），并兼容 legacy key，扁平/嵌套资源都能无缝读取；
- `fallback` 与回退链内建去重过滤，缺失时自动搜索其它语言，并触发 `onMissing`；
- `has()`、`getAvailableLanguages()`、`getCacheStats()` 等辅助方法便于预检 key；
- 内置语言变更监听器与缓存，可通过 `cache: false` 关闭，也可手动 `clearCache()`；
- 完整的运行时校验，非法语言或资源会在创建/切换阶段抛错，避免默默失败。

## 安装

```bash
pnpm add @ziweijs/i18n
```

## 使用示例

```ts
import { createI18n, type I18n, type I18nLanguages, type TranslationKey } from "@ziweijs/i18n";

const resources = {
  "zh-CN": {
    greeting: { welcome: "欢迎" },
    farewell: "再见",
  },
  "zh-Hant": {
    greeting: { welcome: "歡迎" },
    farewell: "再見",
    legacy: "只有繁體有的文案",
  },
} as const;

const i18n = createI18n({
  lang: "zh-CN",
  resources,
  fallback: "N/A",
  fallbackLanguages: "zh-Hant",
  onMissing({ key, languagesTried }) {
    console.warn(`[i18n] missing key "${key}"`, languagesTried);
  },
});

i18n.$t("greeting.welcome"); // => 欢迎
i18n.$t("legacy"); // => 只有繁體有的文案（来自 zh-Hant）
i18n.has("legacy", "zh-CN"); // => false

const dispose = i18n.onLanguageChange(console.log);
i18n.setCurrentLanguage("zh-Hant");
dispose();

type SupportedLang = I18nLanguages<typeof resources>;
// SupportedLang === "zh-CN" | "zh-Hant"

type TranslationKeys = TranslationKey<typeof resources>;
// TranslationKeys === "greeting.welcome" | "farewell" | "legacy"
```

### 自定义分隔符与扁平资源

```ts
import { createI18n } from "@ziweijs/i18n";

const flat = {
  "zh-CN": {
    "layout/header/title": "主页",
    "layout.header.subtitle": "子标题（兼容旧 key）",
  },
  "en-US": {
    "layout/header/title": "Home",
    "layout.header.subtitle": "Subtitle",
  },
} as const;

const i18n = createI18n({
  lang: "zh-CN",
  resources: flat,
  separator: "/",
});

i18n.$t("layout/header/title"); // => 主页
i18n.$t("layout.header.subtitle"); // => 兼容 "." 分隔符
```

### 监听语言切换并动态修改回退链

```ts
const i18n = createI18n({
  lang: "zh-CN",
  resources,
  fallbackLanguages: ["zh-Hant"],
});

const dispose = i18n.onLanguageChange((lang) => {
  console.log("[i18n] 切换为", lang);
});

i18n.setCurrentLanguage("zh-Hant"); // 回调触发
i18n.setFallbackLanguages(["zh-CN", "en-US" as never]); // 非法语言会被过滤
dispose(); // 取消监听
```

### 使用缓存统计与禁用缓存模式

```ts
const i18n = createI18n({ lang: "zh-CN", resources });
console.log(i18n.getCacheStats()); // { size: 0, enabled: true }

i18n.$t("greeting.welcome");
console.log(i18n.getCacheStats()); // { size: 1, enabled: true }
i18n.clearCache();

const noCache = createI18n({ lang: "zh-CN", resources, cache: false });
noCache.$t("greeting.welcome");
console.log(noCache.getCacheStats()); // { size: 0, enabled: false }
```

### 自定义 onMissing 上报

```ts
const i18n = createI18n({
  lang: "zh-CN",
  resources,
  onMissing({ key, languagesTried }) {
    fetch("/api/i18n-missing", {
      method: "POST",
      body: JSON.stringify({ key, languagesTried }),
    });
  },
});

i18n.$t("non-existent.key", "默认文案");
```

## 配置项
- `lang`: 默认语言，必须是资源对象的 key。
- `resources`: 多语言资源对象（推荐 `as const`）；可为嵌套对象或已扁平化的字典。
- `fallback`: 缺失文案时的默认文本，可被 `$t(key, override)` 覆盖。
- `fallbackLanguages`: 单个或多个候选语言，按顺序作为兜底；重复或非法语言会被过滤。
- `separator`: 自定义分隔符，默认 `"."`，常见如 `"/"`、`":"` 等；同时兼容原有 `"."` key。
- `cache`: 是否开启翻译缓存（默认 `true`），禁用时每次 `$t` 都会穿透资源。
- `onMissing`: 文案缺失时触发的回调，参数包含缺失 `key` 与已尝试的语言顺序，便于监控。

## 实例方法
- `$t(key, defaultText?)`: 读取翻译，支持嵌套 key；若缺失则按 `defaultText → fallback → fallbackLanguages` 顺序回退。
- `has(key, lang?)`: 判断当前语言或指定语言是否存在某个 key。
- `setCurrentLanguage(lang) / getCurrentLanguage()`: 切换或读取当前语言，非法语言会抛错。
- `setFallbackLanguages(langs) / getFallbackLanguages()`: 动态调整兜底链，内部返回快照，外部修改不会污染内部状态。
- `getAvailableLanguages()`: 返回所有可用语言列表（只读）。
- `onLanguageChange(listener)`: 监听语言切换，返回取消订阅函数，便于在组件卸载时清理。
- `clearCache() / getCacheStats()`: 手动清空缓存或获取 `{ size, enabled }` 统计信息，方便 debug 与监控。

## 常见模式
- **类型透传**：结合 `I18nLanguages`、`TranslationKey`、`NestedKeyOf`、`DeepReadonly` 等类型，可为组件 props 或自定义 hooks 提供严格类型约束。
- **UI 集成**：在 React/Vue 状态管理中缓存 `i18n` 实例，使用 `onLanguageChange` 触发重渲染；也可搭配 Zustand/Redux/Vuex。
- **缺失监控**：在 `onMissing` 中上报埋点，记录缺失 key 与语言顺序，方便翻译团队补齐。
- **懒加载语言**：异步加载语言文件后，重新创建 `i18n` 或调用 `setFallbackLanguages`，即可实现按需加载。
- **缓存调优**：通过 `cache: false` 禁用缓存或使用 `getCacheStats()` 监控命中率，在多语言调试场景尤其实用。
- **SSR/同构**：在服务端根据请求语言构造实例，并把 `lang` 与资源快照注入到前端，保证 `getCurrentLanguage()` 一致。
