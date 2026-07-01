import { normalizeDetailLevel3Way } from '../../shared/render-utils.js';

import type { AstrologyCanonicalTextOptions } from '../shared/text-options.js';
import type { AstrologyAspect, AstrologyFactor, AstrologyHouse, AstrologyOutput, AstrologyZodiacCusp } from './types.js';

export type AstrologyDetailLevel = 'default' | 'more' | 'full';

export interface AstrologyGroupedFactor {
  factor: AstrologyFactor;
  aspects: AstrologyAspect[];
}

export interface AstrologyPointPair {
  key: string;
  label: string;
  natal: AstrologyFactor;
  transit: AstrologyFactor | null;
}

export interface AstrologyRenderModel {
  detailLevel: AstrologyDetailLevel;
  isApproximate: boolean;
  basicInfo: {
    calculationModeLabel: string;
    calculationNote?: string;
    birthPlace?: string;
    coordinatesLabel: string;
    natalTimeZoneLabel: string;
    natalDateTime: string;
    transitDateTime: string;
    zodiacLabel: string;
    houseSystemLabel: string;
  };
  anchors: {
    sun: AstrologyFactor;
    moon: AstrologyFactor;
    ascendant?: AstrologyFactor;
    midheaven?: AstrologyFactor;
  };
  natalBodies: AstrologyGroupedFactor[];
  transitTriggers: AstrologyGroupedFactor[];
  pointPairs: AstrologyPointPair[];
  houses: AstrologyHouse[];
  zodiacCusps: AstrologyZodiacCusp[];
  fullNatalAspects: AstrologyAspect[];
  fullTransitAspects: AstrologyAspect[];
}

const DEFAULT_VISIBLE_FACTOR_KEYS = new Set([
  'sun',
  'moon',
  'mercury',
  'venus',
  'mars',
  'jupiter',
  'saturn',
  'uranus',
  'neptune',
  'pluto',
  'ascendant',
  'midheaven',
]);

const SLOW_TRANSIT_FACTOR_KEYS = new Set([
  'jupiter',
  'saturn',
  'uranus',
  'neptune',
  'pluto',
]);

const NATAL_INLINE_MAX_ORB = 6;
const TRANSIT_TRIGGER_MAX_ORB = 4;

function entrySortByClosestAspect(left: AstrologyGroupedFactor, right: AstrologyGroupedFactor): number {
  const leftOrb = left.aspects[0]?.orb ?? Number.POSITIVE_INFINITY;
  const rightOrb = right.aspects[0]?.orb ?? Number.POSITIVE_INFINITY;
  if (leftOrb !== rightOrb) return leftOrb - rightOrb;
  return left.factor.label.localeCompare(right.factor.label, 'zh-CN');
}

function buildNatalBodyEntries(result: AstrologyOutput): AstrologyGroupedFactor[] {
  const inlineAspects = result.majorAspects.filter((aspect) =>
    aspect.orb <= NATAL_INLINE_MAX_ORB
    && DEFAULT_VISIBLE_FACTOR_KEYS.has(aspect.from.key)
    && DEFAULT_VISIBLE_FACTOR_KEYS.has(aspect.to.key),
  );

  return result.natal.bodies.map((factor) => ({
    factor,
    aspects: inlineAspects.filter((aspect) => aspect.from.key === factor.key || aspect.to.key === factor.key),
  }));
}

function buildTransitTriggerEntries(result: AstrologyOutput): AstrologyGroupedFactor[] {
  return result.transit.bodies
    .filter((factor) => SLOW_TRANSIT_FACTOR_KEYS.has(factor.key))
    .map((factor) => ({
      factor,
      aspects: result.transitToNatalAspects.filter((aspect) =>
        aspect.from.key === factor.key
        && aspect.orb <= TRANSIT_TRIGGER_MAX_ORB
        && DEFAULT_VISIBLE_FACTOR_KEYS.has(aspect.to.key),
      ),
    }))
    .filter((entry) => entry.aspects.length > 0)
    .sort(entrySortByClosestAspect);
}

function buildPointPairs(result: AstrologyOutput): AstrologyPointPair[] {
  const transitPointByKey = new Map(result.transit.points.map((item) => [item.key, item]));
  return result.natal.points.map((natal) => ({
    key: natal.key,
    label: natal.label,
    natal,
    transit: transitPointByKey.get(natal.key) ?? null,
  }));
}

export function ensureAstrologyDetailLevelSupported(result: AstrologyOutput, detailLevel: AstrologyDetailLevel): void {
  if (detailLevel === 'full' && result.chartMeta.calculationMode === 'approximate') {
    throw new Error('astrology 在 detailLevel=full 时需要显式提供 latitude 与 longitude');
  }
}

export function buildAstrologyRenderModel(
  result: AstrologyOutput,
  options: AstrologyCanonicalTextOptions = {},
): AstrologyRenderModel {
  const detailLevel = normalizeDetailLevel3Way(options.detailLevel);
  ensureAstrologyDetailLevelSupported(result, detailLevel);

  const ascendant = result.natal.angles.find((item) => item.key === 'ascendant');
  const midheaven = result.natal.angles.find((item) => item.key === 'midheaven');
  const sun = result.natal.bodies.find((item) => item.key === 'sun');
  const moon = result.natal.bodies.find((item) => item.key === 'moon');

  if (!sun || !moon) {
    throw new Error('astrology 渲染失败：缺少太阳或月亮数据');
  }

  const isApproximate = result.chartMeta.calculationMode === 'approximate';

  return {
    detailLevel,
    isApproximate,
    basicInfo: {
      calculationModeLabel: isApproximate ? '近似盘' : '精准盘',
      ...(result.chartMeta.calculationNote ? { calculationNote: result.chartMeta.calculationNote } : {}),
      ...(result.natal.origin.birthPlace ? { birthPlace: result.natal.origin.birthPlace } : {}),
      coordinatesLabel: isApproximate
        ? `未提供（按 ${result.natal.origin.latitude}, ${result.natal.origin.longitude} 近似）`
        : `${result.natal.origin.latitude}, ${result.natal.origin.longitude}`,
      natalTimeZoneLabel: isApproximate
        ? `未提供（按 ${result.natal.origin.derivedTimeZone} 近似）`
        : result.natal.origin.derivedTimeZone,
      natalDateTime: result.natal.origin.localDateTime,
      transitDateTime: result.transit.origin.localDateTime,
      zodiacLabel: 'Tropical',
      houseSystemLabel: 'Placidus',
    },
    anchors: {
      sun,
      moon,
      ...(ascendant ? { ascendant } : {}),
      ...(midheaven ? { midheaven } : {}),
    },
    natalBodies: buildNatalBodyEntries(result),
    transitTriggers: buildTransitTriggerEntries(result),
    pointPairs: buildPointPairs(result),
    houses: result.natal.houses,
    zodiacCusps: result.natal.zodiacCusps,
    fullNatalAspects: result.majorAspects,
    fullTransitAspects: result.transitToNatalAspects,
  };
}
