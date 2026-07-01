export type AstrologyHouseSystem = 'placidus';

export type AstrologyAspectType = 'conjunction' | 'opposition' | 'trine' | 'square' | 'sextile';

export type AstrologyFactorCategory = 'body' | 'point' | 'angle';

export type AstrologyCalculationMode = 'exact' | 'approximate';

export type AstrologyCoordinateSource = 'provided' | 'assumed_zero';

export interface AstrologyInput {
  birthYear: number;
  birthMonth: number;
  birthDay: number;
  birthHour: number;
  birthMinute?: number;
  latitude?: number;
  longitude?: number;
  birthPlace?: string;
  transitDateTime?: string;
  houseSystem?: AstrologyHouseSystem;
}

export interface AstrologySignInfo {
  key: string;
  label: string;
  element: string;
  modality: string;
}

export interface AstrologyDegreeInfo {
  decimal: number;
  absolute: string;
  withinSign: string;
}

export interface AstrologyFactor {
  key: string;
  label: string;
  category: AstrologyFactorCategory;
  sign: AstrologySignInfo;
  house?: number;
  retrograde?: boolean;
  position: AstrologyDegreeInfo;
}

export interface AstrologyHouse {
  id: number;
  label: string;
  sign: AstrologySignInfo;
  start: AstrologyDegreeInfo;
  end: AstrologyDegreeInfo;
}

export interface AstrologyZodiacCusp {
  sign: AstrologySignInfo;
  start: AstrologyDegreeInfo;
}

export interface AstrologyAspect {
  type: AstrologyAspectType;
  label: string;
  from: {
    key: string;
    label: string;
    category: AstrologyFactorCategory;
  };
  to: {
    key: string;
    label: string;
    category: AstrologyFactorCategory;
  };
  orb: number;
  actualAngle: number;
}

export interface AstrologyChartSnapshot {
  origin: {
    localDateTime: string;
    derivedTimeZone: string;
    latitude: number;
    longitude: number;
    coordinateSource: AstrologyCoordinateSource;
    birthPlace?: string;
  };
  sunSign: AstrologySignInfo;
  bodies: AstrologyFactor[];
  points: AstrologyFactor[];
  angles: AstrologyFactor[];
  houses: AstrologyHouse[];
  zodiacCusps: AstrologyZodiacCusp[];
}

export interface AstrologyOutput {
  chartMeta: {
    zodiac: 'tropical';
    houseSystem: AstrologyHouseSystem;
    supportedBodies: string[];
    supportedAspectTypes: AstrologyAspectType[];
    calculationMode: AstrologyCalculationMode;
    calculationNote?: string;
  };
  natal: AstrologyChartSnapshot;
  transit: AstrologyChartSnapshot;
  majorAspects: AstrologyAspect[];
  transitToNatalAspects: AstrologyAspect[];
}
