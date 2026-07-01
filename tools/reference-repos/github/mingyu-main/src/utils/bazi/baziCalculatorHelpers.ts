import { BASIC_MAPPINGS, HIDDEN_STEMS, NAYIN_MAP, TWELVE_STAGES_MAP } from './baziDefinitions';
import { getTenGod } from './baziUtils';
import type {
  HiddenStems,
  KongWangResult,
  Nayin,
  PillarLifeStages,
  Pillars,
  ZiZuoResult,
} from './baziTypes';

export function calculatePillarLifeStages(pillars: Pillars): PillarLifeStages {
  const result = {} as PillarLifeStages;
  (Object.keys(pillars) as Array<keyof Pillars>).forEach((key) => {
    const pillar = pillars[key];
    const stageMapForGan = TWELVE_STAGES_MAP[pillar.gan] || {};
    result[key] = stageMapForGan[pillar.zhi] || '未知';
  });
  return result;
}

export function calculateTenGods(pillars: Pillars, dayMaster: string): Record<string, string> {
  return Object.fromEntries(
    Object.entries(pillars).map(([pillar, { gan }]) => {
      if (pillar === 'day') {
        return [pillar, '日主'];
      }
      return [pillar, getTenGod(gan, dayMaster)];
    }),
  );
}

export function calculateHiddenStems(pillars: Pillars): HiddenStems {
  const result = {} as HiddenStems;
  (Object.keys(pillars) as Array<keyof Pillars>).forEach((key) => {
    result[key] = HIDDEN_STEMS[pillars[key].zhi] || [];
  });
  return result;
}

export function calculateHiddenTenGods(
  hiddenStems: HiddenStems,
  dayMaster: string,
): Record<string, string[]> {
  return Object.fromEntries(
    Object.entries(hiddenStems).map(([pillar, stems]) => [
      pillar,
      stems.map((stem: string) => getTenGod(stem, dayMaster)),
    ]),
  );
}

export function calculateLifeStages(pillars: Pillars, dayMaster: string): Record<string, string> {
  const stageMap = TWELVE_STAGES_MAP[dayMaster] || {};
  return Object.fromEntries(
    Object.entries(pillars).map(([pillar, { zhi }]) => [pillar, stageMap[zhi] || '未知']),
  );
}

export function calculateNayin(pillars: Pillars): Nayin {
  const result = {} as Nayin;
  (Object.keys(pillars) as Array<keyof Pillars>).forEach((key) => {
    const pillar = pillars[key];
    result[key] = NAYIN_MAP[pillar.gan + pillar.zhi] || '未知';
  });
  return result;
}

export function calculateKongWang(pillars: Pillars): KongWangResult {
  const result = {} as KongWangResult;
  const heavenlyStems = BASIC_MAPPINGS.HEAVENLY_STEMS as readonly string[];
  const earthlyBranches = BASIC_MAPPINGS.EARTHLY_BRANCHES as readonly string[];

  (Object.keys(pillars) as Array<keyof Pillars>).forEach((key) => {
    const pillar = pillars[key];
    const ganIndex = heavenlyStems.indexOf(pillar.gan);
    const zhiIndex = earthlyBranches.indexOf(pillar.zhi);
    if (ganIndex === -1 || zhiIndex === -1) {
      result[key] = [];
      return;
    }

    const emptyBranch1Index = (10 + zhiIndex - ganIndex) % 12;
    const emptyBranch2Index = (11 + zhiIndex - ganIndex) % 12;
    result[key] = [earthlyBranches[emptyBranch1Index], earthlyBranches[emptyBranch2Index]];
  });

  return result;
}

/**
 * 计算自坐（十二长生在四柱的表现）
 * 与 calculatePillarLifeStages 逻辑相同。
 * @deprecated 请使用 calculatePillarLifeStages
 */
export function calculateZiZuo(pillars: Pillars): ZiZuoResult {
  const result = {} as ZiZuoResult;
  (Object.keys(pillars) as Array<keyof Pillars>).forEach((key) => {
    const pillar = pillars[key];
    const stageMapForGan = TWELVE_STAGES_MAP[pillar.gan] || {};
    result[key] = stageMapForGan[pillar.zhi] || '未知';
  });
  return result;
}
