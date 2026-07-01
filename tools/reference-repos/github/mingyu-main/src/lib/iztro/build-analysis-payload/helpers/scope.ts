import type { IztroHoroscope, IztroHoroscopeScope } from '../../../../types/iztro';
import type { ScopeType } from '../../../../types/analysis';

export type HoroscopeScopeItem = IztroHoroscopeScope;

export function mapScopeLabel(scope: ScopeType): string {
  switch (scope) {
    case 'origin':
      return '本命';
    case 'decadal':
      return '大限';
    case 'yearly':
      return '流年';
    case 'monthly':
      return '流月';
    case 'daily':
      return '流日';
    case 'hourly':
      return '流时';
    case 'age':
      return '小限';
  }
}

export function resolveScopeLabel(currentScope: ScopeType, currentScopeItem?: HoroscopeScopeItem) {
  if (currentScope !== 'origin' && currentScopeItem?.name) {
    return currentScopeItem.name;
  }

  return mapScopeLabel(currentScope);
}

export function getCurrentScopeItem(
  horoscope: IztroHoroscope,
  currentScope: ScopeType,
): HoroscopeScopeItem | undefined {
  switch (currentScope) {
    case 'decadal':
      return horoscope.decadal;
    case 'yearly':
      return horoscope.yearly;
    case 'monthly':
      return horoscope.monthly;
    case 'daily':
      return horoscope.daily;
    case 'hourly':
      return horoscope.hourly;
    case 'age':
      return horoscope.age;
    case 'origin':
    default:
      return undefined;
  }
}
