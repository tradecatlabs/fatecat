/**
 * MCP Key 内存验证缓存
 *
 * TTL 5 分钟，避免每次请求都查 DB
 */

export interface CachedKeyInfo {
  userId: string;
  keyId: string;
  cachedAt: number;
}

const KEY_CACHE_TTL = 60 * 1000; // 60 秒（短 TTL 以便封禁/重置快速生效）
const MAX_CACHE_SIZE = 10_000;
const cache = new Map<string, CachedKeyInfo>();

export function getCachedKey(keyCode: string): CachedKeyInfo | null {
  const entry = cache.get(keyCode);
  if (!entry) return null;

  if (Date.now() - entry.cachedAt > KEY_CACHE_TTL) {
    cache.delete(keyCode);
    return null;
  }

  return entry;
}

export function setCachedKey(keyCode: string, info: Omit<CachedKeyInfo, 'cachedAt'>): void {
  if (cache.size >= MAX_CACHE_SIZE && !cache.has(keyCode)) {
    // 淘汰最旧的条目
    const oldest = cache.keys().next().value;
    if (oldest !== undefined) cache.delete(oldest);
  }
  cache.set(keyCode, { ...info, cachedAt: Date.now() });
}

export function invalidateCachedKey(keyCode: string): void {
  cache.delete(keyCode);
}

// 定期清理过期缓存
const cleanupTimer = setInterval(() => {
  const now = Date.now();
  for (const [key, entry] of cache) {
    if (now - entry.cachedAt > KEY_CACHE_TTL) {
      cache.delete(key);
    }
  }
}, 60 * 1000);
cleanupTimer.unref?.();
