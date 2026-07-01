type LocalCachePayload<T> = {
  value: T;
  cachedAt: number;
};

export function readLocalCache<T>(key: string, maxAgeMs: number): T | null {
  if (typeof window === 'undefined') return null;
  const raw = window.localStorage.getItem(key);
  if (!raw) return null;
  try {
    const parsed = JSON.parse(raw) as LocalCachePayload<T> | { ts?: number; value?: T } | T;
    if (typeof parsed === 'object' && parsed !== null) {
      if ('cachedAt' in parsed && 'value' in parsed) {
        const payload = parsed as LocalCachePayload<T>;
        if (!payload.cachedAt || Date.now() - payload.cachedAt > maxAgeMs) {
          return null;
        }
        return payload.value;
      }
      if ('ts' in parsed && 'value' in parsed) {
        const legacyPayload = parsed as { ts?: number; value?: T };
        if (!legacyPayload.ts || Date.now() - legacyPayload.ts > maxAgeMs) {
          return null;
        }
        return legacyPayload.value ?? null;
      }
    }
    return parsed as T;
  } catch {
    return null;
  }
}

export function writeLocalCache<T>(key: string, value: T) {
  if (typeof window === 'undefined') return;
  const payload: LocalCachePayload<T> = { value, cachedAt: Date.now() };
  window.localStorage.setItem(key, JSON.stringify(payload));
}

export function removeLocalCache(key: string) {
  if (typeof window === 'undefined') return;
  window.localStorage.removeItem(key);
}

export function removeLocalCacheKeys(keys: string[]) {
  if (typeof window === 'undefined') return;
  for (const key of keys) {
    window.localStorage.removeItem(key);
  }
}

export function removeLocalCacheByPrefix(prefix: string) {
  if (typeof window === 'undefined') return;
  const keys: string[] = [];
  for (let i = 0; i < window.localStorage.length; i += 1) {
    const key = window.localStorage.key(i);
    if (key && key.startsWith(prefix)) {
      keys.push(key);
    }
  }
  for (const key of keys) {
    window.localStorage.removeItem(key);
  }
}

export type LocalCacheScope =
  | 'data_sources'
  | 'knowledge_bases'
  | 'default_bazi_chart';

const CACHE_SCOPE_PREFIXES: Record<Exclude<LocalCacheScope, 'default_bazi_chart'>, string> = {
  data_sources: 'taibu.data_sources.',
  knowledge_bases: 'taibu.knowledge_bases.',
};

const CACHE_SCOPE_KEYS: Record<'default_bazi_chart', string[]> = {
  default_bazi_chart: ['taibu.pref.defaultBaziChartId', 'mingai.pref.defaultBaziChartId', 'defaultBaziChartId'],
};

export function invalidateLocalCaches(scopes: LocalCacheScope[]) {
  if (typeof window === 'undefined' || scopes.length === 0) return;
  const uniqueScopes = Array.from(new Set(scopes));
  for (const scope of uniqueScopes) {
    if (scope === 'default_bazi_chart') {
      removeLocalCacheKeys(CACHE_SCOPE_KEYS.default_bazi_chart);
      continue;
    }
    removeLocalCacheByPrefix(CACHE_SCOPE_PREFIXES[scope]);
    removeLocalCacheByPrefix(CACHE_SCOPE_PREFIXES[scope].replace(/^taibu/u, 'mingai'));
  }
}
