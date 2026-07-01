function getStorage(): Storage | null {
  if (typeof window === 'undefined') {
    return null;
  }
  try {
    return window.localStorage;
  } catch {
    return null;
  }
}

export const safeStorage = {
  get(key: string): string | null {
    const storage = getStorage();
    if (!storage) return null;
    try {
      return storage.getItem(key);
    } catch {
      return null;
    }
  },

  set(key: string, value: string): boolean {
    const storage = getStorage();
    if (!storage) return false;
    try {
      storage.setItem(key, value);
      return true;
    } catch {
      return false;
    }
  },

  remove(key: string): void {
    const storage = getStorage();
    if (!storage) return;
    try {
      storage.removeItem(key);
    } catch {
      // 隐私模式或权限受限时静默忽略
    }
  },

  getJSON<T>(key: string, fallback: T): T {
    const raw = safeStorage.get(key);
    if (raw === null) return fallback;
    try {
      const parsed = JSON.parse(raw);
      return parsed as T;
    } catch {
      return fallback;
    }
  },

  setJSON<T>(key: string, value: T): boolean {
    try {
      return safeStorage.set(key, JSON.stringify(value));
    } catch {
      return false;
    }
  },
};
