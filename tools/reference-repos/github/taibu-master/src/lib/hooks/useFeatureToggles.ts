/**
 * 功能模块开关 Hook
 *
 * 浏览器侧 server state 统一走 app bootstrap query。
 */
'use client';

import { useCallback } from 'react';
import { useAppBootstrap } from '@/lib/hooks/useAppBootstrap';

type FeatureTogglesState = {
  isLoading: boolean;
  loaded: boolean;
  error: Error | null;
  isFeatureEnabled: (featureId: string) => boolean;
  refresh: () => Promise<void>;
};

type UseFeatureTogglesOptions = {
  enabled?: boolean;
};

export function useFeatureToggles(options: UseFeatureTogglesOptions = {}): FeatureTogglesState {
  const enabled = options.enabled ?? true;
  const bootstrap = useAppBootstrap({ enabled });
  const toggles = bootstrap.data.featureToggles;
  const togglesLoaded = bootstrap.data.featureTogglesLoaded;
  const bootstrapPending = enabled
    && !togglesLoaded
    && !bootstrap.hasBootstrapData
    && !(bootstrap.error instanceof Error);
  const toggleError = !togglesLoaded && !bootstrapPending
    ? (
      bootstrap.error instanceof Error && !bootstrap.hasBootstrapData
        ? bootstrap.error
        : new Error(bootstrap.data.featureTogglesErrorMessage || '功能状态加载失败')
    )
    : null;

  const refresh = useCallback(async () => {
    await bootstrap.refresh();
  }, [bootstrap]);

  const isFeatureEnabled = useCallback(
    (featureId: string) => enabled && togglesLoaded && toggles[featureId] !== true,
    [enabled, toggles, togglesLoaded],
  );

  return {
    isLoading: enabled ? (bootstrapPending || bootstrap.isLoading) : false,
    loaded: enabled ? togglesLoaded : true,
    error: enabled ? toggleError : null,
    isFeatureEnabled,
    refresh,
  };
}
