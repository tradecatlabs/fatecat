/** 语言资源映射：键为语言标识，值为任意层级的字典。 */
type ResourceMap = Record<string, Record<string, unknown>>;

/** 扁平化后的资源映射。 */
type FlatResourceMap = Record<string, Record<string, string>>;

/** 默认的缺省文案。 */
const DEFAULT_FALLBACK_TEXT = "Missing translation";

/** 默认的键分隔符。 */
const DEFAULT_SEPARATOR = ".";

/** 将值归一化为数组，便于统一处理单个或多个输入。 */
const toArray = <T>(value?: T | readonly T[]): readonly T[] => {
  if (value === undefined) {
    return [];
  }
  return Array.isArray(value) ? (value as readonly T[]) : ([value] as readonly T[]);
};

/** 过滤并去重回退语言数组，保证所有语言合法可用。 */
const sanitizeFallbacks = <Lang extends string>(
  value: Lang | readonly Lang[] | undefined,
  available: readonly Lang[],
): Lang[] => {
  const unique = new Set<Lang>();
  for (const candidate of toArray(value)) {
    if (available.includes(candidate) && !unique.has(candidate)) {
      unique.add(candidate);
    }
  }
  return Array.from(unique);
};

/** 判断某个值是否为可遍历的对象。 */
const isRecord = (value: unknown): value is Record<string, unknown> =>
  typeof value === "object" && value !== null && !Array.isArray(value);

/**
 * 扁平化嵌套对象为点分隔的键值对。
 */
const flattenObject = (
  obj: Record<string, unknown>,
  prefix: string = "",
  separator: string = DEFAULT_SEPARATOR,
  legacySeparator: string = DEFAULT_SEPARATOR,
): Record<string, string> => {
  const result: Record<string, string> = {};
  for (const key in obj) {
    if (!Object.hasOwn(obj, key)) {
      continue;
    }
    const value = obj[key];
    const newKey = prefix ? `${prefix}${separator}${key}` : key;
    if (isRecord(value)) {
      Object.assign(result, flattenObject(value, newKey, separator, legacySeparator));
    } else if (typeof value === "string") {
      result[newKey] = value;
      if (separator !== legacySeparator && newKey.includes(separator)) {
        const legacyKey = newKey.split(separator).join(legacySeparator);
        if (!(legacyKey in result)) {
          result[legacyKey] = value;
        }
      }
    }
  }
  return result;
};

/**
 * 检测资源对象是否已经是扁平结构。
 */
const isFlatResource = (resource: Record<string, unknown>): boolean => {
  for (const key in resource) {
    if (!Object.hasOwn(resource, key)) {
      continue;
    }
    const value = resource[key];
    if (typeof value !== "string") {
      return false;
    }
  }
  return true;
};

/**
 * 扁平化所有语言资源。
 */
const flattenResources = (
  resources: ResourceMap,
  separator: string = DEFAULT_SEPARATOR,
  legacySeparator: string = DEFAULT_SEPARATOR,
): FlatResourceMap => {
  const result: FlatResourceMap = {};
  for (const lang in resources) {
    if (!Object.hasOwn(resources, lang)) {
      continue;
    }
    const resource = resources[lang];
    if (isFlatResource(resource)) {
      const flat = resource as Record<string, string>;
      if (separator !== legacySeparator) {
        const augmented: Record<string, string> = { ...flat };
        for (const key in flat) {
          if (!Object.hasOwn(flat, key) || !key.includes(separator)) {
            continue;
          }
          const legacyKey = key.split(separator).join(legacySeparator);
          if (!(legacyKey in augmented)) {
            augmented[legacyKey] = flat[key];
          }
        }
        result[lang] = augmented;
      } else {
        result[lang] = flat;
      }
    } else {
      result[lang] = flattenObject(resource, "", separator, legacySeparator);
    }
  }
  return result;
};

/** 构建最终的语言尝试顺序：当前语言优先，再按回退链依次尝试。 */
const buildSearchOrder = <Lang extends string>(
  primary: Lang,
  fallbacks: readonly Lang[],
): Lang[] => {
  const result = [primary];
  for (const lang of fallbacks) {
    if (lang !== primary) {
      result.push(lang);
    }
  }
  return result;
};

/**
 * 根据点分隔的路径从对象中提取值类型。
 */
export type GetValueByPath<
  T,
  Path extends string,
  Separator extends string = ".",
> = Path extends `${infer First}${Separator}${infer Rest}`
  ? First extends keyof T
    ? GetValueByPath<T[First], Rest, Separator>
    : never
  : Path extends keyof T
    ? T[Path]
    : never;

/** 计算资源对象的所有嵌套键。 */
export type NestedKeyOf<T, Depth extends number = 5> = [Depth] extends [never]
  ? never
  : T extends Record<string, unknown>
    ? {
        [K in Extract<keyof T, string>]: T[K] extends Record<string, unknown>
          ? `${K}.${NestedKeyOf<T[K], Prev[Depth]>}` | K
          : K;
      }[Extract<keyof T, string>]
    : never;

/** 递归深度控制数组。 */
export type Prev = [never, 0, 1, 2, 3, 4, 5];

/** 深度只读类型，禁止资源对象在运行期被修改。 */
export type DeepReadonly<T> = {
  readonly [K in keyof T]: T[K] extends Record<string, unknown> ? DeepReadonly<T[K]> : T[K];
};

export type LanguageKey<TResourcesMap extends ResourceMap> = keyof TResourcesMap & string;
export type I18nLanguages<TResourcesMap extends ResourceMap> = LanguageKey<TResourcesMap>;
export type TranslationKey<TResourcesMap extends ResourceMap> = NestedKeyOf<
  TResourcesMap[LanguageKey<TResourcesMap>]
>;

export interface MissingTranslationInfo<Lang extends string> {
  key: string;
  languagesTried: Lang[];
}

export interface I18nCreateOptions<TResourcesMap extends ResourceMap> {
  /** 默认语言。 */
  lang: LanguageKey<TResourcesMap>;
  /** 语言资源（支持嵌套或扁平结构）。 */
  resources: TResourcesMap;
  /** 默认缺失文案。 */
  fallback?: string;
  /** 回退语言链。 */
  fallbackLanguages?: LanguageKey<TResourcesMap> | readonly LanguageKey<TResourcesMap>[];
  /** 键分隔符，默认为 "."。 */
  separator?: string;
  /** 缺失文案时的回调。 */
  onMissing?: (info: MissingTranslationInfo<LanguageKey<TResourcesMap>>) => void;
  /** 是否启用缓存（默认 true）。 */
  cache?: boolean;
}

/**
 * I18n 实例接口（完全类型安全）。
 */
export interface I18n<TResourcesMap extends ResourceMap> {
  /**
   * 获取翻译文本（不带默认值）。
   */
  $t<K extends TranslationKey<TResourcesMap>>(
    key: K,
  ): GetValueByPath<TResourcesMap[LanguageKey<TResourcesMap>], K> extends string
    ? GetValueByPath<TResourcesMap[LanguageKey<TResourcesMap>], K>
    : string;

  /**
   * 获取翻译文本（带默认值）。
   */
  $t<K extends TranslationKey<TResourcesMap>, D extends string>(
    key: K,
    defaultValue: D,
  ): GetValueByPath<TResourcesMap[LanguageKey<TResourcesMap>], K> extends string
    ? GetValueByPath<TResourcesMap[LanguageKey<TResourcesMap>], K> | D
    : D;

  /**
   * 判断某个键在当前或指定语言中是否存在。
   */
  has(key: TranslationKey<TResourcesMap>, lang?: LanguageKey<TResourcesMap>): boolean;

  /** 获取当前语言。 */
  getCurrentLanguage(): LanguageKey<TResourcesMap>;

  /**
   * 设置当前语言。
   */
  setCurrentLanguage(lang: LanguageKey<TResourcesMap>): void;

  /** 列出可用语言。 */
  getAvailableLanguages(): readonly LanguageKey<TResourcesMap>[];

  /** 读取回退语言链。 */
  getFallbackLanguages(): readonly LanguageKey<TResourcesMap>[];

  /**
   * 设置回退语言链。
   */
  setFallbackLanguages(
    langs: LanguageKey<TResourcesMap> | readonly LanguageKey<TResourcesMap>[],
  ): void;

  /**
   * 注册语言变更监听器。
   */
  onLanguageChange(fn: (lang: LanguageKey<TResourcesMap>) => void): () => void;

  /**
   * 清空翻译缓存。
   */
  clearCache(): void;

  /**
   * 获取缓存统计信息。
   */
  getCacheStats(): { size: number; enabled: boolean };
}

/**
 * 创建一个轻量级的 i18n 实例（完全类型安全，无 any）。
 */
export function createI18n<const TResourcesMap extends ResourceMap>({
  lang,
  resources,
  fallback,
  fallbackLanguages,
  separator = DEFAULT_SEPARATOR,
  onMissing,
  cache = true,
}: I18nCreateOptions<TResourcesMap>): I18n<TResourcesMap> {
  type Lang = LanguageKey<TResourcesMap>;
  type TKey = TranslationKey<TResourcesMap>;

  if (!(lang in resources)) {
    throw new Error(`Language "${lang}" is not provided in resources`);
  }

  const availableLanguages = Object.freeze(Object.keys(resources) as Lang[]) as readonly Lang[];

  const flatResources = flattenResources(resources, separator, DEFAULT_SEPARATOR);

  let fallbackChain = sanitizeFallbacks(fallbackLanguages as Lang | readonly Lang[] | undefined, [
    ...availableLanguages,
  ]);

  const listeners = new Set<(lang: Lang) => void>();
  let currentLanguage = lang as Lang;

  const translationCache = new Map<string, string>();
  const cacheEnabled = cache;

  const ensureLanguageExists = (language: Lang): Lang => {
    if (!(language in flatResources)) {
      throw new Error(`Language "${language}" is not provided in resources`);
    }
    return language;
  };

  const translateFromLanguage = (language: Lang, key: string): string | undefined => {
    const resource = flatResources[language];
    if (!resource) {
      return undefined;
    }
    return resource[key];
  };

  const translate = (key: string, order: readonly Lang[]): string | undefined => {
    if (cacheEnabled) {
      const cacheKey = `${order[0]}:${key}`;
      const cached = translationCache.get(cacheKey);
      if (cached !== undefined) {
        return cached;
      }
    }

    for (const language of order) {
      const value = translateFromLanguage(language, key);
      if (value !== undefined) {
        if (cacheEnabled) {
          const cacheKey = `${order[0]}:${key}`;
          translationCache.set(cacheKey, value);
        }
        return value;
      }
    }

    return undefined;
  };

  const emitLanguageChange = (nextLanguage: Lang): void => {
    listeners.forEach((fn) => {
      fn(nextLanguage);
    });
  };

  // 🎯 完全类型安全的实现（无 any）
  const $t = ((key: TKey, defaultValue?: string): string => {
    const fallbackText = defaultValue ?? fallback ?? DEFAULT_FALLBACK_TEXT;
    const searchOrder = buildSearchOrder(currentLanguage, fallbackChain);
    const result = translate(key, searchOrder);

    if (result !== undefined) {
      return result;
    }

    onMissing?.({
      key,
      languagesTried: searchOrder,
    });
    return fallbackText;
  }) as unknown as I18n<TResourcesMap>["$t"];

  return {
    $t,
    has(key: TKey, lang?: Lang): boolean {
      const searchOrder = lang
        ? [ensureLanguageExists(lang)]
        : buildSearchOrder(currentLanguage, fallbackChain);
      return translate(key, searchOrder) !== undefined;
    },
    getCurrentLanguage(): Lang {
      return currentLanguage;
    },
    setCurrentLanguage(language: Lang): void {
      const nextLanguage = ensureLanguageExists(language);
      if (nextLanguage === currentLanguage) {
        return;
      }
      currentLanguage = nextLanguage;

      if (cacheEnabled) {
        translationCache.clear();
      }

      emitLanguageChange(nextLanguage);
    },
    getAvailableLanguages(): readonly Lang[] {
      return availableLanguages;
    },
    getFallbackLanguages(): readonly Lang[] {
      return [...fallbackChain];
    },
    setFallbackLanguages(langs: Lang | readonly Lang[]): void {
      fallbackChain = sanitizeFallbacks(langs as Lang | readonly Lang[] | undefined, [
        ...availableLanguages,
      ]);
    },
    onLanguageChange(fn: (lang: Lang) => void): () => void {
      listeners.add(fn);
      return (): void => {
        listeners.delete(fn);
      };
    },
    clearCache(): void {
      translationCache.clear();
    },
    getCacheStats(): { size: number; enabled: boolean } {
      return {
        size: translationCache.size,
        enabled: cacheEnabled,
      };
    },
  };
}
