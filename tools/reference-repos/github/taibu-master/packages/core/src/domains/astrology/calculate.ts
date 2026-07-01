import { createRequire } from 'node:module';

import type { AstrologyAspect, AstrologyAspectType, AstrologyChartSnapshot, AstrologyDegreeInfo, AstrologyFactor, AstrologyFactorCategory, AstrologyHouse, AstrologyInput, AstrologyOutput, AstrologySignInfo, AstrologyZodiacCusp } from './types.js';

const require = createRequire(import.meta.url);
const horoscopePackage = require('circular-natal-horoscope-js') as typeof import('circular-natal-horoscope-js');
const { Origin, Horoscope } = horoscopePackage;

export type {
  AstrologyAspect,
  AstrologyAspectType,
  AstrologyChartSnapshot,
  AstrologyFactor,
  AstrologyFactorCategory,
  AstrologyHouse,
  AstrologyHouseSystem,
  AstrologyInput,
  AstrologyOutput,
  AstrologySignInfo,
  AstrologyZodiacCusp,
} from './types.js';

const BODY_KEYS = ['sun', 'moon', 'mercury', 'venus', 'mars', 'jupiter', 'saturn', 'uranus', 'neptune', 'pluto'] as const;
const POINT_KEYS = ['northnode', 'southnode', 'lilith'] as const;
const ANGLE_KEYS = ['ascendant', 'midheaven'] as const;
const MAJOR_ASPECT_TYPES = ['conjunction', 'opposition', 'trine', 'square', 'sextile'] as const;
const SUPPORTED_ASPECT_KEYS = [...BODY_KEYS, ...POINT_KEYS, ...ANGLE_KEYS] as const;

const BODY_LABELS: Record<string, string> = {
  sun: '太阳',
  moon: '月亮',
  mercury: '水星',
  venus: '金星',
  mars: '火星',
  jupiter: '木星',
  saturn: '土星',
  uranus: '天王星',
  neptune: '海王星',
  pluto: '冥王星',
  northnode: '北交点',
  southnode: '南交点',
  lilith: '莉莉丝',
  ascendant: '上升点',
  midheaven: '天顶',
};

const SIGN_LABELS: Record<string, { label: string; element: string; modality: string; }> = {
  aries: { label: '白羊座', element: '火', modality: '本位' },
  taurus: { label: '金牛座', element: '土', modality: '固定' },
  gemini: { label: '双子座', element: '风', modality: '变动' },
  cancer: { label: '巨蟹座', element: '水', modality: '本位' },
  leo: { label: '狮子座', element: '火', modality: '固定' },
  virgo: { label: '处女座', element: '土', modality: '变动' },
  libra: { label: '天秤座', element: '风', modality: '本位' },
  scorpio: { label: '天蝎座', element: '水', modality: '固定' },
  sagittarius: { label: '射手座', element: '火', modality: '变动' },
  capricorn: { label: '摩羯座', element: '土', modality: '本位' },
  aquarius: { label: '水瓶座', element: '风', modality: '固定' },
  pisces: { label: '双鱼座', element: '水', modality: '变动' },
};

const ASPECT_LABELS: Record<AstrologyAspectType, string> = {
  conjunction: '合相',
  opposition: '对冲',
  trine: '三分',
  square: '四分',
  sextile: '六合',
};

const ASPECT_ANGLES: Record<AstrologyAspectType, { angle: number; orb: number; }> = {
  conjunction: { angle: 0, orb: 8 },
  opposition: { angle: 180, orb: 8 },
  trine: { angle: 120, orb: 8 },
  square: { angle: 90, orb: 7 },
  sextile: { angle: 60, orb: 6 },
};

const APPROXIMATE_COORDINATE_FALLBACK = {
  latitude: 0,
  longitude: 0,
} as const;

const APPROXIMATE_CALCULATION_NOTE = '未提供完整经纬度，已按 0°N, 0°E 与 Etc/GMT 近似计算；上升、天顶、宫位不作为默认输出。';

type AstrologyLocationContext = {
  latitude: number;
  longitude: number;
  calculationMode: AstrologyOutput['chartMeta']['calculationMode'];
  coordinateSource: AstrologyChartSnapshot['origin']['coordinateSource'];
  calculationNote?: string;
};

type DateTimeParts = {
  year: number;
  month: number;
  day: number;
  hour: number;
  minute: number;
  second: number;
};

type HoroscopeSignLike = {
  key?: string;
  label?: string;
};

type HoroscopeFactorLike = {
  key: string;
  label?: string;
  Sign: HoroscopeSignLike;
  House?: { id?: number; };
  isRetrograde?: boolean;
  ChartPosition: {
    Ecliptic: {
      DecimalDegrees: number;
    };
  };
};

type HoroscopeHouseLike = {
  id: number;
  Sign: HoroscopeSignLike;
  ChartPosition: {
    StartPosition: {
      Ecliptic: {
        DecimalDegrees: number;
      };
    };
    EndPosition: {
      Ecliptic: {
        DecimalDegrees: number;
      };
    };
  };
};

type HoroscopeZodiacCuspLike = {
  Sign: HoroscopeSignLike;
  ChartPosition: {
    Ecliptic: {
      DecimalDegrees: number;
    };
  };
};

type HoroscopeAspectLike = {
  aspectKey: string;
  point1Key: string;
  point1Label?: string;
  point2Key: string;
  point2Label?: string;
  orb?: number;
};

function ensureRange(value: number, min: number, max: number, label: string): void {
  if (!Number.isFinite(value) || value < min || value > max) {
    throw new Error(`${label} 必须在 ${min} 到 ${max} 之间`);
  }
}

function ensureInteger(value: number, min: number, max: number, label: string): void {
  if (!Number.isInteger(value) || value < min || value > max) {
    throw new Error(`${label} 必须是 ${min}-${max} 的整数`);
  }
}

function ensureValidCivilDate(year: number, month: number, day: number, label: string): void {
  const date = new Date(Date.UTC(year, month - 1, day));
  if (
    Number.isNaN(date.getTime()) ||
    date.getUTCFullYear() !== year ||
    date.getUTCMonth() !== month - 1 ||
    date.getUTCDate() !== day
  ) {
    throw new Error(`${label} 日期无效，请检查年月日是否存在`);
  }
}

function normalizeBirthInput(input: AstrologyInput) {
  ensureInteger(input.birthYear, 1, 9999, 'birthYear');
  ensureInteger(input.birthMonth, 1, 12, 'birthMonth');
  ensureInteger(input.birthDay, 1, 31, 'birthDay');
  ensureInteger(input.birthHour, 0, 23, 'birthHour');
  const birthMinute = input.birthMinute ?? 0;
  ensureInteger(birthMinute, 0, 59, 'birthMinute');
  ensureValidCivilDate(input.birthYear, input.birthMonth, input.birthDay, 'birth');
  if (input.houseSystem && input.houseSystem !== 'placidus') {
    throw new Error('houseSystem 当前仅支持 placidus');
  }
  return {
    birthYear: input.birthYear,
    birthMonth: input.birthMonth,
    birthDay: input.birthDay,
    birthHour: input.birthHour,
    birthMinute,
  };
}

function resolveLocationContext(input: AstrologyInput): AstrologyLocationContext {
  const hasLatitude = input.latitude !== undefined;
  const hasLongitude = input.longitude !== undefined;

  if (hasLatitude !== hasLongitude) {
    throw new Error('latitude 和 longitude 需要同时提供，或同时省略');
  }

  if (hasLatitude && hasLongitude) {
    ensureRange(input.latitude as number, -90, 90, 'latitude');
    ensureRange(input.longitude as number, -180, 180, 'longitude');
    return {
      latitude: input.latitude as number,
      longitude: input.longitude as number,
      calculationMode: 'exact',
      coordinateSource: 'provided',
    };
  }

  return {
    ...APPROXIMATE_COORDINATE_FALLBACK,
    calculationMode: 'approximate',
    coordinateSource: 'assumed_zero',
    calculationNote: APPROXIMATE_CALCULATION_NOTE,
  };
}

function pad(value: number): string {
  return String(value).padStart(2, '0');
}

function formatDateTimeParts(parts: { year: number; month: number; day: number; hour: number; minute: number; second: number; }): string {
  return `${parts.year}-${pad(parts.month)}-${pad(parts.day)} ${pad(parts.hour)}:${pad(parts.minute)}:${pad(parts.second)}`;
}

function getTimeZoneParts(date: Date, timeZone: string): { year: number; month: number; day: number; hour: number; minute: number; second: number; } {
  const formatter = new Intl.DateTimeFormat('en-US', {
    timeZone,
    hour12: false,
    year: 'numeric',
    month: '2-digit',
    day: '2-digit',
    hour: '2-digit',
    minute: '2-digit',
    second: '2-digit',
  });
  const values: Record<string, number> = {};
  for (const part of formatter.formatToParts(date)) {
    if (part.type !== 'literal') {
      values[part.type] = Number(part.value);
    }
  }
  return {
    year: values.year ?? 1970,
    month: values.month ?? 1,
    day: values.day ?? 1,
    hour: values.hour ?? 0,
    minute: values.minute ?? 0,
    second: values.second ?? 0,
  };
}

function validateDateTimeParts(parts: DateTimeParts, label: string): DateTimeParts {
  ensureInteger(parts.year, 1, 9999, `${label}.year`);
  ensureInteger(parts.month, 1, 12, `${label}.month`);
  ensureInteger(parts.day, 1, 31, `${label}.day`);
  ensureInteger(parts.hour, 0, 23, `${label}.hour`);
  ensureInteger(parts.minute, 0, 59, `${label}.minute`);
  ensureInteger(parts.second, 0, 59, `${label}.second`);
  ensureValidCivilDate(parts.year, parts.month, parts.day, label);
  return parts;
}

function parseTransitDateTime(value: string | undefined, derivedTimeZone: string) {
  if (!value) {
    return getTimeZoneParts(new Date(), derivedTimeZone);
  }

  const trimmed = value.trim();
  const naive = trimmed.match(/^(\d{4})-(\d{2})-(\d{2})T(\d{2}):(\d{2})(?::(\d{2}))?$/);
  if (naive) {
    return validateDateTimeParts({
      year: Number(naive[1]),
      month: Number(naive[2]),
      day: Number(naive[3]),
      hour: Number(naive[4]),
      minute: Number(naive[5]),
      second: Number(naive[6] ?? '0'),
    }, 'transitDateTime');
  }

  const zoned = trimmed.match(/^(\d{4})-(\d{2})-(\d{2})T(\d{2}):(\d{2})(?::(\d{2}))?(Z|([+-])(\d{2}):(\d{2}))$/);
  if (zoned) {
    validateDateTimeParts({
      year: Number(zoned[1]),
      month: Number(zoned[2]),
      day: Number(zoned[3]),
      hour: Number(zoned[4]),
      minute: Number(zoned[5]),
      second: Number(zoned[6] ?? '0'),
    }, 'transitDateTime');

    if (zoned[7] !== 'Z') {
      ensureInteger(Number(zoned[8]), 0, 23, 'transitDateTime.offsetHour');
      ensureInteger(Number(zoned[9]), 0, 59, 'transitDateTime.offsetMinute');
    }

    const parsed = new Date(trimmed);
    if (Number.isNaN(parsed.getTime())) {
      throw new Error('transitDateTime 格式无效，请使用 YYYY-MM-DDTHH:mm[:ss] 或带时区偏移的 ISO 时间');
    }
    return getTimeZoneParts(parsed, derivedTimeZone);
  }

  throw new Error('transitDateTime 格式无效，请使用 YYYY-MM-DDTHH:mm[:ss] 或带时区偏移的 ISO 时间');
}

function formatDegrees(decimal: number): AstrologyDegreeInfo {
  const normalized = ((decimal % 360) + 360) % 360;
  const absoluteDegrees = Math.floor(normalized);
  const absoluteMinutes = Math.floor((normalized - absoluteDegrees) * 60);
  const withinSign = normalized % 30;
  const withinSignDegrees = Math.floor(withinSign);
  const withinSignMinutes = Math.floor((withinSign - withinSignDegrees) * 60);
  return {
    decimal: Number(normalized.toFixed(4)),
    absolute: `${absoluteDegrees}°${pad(absoluteMinutes)}`,
    withinSign: `${withinSignDegrees}°${pad(withinSignMinutes)}`,
  };
}

function buildSignInfo(sign: { key?: string; label?: string; }): AstrologySignInfo {
  const key = String(sign?.key || '').toLowerCase();
  const found = SIGN_LABELS[key] || { label: sign?.label || key || '未知', element: '未知', modality: '未知' };
  return {
    key,
    label: found.label,
    element: found.element,
    modality: found.modality,
  };
}

function buildFactor(entity: HoroscopeFactorLike, category: AstrologyFactorCategory): AstrologyFactor {
  return {
    key: entity.key,
    label: BODY_LABELS[entity.key] || entity.label || entity.key,
    category,
    sign: buildSignInfo(entity.Sign),
    ...(typeof entity.House?.id === 'number' ? { house: entity.House.id } : {}),
    ...(typeof entity.isRetrograde === 'boolean' ? { retrograde: entity.isRetrograde } : {}),
    position: formatDegrees(entity.ChartPosition.Ecliptic.DecimalDegrees),
  };
}

function buildHouse(entity: HoroscopeHouseLike): AstrologyHouse {
  return {
    id: entity.id,
    label: `第${entity.id}宫`,
    sign: buildSignInfo(entity.Sign),
    start: formatDegrees(entity.ChartPosition.StartPosition.Ecliptic.DecimalDegrees),
    end: formatDegrees(entity.ChartPosition.EndPosition.Ecliptic.DecimalDegrees),
  };
}

function buildZodiacCusp(entity: HoroscopeZodiacCuspLike): AstrologyZodiacCusp {
  return {
    sign: buildSignInfo(entity.Sign),
    start: formatDegrees(entity.ChartPosition.Ecliptic.DecimalDegrees),
  };
}

function classifyFactorCategory(key: string): AstrologyFactorCategory {
  if ((ANGLE_KEYS as readonly string[]).includes(key)) return 'angle';
  if ((POINT_KEYS as readonly string[]).includes(key)) return 'point';
  return 'body';
}

function normalizeAspectType(value: string): AstrologyAspectType | null {
  return (MAJOR_ASPECT_TYPES as readonly string[]).includes(value)
    ? value as AstrologyAspectType
    : null;
}

function computeAngularDistance(left: number, right: number): number {
  const diffRaw = Math.abs(left - right);
  const diff = diffRaw > 180 ? 360 - diffRaw : diffRaw;
  return Number(diff.toFixed(4));
}

function buildAspectFromLibrary(aspect: HoroscopeAspectLike, factorPositionByKey: Map<string, number>): AstrologyAspect | null {
  const type = normalizeAspectType(aspect.aspectKey);
  if (!type) return null;
  const fromPosition = factorPositionByKey.get(aspect.point1Key);
  const toPosition = factorPositionByKey.get(aspect.point2Key);
  if (typeof fromPosition !== 'number' || typeof toPosition !== 'number') {
    throw new Error(`astrology 相位点缺少位置数据: ${aspect.point1Key} / ${aspect.point2Key}`);
  }
  return {
    type,
    label: ASPECT_LABELS[type],
    from: {
      key: aspect.point1Key,
      label: BODY_LABELS[aspect.point1Key] || aspect.point1Label || aspect.point1Key,
      category: classifyFactorCategory(aspect.point1Key),
    },
    to: {
      key: aspect.point2Key,
      label: BODY_LABELS[aspect.point2Key] || aspect.point2Label || aspect.point2Key,
      category: classifyFactorCategory(aspect.point2Key),
    },
    orb: Number(Number(aspect.orb ?? 0).toFixed(4)),
    actualAngle: computeAngularDistance(fromPosition, toPosition),
  };
}

function computeMajorAspect(from: AstrologyFactor, to: AstrologyFactor): AstrologyAspect | null {
  const diff = computeAngularDistance(from.position.decimal, to.position.decimal);

  for (const type of MAJOR_ASPECT_TYPES) {
    const target = ASPECT_ANGLES[type];
    const orb = Math.abs(diff - target.angle);
    if (orb <= target.orb) {
      return {
        type,
        label: ASPECT_LABELS[type],
        from: { key: from.key, label: from.label, category: from.category },
        to: { key: to.key, label: to.label, category: to.category },
        orb: Number(orb.toFixed(4)),
        actualAngle: Number(diff.toFixed(4)),
      };
    }
  }

  return null;
}

function createHoroscope(origin: InstanceType<typeof Origin>, includeAngles: boolean) {
  const aspectKeys = includeAngles
    ? [...SUPPORTED_ASPECT_KEYS]
    : [...BODY_KEYS, ...POINT_KEYS];
  return new Horoscope({
    origin,
    houseSystem: 'placidus',
    zodiac: 'tropical',
    aspectPoints: aspectKeys,
    aspectWithPoints: aspectKeys,
    aspectTypes: [...MAJOR_ASPECT_TYPES],
    language: 'en',
  });
}

function buildHoroscopeSnapshot(
  origin: InstanceType<typeof Origin>,
  locationContext: AstrologyLocationContext,
  birthPlace?: string,
): AstrologyChartSnapshot {
  const includeAngles = locationContext.calculationMode === 'exact';
  const horoscope = createHoroscope(origin, includeAngles);

  const bodies = BODY_KEYS.map((key) => buildFactor(horoscope.CelestialBodies[key] as HoroscopeFactorLike, 'body'));
  const points = POINT_KEYS.map((key) => buildFactor(horoscope.CelestialPoints[key] as HoroscopeFactorLike, 'point'));
  const angles = includeAngles
    ? ANGLE_KEYS.map((key) => buildFactor(horoscope.Angles[key] as HoroscopeFactorLike, 'angle'))
    : [];
  const houses = includeAngles
    ? (horoscope.Houses as HoroscopeHouseLike[]).map((house) => buildHouse(house))
    : [];
  const zodiacCusps = (horoscope.ZodiacCusps as HoroscopeZodiacCuspLike[]).map((cusp) => buildZodiacCusp(cusp));

  return {
    origin: {
      localDateTime: formatDateTimeParts({
        year: origin.localTime.year(),
        month: origin.localTime.month() + 1,
        day: origin.localTime.date(),
        hour: origin.localTime.hour(),
        minute: origin.localTime.minute(),
        second: origin.localTime.second(),
      }),
      derivedTimeZone: origin.timezone?.name || 'unknown',
      latitude: origin.latitude,
      longitude: origin.longitude,
      coordinateSource: locationContext.coordinateSource,
      ...(birthPlace ? { birthPlace } : {}),
    },
    sunSign: buildSignInfo(horoscope.SunSign),
    bodies,
    points,
    angles,
    houses,
    zodiacCusps,
  };
}

function createNatalOrigin(input: AstrologyInput, locationContext: AstrologyLocationContext) {
  const birth = normalizeBirthInput(input);
  return new Origin({
    year: birth.birthYear,
    month: birth.birthMonth - 1,
    date: birth.birthDay,
    hour: birth.birthHour,
    minute: birth.birthMinute,
    second: 0,
    latitude: locationContext.latitude,
    longitude: locationContext.longitude,
  });
}

function createTransitOrigin(
  input: AstrologyInput,
  derivedTimeZone: string,
  locationContext: AstrologyLocationContext,
) {
  const transit = parseTransitDateTime(input.transitDateTime, derivedTimeZone);
  ensureInteger(transit.month, 1, 12, 'transitDateTime.month');
  ensureInteger(transit.day, 1, 31, 'transitDateTime.day');
  ensureInteger(transit.hour, 0, 23, 'transitDateTime.hour');
  ensureInteger(transit.minute, 0, 59, 'transitDateTime.minute');
  ensureInteger(transit.second, 0, 59, 'transitDateTime.second');

  return new Origin({
    year: transit.year,
    month: transit.month - 1,
    date: transit.day,
    hour: transit.hour,
    minute: transit.minute,
    second: transit.second,
    latitude: locationContext.latitude,
    longitude: locationContext.longitude,
  });
}

function sortAspects(aspects: AstrologyAspect[]): AstrologyAspect[] {
  return [...aspects].sort((left, right) => {
    if (left.orb !== right.orb) return left.orb - right.orb;
    if (left.from.label !== right.from.label) return left.from.label.localeCompare(right.from.label, 'zh-CN');
    return left.to.label.localeCompare(right.to.label, 'zh-CN');
  });
}

export function calculateAstrology(input: AstrologyInput): AstrologyOutput {
  const locationContext = resolveLocationContext(input);
  const natalOrigin = createNatalOrigin(input, locationContext);
  const natal = buildHoroscopeSnapshot(natalOrigin, locationContext, input.birthPlace);
  const transitOrigin = createTransitOrigin(input, natal.origin.derivedTimeZone, locationContext);
  const transit = buildHoroscopeSnapshot(transitOrigin, locationContext, input.birthPlace);

  const includeAngles = locationContext.calculationMode === 'exact';
  const natalHoroscope = createHoroscope(natalOrigin, includeAngles);
  const natalFactorPositionByKey = new Map(
    [...natal.bodies, ...natal.points, ...natal.angles].map((factor) => [factor.key, factor.position.decimal]),
  );

  const majorAspects = sortAspects(
    (natalHoroscope.Aspects.all as HoroscopeAspectLike[])
      .map((aspect) => buildAspectFromLibrary(aspect, natalFactorPositionByKey))
      .filter((aspect: AstrologyAspect | null): aspect is AstrologyAspect => !!aspect),
  );

  const transitFactors = [...transit.bodies, ...transit.points];
  const natalTargets = [...natal.bodies, ...natal.points, ...natal.angles];
  const transitToNatalAspects = sortAspects(
    transitFactors.flatMap((from) =>
      natalTargets.flatMap((to) => {
        if (from.key === to.key && from.category === to.category) return [];
        const aspect = computeMajorAspect(from, to);
        return aspect ? [aspect] : [];
      })),
  );

  return {
    chartMeta: {
      zodiac: 'tropical',
      houseSystem: 'placidus',
      supportedBodies: [...BODY_KEYS],
      supportedAspectTypes: [...MAJOR_ASPECT_TYPES],
      calculationMode: locationContext.calculationMode,
      ...(locationContext.calculationNote ? { calculationNote: locationContext.calculationNote } : {}),
    },
    natal,
    transit,
    majorAspects,
    transitToNatalAspects,
  };
}
