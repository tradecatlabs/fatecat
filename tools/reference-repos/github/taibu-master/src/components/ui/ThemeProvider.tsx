/**
 * ThemeProvider 组件
 *
 * 支持三种主题模式：
 * - light: 浅色主题
 * - dark: 深色主题
 * - system: 跟随系统设置自动切换
 */
'use client';

import { createContext, useContext, useEffect, useState, ReactNode } from 'react';
import { removeLocalCache, writeLocalCache } from '@/lib/cache/local-storage';

// 主题模式：light、dark 或 system（跟随系统）
type ThemeMode = 'light' | 'dark' | 'system';
// 实际应用的主题（只有 light 或 dark）
type AppliedTheme = 'light' | 'dark';

const THEME_MODE_CACHE_KEY = 'taibu.pref.themeMode';
const LEGACY_THEME_CACHE_KEY = 'taibu.pref.theme';
const REMOVED_THEME_CACHE_KEYS = ['mingai.pref.themeMode', 'mingai.pref.theme'];
const THEME_COLORS: Record<AppliedTheme, string> = {
  light: '#f7f6f3',
  dark: '#0a0a0a',
};

interface ThemeContextType {
  theme: AppliedTheme;
  themeMode: ThemeMode;
  toggleTheme: () => void;
  setThemeMode: (mode: ThemeMode) => void;
}

const ThemeContext = createContext<ThemeContextType | undefined>(undefined);

function readStoredLocalValue<T>(key: string): T | null {
  if (typeof window === 'undefined') return null;

  const raw = window.localStorage.getItem(key);
  if (!raw) return null;

  try {
    const parsed = JSON.parse(raw) as { value?: T } | T;
    if (parsed && typeof parsed === 'object' && 'value' in parsed) {
      return (parsed as { value?: T }).value ?? null;
    }
    return parsed as T;
  } catch {
    return raw as T;
  }
}

// 获取系统主题偏好
function getSystemTheme(): AppliedTheme {
  if (typeof window === 'undefined') return 'dark';
  return window.matchMedia('(prefers-color-scheme: dark)').matches ? 'dark' : 'light';
}

function getStoredThemeMode(): ThemeMode {
  const saved = readStoredLocalValue<ThemeMode>(THEME_MODE_CACHE_KEY);
  if (saved === 'light' || saved === 'dark' || saved === 'system') {
    return saved;
  }

  const legacy = readStoredLocalValue<string>(LEGACY_THEME_CACHE_KEY);
  if (legacy === 'light' || legacy === 'dark') {
    return legacy;
  }

  return 'system';
}

function applyThemeToDocument(theme: AppliedTheme) {
  const root = document.documentElement;
  root.classList.toggle('dark', theme === 'dark');
  root.style.colorScheme = theme;

  const themeColorMeta = document.querySelector('meta[name="theme-color"]');
  if (themeColorMeta instanceof HTMLMetaElement) {
    themeColorMeta.setAttribute('content', THEME_COLORS[theme]);
  }
}

export function ThemeProvider({ children }: { children: ReactNode }) {
  // 用户选择的主题模式
  const [themeMode, setThemeModeState] = useState<ThemeMode>(() => {
    if (typeof window === 'undefined') return 'system';
    return getStoredThemeMode();
  });
  const [systemTheme, setSystemTheme] = useState<AppliedTheme>(() => {
    if (typeof window === 'undefined') return 'dark';
    return getSystemTheme();
  });
  const theme = themeMode === 'system' ? systemTheme : themeMode;

  // 监听系统主题变化
  useEffect(() => {
    if (themeMode !== 'system') return;

    const mediaQuery = window.matchMedia('(prefers-color-scheme: dark)');
    const handleChange = (e: MediaQueryListEvent) => {
      setSystemTheme(e.matches ? 'dark' : 'light');
    };

    mediaQuery.addEventListener('change', handleChange);
    return () => mediaQuery.removeEventListener('change', handleChange);
  }, [themeMode]);

  // 当主题模式变化时，更新实际主题
  useEffect(() => {
    writeLocalCache(THEME_MODE_CACHE_KEY, themeMode);
    REMOVED_THEME_CACHE_KEYS.forEach(removeLocalCache);
  }, [themeMode]);

  useEffect(() => {
    REMOVED_THEME_CACHE_KEYS.forEach(removeLocalCache);
  }, []);

  // 当实际主题变化时，更新 DOM
  useEffect(() => {
    applyThemeToDocument(theme);
  }, [theme]);

  // 切换主题：light -> dark -> system -> light
  const toggleTheme = () => {
    setThemeModeState(prev => {
      if (prev === 'light') return 'dark';
      if (prev === 'dark') return 'system';
      return 'light';
    });
  };

  const setThemeMode = (mode: ThemeMode) => {
    setThemeModeState(mode);
  };

  return (
    <ThemeContext.Provider value={{ theme, themeMode, toggleTheme, setThemeMode }}>
      {children}
    </ThemeContext.Provider>
  );
}

export function useTheme() {
  const context = useContext(ThemeContext);
  if (context === undefined) {
    throw new Error('useTheme must be used within a ThemeProvider');
  }
  return context;
}
