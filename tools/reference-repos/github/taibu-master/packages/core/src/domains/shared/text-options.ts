/**
 * 文本渲染契约层
 *
 * 这里只保留 text renderer 选项类型与统一出口，
 * 不再承载任何具体术数实现。
 */

import type { DayunOutput } from '../bazi-dayun/types.js';
import type { DetailLevel } from './types.js';

export type BaziCanonicalTextOptions = {
  name?: string;
  dayun?: DayunOutput;
  detailLevel?: DetailLevel;
};

export type DayunCanonicalTextOptions = {
  detailLevel?: DetailLevel;
};

export type TarotCanonicalTextOptions = {
  birthDate?: string | null;
  detailLevel?: DetailLevel;
};

export type ZiweiCanonicalTextOptions = {
  detailLevel?: DetailLevel;
  horoscope?: {
    decadal: { palaceName: string; ageRange: string; };
    yearly: { palaceName: string; period: string; };
    monthly: { palaceName: string; period: string; };
    daily: { palaceName: string; period: string; };
  };
};

export type QimenCanonicalTextOptions = {
  detailLevel?: DetailLevel;
};

export type DaliurenCanonicalTextOptions = {
  detailLevel?: DetailLevel;
};

export type ZiweiHoroscopeCanonicalTextOptions = {
  detailLevel?: DetailLevel;
};

export type AlmanacCanonicalTextOptions = {
  detailLevel?: DetailLevel;
};

export type MeihuaCanonicalTextOptions = {
  detailLevel?: DetailLevel;
};

export type TaiyiCanonicalTextOptions = {
  detailLevel?: DetailLevel;
};

export type AstrologyCanonicalTextOptions = {
  detailLevel?: DetailLevel;
};
