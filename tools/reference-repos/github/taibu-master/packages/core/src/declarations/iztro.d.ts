declare module 'iztro' {
  export type Mutagen = '禄' | '权' | '科' | '忌';

  export interface Star {
    name: string;
    type?: string;
    brightness?: string;
    mutagen?: string;
  }

  export interface Decadal {
    range: [number, number];
    heavenlyStem: string;
    earthlyBranch: string;
  }

  export interface Palace {
    index: number;
    name: string;
    heavenlyStem: string;
    earthlyBranch: string;
    isBodyPalace: boolean;
    isOriginalPalace: boolean;
    majorStars: Star[];
    minorStars: Star[];
    adjectiveStars: Star[];
    changsheng12: string;
    boshi12: string;
    jiangqian12: string;
    suiqian12: string;
    decadal: Decadal;
    ages: number[];
  }

  export interface FunctionalPalace extends Palace {
    has(stars: string[]): boolean;
    hasOneOf(stars: string[]): boolean;
    hasMutagen(mutagen: Mutagen): boolean;
    isEmpty(excludeStars?: string[]): boolean;
    fliesTo(to: number | string, withMutagens: Mutagen | Mutagen[]): boolean;
    selfMutaged(withMutagens: Mutagen | Mutagen[]): boolean;
    mutagedPlaces(): (FunctionalPalace | undefined)[];
  }

  export interface SurroundedPalaces {
    target: FunctionalPalace;
    opposite: FunctionalPalace;
    wealth: FunctionalPalace;
    career: FunctionalPalace;
  }

  export interface HoroscopeItem {
    index: number;
    name: string;
    heavenlyStem: string;
    earthlyBranch: string;
    palaceNames: string[];
    mutagen: string[];
    stars?: Star[][];
  }

  export interface Horoscope {
    lunarDate: string;
    solarDate: string;
    decadal: HoroscopeItem;
    age: HoroscopeItem & { nominalAge: number; };
    yearly: HoroscopeItem & {
      yearlyDecStar: { jiangqian12: string[]; suiqian12: string[]; };
    };
    monthly: HoroscopeItem;
    daily: HoroscopeItem;
    hourly: HoroscopeItem;
  }

  export interface Astrolabe {
    gender?: string;
    palaces: FunctionalPalace[];
    chineseDate?: string;
    solarDate?: string;
    lunarDate?: string;
    sign?: string;
    zodiac?: string;
    earthlyBranchOfSoulPalace?: string;
    earthlyBranchOfBodyPalace?: string;
    soul?: string;
    body?: string;
    fiveElementsClass?: string;
    time?: string;
    timeRange?: string;
    rawDates?: {
      lunarDate: { lunarYear: number; lunarMonth: number; lunarDay: number; isLeap: boolean; };
      chineseDate: { yearly: [string, string]; monthly: [string, string]; daily: [string, string]; hourly: [string, string]; };
    };
    horoscope(date?: string | Date, timeIndex?: number): Horoscope;
    palace(indexOrName: number | string): FunctionalPalace | undefined;
    surroundedPalaces(indexOrName: number | string): SurroundedPalaces;
  }

  export const astro: {
    bySolar(
      dateStr: string,
      timeIndex: number,
      gender: string,
      fixLeap?: boolean,
      language?: string
    ): Astrolabe;
    byLunar(
      dateStr: string,
      timeIndex: number,
      gender: string,
      isLeapMonth?: boolean,
      fixLeap?: boolean,
      language?: string
    ): Astrolabe;
  };
}
