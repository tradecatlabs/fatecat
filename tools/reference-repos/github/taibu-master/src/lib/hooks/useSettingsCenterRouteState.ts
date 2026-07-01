'use client';

import { useSyncExternalStore } from 'react';
import {
  readSettingsCenterSubpathFromWindow,
  readSettingsCenterTabFromWindow,
  subscribeSettingsCenterLocation,
} from '@/lib/settings-center';

export function useActiveSettingsCenterTab() {
  return useSyncExternalStore(
    subscribeSettingsCenterLocation,
    readSettingsCenterTabFromWindow,
    () => null,
  );
}

export function useSettingsCenterSubpath() {
  return useSyncExternalStore(
    subscribeSettingsCenterLocation,
    readSettingsCenterSubpathFromWindow,
    () => null,
  );
}
