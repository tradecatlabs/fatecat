import type {
  BirthTimeInput,
  Gender
} from '../shared/types.js';

// ===== 紫微运限类型 =====

export interface ZiweiHoroscopeInput extends BirthTimeInput {
  gender: Gender;
  longitude?: number;
  targetDate?: string;
  targetTimeIndex?: number;
}

export interface HoroscopePeriodInfo {
  index: number;
  name: string;
  heavenlyStem: string;
  earthlyBranch: string;
  palaceNames: string[];
  mutagen: string[];
  startAge?: number;
  endAge?: number;
}

export interface TransitStarEntry {
  starName: string;
  palaceName: string;
}

export interface YearlyDecStarInfo {
  jiangqian12: string[];  // 将前十二星
  suiqian12: string[];    // 岁前十二星
}

export interface ZiweiHoroscopeOutput {
  solarDate: string;
  lunarDate: string;
  soul: string;
  body: string;
  fiveElement: string;
  targetDate: string;
  hasExplicitTargetTime: boolean;
  decadal: HoroscopePeriodInfo;
  age: HoroscopePeriodInfo & { nominalAge: number; };
  yearly: HoroscopePeriodInfo;
  monthly: HoroscopePeriodInfo;
  daily: HoroscopePeriodInfo;
  hourly: HoroscopePeriodInfo;
  transitStars?: TransitStarEntry[];      // 流年星曜
  yearlyDecStar?: YearlyDecStarInfo;      // 流年神煞（岁前/将前十二星）
}
