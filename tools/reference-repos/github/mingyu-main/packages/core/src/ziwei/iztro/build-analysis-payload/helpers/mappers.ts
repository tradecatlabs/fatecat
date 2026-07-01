import type { IztroPalace, IztroStar } from '../../../../types/iztro';
import type { MutagenName, ScopeMutagenItem, StarFact } from '../../../../types/analysis';
import { findPalaceByIndex, findStarPalaceIndex, normalizeStarName } from './palace-lookup';

export const MUTAGEN_ORDER: MutagenName[] = ['禄', '权', '科', '忌'];

export function mapScopeMutagenMap(stars: string[], palaces: IztroPalace[]): ScopeMutagenItem[] {
  return stars.slice(0, 4).map((star, index) => {
    const palaceIndex = findStarPalaceIndex(palaces, star);
    const palace = findPalaceByIndex(palaces, palaceIndex);
    return {
      mutagen: MUTAGEN_ORDER[index],
      star,
      palace_index: palaceIndex,
      palace_name: palace?.name,
    };
  });
}

export function mapStarFact(
  star: IztroStar,
  activeScopeMutagenMap: ScopeMutagenItem[],
  options: { isHoroscopeStar?: boolean } = {},
): StarFact {
  const normalizedStarName = normalizeStarName(star.name);
  const activeScopeMutagen = activeScopeMutagenMap.find(
    (item) => normalizeStarName(item.star) === normalizedStarName,
  )?.mutagen;
  const rawMutagen = star.mutagen || undefined;
  const isHoroscopeStar = options.isHoroscopeStar ?? star.scope !== 'origin';

  return {
    name: star.name,
    kind: star.type,
    scope: star.scope,
    brightness: star.brightness || undefined,
    birth_mutagen: isHoroscopeStar ? undefined : (rawMutagen as MutagenName | undefined),
    horoscope_mutagen: isHoroscopeStar ? (rawMutagen as MutagenName | undefined) : undefined,
    active_scope_mutagen: activeScopeMutagen,
  };
}
