type CacheEntry<T> = {
  value: T;
  expiresAt: number;
};

export function createMemoryCache<T>(defaultTtlMs: number, maxSize: number = 1000) {
  const store = new Map<string, CacheEntry<T>>();

  const evictOldest = () => {
    let toDelete = store.size - maxSize;
    if (toDelete <= 0) return;
    for (const key of store.keys()) {
      if (toDelete <= 0) break;
      store.delete(key);
      toDelete -= 1;
    }
  };

  const get = (key: string): T | null => {
    const entry = store.get(key);
    if (!entry) return null;
    if (entry.expiresAt <= Date.now()) {
      store.delete(key);
      return null;
    }
    return entry.value;
  };

  const set = (key: string, value: T, ttlMs: number = defaultTtlMs) => {
    store.set(key, { value, expiresAt: Date.now() + ttlMs });
    if (store.size > maxSize) {
      evictOldest();
    }
  };

  const remove = (key: string) => {
    store.delete(key);
  };

  const clear = () => {
    store.clear();
  };

  const cleanup = () => {
    const now = Date.now();
    for (const [key, entry] of store) {
      if (entry.expiresAt <= now) {
        store.delete(key);
      }
    }
  };

  return { get, set, remove, clear, cleanup };
}

export function createSingleFlight<T>() {
  const inflight = new Map<string, Promise<T>>();

  const run = (key: string, task: () => Promise<T>) => {
    if (inflight.has(key)) {
      return inflight.get(key)!;
    }
    const promise = task().finally(() => {
      inflight.delete(key);
    });
    inflight.set(key, promise);
    return promise;
  };

  const clear = (key?: string) => {
    if (!key) {
      inflight.clear();
      return;
    }
    inflight.delete(key);
  };

  return { run, clear };
}
